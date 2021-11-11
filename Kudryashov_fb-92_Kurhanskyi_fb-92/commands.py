import re

def create(name, collections_instances):
    # not unique name
    if name in collections_instances.keys():
        return collections_instances, name, -3

    collections_instances[name] = {}
    return collections_instances, name, 1

def insert(name, text, collections_instances, inverted_indexes):
    index = 0
    # incorrect name        
    if collections_instances.get(name) == None:
        return collections_instances, inverted_indexes, name, index, -5
    # getting new index
    indexes = [int(x) for x in collections_instances[name].keys()]
    index = str(int(max(indexes)) + 1) \
        if len(collections_instances[name].keys()) else '0'
    # adding text to collections
    collections_instances[name].update({index: text})
    # creating inverted indexes
    words = re.split('[^a-zA-Z0-9_]+', text)

    for i in range(len(words)):
        if words[i] in inverted_indexes.keys():
            try: 
                inverted_indexes[words[i]][name][index].append(i)
            except: 
                try: inverted_indexes[words[i]][name][index] = [i]
                except: inverted_indexes[words[i]][name] = {index: [i]}
                
        else: # {"world": {colection1:{ doc1: [номер в тексте]: }
            inverted_indexes[words[i]] = {name:{index:[i]}}

    return collections_instances, inverted_indexes, name, index, 2

def remove(case, name, collections_instances, inverted_indexes, index = 0):
    index = str(index)
    # incorrect name        
    if collections_instances.get(name) == None:
        return collections_instances, name, inverted_indexes, index, -5
    
    if case == 1: # removing colection {"world": {colection1:{ doc1: [номер в тексте]: }
        collections_instances.pop(name)
        for word in inverted_indexes.keys():
            try:
                inverted_indexes[word].pop(name)
            except: pass
        return collections_instances, name, inverted_indexes, index, 3
    elif case == 2: # removing doc from colection
        if collections_instances[name].get(index) == None:
            return collections_instances, name, inverted_indexes, index, -11
        collections_instances[name].pop(index)
        for word in inverted_indexes.keys():
            try:
                inverted_indexes[word][name].pop(index)
            except: pass

        return collections_instances, name, inverted_indexes, index, 4

def exit(command):
    pass

def search(name, condition, case, collections_instances):
    # incorrect name        
    if collections_instances.get(name) == None:
        return collections_instances, name, -5

    print(f"searching in collection: {name} case: {case}")
    print(f"Condition: {condition}")

    return collections_instances, name, 100

def print_indexex(name, inverted_indexes):    
    for word in inverted_indexes.keys():
        if name not in inverted_indexes[word].keys(): continue
        print(f'"{word}":')
        for doc in inverted_indexes[word][name]:
            print(f"{doc} -> {inverted_indexes[word][name][doc]}")

def check_status(status, name ="", index = 0):
    statuses = {
        4: f"text index {index} has been deleted from collection {name}",
        3: f"Collection {name} has been deleted",
        2: f"The text has been added to '{name}' by index {index}!",
        1: f"New collection '{name}' has been created!",
        0: "Command not found!",
        -1: "Incorect first symbol in name!",
        -2: "Incorect symbol in name!",
        -3: "The name is used!",
        -4: "Too many parameters!",
        -5: "Collection not found!",
        -6: "Incorrect \"\"",
        -7: "Incorrect input",
        -8: "Missing WHERE!",
        -9: "Missing condition!",
        -10: "Incorrect syntax!",
        -11: "Incorrect index!",
        -12: "Missing text!"
    }

    if status != 100:
        print(statuses[status])

