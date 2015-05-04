import os, re
import subprocess, tempfile
from itertools import islice 
from mapper import make_asp_script


SATISFIABLE = 1
UNSATISFIABLE = -1
UNKNOWN = 0 
aspParser = 'clingo.exe' 
GROUNDER = 'gringo.exe'
SOLVER = 'clasp.exe' 
MAX_ANSWERS = 120 # max number of answers to get from solver.

# detect system and architecture
# run subprocess to compile input file
# read file to parse
# 

# def reversed_lines(file):
#     "Generate the lines of file in reverse order."
#     part = ''
#     for block in reversed_blocks(file):
#         for c in reversed(block):
#             if c == '\n' and part:
#                 yield part[::-1]
#                 part = ''
#             part += c
#     if part: yield part[::-1]

# def reversed_blocks(file, blocksize=4096):
#     "Generate blocks of file's contents in reverse order."
#     with open(file, 'r') as file: 
#         file.seek(0, os.SEEK_END)
#         here = file.tell()
#         while 0 < here:
#             delta = min(blocksize, here)
#             here -= delta
#             file.seek(here, os.SEEK_SET)
#             yield file.read(delta)

def check_solution_status(answerSet): 
    """Return the status of answer set: 
        SATISFIABLE - ASP is satisfiable (has answers).
        UNSATISFIABLE - ASP is unsatisfiable (not solvable)
        UNKNOWN - Unknown status.
    """
	# check last 20 lines to find out solution status
    status = UNKNOWN
    for line in answerSet.split('\n'):
        if 'UNSATISFIABLE' in line.upper(): 
            status = UNSATISFIABLE
            break
        elif 'SATISFIABLE' in line.upper():
            status = SATISFIABLE
            break
    return status
    # for line in islice(reversed_lines(file), 20):
    #     for l in line.strip().split('\n'):
    #         # print l, '**'
    #         if l.upper() == 'SATISFIABLE':
    #             status = SATISFIABLE
    #             break
    #         elif l.upper() == 'UNSATISFIABLE':
    #             status = UNSATISFIABLE
    #             break
    # return status
         
