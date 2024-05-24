from app.models import *

def test_vaga():
    vaga = Vaga(nomeVaga = 'Teste', departamento_id = 1, areaAtuacao_id = 1)
    perfilDesejado = PerfilDesejado(vaga_id=vaga.id)
