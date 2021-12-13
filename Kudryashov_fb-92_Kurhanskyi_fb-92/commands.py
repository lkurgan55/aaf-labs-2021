import re
from tree import Node

class Collection:
    def __init__(self):
        self.indx = 0
        self.docs = {}

def create(col, collections_instances):
    # not unique name
    if col in collections_instances.keys():
        return collections_instances, col, -3

    collections_instances[col] = Collection()
    return collections_instances, col, 1

def insert(col, text, collections_instances, inverted_indexes):
    index = 0
    # incorrect name        
    if collections_instances.get(col) == None:
        return collections_instances, inverted_indexes, col, index, -5
    # getting new index
    
    doc = collections_instances[col].indx
    collections_instances[col].indx += 1
    # adding text to collections
    collections_instances[col].docs.update({doc: text})
    # creating inverted indexes
    
    words = re.split('[^a-zA-Z0-9_]+', text)
    while '' in words: words.remove('')
    words = [x.lower() for x in words]
    #print(words)
    if col not in inverted_indexes.keys():
        inverted_indexes[col] = Node(words[0], doc, 0)
        range_list = range(1,len(words))
    else:  
        range_list = range(len(words))

    for i in range_list: # {colection1: Tree}
        inverted_indexes[col].insert(words[i], doc, i)

    return collections_instances, inverted_indexes, col, doc, 2

def exit(command):
    pass

def search(col, condition, case, collections_instances, inverted_indexes):
    # incorrect name        
    if collections_instances.get(col) == None:
        return collections_instances, col, -5
    
    # collection is empty
    if collections_instances[col].docs == {}:
        return collections_instances, col, -14

    #print(f"searching in collection: {col} case: {case}")
    #print(f"Condition: {condition} \n")

    result = None

    if case == 0:
        for doc in collections_instances[col].docs:
            print(f"{doc}: \"{collections_instances[col].docs[doc]}\"")
        result = True

    elif case == 1:
        result = inverted_indexes[col].find1(condition.lower())
        if result != None:
            for doc in result.keys():
                print(f"{doc}: \"{collections_instances[col].docs[doc]}\"")

    elif case == 2:
        result = inverted_indexes[col].find2(condition.lower())
        set_docs = set()
        if result != []:
            for elem in result:
                set_docs.update(elem.indexes.keys())
            
            for doc in set_docs:
                print(f"{doc}: \"{collections_instances[col].docs[doc]}\"")
        else: result = None

    elif case == 3:
        word1 = condition[0].lower()
        word2 = condition[1].lower()
        n = condition[2]

        # getting inverted indexes for keywords
        w1_index = inverted_indexes[col].find1(word1)
        w2_index = inverted_indexes[col].find1(word2)

        if w1_index == None or w2_index == None: # incorrect keyword
            return collections_instances, col, -15

        #print(w1_index)
        #print(w2_index)

        docs = list(set(w1_index.keys()) & set(w2_index.keys())) # the common docs
        for doc in docs:
            found = False
            ###if abs(w2_index[doc][-1] - w1_index[doc][0]) < n: continue # unreal condition
            i, j = 0, 0
            while(i < len(w2_index[doc]) and j < len(w1_index[doc])):
                #print(i, j)
                if abs(w2_index[doc][i] - w1_index[doc][j]) == n:
                    print(f"{doc}: {collections_instances[col].docs[doc]}")
                    result = True 
                    found = True
                    break
                elif w2_index[doc][i] - w1_index[doc][j] < n: i += 1
                elif w2_index[doc][i] - w1_index[doc][j] > n: j += 1
            
            if found: continue
            
            i, j = 0, 0
            w2_index, w1_index = w1_index, w2_index # replace word1 and word2
            while(i < len(w2_index[doc]) and j < len(w1_index[doc])):
                #print(i, j)
                if abs(w2_index[doc][i] - w1_index[doc][j]) == n:
                    print(f"{doc}: {collections_instances[col].docs[doc]}")
                    result = True 
                    break
                elif w2_index[doc][i] - w1_index[doc][j] < n: i += 1
                elif w2_index[doc][i] - w1_index[doc][j] > n: j += 1
    
    if result == None:
        return collections_instances, col, -13

    return collections_instances, col, 100

def print_indexes(col, inverted_indexes):
    if col in inverted_indexes.keys():
        inverted_indexes[col].PrintTree()    
    else: print("Collection not found or is empty!")
    

def check_status(status, col ="", index = 0):
    statuses = {
        4: f"text index {index} has been deleted from collection {col}",
        3: f"Collection {col} has been deleted",
        2: f"The text has been added to '{col}' by index {index}!",
        1: f"New collection '{col}' has been created!",
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
        -12: "Missing text!",
        -13: "I have found nothing :(",
        -14: "The collection is empty!",
        -15: "Keyword is not found!"
    }

    if status != 100:
        print(statuses[status])

