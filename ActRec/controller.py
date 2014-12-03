import pickle, re
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.exc import IntegrityError

from models import * #Base, Fluent, Action 

engine = create_engine('sqlite:///models.db')
# Bind the engine to the metadata of Base class
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# DBSession instance establishes all conversations with the database 
 

def add_fluent(session, fluent): 
	try: 
		# session = DBSession()
		new_fluent = Fluent(name=fluent)
		session.add(new_fluent)
		session.commit() 
	except IntegrityError, e:
		print "Error inserting fluent '{}'! Duplicate fluent (probably).".\
			format(fluent)
	except Exception, e: 
		print e
	finally: 
		session.close()
def add_fluent_string(string): 
	fluents = [ i.strip().replace(' ', '_') for i in string.split(',') ]
	for i in fluents: 
		session = DBSession()
		add_fluent(session, i)

def add_action(session, action):
	try: 
		# session = DBSession()
		new_action = Action(name=action)
		session.add(new_action)
		session.commit() 
	except IntegrityError: 
		print "Error inserting action '{}'! Duplicate action (probably).".\
			format(action)
	except Exception, e: 
		print e
	finally: 
		session.close() 

def add_action_string(string): 
	actions = [ i.strip().replace(' ', '_') for i in string.split(',') ]
	for i in actions: 
		session = DBSession()
		add_fluent(session, i)

def add_rule(session, r_type,**kwargs ): 
	session = session
	try: 
		if r_type == 'causal':
			action = kwargs.get('action')
			effect = kwargs.get('effect')
			precond = kwargs.get('precond')
			new_rule = CausalRule(action=action, effect=effect, precond=precond)

		elif r_type == 'trigger':
			action = kwargs.get('action')
			precond = kwargs.get('precond')
			new_rule = TriggerRule(action=action, precond=precond)

		elif r_type == 'allowance': 
			action = kwargs.get('action')
			precond = kwargs.get('precond')
			new_rule = AllowanceRule(action=action, precond=precond)

		elif r_type == 'inhibition':
			action = kwargs.get('action')
			precond = kwargs.get('precond')
			new_rule = InhibitionRule(action=action, precond=precond)

		elif r_type == 'nonconcurrency': 
			actions = kwargs.get('actions')
			new_rule = NonconcurrencyRule(actions=actions)

		elif r_type == 'default':
			fluent = kwargs.get('fluent')
			new_rule =DefaultRule(fluent=fluent)

		elif r_type == 'fluentobservation': 
			fluent = kwargs.get('fluent')
			time = kwargs.get('time')
			new_rule = FluentObservation(fluent=fluent, time=time)

		elif r_type == 'actionquery': 
			action = kwargs.get('action')
			time = kwargs.get('time')
			new_rule = ActionQuery(action=action, time=time)

		else: 
			raise "r_type not valid."
			# return 
		session.add(new_rule)
		session.commit()
		print "Success! New {} rule inserted!".format(r_type)
	except IntegrityError, e:
		print "Error! New {} rule not inserted: Duplicate row (probably).".\
			format(r_type)
		print e 
	except Exception,e:
		print "Error! Rule {0} not inserted:".format(r_type)
		print e 
	finally: 
		session.close()

def assert_islist(alist):
	if not isinstance(alist, list):
		raise Exception("Error! '{0}' must be a list not {1}".\
				format(alist, type(alist).__name__) )

def assert_action_defined(action): 
	actions = all_actions()
	if action not in actions:
		raise Exception("Error! Action '{}' is not defined.".\
			format(action))

def assert_fluent_defined(fluent):
	fluents = all_fluents()
	fluent = get_fluent(fluent)

	if fluent not in fluents:
		raise Exception("Error! Fluent '{}' is not defined.".\
			format(fluent) )

def add_dynamic_causal_rule(action, effects, preconds):
	assert_islist(effects)
	assert_islist(preconds)
	assert_action_defined(action)
	for fluent in effects:
		assert_fluent_defined(fluent)
	for fluent in preconds:
		assert_fluent_defined(fluent)
	
	# add rule 
	session = DBSession()
	kwargs = {}
	kwargs['action'] = action 
	kwargs['effect'] = pickle.dumps(effects)
	kwargs['precond'] = pickle.dumps(preconds)
	add_rule(session, r_type='causal', **kwargs)

def add_static_causal_rule(effects, preconds):
	assert_islist(effects)
	assert_islist(preconds)
	for fluent in effects:
		assert_fluent_defined(fluent)
	for fluent in preconds:
		assert_fluent_defined(fluent)
	
	# add rule 
	session = DBSession()
	kwargs = {}
	kwargs['effect'] = pickle.dumps(effects)
	kwargs['precond'] = pickle.dumps(preconds)
	add_rule(session, r_type='causal', **kwargs)

