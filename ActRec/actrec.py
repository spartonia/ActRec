from __future__ import division 
from asp_parser import * 
import collections 

RECOGNIZED = 1
UNCOMPLETE = 0 
NOTRECOGNIZED = -1

def make_fluent_world(answerSet): 
    """creates a world from the answer set, representing all states and their fluents holding in the states."""
    states = {}
     
    for state, fluent in get_answerset_fluents(answerSet): 
        # fset.add(fluent)
        try:
            states[state]
        except KeyError, e:
            states[state] = set() 
        states[state].add(fluent)
    for state, setOfFluents in states.iteritems():
        yield state, setOfFluents

def make_action_world(answerSet): 
    """Creates a world from the answer set, representing all states and actions which hold in those states."""
    states = {} 
    for state, action in get_answerset_actions(answerSet):
        try:
            states[state]
        except KeyError, e:
            states[state] = set() 
        states[state].add(action)
    for state, setOfActions in states.iteritems(): 
    	print state, setOfActions
        yield state, setOfActions

def activity_recog_by_actions(answerSet, actionList, printTrajectory=False, printAllActions=False):
	"""Recognize activty by checking whether a sequence of actions performed."""

	states = {}
	for state, actionSet in make_action_world(answerSet):
		states[state] = actionSet
	states = collections.OrderedDict(sorted(states.items()))
	actionList = collections.OrderedDict(sorted(actionList.items()))
	if (not actionList) or (not states): return NOTRECOGNIZED # NO action list privided 
	if printAllActions:
		print "All actions (World): "
		for state, actionSet in states.iteritems(): 
			print 'State ', state, ' : ', actionSet
		print '*' * 60
		print 
	startState = None
	prevState = None 
	for action_no, action in actionList.iteritems(): 
		# print action_no, action 
		for state, actionSet in states.iteritems(): 
			# print startState, 'startState'
			if startState == None: 
				if action.issubset(actionSet):
					startState = state
					prevState = state
					if printTrajectory: 
						print "action" , action_no, action
						print "is subset of (init state):", state, actionSet
					# print 'Start State:', startState
					break
				else:
					continue
			if startState != None and state <= prevState: 
				continue
			
			if action.issubset(actionSet):
				prevState = state
				if printTrajectory: 
					print "action ", action_no, action
					print "is subset of ", state, actionSet
				break 
			else:
				if printTrajectory: 
					print "action ", action_no, action
					print "is not a subset of ", state, actionSet
					print "NOTRECOGNIZED"
				return NOTRECOGNIZED # activity not found 

			# print action_no, state
	# print len(actionList), prevState, startState
	if printTrajectory: 
		print "RECOGNIZED"
		print "Activity started at state '{0}' and finished at state '{1}'.".\
		format(startState, startState) # +len(actionList)-1
	return RECOGNIZED


def activity_recog_by_fluents(answerSet, initSet, finalSet, printTrajectory=False, printAllStates=False): 
	""" Recognize activty by checking whether Initial and final state conditions are met."""
	# what if initSet and final sets are empty? 
	states = {} 
	for state, fluentSet in make_fluent_world(answerSet): 
		states[state] = fluentSet
	# sort states 
	states = collections.OrderedDict(sorted(states.items()))
 	if printAllStates:
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
	if initState != None and finalState != None and printTrajectory:
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

def actRec(initState=[], finalState=[], actionList=[]): 
	# if not initState and not finalState:
	cnt_recognized = 0
 	cnt_uncomplete = 0
 	cnt_notrecognized = 0 
 	cnt_recognized_by_action_list = 0
 	cnt_notrecognized_by_action_list = 0
 	if actionList: 
 		for i, j in actionList.iteritems(): 
 			print i, j

 	for i, answerSet in get_answers():
 		print "Recognizing activity for answer:", i
 		status = activity_recog_by_fluents(answerSet, initSet, finalSet, printTrajectory=True, printAllStates=True)
 		if status == RECOGNIZED: 
 			cnt_recognized += 1
 		elif status == NOTRECOGNIZED: 
 			cnt_notrecognized += 1
 		else: 
 			cnt_uncomplete += 1 
 		status = activity_recog_by_actions(answerSet, actionList, printTrajectory=True, printAllActions=True)
 		if status == RECOGNIZED: 
 			cnt_recognized_by_action_list += 1 
 		else:
 			cnt_notrecognized_by_action_list += 1
 		print '*' * 60 
 	print "Summary: "
 	print "By fluents: "
 	print "\tTotal recognized activities: ", cnt_recognized
 	print "\tTotal uncomplete activities: ", cnt_uncomplete
 	print "\tTotal not recognized trajectories: ", cnt_notrecognized
 	print "\tActivity performed with the probability of:  ", (cnt_recognized / (cnt_recognized+cnt_notrecognized+cnt_uncomplete))
 	print "By action set: "
 	print "\tTotal recognized activities: ", cnt_recognized_by_action_list
 	print "\tTotal uncomplete activities: ", cnt_notrecognized_by_action_list
 	print "\tActivity performed with the probability of:  ", (cnt_recognized_by_action_list/(cnt_recognized_by_action_list+cnt_notrecognized_by_action_list))

