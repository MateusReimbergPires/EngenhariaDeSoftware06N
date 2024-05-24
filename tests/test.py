from app.models import *

def test_vaga():
    vaga = Vaga(nomeVaga = 'Teste', departamento_id = 1, areaAtuacao_id = 1)
    db.session.add(vaga)
    perfilDesejado = PerfilDesejado(vaga_id=vaga.id)
    db.session.add(perfilDesejado)
    habilidadesBase = HabilidadeBase.query.all()
    habilidades = 'Programação,SEO,Recrutamento'
    habilidadesNecessaria = []
    for habilidade in habilidades:
        for base in habilidadesBase:
            if habilidade == base.nomeHabilidade:
                habilidadeNova = HabilidadeNecessaria(habilidadeBase_id=base.id, perfilDesejado=perfilDesejado)
                habilidadesNecessaria.append(habilidadeNova)

    for habilidade in habilidadesNecessaria:
        db.session.add(habilidade)

    db.session.commit()