def add_trigger_rule(action, preconds):
	assert_islist(preconds)
	assert_action_defined(action)
	for fluent in preconds:
		assert_fluent_defined(fluent)
	
	# add rule 
	session = DBSession()
	kwargs = {}
	kwargs['action'] = action 
	kwargs['precond'] = pickle.dumps(preconds)
	add_rule(session, r_type='trigger', **kwargs)

def add_allowance_rule(action, preconds):
	assert_islist(preconds)
	assert_action_defined(action)
	for fluent in preconds:
		assert_fluent_defined(fluent)
	
	# add rule 
	session = DBSession()
	kwargs = {}
	kwargs['action'] = action 
	kwargs['precond'] = pickle.dumps(preconds)
	add_rule(session, r_type='allowance', **kwargs)

def add_inhibition_rule(action, preconds):
	assert_islist(preconds)
	assert_action_defined(action)
	for fluent in preconds:
		assert_fluent_defined(fluent)
	
	# add rule 
	session = DBSession()
	kwargs = {}
	kwargs['action'] = action 
	kwargs['precond'] = pickle.dumps(preconds)
	add_rule(session, r_type='inhibition', **kwargs)

def add_nonconcurrency_rule(actions):
	assert_islist(actions)
	if len(actions) < 2: 
		raise Exception("Error! Non-concurrency rule must contain at least two actions.")
	for action in actions: 
		assert_action_defined(action)
	
	# add rule 
	session = DBSession()
	kwargs = {}
	kwargs['actions'] = pickle.dumps(actions)  
	add_rule(session, r_type='nonconcurrency', **kwargs)

def add_default_rule(fluent):
	assert_fluent_defined(fluent)
	
	# add rule 
	session = DBSession()
	kwargs = {}
	kwargs['fluent'] = fluent  
	add_rule(session, r_type='default', **kwargs)

def add_fluent_observation(fluent, at_time):
	assert_fluent_defined(fluent)
	
	# add rule 
	session = DBSession()
	kwargs = {}
	kwargs['fluent'] = fluent
	kwargs['time'] = at_time  
	add_rule(session, r_type='fluentobservation', **kwargs)

def add_action_query(action, at_time):
	assert_action_defined(action)
	
	# add rule 
	session = DBSession()
	kwargs = {}
	kwargs['action'] = action
	kwargs['time'] = at_time  
	add_rule(session, r_type='actionquery', **kwargs)

def remove_rule(session, table, row_id): 
	session = session
	try: 
		if session.query(table).filter_by(id=row_id).delete() == 1:
			print "row_id '%s' deleted from table %s" %(row_id, table.__name__)
		else:
			print "Record not deleted!" 
	except Exception, e:
		raise e 
		# print "Record not deleted!"
	finally:
		session.commit()
		session.close() 

def clear_table(tbl_name): 
	session = DBSession()
	try: 
		dlt = session.query(tbl_name).filter().delete()
		print "{} row(s) removed from table '{}'.".format(dlt, tbl_name.__name__)
	except Exception, e:
		session.close()
		print e 
	finally: 
		session.commit() 

def get_fluent(string):
	""" Extracts fluent out of string, e.g. 'neg(fluent)' -> 'fluent'. """
	pattern = r'^neg[\s]*\([\s]*(\w+)[\s]*\)|(\w+)'
	obj = re.search(pattern, string, re.I)
	try: 
		if obj.group(1): 
			return obj.group(1)
		else: 
			return obj.group(2)
	except: 
			return string
	
def all_fluents():
	session = DBSession()
	fluents = set() 
	try:
		for fluent in session.query(Fluent).all(): 
			fluents.add(fluent.name)

	except Exception, e:
		raise e
	return fluents

def all_actions():
	session = DBSession()
	actions = set() 
	try:
		for action in session.query(Action).all(): 
			actions.add(action.name)

	except Exception, e:
		raise e
	return actions

def allowance_actions():
	session = DBSession()
	actions = set() 
	try:
		for rule in session.query(AllowanceRule).all():
			actions.add(rule.action)

	except Exception, e:
		raise e
	return actions

def trigger_actions():
	session = DBSession()
	actions = set() 
	try:
		for rule in session.query(TriggerRule).all():
			actions.add(rule.action)

	except Exception, e:
		raise e
	finally:
		session.close() 
	return actions

