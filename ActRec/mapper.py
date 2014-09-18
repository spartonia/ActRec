# module for mapping AL and Observations to ASP. 

import subprocess 
import tempfile
import sys, os


if sys.version.rsplit()[0] < '2.5':
	print 'You need at least python 2.5 to run coala'
	sys.exit(1)
	
# defined that early to extract coala version from binary
def checkProgram(prog):
	try:
		(result, error) = subprocess.Popen([prog, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	except OSError, err:
		print err
		return False
	
	if result != '':
		return result.splitlines()[0]
	else:
		return False

version = checkProgram("coala.bin")
if not version:
	print "There is a problem with the coala binary file. Is it in your $PATH, is it executable, is it compiled for your architecture?"
	sys.exit(1)


fluent_set = set() #[]
action_set = set() #[]
rule_list = []
observation_list = []
query_list = []


def add_fluent(fluent):
	fluent_set.add(fluent)

def add_action(action):
	action_set.add(action)

def add_causal_rule(cause, effect, if_=None):
	""" Rules of the form:  'a' causes (f1, f2, ...) [if (g1, g2,..)] """
	rule_string = ', '.join(cause) + " <causes> "+ ', '.join(effect)
	if if_:
		rule_string += " <if> " + ', '.join(if_)

	rule_list.append(rule_string)

def add_triger_rule(fluent_list, action):
	""" Rules of the form (f1, f2, ..) triggers 'a' """
	rule_string = ', '.join(fluent_list) + ' <triggers> ' + ', '.join(action)
	rule_list.append(rule_string)

def add_allowance_rule(fluent_list, action):
	""" Rules of the form (f1, f2, ..) allows 'a' """
	rule_string = ', '.join(fluent_list) + ' <allows> ' + ', '.join(action)
	rule_list.append(rule_string)

def add_inhibition_rule(fluent_list, action):
	""" Rules of the form (f1, f2, ..) inhibits 'a' """
	rule_string = ', '.join(fluent_list) + ' <inhibits> ' + ', '.join(action)
	rule_list.append(rule_string)

def add_nonconcurrency_rule(action_list):
	""" Rules of the form (nonconcurrency a1, a2, ..) """
	rule_string = '<nonconcurrency> ' + ', '.join(action_list)
	rule_list.append(rule_string)

def add_default(fluent):
	rule_string = '<default> ' + ', '.join(fluent)
	print rule_string
	rule_list.append(rule_string)

######## Observation: 
def add_at(fluent, time):
	""" Observation of the form 'f' <at> 't' """
	return '{0} <at> {1}'.format(fluent, time)

def add_occurs_at(action, time):
	""" Observation of the form 'a' <occurs at> 't' """
	return '{0} <occurs at> {1}'.format(action, time)


## query:
# do something here. 

def make_input_script():
	""" makes a string script to feed into subprocess as input file"""
	ctaid_string = ""
	## add actions 
	ctaid_string += "<action> "
	ctaid_string += ", ".join(action_set)
	ctaid_string += ".\n\n"

	## add fluents
	ctaid_string += "<fluent> "
	ctaid_string += ", ".join(fluent_set)
	ctaid_string += ".\n\n"
	
	## add rules
	for rule in rule_list:
		ctaid_string += rule + '.\n'
	if observation_list:
		for obs in observation_list:
			pass
	## add queries:
	if query_list:
		for query in query_list:
			pass
	return ctaid_string

def main():
	## for test, remove these lines: 
	coffee_fluents = ['coffe_m_is_on', 
					'coffe_m_has_powder', 
					'coffe_m_has_old_coffe_powder',
					'coffe_m_has_water',
					'coffe_m_is_jug_removed']
	coffee_actions = ['coffe_m_activate',
					'coffe_m_add_coffe_powder',
					'coffe_m_remove_coffe_powder',
					'coffe_m_add_water',
					'coffe_m_add_jug',
					'coffe_m_remove_jug']

	# coffe_m_add_coffe_powder CAUSE coffe_m_has_water IF 
						# neg(coffe_m_is_on), neg(coffe_m_has_powder), 
						# coffe_m_in_action_space 

	for fluent in coffee_fluents:
		add_fluent(fluent)
	for action in coffee_actions:
		add_action(action)
	
	test_cause = ['coffe_m_add_coffe_powder']
	test_effect = ['coffe_m_has_water']
	test_precond = ['-coffe_m_is_on', '-coffe_m_has_powder', 'coffe_m_in_action_space']
	add_causal_rule(test_cause, test_effect, test_precond)
	add_default(fluent_set)

	# test_actions = ['a1', 'a2', 'a3', 'a4']
	# test_fluents = ['f1', 'f2', 'f3', 'f4', 'f5']
	# for a in test_actions:
	# 	add_action(a)
	# for f in test_fluents:
	# 	add_fluent(f)

	# add_causal_rule(list(action_set)[1:3], list(fluent_set)[:2])
	# add_causal_rule(list(action_set)[:3], list(fluent_set)[:-1])
	# add_default(list(fluent_set)[3:])

	input_str = make_input_script()
	print input_str
	# sys.exit()
	useiclingo = False

	if not useiclingo: 
		tmp = tempfile.NamedTemporaryFile(delete=False)
		tmp.write(input_str)
		tmp.seek(0)
		(result, error) = subprocess.Popen(['coala.bin', '-l', 'c_taid'], stdin=tmp, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
		# tmp.colse()
		for line in result.split('\n'):
			print line
	else: 
		pass 


if __name__ == '__main__':
	try:
		sys.exit(main())
	except Warning, warn:
		sys.stderr.write('WARNING: %s\n' % str(warn))
	except Exception, err:
		sys.stderr.write('ERROR: %s\n' % str(err))
		sys.exit(1)
