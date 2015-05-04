from __future__ import division 
from asp_parser import * 
import collections 
from controller import add_action_observation_from_file, add_action 

RECOGNIZED = 1
UNCOMPLETE = 0 
NOTRECOGNIZED = -1

def make_fluent_world(answerSet): 
    """creates a world from the answer set, representing all states and their fluents holding in the states."""
    states = {}
     
    for state, fluent in get_answerset_fluents(answerSet): 
        try:
            states[state]
        except KeyError, e:
            states[state] = set() 
        states[state].add(fluent)
    for state, setOfFluents in states.iteritems():
        yield state, setOfFluents

def make_action_world(answerSet, verbose=False): 
    """Creates a world from the answer set, representing all states and actions which hold in those states."""
    states = {} 
    for state, action in get_answerset_actions(answerSet):
        try:
            states[state]
        except KeyError, e:
            states[state] = set() 
        states[state].add(action)
    for state, setOfActions in states.iteritems():
    	if verbose: 
	    	print 'state ', state, ":", [a for a in setOfActions]
        yield state, setOfActions

def activity_recog_by_actions(answerSet, actionList, verbose = False, ordered=True):
	"""Recognize activty by checking whether a sequence of actions performed."""

	states = {}
	for state, actionSet in make_action_world(answerSet, verbose=verbose):
		states[state] = actionSet

	states = collections.OrderedDict(sorted(states.items()))
	if (not actionList) or (not states): return NOTRECOGNIZED # NO action list privided 
	
	if verbose:
		print "\nActions in each state: "
		for state, actionSet in states.iteritems(): 
			print 'State ', state, ' : ', [i for i in actionSet]
		print 
		print "Act list: \n", actionList
		print 

	if len(actionList) > len(states): 
		print "Intended activity (Action list) is longer that the world!"
		print "\t|--> activity length='{0}', world length='{1}'."\
				.format(len(actionList), len(states))
		print 'NOTRECOGNIZED'
		return NOTRECOGNIZED

	if not ordered:
		# A-activity type recognition (un-ordered)
		worldActions = set()
		for i in states.values() :
			worldActions = worldActions.union(i)
		if set(actionList).issubset(worldActions): 
			print "RECOGNIZED"
			return RECOGNIZED
		print "NOTRECOGNIZED"
		return NOTRECOGNIZED

	# O-activity (ordered activity) type recognition
	startState = None
	prevState = None 
	for action_no, action in enumerate(actionList): 
		for state, actionSet in states.iteritems(): 
			if startState == None: 
				if set([action]).issubset(actionSet):
					startState = state
					prevState = state
					if verbose: 
						print "Activity started at state {0}.\n".format(startState)
					break
				else:
					continue
			if startState != None and state <= prevState: 
				continue
			if set([action]).issubset(set(actionSet)):
				prevState = state
				if action_no == len(actionList) -1: 
					# last one in the action list 
					if verbose: 
						print "..and finished at state '{0}'.".\
						format(prevState) 
						print "RECOGNIZED"
					return RECOGNIZED
				else:
					break 
			else:
				continue
	if startState: 
		print "UNCOMPLETE"
		return UNCOMPLETE
	print "NOTRECOGNIZED"
	return NOTRECOGNIZED


def activity_recog_by_fluents(answerSet, initSet, finalSet, verbose=False): 
	""" Recognize activty by checking whether Initial and final state conditions are met."""
	# what if initSet and final sets are empty? 
	states = {} 
	for state, fluentSet in make_fluent_world(answerSet): 
		states[state] = fluentSet
	# sort states 
	states = collections.OrderedDict(sorted(states.items()))
 	if verbose:
 		print "All States: "
 		for state, fluentSet in states.iteritems():
 			print "State ", state, ' : ', fluentSet
		print
	print "Initial State: ", [i for i in initSet]
 	print "Goal State:    ", [i for i in finalSet]
 	print

 	initState = None 
 	finalState = None
 	for state, fluentSet in states.iteritems():
 		if initState == None:
	 		if initSet.issubset(fluentSet):
	 			initState = state
	 			print "init state is subset of state: ", state 
	 			continue
	 	
		if initState != None and finalState == None:
			if finalSet.issubset(fluentSet): 
				finalState = state
				print "Final state is subset of state: ", state
				break 
	if initState != None and finalState != None and verbose:
		for state, fluentSet in states.iteritems():
			if state == initState: 
				print "State:", state, '-->', [i for i in fluentSet]
				print 
				continue 
			print "\t\t\t\t\t\t      __   "            
			print "\t\t\t\t\t\t    _|  |_"
			print "\t\t\t\t\t\t    \\    /"
			print "\t\t\t\t\t\t     \\  /"
			print "\t\t\t\t\t\t      \\/"
			print 
			print "State:", state, '-->', [i for i in fluentSet]
			print 
			if state == finalState: break
	if initState == None: 
		print "Activity not recognized! Initial state conditions not met."
		return NOTRECOGNIZED
	else:
		print "Activity started at state {} (Initial State).".\
			format(initState)
	if finalState == None:  
		print "But not finished yet! (ongoing, final state conditions not met)."
		return UNCOMPLETE
	else: 
		print "and terminated at state {}.".format(finalState)
		return RECOGNIZED