def exogenous_actions():
	session = DBSession()
	ex_actions = set() 
	tr_actions = trigger_actions()
	allow_actions = allowance_actions()
	all_actions = set()
	# exogenous actions = all actions - trigger actions - allowance actions
	try:
		for action in session.query(Action).all(): 
			all_actions.add(action.name)
		ex_actions = all_actions - allow_actions - tr_actions
	except Exception, e:
		print e 
	finally:
		session.close() 
	return ex_actions
	
	# Base.metadata.drop_all()
	# for table in reversed(Base.metadata.sorted_tables):
	# 	print table
	
def clear_db(): 
	""" Drops all tables in the database"""
	Base.metadata.drop_all() 

		
if __name__ == "__main__": 

	# clear_db()
	# string = ""
	# add_fluent_string(string)
	# import sys 
	# sys.exit() 

	# coffee_fluents = ['coffe_m_is_on', 
	# 				'coffe_m_has_powder', 
	# 				'coffe_m_has_old_coffe_powder',
	# 				'coffe_m_has_water',
	# 				'coffe_m_is_jug_removed']
	# coffee_actions = ['coffe_m_activate',
	# 				'coffe_m_add_coffe_powder',
	# 				'coffe_m_remove_coffe_powder',
	# 				'coffe_m_add_water',
	# 				'coffe_m_add_jug',
	# 				'coffe_m_remove_jug']

	pasta_fluents = ['heat_on',
					'vessel_on_heat',
					'vessel_water_full',
					'vessel_pasta_full', 
					'pasta_cooked',
					'vessel_sauce_full', 
					'pasta_sauce_mixed',
					'vessel_has_boiled_water', 
					'pasta_water_drained', 	
					'pasta_ready'
					]
	pasta_actions = ['vessel_water_boil',
					'pasta_boil',
					'pasta_cooked_drain',
					'pasta_sauce_add',
					]

	# for f in pasta_fluents: 
	# 	session = DBSession() 
	# 	add_fluent(session, f)
	# for i in all_fluents(): 
	# 	print i 

	# for a in pasta_actions: 
	# 	session = DBSession() 
	# 	add_action(session, a)

	# for i in all_actions(): 
	# 	print i 

	for i in all_fluents():
		print i 
		
	## 1) To clear a table in the data base, we use following function: #########################
	## clear_table(tbl_name) 																	#
	## Note: tbl_name is the name of table class defined in models.py module. 					# 
	# clear_table(TriggerRule)
	# clear_table(CausalRule)

	#### To clear all tables in the database, all at once, use : 
	# clear_db() 																				


	## 2) Note: If we create a new database, i.e. used clear_db(), then we need to populate DB with new fluents and actions.
	# To do so uncomment the lines below: 

	# # add fluents: 
	# for f in coffee_fluents: 
	# 	session = DBSession()
	# 	add_fluent(session, f)
	# # # add actions: 
	# for a in coffee_actions: 
	# 	session = DBSession() 
	# 	add_action(session, a)


	# 3) To add new rules, we use following functions. #####################################

	# add_action_query('coffe_m_add_coffe_powder', 2)
	# add_fluent_observation('coffe_m_is_jug_removed', 4)
	# add_default_rule('coffe_m_is_jug_removed')
	# add_nonconcurrency_rule(['coffe_m_remove_coffe_powder', 'coffe_m_add_water'])
	# add_inhibition_rule('coffe_m_activate', ['coffe_m_has_old_coffe_powder'] ) 
	# add_allowance_rule('coffe_m_activate', ['coffe_m_has_old_coffe_powder'] ) 
	# add_trigger_rule('coffe_m_activate', ['coffe_m_has_old_coffe_powder'] )
	# add_static_causal_rule(['coffe_m_is_on'], ['coffe_m_has_old_coffe_powder'] )
	# add_dynamic_causal_rule('coffe_m_remove_coffe_powder', ['coffe_m_is_on'], ['coffe_m_has_old_coffe_powder'] )

	# add_dynamic_causal_rule('vessel_water_boil', 
	# 						['vessel_has_boiled_water'], 
	# 						['vessel_water_full', 'heat_on', 'vessel_on_heat'])
	# add_dynamic_causal_rule('pasta_boil', 
	# 						['pasta_cooked'],
	# 						['heat_on', 'vessel_on_heat', 'vessel_has_boiled_water', 'vessel_pasta_full'])
	# add_dynamic_causal_rule('pasta_cooked_drain', 
	# 						['pasta_water_drained'],
	# 						['pasta_cooked'])
	# add_dynamic_causal_rule('pasta_sauce_add', 
	# 						['pasta_sauce_mixed'], 
	# 						['pasta_cooked', 'vessel_sauce_full', 'vessel_pasta_full', 'heat_on', 'vessel_on_heat'])
	# add_static_causal_rule(['pasta_ready'],
	# 						['pasta_sauce_mixed'])



	