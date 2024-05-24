from . import db

class Gestor(db.Model):
    __tablename__ = 'gestor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100))
    entrada = db.Column(db.Date, nullable=False)
    senha = db.Column(db.String(255))
    # Uma relação one-to-one com Departamento
    departamento = db.relationship('Departamento', backref=db.backref('gestor', uselist=False), uselist=False)

class Departamento(db.Model):
    __tablename__ = 'departamento'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    gestor_id = db.Column(db.Integer, db.ForeignKey('gestor.id'), nullable=False)
    # Relações one-to-many com Funcionario e Vaga
    funcionarios = db.relationship('Funcionario', backref='departamento')
    vagas = db.relationship('Vaga', backref='departamento')

class Funcionario(db.Model):
    __tablename__ = 'funcionario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    entrada = db.Column(db.Date, nullable=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'))
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfil.id'))
    # Relação one-to-one com Perfil
    perfil = db.relationship('Perfil', backref=db.backref('funcionario', uselist=False))

class Vaga(db.Model):
    __tablename__ = 'vaga'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeVaga = db.Column(db.String(100), nullable=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'), nullable=False)
    areaAtuacao_id = db.Column(db.Integer, db.ForeignKey('areaAtuacao.id'), nullable=False)
    # Relação one-to-one com PerfilDesejado
    perfilDesejado = db.relationship('PerfilDesejado', backref='vaga', uselist=False)

class Perfil(db.Model):
    __tablename__ = 'perfil'
    id = db.Column(db.Integer, primary_key=True)
    areaAtuacao_id = db.Column(db.Integer, db.ForeignKey('areaAtuacao.id'))

    habilidades = db.relationship('Habilidade', backref='perfil')

class AreaAtuacao(db.Model):
    __tablename__ = 'areaAtuacao'  # Garanta que o nome da tabela está correto aqui e nas ForeignKey
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeArea = db.Column(db.String(100), nullable=False)

    perfis = db.relationship('Perfil', backref='areaAtuacao')
    # Relações one-to-many com Perfil e Vaga
    vagas = db.relationship('Vaga', backref='areaAtuacao')

class HabilidadeBase(db.Model):
    __tablename__ = 'habilidadeBase'
    id = db.Column(db.Integer, primary_key=True)
    nomeHabilidade = db.Column(db.String(100))

    # Relação one-to-many com Habilidade
    habilidades = db.relationship('Habilidade', backref='habilidadeBase')

class Habilidade(db.Model):
    __tablename__ = 'habilidade'
    id = db.Column(db.Integer, primary_key=True)
    pontuacao = db.Column(db.Numeric(5,2))
    habilidadeBase_id = db.Column(db.Integer, db.ForeignKey('habilidadeBase.id'))
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfil.id'))

class PerfilDesejado(db.Model):
    __tablename__ = 'perfilDesejado'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vaga_id = db.Column(db.Integer, db.ForeignKey('vaga.id'))
    # Certifique-se de que as habilidades necessárias estejam corretamente relacionadas.
    habilidadesNecessarias = db.relationship('HabilidadeNecessaria', backref='perfilDesejado')

class HabilidadeNecessaria(db.Model):
    __tablename__ = 'habilidadeNecessaria'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    habilidadeBase_id = db.Column(db.Integer, db.ForeignKey('habilidadeBase.id'), nullable=False)
    perfilDesejado_id = db.Column(db.Integer, db.ForeignKey('perfilDesejado.id'), nullable=False) 

class Recrutador(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeRecrutador = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    senha = db.Column(db.String(255))