def actRec(session, initState=[], finalState=[], actionList=[], 
			verbose=True, method='both', orderedActivity=True): 
	if method not in ('both', 'by_fluent', 'by_action'):
		print "Error!, specify a valid method: ('both', 'by_fluent', 'by_action')"
		return 
	session = session
	cnt_recognized = 0
 	cnt_uncomplete = 0
 	cnt_notrecognized = 0 
 	cnt_recognized_by_action_list = 0
 	cnt_notrecognized_by_action_list = 0
 	cnt_uncomplete_by_action_list = 0 
 	# if actionList: 
 	# 	for i, j in actionList.iteritems(): 
 	# 		print i, j
 	
 	for i, answerSet in get_answers(session):
 		print "Recognizing activity for answer:", i
 		if method != 'by_action':
	 		status = activity_recog_by_fluents(answerSet, initState, finalState, verbose=verbose)
	 		if status == RECOGNIZED: 
	 			cnt_recognized += 1
	 		elif status == NOTRECOGNIZED: 
	 			cnt_notrecognized += 1
	 		else: 
	 			cnt_uncomplete += 1 
	 	if method != 'by_fluent':
	 		status = activity_recog_by_actions(answerSet, actionList, verbose=verbose, ordered=orderedActivity)
	 		if status == RECOGNIZED: 
	 			cnt_recognized_by_action_list += 1
	 		elif status == NOTRECOGNIZED: 
	 			cnt_notrecognized_by_action_list += 1
	 		else:
	 			cnt_uncomplete_by_action_list += 1
	 			
 		print '*' * 60 
 	if cnt_recognized == 0:
 		prob_f = 0
 	else:
 		prob_f = (cnt_recognized / (cnt_recognized+cnt_notrecognized+cnt_uncomplete))
 	
 	if cnt_recognized_by_action_list == 0:
 		prob_a = 0
	else:
		prob_a = (cnt_recognized_by_action_list/(cnt_recognized_by_action_list+cnt_notrecognized_by_action_list + cnt_uncomplete_by_action_list))

 	print "Summary: "
 	if method != 'by_action': 
	 	print "By fluents: "
	 	print "\tTotal recognized activities: ", cnt_recognized
	 	print "\tTotal uncomplete activities: ", cnt_uncomplete
	 	print "\tTotal not recognized trajectories: ", cnt_notrecognized
	 	print "\tActivity performed with the probability of:  ", prob_f
 	if method != 'by_fluent':
	 	print "By action set: "
	 	print "\tTotal recognized activities: ", cnt_recognized_by_action_list
	 	print "\tTotal uncomplete activities: ", cnt_uncomplete_by_action_list
	 	print "\tTotal unrecognized activities: ", cnt_notrecognized_by_action_list
	 	print "\tActivity performed with the probability of:  ", prob_a 

if __name__ == "__main__": 

	
 	# actionWorld = { 0: set(['hold_cup_action']), 
 	# 				2 : set(['cup_to_mouth']), 
 	# 				1 : set(['cup_near_mouth']), 
 	# 				3 : set(['cup_from_mouth']) 
 	# 				}

 	actionList = ['hold_cup_action', 'cup_to_mouth', 'cup_near_mouth', 'cup_from_mouth']

 	from controller import connect 

	def DBSession(): 
		session = connect('drinking.db')
		return session()

	# session = DBSession() 
	# add_action(session, 'Carrying')
	# add_action(session, 'FlippingPaper')
	# observation_log = 'recognitionResults.txt'
	# add_action_observation_from_file(session, observation_log)


	session = DBSession() 
	actRec(session, actionList=actionList, method='by_action', verbose=True)

	# activity_recog_by_actions('answerSet', actionList, verbose=True)
 	
	# action = 'cup_near_mouth'

	# aset = set([action])
	# print aset.issubset(actionList)


	
