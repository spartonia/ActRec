from controller import * 
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///models.db')

DBSession = sessionmaker(bind=engine)



rule_dbs = ['CausalRule', 'TriggerRule', 'AllowanceRule',
			'InhibitionRule', 'NonconcurrencyRule', 'DefaultRule']
# 1.
def add_time(max_time):  
	res_str = "time(0..{max_time}).\n".format(max_time=max_time)
	return res_str

# 2.
def prep_fluents(): 
	res_str = """"""
	session = DBSession() 
	for fluent in session.query(Fluent).all():
		res_str += "fluent({fluent}).\n".format(fluent=get_fluent(fluent.name))
	session.close()
	return res_str
# 2.
def prep_actions(): 
	res_str = """"""
	session = DBSession() 
	for action in session.query(Action).all():
		res_str += "action({action}).\n".format(action=action.name)
	session.close()
	return res_str

def prep_fluent_constraint(): 
	res_str = """"""
	constraint = ":- holds({fluent}, {time}), holds(neg({fluent}), {time}), fluent({fluent}), time({time}).\n"
	session = DBSession() 
	for fluent in session.query(Fluent).all():
		res_str += constraint.format(fluent=get_fluent(fluent.name), time='T')
	return res_str

# 4.
def prep_pair_rule():
	res_str = """"""
	session = DBSession() 
	pair_rule = "holds({fluent}, 0) :- not holds(neg({fluent}), 0).\
	 holds(neg({fluent}), 0) :- not holds({fluent}, 0).\n"
	for fluent in session.query(Fluent).all():
		res_str += pair_rule.format(fluent=get_fluent(fluent.name))
	session.close()
	return res_str
# 5. 
def prep_default_fluent():
	"""For flunets with default value. """
	res_str = """"""
	constraint = "holds({fluent}, {time}):- not holds(neg({fluent}), {time}), default({fluent}), fluent({fluent}), time({time}).\n"
	default_f = "default({fluent}).\n"
	session = DBSession() 
	
	for fluent in session.query(DefaultRule).all():
		res_str += constraint.format(fluent=get_fluent(fluent.name), time='T')
		res_str += default_f.format(fluent=get_fluent(fluent.name)) 
	return res_str
# 6. using grounder.
def prep_non_default_fluent(): 
	"""For fluents without default values (innertial)."""
	res_str = """"""
	constraint = "holds({f}, {t}+1) :- holds({f}, {t}), not holds(neg({f}), {t}+1), \n\
				   not default({f}), fluent({f}), time({t}), time({t}+1). \n\
				   holds(neg({f}), {t}+1) :- holds(neg({f}), {t}), not holds({f}, {t}+1), \n\
				   not default({f}), fluent({f}), time({t}), time({t}+1).\n"
	session = DBSession()
	all_fluents = set()
	for fluent in session.query(Fluent).all(): 
		all_fluents.add(get_fluent(fluent.name))

	default_fluents = set()
	for fluent in session.query(DefaultRule).all():
		default_fluents.add(get_fluent(fluent.fluent))

	for fluent in all_fluents - default_fluents: 
		res_str += constraint.format(f=fluent, t='T')
	return res_str 

# 7. 
def prep_static_rule(): 
	
	res_str = """"""
	eff = []
	pre = [] 
	session = DBSession()
	for srule in session.query(CausalRule).filter(CausalRule.action != None).all(): 
		eff = pickle.loads(srule.effect)
		pre = pickle.loads(srule.precond)
		current = ""
		for fluent in eff: 

			current += "holds({f}, {t}) :- ".format(f=fluent, t='T')
			for precond in pre: 
				current += 'holds({g},{t}), '.format(g=precond, t='T')
			current += '\n'
			for precond in pre: 
				current += "fluent({g}), ".format(g=get_fluent(precond))
			current += "fluent({f}), time({t}).\n\n".format(f=get_fluent(fluent), t='T')
		res_str += current + '\n'
	return res_str
# 8.
def prep_dynamic_rule(): 
	
	res_str = """"""
	eff = []
	pre = [] 
	session = DBSession()
	for srule in session.query(CausalRule).filter(CausalRule.action != None).all(): 
		eff = pickle.loads(srule.effect)
		pre = pickle.loads(srule.precond)
		action = srule.action
		current = ""
		for fluent in eff: 
			current += "holds({f}, {t}+1) :- holds(occurs({a}), {t}),".\
				format(f=fluent, t='T', a=action)
			for precond in pre: 
				current += 'holds({g},{t}), '.format(g=precond, t='T')
			current += '\n'
			for precond in pre: 
				current += "fluent({g}), ".format(g=get_fluent(precond)) 
			current += "fluent({f}), action({a}), time({t}), time({t}+1).\n\n".\
				format(f=get_fluent(fluent), t='T', a=action)
		res_str += current + '\n'

	return res_str

# 9. 
def prep_allowance_rule(): 
	res_str = """"""
	session = DBSession() 
	pre = []

	# to debug: for rule in session.query(CausalRule).filter(CausalRule.action != None).all():
	for rule in session.query(AllowanceRule).all(): 
		action = rule.action
		pre = pickle.loads(rule.precond)
		# print pre , action
		current = "" 
		current += "holds(allow(occurs({a})),{t}) :- not holds(ab(occurs({a})),{t}),\n".\
			format(a=action, t='T')
		for fluent in pre: 
			current += "holds({f}, {t}),".format(f=fluent, t='T')
		for fluent in pre: 
			current += "fluent({f}),".format(f=get_fluent(fluent))
		current += "action({a}), time({t}).\n\n".format(a=action, t='T')
		res_str += current + '\n'
	return res_str
