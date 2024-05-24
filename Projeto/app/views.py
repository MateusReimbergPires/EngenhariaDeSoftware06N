import ast
from flask import Blueprint, render_template, url_for, redirect, request, session, jsonify
from flask_bcrypt import check_password_hash
from .models import *
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

views = Blueprint('views', __name__)

cliente = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
modelo = 'gpt-4'
prompt_sistema = """
Baseado no texto recebido, crie uma lista de habilidades desejadas, somente com as habilidades base listadas. Caso haja algum erro de escrita, tente encontrar a palavra correta. Caso não encontre a habilidade solicitada, ignore.
Habilidades bases:
Programação, SEO, Recrutamento, Atendimento ao Cliente, Análise Financeira, Gestão Estratégica, Planejamento de Rota, Negociação, Testes de Qualidade, Inovação Tecnológica;

A saída precisa ser somente uma linha com as habilidades separadas por vírgula. Não pode haver espaços.
Exemplo de saída:
Programação,SEO,Recrutamento

Exemplo errado de saída:
Programação,
SEO,
Recrutamento
"""

prompt_ranking = """
Você receberá uma lista que contem duas listas. Uma de identificadores de habilidades necessárias para uma vaga de emprego e uma segunda lista de dicionários com dados de funcionários(id, nome e lista de habilidade que o funcionario possui).
Baseado na primeira lista, crie uma lista de funcionários que possuem pelo menos uma das habilidades listadas na primeira lista recebida. Se o funcionario nao possuir pelo menos uma habilidade listada na lista recebida, ignore. Retorne todos os funcionarios possiveis.
Não retorne nenhum texto. Retorne apenas como exemplificado abaixo em Exemplo de saida:

Exemplo de saida:
1,2,3
"""



@views.route('/redirect', methods=['POST', 'GET'])
def redirect_to_page():
    next = request.form['go-to-page']
    return redirect(url_for(next))

@views.route('/')
@views.route('/login')
def login():
    return render_template('login.html', title = "Login")

@views.route('/autenticar', methods=['POST', 'GET'])
def autenticar():

    gestor = Gestor.query.filter_by(email=request.form['usuario']).first()
    if gestor:
        if check_password_hash(gestor.senha, request.form['senha']):
            session['usuario_logado'] = request.form['usuario']
            session['role'] = 'gestor'
            return redirect(url_for('views.painel_gestor'))
        
    recrutador = Recrutador.query.filter_by(email=request.form['usuario']).first()
    if recrutador:
        if recrutador.senha == request.form['senha']:
            session['usuario_logado'] = request.form['usuario']
            session['role'] = 'recrutador'
            return redirect(url_for('views.painel_recrutador'))

    return redirect(url_for('views.login'))

@views.route('/painel_gestor')
def painel_gestor():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('views.login'))

    if session.get('role') == 'gestor':
        gestor = Gestor.query.filter_by(email=session['usuario_logado']).first()
        if not gestor:
            return redirect(url_for('views.login'))  # Se não encontrar o gestor, redireciona para login

        departamento = Departamento.query.filter_by(gestor_id = gestor.id).first()
        vagas = Vaga.query.filter_by(departamento_id = departamento.id).all()
        print(session['usuario_logado'])
        return render_template('painel_gestor.html', title='Painel - Gestor', usuario_logado=session['usuario_logado'], vagas=vagas)

    return redirect(url_for('views.nao_autorizado'))

@views.route('/relatorio_vaga', methods=['POST', 'GET'])
def relatorio_vaga():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('views.login'))
    
    if session.get('role') == 'gestor' or session.get('role') == 'recrutador':
        vaga_id = request.form['vaga']
        vaga = Vaga.query.get(vaga_id)
        departamento = Departamento.query.get(vaga.departamento_id)
        areaAtuacao = AreaAtuacao.query.get(vaga.areaAtuacao_id)
        perfilDesejado = PerfilDesejado.query.filter_by(vaga_id=vaga.id).first()
        habilidadesNecessarias = HabilidadeNecessaria.query.filter_by(perfilDesejado_id=perfilDesejado.id).all()
        habilidades = ''
        for habilidade in habilidadesNecessarias:
            habilidadeBase = HabilidadeBase.query.get(habilidade.habilidadeBase_id)
            habilidades += habilidadeBase.nomeHabilidade + ', '


        return render_template('relatorio_vaga.html', title='Cadastrar Vaga', usuario_logado=session['usuario_logado'], vaga=vaga, departamento=departamento, areaAtuacao=areaAtuacao, habilidades=habilidades)

    return redirect(url_for('views.nao_autorizado'))


@views.route('/cadastro_vaga')
def cadastro_vaga():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('views.login'))
    
    if session.get('role') == 'gestor':
        gestor = Gestor.query.filter_by(email=session['usuario_logado']).first()
        departamento = Departamento.query.filter_by(gestor_id = gestor.id).first()
        areasAtuacao = AreaAtuacao.query.all()
        return render_template('cadastro_vaga.html', title='Cadastrar Vaga', usuario_logado=session['usuario_logado'], departamento=departamento, areasAtuacao=areasAtuacao)

    return redirect(url_for('views.nao_autorizado'))


