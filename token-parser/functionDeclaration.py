# Eric Diskin
# October 11, 2022
# S23
# this is for function declarations
# parses funciton name, return type, & arguments

## TODO: when bodyParser is complete, have it parse the body of the function.

##############
## FUNC_DEC ##
##############

from node import Node
from lexer import LexList, Types


# expects to be pointing to func statement
def functionDeclaration(lexed: LexList) -> Node:

    lexed.expect(Types.STATEMENT)

    # step and skip whitespace
    lexed.step()
    lexed.skipSpace()

    # now get the function name
    lexed.expect(Types.ID)
    funcName = lexed.val()

    # step and skip whitespace again
    lexed.step()
    lexed.skipSpace()

    # expect an @ symbol
    lexed.expect(Types.AT)
    # then skip
    lexed.step()
    lexed.skipSpace()

    # get the return type
    lexed.expect(Types.ID)
    returnType = lexed.val()

    # get the arguments next.
    arguments = []

    # expect an opening (
    lexed.expect(Types.PARENTH)
    # chekc to make sure it is the correct type of parenthesis
    if lexed.val() != "(":
        # TODO: create an error here.
        pass 

    # step and skip whitespace
    lexed.step()
    lexed.skipSpace()
    
    while lexed.type() != Types.EOF:
        # first, get the name of the variable
        lexed.expect(Types.ID)
        argName = lexed.val()

        # expect an @ symbol
        lexed.expect(Types.AT)
        # then skip
        lexed.step()
        lexed.skipSpace()

        # get the  type
        lexed.expect(Types.ID)
        argType = lexed.val()

        # expect either a comma or a closing parenthesis
        # then skip
        lexed.step()
        lexed.skipSpace()

        # add the argument to the arguments list
        argNode = Node(Node.ARGUMENT)
        argNode.name = argName
        argNode.type = argType
        arguments.append(argNode)

        if lexed.val() == ")":
            # the end of the arguments have been found
            break
        # otherwise, expect a comma now
        lexed.expect(Types.COMMA)
        # skip to the next argument, which should be an ID
        lexed.step()
        lexed.skipSpace()
    # the above while loop ends pointing to a ), so step and expect the {
    lexed.step()
    lexed.skipSpace()
    lexed.expect(Types.CURLY_PAREN)
    # make sure that it is a { and not a }
    if lexed.val() != "{":
        #TODO: make an error here
        pass
    
    # here I would use the parseStatement function in a loop until the token being pointed to is a }

    # create and return the function node.
    funcNode = Node(Node.FUNC_DEC)
    funcNode.name = funcName
    funcNode.type = returnType
    funcNode.arguments = arguments
    funcNode.children = [] # TODO: the parse statement function

    # this function ends pointing to a } token
    return funcNode