if __name__ == "__main__": 

	string = """fluent(coffe_m_is_on) fluent(coffe_m_has_powder) fluent(coffe_m_has_old_coffe_powder) fluent(coffe_m_has_water) fluent(coffe_m_is_jug_removed) action(coffe_m_activate) action(coffe_m_add_coffe_powder) action(coffe_m_remove_coffe_powder) action(coffe_m_add_water) action(coffe_m_add_jug) action(coffe_m_remove_jug) holds(occurs(coffe_m_add_coffe_powder),2) time(0) time(1) time(2) time(3) time(4) time(5) holds(coffe_m_has_old_coffe_powder,0) holds(coffe_m_has_old_coffe_powder,1) holds(coffe_m_has_old_coffe_powder,2) holds(coffe_m_has_old_coffe_powder,3) holds(coffe_m_has_old_coffe_powder,4) holds(coffe_m_has_old_coffe_powder,5) holds(coffe_m_is_on,0) holds(coffe_m_is_on,1) holds(coffe_m_is_on,2) holds(coffe_m_is_on,3) holds(coffe_m_is_on,4) holds(coffe_m_is_on,5) holds(allow(occurs(coffe_m_remove_coffe_powder)),0) holds(allow(occurs(coffe_m_remove_coffe_powder)),1) holds(allow(occurs(coffe_m_remove_coffe_powder)),2) holds(allow(occurs(coffe_m_remove_coffe_powder)),3) holds(allow(occurs(coffe_m_remove_coffe_powder)),4) holds(allow(occurs(coffe_m_remove_coffe_powder)),5) holds(ab(occurs(coffe_m_remove_coffe_powder)),0) holds(ab(occurs(coffe_m_remove_coffe_powder)),1) holds(ab(occurs(coffe_m_remove_coffe_powder)),2) holds(ab(occurs(coffe_m_remove_coffe_powder)),3) holds(ab(occurs(coffe_m_remove_coffe_powder)),4) holds(ab(occurs(coffe_m_remove_coffe_powder)),5) holds(neg(occurs(coffe_m_remove_coffe_powder)),0) holds(neg(occurs(coffe_m_remove_coffe_powder)),1) holds(neg(occurs(coffe_m_remove_coffe_powder)),2) holds(neg(occurs(coffe_m_remove_coffe_powder)),3) holds(neg(occurs(coffe_m_remove_coffe_powder)),4) holds(neg(coffe_m_has_powder),0) holds(neg(coffe_m_has_powder),1) holds(neg(coffe_m_has_powder),2) holds(neg(coffe_m_has_powder),3) holds(neg(coffe_m_has_powder),4) holds(neg(coffe_m_has_powder),5) holds(coffe_m_has_water,0) holds(coffe_m_has_water,1) holds(coffe_m_has_water,2) holds(coffe_m_has_water,3) holds(coffe_m_has_water,4) holds(coffe_m_has_water,5) holds(coffe_m_is_jug_removed,0) holds(allow(occurs(coffe_m_activate)),0) holds(allow(occurs(coffe_m_activate)),1) holds(allow(occurs(coffe_m_activate)),2) holds(allow(occurs(coffe_m_activate)),3) holds(allow(occurs(coffe_m_activate)),4) holds(allow(occurs(coffe_m_activate)),5) holds(allow(occurs(coffe_m_add_wate)),0) holds(allow(occurs(coffe_m_add_water)),1) holds(allow(occurs(coffe_m_add_water)),2) holds(allow(occurs(coffe_m_add_water)),3) holds(allow(occurs(coffe_m_add_water)),4) holds(allow(occurs(coffe_m_add_water)),5) holds(allow(occurs(coffe_m_remove_jug)),0) holds(allow(occurs(coffe_m_remove_jug)),1) holds(allow(occurs(coffe_m_remove_jug)),2) holds(allow(occurs(coffe_m_remove_jug)),3) holds(allow(occurs(coffe_m_remove_jug)),4) holds(allow(occurs(coffe_m_remove_jug)),5) holds(allow(occurs(coffe_m_add_jug)),0) holds(allow(occurs(coffe_m_add_jug)),1) holds(allow(occurs(coffe_m_add_jug)),2) holds(allow(occurs(coffe_m_add_jug)),3) holds(allow(occurs(coffe_m_add_jug)),4) holds(allow(occurs(coffe_m_add_jug)),5) holds(allow(occurs(coffe_m_add_coffe_powder)),0) holds(allow(occurs(coffe_m_add_coffe_powder)),1) holds(allow(occurs(coffe_m_add_coffe_powder)),2) holds(allow(occurs(coffe_m_add_coffe_powder)),3) holds(allow(occurs(coffe_m_add_coffe_powder)),4) holds(allow(occurs(coffe_m_add_coffe_powder)),5) holds(occurs(coffe_m_add_jug),0) holds(occurs(coffe_m_add_jug),1) holds(occurs(coffe_m_add_jug),2) holds(occurs(coffe_m_add_jug),3) holds(occurs(coffe_m_add_jug),4) holds(occurs(coffe_m_activate),0) holds(occurs(coffe_m_activate),1) holds(occurs(coffe_m_activate),2) holds(occurs(coffe_m_activate),3) holds(occurs(coffe_m_activate),4) holds(occurs(coffe_m_activate),5) holds(occurs(coffe_m_add_coffe_powder),0) holds(occurs(coffe_m_add_coffe_powder),1) holds(occurs(coffe_m_add_coffe_powder),3) holds(occurs(coffe_m_add_coffe_powder),4) holds(occurs(coffe_m_add_waterrrrrrr),0) holds(occurs(coffe_m_add_water),1) holds(occurs(coffe_m_add_water),2) holds(occurs(coffe_m_add_water),3) holds(occurs(coffe_m_add_water),4) holds(occurs(coffe_m_remove_jug),0) holds(occurs(coffe_m_remove_jug),1) holds(occurs(coffe_m_remove_jug),2) holds(occurs(coffe_m_remove_jug),3) holds(occurs(coffe_m_remove_jug),4)
 	"""
 	string2 = """fluent(coffe_m_is_on) fluent(coffe_m_has_powder) fluent(coffe_m_has_old_coffe_powder) fluent(coffe_m_has_water) fluent(coffe_m_is_jug_removed) action(coffe_m_activate) action(coffe_m_add_coffe_powder) action(coffe_m_remove_coffe_powder) action(coffe_m_add_water) action(coffe_m_add_jug) action(coffe_m_remove_jug) holds(occurs(coffe_m_add_coffe_powder),2) time(0) time(1) time(2) time(3) time(4) time(5) holds(coffe_m_has_old_coffe_powder,0) holds(coffe_m_has_old_coffe_powder,1) holds(coffe_m_has_old_coffe_powder,2) holds(coffe_m_has_old_coffe_powder,3) holds(coffe_m_has_old_coffe_powder,4) holds(coffe_m_has_old_coffe_powder,5) holds(coffe_m_is_on,0) holds(coffe_m_is_on,1) holds(coffe_m_is_on,2) holds(coffe_m_is_on,3) holds(coffe_m_is_on,4) holds(coffe_m_is_on,5) holds(allow(occurs(coffe_m_remove_coffe_powder)),0) holds(allow(occurs(coffe_m_remove_coffe_powder)),1) holds(allow(occurs(coffe_m_remove_coffe_powder)),2) holds(allow(occurs(coffe_m_remove_coffe_powder)),3) holds(allow(occurs(coffe_m_remove_coffe_powder)),4) holds(allow(occurs(coffe_m_remove_coffe_powder)),5) holds(ab(occurs(coffe_m_remove_coffe_powder)),0) holds(ab(occurs(coffe_m_remove_coffe_powder)),1) holds(ab(occurs(coffe_m_remove_coffe_powder)),2) holds(ab(occurs(coffe_m_remove_coffe_powder)),3) holds(ab(occurs(coffe_m_remove_coffe_powder)),4) holds(ab(occurs(coffe_m_remove_coffe_powder)),5) holds(neg(occurs(coffe_m_remove_coffe_powder)),0) holds(neg(occurs(coffe_m_remove_coffe_powder)),1) holds(neg(occurs(coffe_m_remove_coffe_powder)),2) holds(neg(occurs(coffe_m_remove_coffe_powder)),3) holds(neg(occurs(coffe_m_remove_coffe_powder)),4) holds(neg(coffe_m_has_powder),0) holds(neg(coffe_m_has_powder),1) holds(neg(coffe_m_has_powder),2) holds(neg(coffe_m_has_powder),3) holds(neg(coffe_m_has_powder),4) holds(neg(coffe_m_has_powder),5) holds(coffe_m_has_water,0) holds(coffe_m_has_water,1) holds(coffe_m_has_water,2) holds(coffe_m_has_water,3) holds(coffe_m_has_water,4) holds(coffe_m_has_water,5) holds(coffe_m_is_jug_removed,0) holds(allow(occurs(coffe_m_activate)),0) holds(allow(occurs(coffe_m_activate)),1) holds(allow(occurs(coffe_m_activate)),2) holds(allow(occurs(coffe_m_activate)),3) holds(allow(occurs(coffe_m_activate)),4) holds(allow(occurs(coffe_m_activate)),5) holds(allow(occurs(coffe_m_add_water)),0) holds(allow(occurs(coffe_m_add_water)),1) holds(allow(occurs(coffe_m_add_water)),2) holds(allow(occurs(coffe_m_add_water)),3) holds(allow(occurs(coffe_m_add_water)),4) holds(allow(occurs(coffe_m_add_water)),5) holds(allow(occurs(coffe_m_remove_jug)),0) holds(allow(occurs(coffe_m_remove_jug)),1) holds(allow(occurs(coffe_m_remove_jug)),2) holds(allow(occurs(coffe_m_remove_jug)),3) holds(allow(occurs(coffe_m_remove_jug)),4) holds(allow(occurs(coffe_m_remove_jug)),5) holds(allow(occurs(coffe_m_add_jug)),0) holds(allow(occurs(coffe_m_add_jug)),1) holds(allow(occurs(coffe_m_add_jug)),2) holds(allow(occurs(coffe_m_add_jug)),3) holds(allow(occurs(coffe_m_add_jug)),4) holds(allow(occurs(coffe_m_add_jug)),5) holds(allow(occurs(coffe_m_add_coffe_powder)),0) holds(allow(occurs(coffe_m_add_coffe_powder)),1) holds(allow(occurs(coffe_m_add_coffe_powder)),2) holds(allow(occurs(coffe_m_add_coffe_powder)),3) holds(allow(occurs(coffe_m_add_coffe_powder)),4) holds(allow(occurs(coffe_m_add_coffe_powder)),5) holds(occurs(coffe_m_add_jug),0) holds(occurs(coffe_m_add_jug),1) holds(neg(occurs(coffe_m_add_jug)),2) holds(occurs(coffe_m_add_jug),3) holds(occurs(coffe_m_add_jug),4) holds(occurs(coffe_m_activate),0) holds(occurs(coffe_m_activate),1) holds(occurs(coffe_m_activate),2) holds(occurs(coffe_m_activate),3) holds(occurs(coffe_m_activate),4) holds(occurs(coffe_m_activate),5) holds(occurs(coffe_m_add_coffe_powder),0) holds(occurs(coffe_m_add_coffe_powder),1) holds(occurs(coffe_m_add_coffe_powder),3) holds(occurs(coffe_m_add_coffe_powder),4) holds(occurs(coffe_m_add_water),0) holds(occurs(coffe_m_add_water),1) holds(occurs(coffe_m_add_water),2) holds(occurs(coffe_m_add_water),3) holds(occurs(coffe_m_add_water),4) holds(occurs(coffe_m_remove_jug),0) holds(occurs(coffe_m_remove_jug),1) holds(occurs(coffe_m_remove_jug),2) holds(occurs(coffe_m_remove_jug),3) holds(occurs(coffe_m_remove_jug),4)
 	"""


 	# actionList = { 0: set(['coffe_m_add_water']), 
 	# 				2 : set(['coffe_m_remove_jug']), 
 	# 				1 : set(['coffe_m_add_jug']), 
 	# 				3 : set(['coffe_m_activate'])}#, 
 					# 4 : set(['coffe_m_add_coffe_powder']), 
 					# 5 : set(['coffe_m_activate'])}
 	
 	

 	############################################################
 	# initSet = set(['neg(coffe_m_has_powder)', 'coffe_m_is_jug_removed'])
 	# finalSet = set(['coffe_m_is_on', 'neg(coffe_m_has_powder)'])
 	initSet = set(['heat_on', 'vessel_on_heat', 'vessel_water_full'])
 	finalSet = set(['pasta_ready'])

 	actionList = { 0: set(['vessel_water_boil']), 
 					2 : set(['pasta_boil']), 
 					1 : set(['pasta_cooked_drain']), 
 					3 : set(['pasta_sauce_add'])}
 					
 	actRec(initSet, finalSet, actionList)
 	############################################################
