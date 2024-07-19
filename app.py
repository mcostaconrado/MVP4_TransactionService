from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from model import Session
#from model.Registro import Registro
from model.Transaction import Transaction
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="PUC Trading Bank - Transaction service", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentation", description="Documentation of User service")
routes_tag = Tag(name="Routes", description="Implemented routes for Transaction service")


@app.get('/', tags=[home_tag])
def home():
    """Redirects to the Swagger documentation of Transaction Service
    """
    return redirect('/openapi/swagger')

@app.post('/transaction', tags=[routes_tag],
          responses={"200": TransactionViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_transaction(form: TransactionSchema):
    """Insert a new transaction to the database
    Returns a representation of the new inserted transaction
    """      
        
    transaction = Transaction(
        id_source = form.id_source,
        currency_source = form.currency_source,
        id_target = form.id_target,
        currency_target = form.currency_target,
        amount = form.amount,
        translation_rate=1   
        )
        
    try: 
        session = Session()
        session.add(transaction)
        session.commit()
        logger.debug(f"Adding transaction'")
        return reprTransaction(transaction), 200
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Error regis]"
        error_msg = e
        # logger.warning(e)
        # logger.warning(f"Erro ao adicionar registro '{registro.titulo}' do dia '{registro.data_registro}, {error_msg}")
        return {"mesage": error_msg}, 400
  
@app.get('/transaction', tags=[routes_tag],
         responses={"200": TransactionViewSchema, "404": ErrorSchema})
def get_transaction(query: TransactionSearchSchema):
    """ Search for a transaction id in the database
    Returns information about the transaction
    """
    
    id = query.id     
    
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    
    transaction = session.query(Transaction).filter(Transaction.id == id).first()
    
    if not transaction:
        # se o registro não foi encontrado
        error_msg = "There is no transaction registered with this id in the database."
        logger.warning(f"Error getting a transaction with id #{id}, {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Registro encontrado!")
        # retorna a representação de registro
        return reprTransaction(transaction), 200

@app.get('/transactions', tags=[routes_tag],
         responses={"200": ListTransactionsViewSchema, "404": ErrorSchema})
def get_transactions(query: TransactionsSearchSchema):
    """ Search for all transactions a user was involved in
    Returns a list of transactions and their information
    """
    id_user = query.id_user
    
    # criando conexão com a base
    session = Session()
    # fazendo a busca

    transactions = session.query(Transaction).filter(or_(Transaction.id_source == id_user, Transaction.id_target == id_user))
    response = []
    
    for transaction in transactions:
        response.append(reprTransaction(transaction))
    
    return {"transactions": response}, 200
