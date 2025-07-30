#Trie node, representing each letter in a genre
class LetterNode:
    def __init__(self, letter):
        self.letter = letter
        self.children = {}
        self.isEnd = False

#Trie for storing and searching genres efficiently
class GenreTree:
    #Initializes an empty trie with a dummy root node
    def __init__(self):
        self.root = LetterNode("*")

    """Inserts a new genre into the trie
    
    Args: genre (str): Genre to be added"""
    def AddWord(self, genre):
        current_node = self.root
        for letter in genre:
            if letter not in current_node.children.keys():
                current_node.children[letter] = LetterNode(letter)
            current_node = current_node.children[letter]
        current_node.isEnd = True #Marks the end of the genre

    """Finds genres matching or starting with user's input.
    
    Args: search_term (str): User input for search
    
    returns: list or False: List of genres matching user input or False if none found"""
    def SearchTree(self, search_term):
        current_node = self.root
        for letter in search_term:
            if letter not in current_node.children.keys():
                return False
            current_node = current_node.children[letter]
        if current_node.isEnd: #Exact match found
            return [search_term]
        else:
            return self.ListGenres(current_node.children, search_term, []) #Find genres starting with search_term

    """Builds a sorted list of genres starting with prefix.
    
    Args:   children_list (dict): Dictionary of child nodes from the current trie node
            prefix (str): Current genre prefix
            genre_list (list): Accumulating of matching genres
            
    Returns: list: Sorted list of matching genres"""
    def ListGenres(self, children_list, prefix, genre_list):
        for letter in children_list.values():
            if letter.isEnd:
                genre_list.append(prefix + letter.letter)
            else:
                self.ListGenres(letter.children, prefix + letter.letter, genre_list) #Recursively collect genres
        genre_list.sort()
        return genre_list