# 10. ? 
def prep_exogenous_rule():
	ex_axtions = exogenous_actions()
	res_str = """"""
	for action in ex_axtions:
		res_str += "holds(allow(occurs({a})), {time}) :- action({a}), time({time}).\n".\
				format(a=action, time='T')
	return res_str
# 11. what should be 'm' replaced with? 
def prep_exogenous_allowed_rule(max_time):
	actions = exogenous_actions()
	actions.update(allowance_actions()) 

	res_str1 = """"""
	res_str2 = """"""
	for action in actions:
		res_str1 += "holds(occurs({action}), {time}) :- holds(allow(occurs({action})), {time}),\n\
		not holds(ab(occurs({action})), {time}),\n\
		not holds(neg(occurs({action})), {time}),\n\
		action({action}), time({time}), {time} < {m}.\n".\
		format(action=action, time='T', m=max_time)

		res_str2 += "holds(neg(occurs({action})), {time}) :- not holds(occurs({action}), {time}),\n\
		action({action}), time({time}), {time} < {m}.\n".\
		format(action=action, time='T', m=max_time)
	return res_str1 + '\n' + res_str2 
# 12. 
def prep_trigger_rule(): 
	res_str = """"""
	session = DBSession() 
	pre = []

	# debug : for rule in session.query(CausalRule).filter(CausalRule.action != None).all():
	for rule in session.query(TriggerRule).all(): 
		action = rule.action
		pre = pickle.loads(rule.precond)
		# print pre , action
		current = "" 
		current += "holds(occurs({a}),{t}) :- not holds(ab(occurs({a})),{t}),\n".\
			format(a=action, t='T')
		for fluent in pre: 
			current += "holds({f}, {t}),".format(f=fluent, t='T')
		for fluent in pre: 
			current += "fluent({f}),".format(f=get_fluent(fluent))
		current += "action({a}), time({t}).\n\n".format(a=action, t='T')
		res_str += current + '\n'
	return res_str
# 13.
def prep_inhibition_rule(): 
	res_str = """"""
	session = DBSession() 
	pre = []

	for rule in session.query(CausalRule).filter(CausalRule.action != None).all():
	# for rule in session.query(InhibitionRule).all(): 
		action = rule.action
		pre = pickle.loads(rule.precond)
		# print pre , action
		current = "" 
		current += "holds(ab(occurs({a})),{t}) :- ".\
			format(a=action, t='T')
		for fluent in pre: 
			current += "holds({f}, {t}),".format(f=fluent, t='T')
		for fluent in pre: 
			current += "fluent({f}),".format(f=get_fluent(fluent))
		current += "action({a}), time({t}).\n\n".format(a=action, t='T')
		res_str += current + '\n'
	return res_str

# 14. 
def prep_nonconcurrency_rule(): 
	res_str = """"""
	session = DBSession() 
	actions = []

	for rule in session.query(NonconcurrencyRule).all():
		actions = pickle.loads(rule.actions)
		current= " :- time({t}), 2{{".format(t='T')
		for action in actions: 
			current += "holds(occurs({a}), {t}) : action({a}),".\
				format(a=action, t='T')
		current = current[:-1] + "}.\n"
		res_str += current + '\n'
	return res_str

def prep_fluent_observation(): 
	res_str = """"""
	session = DBSession() 

	for rule in session.query(FluentObservation).all():
		if rule.time == 0: #belongs to initial observation
			res_str += "holds({f}, {t}).\n".\
			format(f=rule.fluent, t=rule.time)
	return res_str

def prep_action_query():
	res_str1 = ""
	res_str2 = ""
	session = DBSession()
	ex_axtions = exogenous_actions()

	for rule in session.query(ActionQuery).all():
		if rule.action in ex_axtions:
			res_str1 += "holds(occurs({a}), {t}).\n".\
			format(a=rule.action, t=rule.time)
		else: 
			res_str2 += ":- holds(neg(occurs({a})), {t}), action({a}), time({t}).\n".\
			format(a=rule.action, t=rule.time)
	return res_str1 + res_str2
	
def make_asp_script(): 
	"""Returns final mapped script in ASP format."""
	final_script = ""
	max_time = 5
	final_script += "\n%time\n"
	final_script += add_time(max_time)
	final_script += "\n%fluents\n"
	final_script += prep_fluents()
	final_script += "\n%actions\n"
	final_script += prep_actions()
	final_script += "\n%fluent constraint\n"
	final_script += prep_fluent_constraint()
	final_script += "\n%pair rule constraint\n"
	final_script += prep_pair_rule()
	 # default fluent test again.
	final_script += "\n%default fluent constraint\n"
	final_script += prep_non_default_fluent()
	final_script += "\n%static causal rule\n"
	final_script += prep_static_rule()
	final_script += "\n%dynamic causal rule\n"
	final_script += prep_dynamic_rule()
	# final_script += "\n%allowance rule\n"
	# final_script += prep_allowance_rule() 
	# final_script += "\n%exogenous actions\n"
	# final_script += prep_exogenous_rule()
	# final_script += "\n%exogenous or allowed actions \n"
	# final_script += prep_exogenous_allowed_rule(max_time)
	# final_script += "\n%trigger rule\n"
	# final_script += prep_trigger_rule()
	# final_script += "\n%inhibition rule\n"
	# final_script += prep_inhibition_rule()
	# final_script += "\n%non concurrency rule\n"
	# # final_script += prep_nonconcurrency_rule()
	# final_script += "\n%fluent observation\n"
	# final_script += prep_fluent_observation()
	# final_script += "\n%action query\n"
	# final_script += prep_action_query()

	return final_script 


if __name__ == "__main__": 
	print make_asp_script()

	


