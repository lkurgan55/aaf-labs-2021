class Node:

    def __init__(self, word, doc, index):
        self.left = None
        self.right = None
        self.word = word.lower()
        self.indexes = {doc: [index]}

    def insert(self, word, doc, index):
        if self.word != word:
            if word < self.word:
                if self.left is None:
                    self.left = Node(word, doc, index)
                else:
                    self.left.insert(word, doc, index)
            elif word > self.word:
                if self.right is None:
                    self.right = Node(word, doc, index)
                else:
                    self.right.insert(word, doc, index)
        else:
            if doc in self.indexes.keys():
                self.indexes[doc].append(index)
            else:
                self.indexes[doc] = [index]
                

    def find1(self, word):
        if self.word == word: # keyword
            return self.indexes        
        elif self.word > word:
            if self.left:
                return self.left.find1(word)
            else:
                return None
        elif self.word < word:
            if self.right:
                return self.right.find1(word)
            else:
                return None

    def find2(self, word):
        result = []
        if self.word[:len(word)] == word: # prefix
            result.append(self)
            if self.left: result += self.left.find2(word)
            if self.right: result += self.right.find2(word)
            return result

        elif self.word > word:
            if self.left:
                return self.left.find2(word)
            else:
                return []
        elif self.word < word:
            if self.right:
                return self.right.find2(word)
            else:
                return []
        else: None

    def __str__(self):
        return f"{self.word}: {self.indexes}" 

    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(f"{self.word}:")
        for doc in self.indexes.keys():
            print(f"  {doc} -> {self.indexes[doc]}")
        if self.right:
            self.right.PrintTree()