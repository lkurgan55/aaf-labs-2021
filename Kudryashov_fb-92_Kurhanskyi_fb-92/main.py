import json
import os

import myparser
import commands

collections_instances = {}
inverted_indexes = {} # {"world": {colection1:{ doc1: [номер в тексте]: }

# loading data
if os.path.exists("./collections_instances.json"):
    with open("collections_instances.json", "r") as read_file:
        collections_instances = json.load(read_file)
else:
    pass

if os.path.exists("./inverted_indexes.json"):
    with open("inverted_indexes.json", "r") as read_file:
        inverted_indexes = json.load(read_file)
else:
    pass


print("Enter commands")

while(True):
    status = 0

    print(collections_instances) # delete before release
    print(inverted_indexes) # delete before release
    
    text = input(">>")
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

        collections_instances, name, status = commands.search(name, condition, case, collections_instances)
        commands.check_status(status)

    elif command == "PRINT_INDEX":
        name, status = myparser.parse_print_index(text)
        commands.check_status(status)
        if status < 0: continue
        commands.print_indexex(name, inverted_indexes)

    
    elif command == "SHOW":
        status = myparser.parse_show(text)
        commands.check_status(status)
        if status < 0: continue
        print(collections_instances)

    elif command == "EXIT":
        status = myparser.parse_exit(text)
        commands.check_status(status)
        if status < 0: continue
        # saving data
        with open("collections_instances.json", "w") as write_file:
            json.dump(collections_instances, write_file)
        with open("inverted_indexes.json", "w") as write_file:
            json.dump(inverted_indexes, write_file)
        break
    else:
        commands.check_status(0)