# import sqlalchemy 
from sqlalchemy import create_engine 
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, PickleType
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import relationship 

Base = declarative_base()

class Action(Base):
	__tablename__ = 'action'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False, unique=True)

class Fluent(Base):
	__tablename__ = 'fluent'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False, unique=True)

class CausalRule(Base): 
	__tablename__ = 'causal_rule'
	id = Column(Integer, primary_key=True)
	action = Column(String(250), nullable=True)
	effect = Column(PickleType, nullable=False)
	precond = Column(PickleType, nullable=False)
	__table_args__ = (UniqueConstraint('action', 'effect', 'precond', name='_causal_rule_uc'),
					)

class TriggerRule(Base): 
	__tablename__ = 'trigger_rule'
	id = Column(Integer, primary_key=True)
	precond = Column(PickleType, nullable=False)
	action = Column(String(250), nullable=False)
	__table_args__ = (UniqueConstraint('precond', 'action', name='_trigger_rule_uc'),
		)

class AllowanceRule(Base): 
	__tablename__ = 'allowance_rule'
	id = Column(Integer, primary_key=True)
	precond = Column(PickleType, nullable=False)
	action = Column(String(250), nullable=False)
	__table_args__ = (UniqueConstraint('precond', 'action', name='_allowance_rule_uc'),
		)

class InhibitionRule(Base): 
	__tablename__ = 'Inhibition_rule'
	id = Column(Integer, primary_key=True)
	precond = Column(PickleType, nullable=False)
	action = Column(String(250), nullable=False)
	__table_args__ = (UniqueConstraint('precond', 'action', name='_Inhibition_rule_uc'),
		)

class NonconcurrencyRule(Base):
	__tablename__ = "nonconcurrency_rule"
	id = Column(Integer, primary_key=True)
	actions = Column(PickleType, nullable=False)
	__table_args__ = (UniqueConstraint('actions', name='_nonconcurrency_uc'),
		)
class DefaultRule(Base):
	__tablename__ = "default_rule"
	id = Column(Integer, primary_key=True)
	fluent = Column(String(250), nullable=False)
	value = Column(Boolean(), nullable=False)
	__table_args__ = (UniqueConstraint('fluent', name='_default_rule_uc'),
		)
class FluentObservation(Base): 
	__tablename__ = "fluent_observation"
	id = Column(Integer, primary_key=True)
	fluent = Column(String(250), nullable=False)
	time = Column(Integer, nullable=False)
	__table_args__ = (UniqueConstraint('fluent', 'time', name='_fluent_time_uc'),
		)

class ActionQuery(Base):
	__tablename__ = 'action_query'
	id = Column(Integer, primary_key=True)
	action = Column(String(250), nullable=False)
	time = Column(Integer, nullable=False)
	__table_args__ = (UniqueConstraint('action', 'time', name='_action_time_uc'),
		)
def create_db(dbName): 
	db = 'sqlite:///' + dbName
	engine = create_engine(db)
	Base.metadata.create_all(engine, checkfirst=True) # , checkfirst=True


if __name__ == "__main__":
	create_db('models.db')
	print "Database model created!"	



