from pydantic import BaseModel
from typing import Optional, List
from model.Transaction import Transaction
from datetime import datetime

class TransactionSchema(BaseModel):
    """ Defines data for a new transaction to be insert
    """
    id_source: int = 1
    currency_source: str = "USD"
    id_target: int = None
    currency_target: str = "USD"
    amount: float = 50.0


class TransactionViewSchema(BaseModel):
    """ Defines how a transaction is returned
    """
    id_transaction: int = 1
    id_source: int = 1
    currency_source: str = "USD"
    id_target: int = 1
    currency_target: str = "USD"
    amount: float = 50.0
    translation_rate: float = 1.0
    registration_date : datetime = datetime.now()

    

def reprTransaction(transaction:Transaction):
    return {
        "id": transaction.get_id(),
        "id_source": transaction.get_source()[0],
        "currency_source": transaction.get_source()[1],
        "id_target": transaction.get_target()[0],
        "currency_target": transaction.get_target()[1],
        "amount": transaction.get_amount(),
        "translation_rate": transaction.get_translation_rate(),
        "registration_date": transaction.get_registration_date()
    }

class TransactionSearchSchema(BaseModel):
    """ Defines the structure to search for a specific transaction by giving its id. 
    """
    id: int = 1 
    
class TransactionsSearchSchema(BaseModel):
    """ Defines the structure to search for all the transactions envolving a specific user by giving its id.
    """
    id_user: int = 1 

class ListTransactionsViewSchema(BaseModel):
    """ Define the structure of a list of transactions.
    """
    transactions:List[TransactionViewSchema]