#this program autogenerates truthtables formatted for latex

#this functions checks if a string is a variable
def is_variable(statement:str) -> bool:
    for element in statement.split():
        if '\\' in element:
            return False
    return True

#this function takes in a number of propositions and compound propositions and returns a solved truth table
def get_solved_truth_table(header: list) -> list:
    '''
    >>> get_solved_truth_table(['p','q','p \Rightarrow q'])
    [['p', 'q', 'p \Rightarrow q'], [0, 0, 1], [0, 1, 1], [1, 0, 0], [1, 1, 1]]
    '''
    #creates a list of lists (a matrix) with the first line (list) being the arguments the function received
    truth_table = [header]

    #creates a list of all the variables in the given arguments
    variables = []
    for element in header:
        if is_variable(element): variables.append(element)


    #generates rows and collumns in truth table
    for i in range(1,2**len(variables)+1):
        truth_table.append([])
        for element in header:
            truth_table[i].append('?')
    
    #generates truth values for all the variables
    collumn = len(truth_table[0])-1
    varnum = 1
    while collumn >= 0:
        if truth_table[0][collumn] in variables:
            for row in range(1,len(truth_table)):
                truth_table[row][collumn] = int(((row-1)//varnum)%(2)>0)
            varnum *= 2
        collumn -= 1


    #finds truth values for compound propositions
    for row in range(0,len(truth_table)):
        for collumn  in range(0,len(truth_table[row])):
            if truth_table[row][collumn] == '?':
                truth_table[row][collumn] = int(solve_compound_proposition(truth_table[0],truth_table[row],truth_table[0][collumn]))
    return truth_table


#this function formats a compound proposition with spaces around all special elements
def format_proposition(p:str) -> str:
    #make space around all special elements in proposition
    special_elements = ['(',')']
    p_formatted = ""
    for index in range (0,len(p)):
        if p[index] in special_elements:
            p_formatted += " " + p[index] + " "
            continue
        p_formatted += p[index]
    return p_formatted

#this function solves a compound proposition
def solve_compound_proposition(header:list, variables:list, p:str) -> bool:
    return _solve_compound_proposition(header, variables, format_proposition(p),0, len(p)-1)

def _solve_compound_proposition(header:list, variables:list, p:str, start:int, end:int) -> bool:
    #base case
    if p[start:end] in header:
        p_value = variables[header.index(p)]
        if p_value == 0 or p_value == 1: return p_value

    #recursive case
    operators = ['\iff','\Rightarrow','\oplus','\lor','\land','\lnot','('] #this list is sorted with the lowest precedence at 0 and highest precedence in the end
    elements = p.split()
    #need parantheses counter in case of nested parantheses - ex. ((p)andq) - implement parantheses later
    for operator in operators:
        for index in range(0,len(elements)):
            if elements[index] == operator:
                p = _solve_compound_proposition(header, variables,' '.join(elements[:index]))
                q = _solve_compound_proposition(header, variables,' '.join(elements[index+1:]))
                #print('p : ',p)
                #print('q : ',q)
                if operator == '\iff':
                    return (not(p) or q) and (not(q) or p)
                if operator == '\Rightarrow':
                    #print('operator is implies')
                    return not(p) or q
                if operator == '\oplus':
                    return p != q
                if operator == '\lor':
                    return p or q
                if operator == '\land':
                    return p and q
                if operator == '\lnot':
                    return not(q)
    return True


def latex_truth_table(header:list) -> str:
    table = get_solved_truth_table(header)

    latex = "\\begin{center}\n \\begin{tabular}{|"
    for element in table[0]:
        latex += "c|"
    latex +=  "}\n \\hline \n"
    
    #adds header row with vertical line
    for element in table[0]:
        latex += '$' + str(element) + '$ & '
    latex = latex[:-3] + '\\\\\n\\hline\\n'

    #add remaining rows without vertical lines
    for row in table[1:]:
        for element in row:
            latex += '$' + str(element) + '$ & '
        latex = latex[:-3] + '\\\\\n'
    latex += '\\hline\n\\end{tabular}\n\\end{center}'

    #print
    print(latex)

    return latex

#this function prints a list of lists as a matrix
def print_as_matrix(matrix):
    for row in matrix:
        print(row)


def test_loop():
    while 1:
        print(solve_compound_proposition(input('header : '),input('variables : '),input('proposition : ')))

def print_truthtable(*args):
    print_as_matrix(get_solved_truth_table(args))

#proposition = 'p \lor q \Rightarrow p \land q'
#header = ['p','q','p \land q','p \lor q' ,proposition]
#variables = [0,1,'?','?','?']

#print('header : ',header,'\nvariables : ',variables,'\n proposition : ',proposition,'\n',solve_compound_proposition(header,variables,proposition))

#print_as_matrix(get_solved_truth_table('p','q','\lnot p','p \land q','p \lor q','p \land q \Rightarrow p \lor q'))


#test_loop()
