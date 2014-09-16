# module for mapping AL and Observations to ASP. 

import subprocess 
import tempfile
import sys 

fluent_set = set() #[]
action_set = set() #[]
rule_list = []

def add_fluent(fluent):
	fluent_set.add(fluent)

def add_action(action):
	action_set.add(action)

def add_rule(cause, effect, if_=None):
	rule_string = ', '.join(cause) + " <causes> "+ ', '.join(effect)
	if if_:
		rule_string += " <if> " + ', '.join(if_)

	rule_list.append(rule_string)

def add_observation(some_observation):
	pass 
# def add_constraint() # <nonconcurrency> load, shoot.

## for test, remove these lines: 
add_fluent('f1')
add_fluent('f2')
add_action('a1')
add_rule(action_set, fluent_set)
add_rule(['a1'], ['f2'], ['f3'])
# sys.exit()

def make_input_script():
	""" makes a string script to feed into subprocess as input file"""
	ctaid_string = ""
	## add actions 
	ctaid_string += "<action> "
	ctaid_string += ", ".join(fluent_set)
	ctaid_string += ".\n\n"

	## add fluents
	ctaid_string += "<fluent> "
	ctaid_string += ", ".join(action_set)
	ctaid_string += ".\n\n"
	
	## add rules
	for rule in rule_list:
		ctaid_string += rule + '.\n'

	return ctaid_string

def main():
	input_str = make_input_script()
	print input_str
	# sys.exit()
	tmp = tempfile.NamedTemporaryFile(delete=False)
	tmp.write(input_str)
	tmp.seek(0)
	(result, error) = subprocess.Popen(['coala.bin', '-l', 'c_taid'], stdin=tmp, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	# tmp.colse()
	for line in result.split('\n'):
		print line


if __name__ == '__main__':
	main()
