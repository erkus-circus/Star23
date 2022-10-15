# Eric Diskin
# October 11, 2022
# S23
# this file contains the Node

class Node:

    # here is a list of types of nodes

    # NUMBER is a literal, could be an int or a float
    # Uses: value, float,
    NUMBER = 1

    # STRING is a literal, contains a string "Hello World!"    
    # Uses: value
    STRING = 2

    # FUNC_DEC is a function declaration the syntax is:
    # func function_name@return_type (argument_name1@argument_type, argument_name2@argument_type) { ...body... }
    # Uses: name, arguments, type, children
    FUNC_DEC = 3

    # ARGUMENT is for arguments that are declared in a function declaration
    # func a@b (arg1@argType, arg2@argType)
    # Uses: name, type
    ARGUMENT = 4
    
    def __init__(self, nodetype) -> None:
        self.nodetype = nodetype
        self.name = ""
        self.value = ""
        # for arrays, lists
        self.values = []
        # for arguments of a function declaration or call
        self.arguments = []
        # for variable & function types
        self.type = ""
        # for children, like a funciton has nodes that will be run as its children
        self.children = []
        # if a variable is constant
        self.constant = False
        # if a variable is initialized or not
        self.initialized = False
        # for built-in functions (will compile to straight binary)
        self.special = False
        # if a number contains a decimal or not
        self.float = False