@views.route('/cadastrar_vaga', methods=['POST', 'GET'])
def cadastrar_vaga():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('views.login'))
    
    if session.get('role') == 'gestor':
        nome_vaga = request.form['vaga-nome']
        departamento_vaga = request.form['vaga-departamento']
        area_vaga = request.form['vaga-area']
        requisitos_vaga = request.form['vaga-requisitos']

        departamento = Departamento.query.get(departamento_vaga)
        area = AreaAtuacao.query.get(area_vaga)

        vaga = Vaga(nomeVaga = nome_vaga, departamento_id = departamento.id, areaAtuacao_id = area.id)

        db.session.add(vaga)
        db.session.commit()

        habilidadesBase = HabilidadeBase.query.all()

        resposta = cliente.chat.completions.create(
            messages=[
                {
                    "role" : "system",
                    "content" : prompt_sistema
                },
                {
                    "role" : "user",
                    "content" : requisitos_vaga
                }
            ],
            model = modelo
        )
        habilidades = resposta.choices[0].message.content.split(',')

        print(habilidades)

        perfilDesejado = PerfilDesejado(vaga_id=vaga.id)

        db.session.add(perfilDesejado)
        db.session.commit()

        habilidadesNecessaria = []
        for habilidade in habilidades:
            for base in habilidadesBase:
                if habilidade == base.nomeHabilidade:
                    habilidadeNova = HabilidadeNecessaria(habilidadeBase_id=base.id, perfilDesejado=perfilDesejado)
                    habilidadesNecessaria.append(habilidadeNova)

        for habilidade in habilidadesNecessaria:
            db.session.add(habilidade)

        db.session.commit()
        
        return redirect(url_for('views.painel_gestor'))
    
@views.route('/painel_recrutador')
def painel_recrutador():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('views.login'))

    if session.get('role') == 'recrutador':
        recrutador = Recrutador.query.filter_by(email=session['usuario_logado']).first()
        if not recrutador:
            return redirect(url_for('views.login'))  # Se não encontrar o gestor, redireciona para login

        vagas = Vaga.query.all()
        return render_template('painel_recrutador.html', title='Painel - Recrutador',usuario_logado=session['usuario_logado'],  vagas=vagas)

    return redirect(url_for('views.nao_autorizado'))

@views.route('/recomendacoes_vaga', methods=['POST', 'GET'])
def recomendacoes_vaga():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('views.login'))
    
    if session.get('role') == 'recrutador':
        vaga_id = request.form['vaga']
        vaga = Vaga.query.get(vaga_id)
        perfil_desejado = PerfilDesejado.query.filter_by(vaga_id=vaga_id).first()
        habilidades_necessarias = HabilidadeNecessaria.query.filter_by(perfilDesejado_id = perfil_desejado.id).all()
        habilidades_necessarias_lista = []
        for habilidade in habilidades_necessarias:
                habilidades_necessarias_lista.append(habilidade.habilidadeBase_id)


        funcionarios = Funcionario.query.all()
        funcionarios_dados = []
        for funcionario in funcionarios:
            habilidades = Habilidade.query.filter_by(perfil_id = funcionario.perfil_id)
            habilidades_lista = []
            for habilidade in habilidades:
                habilidades_lista.append(habilidade.habilidadeBase_id)
            funcionarios_dados.append(
                {
                    'id' : funcionario.id,
                    'nome' : funcionario.nome,
                    'habilidades' : habilidades_lista
                }
            )
        
        print('Habilidades necessárias:', habilidades_necessarias_lista)
        entrada = [habilidades_necessarias_lista, funcionarios_dados]

        entrada_str = json.dumps(entrada)

        resp = cliente.chat.completions.create(
            messages=[
                {
                    "role" : "system",
                    "content" : prompt_ranking
                },
                {
                    "role" : "user",
                    "content" : entrada_str
                }
            ],
            model = modelo
        )
        ranking = resp.choices[0].message.content
        ranking_list = ast.literal_eval(ranking)

        print(ranking_list)

        recomendacoes = []
        j = 0
        for i in ranking_list:
            j+= 1
            usuario = Funcionario.query.get(i)
            habilidades = Habilidade.query.filter_by(perfil_id = usuario.perfil_id).all()
            str_habilidades = ''
            pontuacao = 0
            for habilidade in habilidades:
                habilidade_nome = HabilidadeBase.query.get(habilidade.habilidadeBase_id)
                pontuacao += habilidade.pontuacao
                str_habilidades += habilidade_nome.nomeHabilidade + ';'
            recomendacao = {'nome': usuario.nome, 'pontuacao': pontuacao, 'habilidades': str_habilidades}
            recomendacoes.append(recomendacao)
            if j> 9:
                break

            recomendacoes = sorted(recomendacoes, key=lambda x: x['pontuacao'], reverse=True)

        return render_template('recomendacoes_vaga.html', title='Recomendações', usuario_logado=session['usuario_logado'],  recomendacoes = recomendacoes, vaga = vaga)

    return redirect(url_for('views.nao_autorizado'))