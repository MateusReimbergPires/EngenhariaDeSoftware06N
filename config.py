import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = 'teste'

SQLALCHEMY_DATABASE_URI = '{SGDB}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGDB = 'mysql+mysqlconnector',
    usuario = 'root',
    senha = os.getenv('SENHA'),
    servidor = 'localhost',
    database = 'empresa'
)