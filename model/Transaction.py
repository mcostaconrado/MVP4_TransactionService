from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class Transaction(Base):
    
    __tablename__ = 'transactions'
    
    id = Column("id", Integer, primary_key = True) 
    id_source = Column(Integer, nullable=True)
    currency_source = Column(String(3))
    id_target = Column(Integer, nullable=True)
    currency_target = Column(String(3))

    amount = Column(Float)
    translation_rate = Column(Float)
    
    registration_date =  Column(DateTime, default = datetime.now())

    
    def __init__(self, id_source:int, currency_source:str, id_target:int, currency_target:str, amount:float, translation_rate:float=1.0):
        
        self.id_source = id_source
        self.currency_source = currency_source
        self.id_target = id_target
        self.currency_target = currency_target
        
        self.amount = amount
        self.translation_rate = translation_rate
   
        self.registration_date = datetime.now()
    
    def get_id(self):
        return self.id
    
    def get_source(self):
        return self.id_source, self.currency_source
    
    def get_target(self):
        return self.id_target, self.currency_target
    
    def get_amount(self):
        return self.amount
    
    def get_translation_rate(self):
        return self.translation_rate
            
    def get_registration_date(self):
        return self.registration_date

        
        