import re

def cleaning_text(text):
    
    # cleaning symbols after ;
    find_end = lambda x: len(x) if x.find(";") == -1 else x.find(";")
    text = text[:find_end(text)] 
    
    # cleaning from space
    text = text.split()
    text = ' '.join([elem for elem in text])

    return text

def define_command(command):
    key_words = ["CREATE", "INSERT", "SEARCH", "REMOVE", "EXIT", "PRINT_INDEX", "SHOW"]
    command = command.upper().split()
    # empy command or only command without parameters
    if not len(command) or (len(command) < 2 and (command[0] != "EXIT" and \
        command[0] != "SHOW")):
        return " ", -7
    if command[0] in key_words:
        return command[0], 100
    else:
        return " ", -7


def parse_create(command):

    command = command.split()
    name = command[1]

    # incorrect name
    if re.search("[a-zA-Z]", name[0]) == None: # first letter
        return name, -1
    if re.search("[a-zA-Z0-9_]*", name) == None: # other symbols
        return name, -2

    # too many parameters 
    if len(command) > 2:
        return name, -4
    
    return name, 100

def parse_insert(command):
    command = command.split()
    name = command[1]

    text = ""
    
    if len(command) < 3: # without text
        return name, text, -12

    index = 0
    i = 0
    while (i < len(command)):
        if command[i][-1] == "\"":
            index = i
        i += 1
    i -= 1

    

    # incorrect ""        
    if command[2][0] != "\"" or command[-1][-1] != "\"": # missing double quote
        return name, text, -6

    # too many parameters 
    if i != index:
        return name, text, -4

    # getting text
    text = ' '.join([elem for elem in command[2:index+1]])
    text = text.strip("\"").strip()
    print(f"'{text}'")
    return name, text, 100

def parse_remove(command):
    command = command.split()
    case = 0
    name = command[1]
    index = 0

    if len(command) == 2:
        case = 1
    elif len(command) == 3:
        case = 2
        index = command[2]
    else:
        return case, name, index, -4
    return case, name, index, 100

def parse_print_index(command):
    command = command.split()
    name = command[1]

    if len(command) > 2:
        return name, -4

    return name, 100

def parse_show(command):
    command = command.split()

    if len(command) > 1:
        return -4

    return 100

def parse_exit(command):
    command = command.split()

    if len(command) > 1:
        return -4

    return 100

def parse_search(command):
    command = command.split()
    name = command[1]
    condition = ""
    # finding WHERE
    if len(command) >= 3:
        # incorrect WHERE
        if command[2].upper() != "WHERE":
            return name, condition, -8
        # missing condition
        if len(command) == 3:
            return name, condition, -9
        # getting condition
        condition = command[3:]
        condition = ' '.join([elem for elem in condition])
    return name, condition, 100

def parse_condition(condition):

    if not len(condition): # without WHERE
        case = 0
    # keyword
    elif condition[0] == "\"" and condition[-1] == "\"" \
        and condition.count("\"") == 2:
        condition = condition[1:-1]
        case = 1
    # keyword + '*'
    elif condition[0] == "\"" and condition[-2] == "\"" and condition[-1] == "*":
        condition = condition[1:-2]
        case = 2
    # keyword1 <N> keyword2
    elif condition[0] == "\"" and condition[-1] == "\"" \
        and condition.count("\"") == 4 and condition.index("<") < condition.index(">"):
        keyword1 = condition[1:condition.index("\"", 1,-1)]
        keyword2 = condition[condition.index("\"", condition[1:].find("\"")+2, -1)+1:-1]
        N = condition[condition.index("<")+1:condition.index(">")]
        condition = [keyword1, keyword2, int(N)]
        case = 3
    else:
        return -1, condition, -10

    return case, condition, 100

    