import json

import myparser
import commands

collections_instances = {}

# loading data
with open("collections_instances.json", "r") as read_file:
    collections_instances = json.load(read_file)

print("Enter commands")

while(True):
    status = 0

    print(collections_instances)
    
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
        collections_instances, name, index, status = commands.insert(name, text, collections_instances)
        commands.check_status(status, name, index)

    elif command == "REMOVE":
        case, name, index, status = myparser.parse_remove(text)
        commands.check_status(status)
        if status <= 0: continue # checking an error
        collections_instances, name, index, status = commands.remove(case, name, collections_instances, index)
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


    elif command == "EXIT":
        # saving data
        with open("collections_instances.json", "w") as write_file:
            json.dump(collections_instances, write_file)
        break
    else:
        commands.check_status(0)