import myparser
import commands

collections_instances = {}
inverted_indexes = {} # {"world": {colection1:{ doc1: [номер в тексте]: }

print("Enter commands")

while(True):
    status = 0

    #print(collections_instances) # delete before release
  
    text = ""

    while(text.find(";") == -1): # multiline input
        text += " "
        text += input(">>")

    text = myparser.cleaning_text(text)
    

    command, status = myparser.define_command(text)
    commands.check_status(status)
    if status == -7:
        continue

    if command == "CREATE":

        name, status = myparser.parse_create(text)
        commands.check_status(status)
        if status <= 0: continue # checking an error
        collections_instances, name, status = commands.create(name, collections_instances)
        commands.check_status(status, name)

    elif command == "INSERT":

        name, text, status = myparser.parse_insert(text)
        commands.check_status(status)
        if status <= 0: continue # checking an error
        collections_instances, inverted_indexes, name, index, status = commands.insert(name, text, collections_instances, inverted_indexes)
        commands.check_status(status, name, index)

    elif command == "REMOVE":
        case, name, index, status = myparser.parse_remove(text)
        commands.check_status(status)
        if status <= 0: continue # checking an error
        collections_instances, name, inverted_indexes, index, status = commands.remove(case, name, collections_instances, inverted_indexes, index)
        commands.check_status(status)
    

    elif command == "SEARCH":
        name, condition, status = myparser.parse_search(text)
        commands.check_status(status)
        if status <= 0: continue # checking an error
        case, condition, status = myparser.parse_condition(condition)
        commands.check_status(status)
        if status <= 0: continue

        collections_instances, name, status = commands.search(name, condition, case, collections_instances, inverted_indexes)
        commands.check_status(status)

    elif command == "PRINT_INDEX":
        name, status = myparser.parse_print_index(text)
        commands.check_status(status)
        if status < 0: continue
        commands.print_indexes(name, inverted_indexes)

    elif command == "SHOW":
        status = myparser.parse_show(text)
        commands.check_status(status)
        if status < 0: continue
        print(collections_instances)

    elif command == "EXIT":
        status = myparser.parse_exit(text)
        commands.check_status(status)
        if status < 0: continue
        break
    else:
        commands.check_status(0)