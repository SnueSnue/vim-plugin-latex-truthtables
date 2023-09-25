#this program autogenerates truthtables formatted for latex

#import vim module
try:
  import vim
except:
  print("No vim module available outside vim")
  pass

#this function is the only one called by vim
def write_truth_table():
    row, col = vim.current.window.cursor
    current_line = vim.current.buffer[row-1]
    
    #format current line as list of propositions
    header = current_line.split(',')

    #get truthtable from header
    truth_table = get_latex_truth_table(header)

    #writes truth table under current line in vim
    vim.current.buffer[row-1]=truth_table[0]
    for index, truth_row in enumerate(truth_table[1:]):
        vim.current.buffer.append(truth_row,row+index)

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
    p_list = format_proposition(p).split()
    return _solve_compound_proposition(header, variables, p_list,0, len(p_list))

def _solve_compound_proposition(header:list, variables:list, total_proposition:list, start:int, end:int) -> bool:
    #base case
    if (start+1 == end) and total_proposition[start] in header:
        p_value = variables[header.index(total_proposition[start])]
        if p_value == 0 or p_value == 1: return p_value

    #recursive case
    #removes outside parantheses if any
    if total_proposition[start] == '(' and total_proposition[end-1] == ')':
        return _solve_compound_proposition(header, variables, total_proposition, start+1, end-1)

    operators = ['\iff','\Rightarrow','\oplus','\lor','\land','\lnot'] #this list is sorted with the lowest precedence at 0 and highest precedence in the end
    #need parantheses counter in case of nested parantheses - ex. ((p)andq) - implement parantheses later
    for operator in operators:
        paranthese_counter = 0
        for index in range(start, end):
            #check if outside paranthese
            if total_proposition[index] == '(':
                paranthese_counter += 1
                continue
            if total_proposition[index] == ')':
                paranthese_counter -= 1
                continue

            if paranthese_counter == 0 and total_proposition[index] == operator:
                p = _solve_compound_proposition(header, variables,total_proposition, start, index)
                q = _solve_compound_proposition(header, variables,total_proposition, index + 1, end)
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


def get_latex_truth_table(header:list) -> list:
    table = get_solved_truth_table(header)
    
    #creates beginning of latex table
    latex = ['\\begin{center}', '\\begin{tabular}{|']

    #creates required number of collumns and double vertical lines between variables and compound propositions
    for index in range(0,len(table[0])):
        if (index+1 < len(table[0]) and is_variable(table[0][index]) and not(is_variable(table[0][index+1]))):
            latex[1] += "c||"
            continue
        latex[1] += "c|"
    latex[1] += '}'
    latex += ['\\hline']
    
    

    #adds header row with horizontal line
    latex.append('')
    for element in table[0]:
        latex[3] += '$' + str(element) + '$ & '
    latex[3] = latex[3][:-3] + '\\\\'
    latex += ['\\hline']

    #add remaining rows without horizontal lines
    for index, row in enumerate(table[1:]):
        latex.append('')
        for element in row:
            latex[index+5] += '$' + str(element) + '$ & '
        latex[index+5] = latex[index+5][:-3] + '\\\\'
    latex += ['\\hline','\\end{tabular}','\\end{center}']

    return latex

def print_latex(header:list) -> None:
    print(get_latex_truth_table(header))


#this function prints a list of lists as a matrix
def print_matrix(header: list):
    for row in get_solved_truth_table(header):
        print(row)

def print_as_matrix(table:list):
    for row in table:
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


#print_as_matrix(get_latex_truth_table(['p','q','p \land q']))

#test_loop()