def get_answers(session): 
    """Return answer sets from an ASP, one at a time, along with corresponding answer id."""
    
    # Creata ASP program and feed it to ASP-solver
    ASPScript = make_asp_script(session)
    # print ASPScript
    tmp = tempfile.NamedTemporaryFile( delete=False) #mode='w+b',
    tmp.write(ASPScript)
    tmp.seek(0)
    (result, error) = subprocess.Popen([GROUNDER], stdin=tmp, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate() 
    grounded = tempfile.NamedTemporaryFile(delete=False)
    grounded.write(result)
    grounded.seek(0)
    (result, error) = subprocess.Popen([SOLVER, "%d" %MAX_ANSWERS], stdin=grounded, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    # check if ASP is satisfiable
    if check_solution_status(result) != SATISFIABLE: return
    
    lines = result.split('\n')
    for i, line in enumerate(lines):
        if 'answer' in line.lower():
            answer_no = int(re.findall('\d+', line)[0])
            yield answer_no, lines[i+1]

    # # if parsing from file: 
    # with open(file, 'r+') as file:
    #     lines = file.readlines() 
    #     for i in range(0, len(lines)):
    #         line = lines[i]
    #         if 'answer' in line.lower():
    #             answer_no = int(re.findall('\d+', line)[0])
    #             yield answer_no, lines[i+1]

def get_answerset_fluents(answerSet):
    """Extraxts all fluents that hold, from an answer set."""
    pattern1 = re.compile('^holds\({1}(.[^,\(\)]*),(\d+)\)', re.I) 
    pattern2 = re.compile('^holds\({1}(neg\(\w+\)),(\d+)\)', re.I)
    # FLUENT = re.compile("^holds\((.*?),?(\d+)\)$")
    strings = answerSet.split()
    for string in strings:
        # print string
        matches = re.findall(pattern1, string)
        if matches: 
            # print matches
            for fluent, state in matches:
                yield  int(state), fluent.strip()
        else: 
            matches = re.findall(pattern2, string)
            if matches: 
                for fluent, state in matches: 
                    yield int(state), fluent.strip()

def get_answerset_actions(answerSet):
    """ Extraxts all actions which hold from an answer set.""" 
    pattern = re.compile('^holds\({1}occurs\((.[^,\(\)]*)\),(\d+)\)', re.I) #
    #   ACTION = re.compile("^occ\((.*?),?(\d+)\)$")
    strings = answerSet.split() 
    for string in strings: 
        matches = re.findall(pattern, string)
        if matches: 
            for action, state in matches: 
                yield  int(state), action.strip()


if __name__ == "__main__":

    # for i, j in get_answerset_fluents(string):
    #     print i, j 

    # for i, j in get_answerset_actions(string): 
    #     print i, j 
    # for i, j in action_world(string): 
    #     print i, j 

   
    
    # ASPScript = make_asp_script()
    # tmp = tempfile.NamedTemporaryFile( delete=False) #mode='w+b',
    # tmp.write(ASPScript)
    # tmp.seek(0)
    # # tmp.colse() 
    # # with open('fake.asp', 'w+') as out: 
    # (result, error) = subprocess.Popen([aspParser, '1'], stdin=tmp, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    # # tmp.colse()
    # for line in result.split('\n'):
    #     print line
    # print check_solution_status(result)
    for no, answer in get_answers():
        print no 
        print answer

    # string = """fluent(coffe_m_is_on) fluent(coffe_m_has_powder) fluent(coffe_m_has_old_coffe_powder) fluent(coffe_m_has_water) fluent(coffe_m_is_jug_removed) action(coffe_m_activate) action(coffe_m_add_coffe_powder) action(coffe_m_remove_coffe_powder) action(coffe_m_add_water) action(coffe_m_add_jug) action(coffe_m_remove_jug) holds(occurs(coffe_m_add_coffe_powder),2) time(0) time(1) time(2) time(3) time(4) time(5) holds(coffe_m_has_old_coffe_powder,0) holds(coffe_m_has_old_coffe_powder,1) holds(coffe_m_has_old_coffe_powder,2) holds(coffe_m_has_old_coffe_powder,3) holds(coffe_m_has_old_coffe_powder,4) holds(coffe_m_has_old_coffe_powder,5) holds(coffe_m_is_on,0) holds(coffe_m_is_on,1) holds(coffe_m_is_on,2) holds(coffe_m_is_on,3) holds(coffe_m_is_on,4) holds(coffe_m_is_on,5) holds(allow(occurs(coffe_m_remove_coffe_powder)),0) holds(allow(occurs(coffe_m_remove_coffe_powder)),1) holds(allow(occurs(coffe_m_remove_coffe_powder)),2) holds(allow(occurs(coffe_m_remove_coffe_powder)),3) holds(allow(occurs(coffe_m_remove_coffe_powder)),4) holds(allow(occurs(coffe_m_remove_coffe_powder)),5) holds(ab(occurs(coffe_m_remove_coffe_powder)),0) holds(ab(occurs(coffe_m_remove_coffe_powder)),1) holds(ab(occurs(coffe_m_remove_coffe_powder)),2) holds(ab(occurs(coffe_m_remove_coffe_powder)),3) holds(ab(occurs(coffe_m_remove_coffe_powder)),4) holds(ab(occurs(coffe_m_remove_coffe_powder)),5) holds(neg(occurs(coffe_m_remove_coffe_powder)),0) holds(neg(occurs(coffe_m_remove_coffe_powder)),1) holds(neg(occurs(coffe_m_remove_coffe_powder)),2) holds(neg(occurs(coffe_m_remove_coffe_powder)),3) holds(neg(occurs(coffe_m_remove_coffe_powder)),4) holds(neg(coffe_m_has_powder),0) holds(neg(coffe_m_has_powder),1) holds(neg(coffe_m_has_powder),2) holds(neg(coffe_m_has_powder),3) holds(neg(coffe_m_has_powder),4) holds(neg(coffe_m_has_powder),5) holds(coffe_m_has_water,0) holds(coffe_m_has_water,1) holds(coffe_m_has_water,2) holds(coffe_m_has_water,3) holds(coffe_m_has_water,4) holds(coffe_m_has_water,5) holds(coffe_m_is_jug_removed,0) holds(allow(occurs(coffe_m_activate)),0) holds(allow(occurs(coffe_m_activate)),1) holds(allow(occurs(coffe_m_activate)),2) holds(allow(occurs(coffe_m_activate)),3) holds(allow(occurs(coffe_m_activate)),4) holds(allow(occurs(coffe_m_activate)),5) holds(allow(occurs(coffe_m_add_wate)),0) holds(allow(occurs(coffe_m_add_water)),1) holds(allow(occurs(coffe_m_add_water)),2) holds(allow(occurs(coffe_m_add_water)),3) holds(allow(occurs(coffe_m_add_water)),4) holds(allow(occurs(coffe_m_add_water)),5) holds(allow(occurs(coffe_m_remove_jug)),0) holds(allow(occurs(coffe_m_remove_jug)),1) holds(allow(occurs(coffe_m_remove_jug)),2) holds(allow(occurs(coffe_m_remove_jug)),3) holds(allow(occurs(coffe_m_remove_jug)),4) holds(allow(occurs(coffe_m_remove_jug)),5) holds(allow(occurs(coffe_m_add_jug)),0) holds(allow(occurs(coffe_m_add_jug)),1) holds(allow(occurs(coffe_m_add_jug)),2) holds(allow(occurs(coffe_m_add_jug)),3) holds(allow(occurs(coffe_m_add_jug)),4) holds(allow(occurs(coffe_m_add_jug)),5) holds(allow(occurs(coffe_m_add_coffe_powder)),0) holds(allow(occurs(coffe_m_add_coffe_powder)),1) holds(allow(occurs(coffe_m_add_coffe_powder)),2) holds(allow(occurs(coffe_m_add_coffe_powder)),3) holds(allow(occurs(coffe_m_add_coffe_powder)),4) holds(allow(occurs(coffe_m_add_coffe_powder)),5) holds(occurs(coffe_m_add_jug),0) holds(occurs(coffe_m_add_jug),1) holds(occurs(coffe_m_add_jug),2) holds(occurs(coffe_m_add_jug),3) holds(occurs(coffe_m_add_jug),4) holds(occurs(coffe_m_activate),0) holds(occurs(coffe_m_activate),1) holds(occurs(coffe_m_activate),2) holds(occurs(coffe_m_activate),3) holds(occurs(coffe_m_activate),4) holds(occurs(coffe_m_activate),5) holds(occurs(coffe_m_add_coffe_powder),0) holds(occurs(coffe_m_add_coffe_powder),1) holds(occurs(coffe_m_add_coffe_powder),3) holds(occurs(coffe_m_add_coffe_powder),4) holds(occurs(coffe_m_add_water),0) holds(occurs(coffe_m_add_water),1) holds(occurs(coffe_m_add_water),2) holds(occurs(coffe_m_add_water),3) holds(occurs(coffe_m_add_water),4) holds(occurs(coffe_m_remove_jug),0) holds(occurs(coffe_m_remove_jug),1) holds(occurs(coffe_m_remove_jug),2) holds(occurs(coffe_m_remove_jug),3) holds(occurs(coffe_m_remove_jug),4)
    # """
    # for i, j in get_answerset_actions(string): 
    #     print i, j 