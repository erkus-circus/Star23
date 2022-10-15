# Eric Diskin
# October 11, 2022
# this file parses literals into their own Nodes.

####################
## STRING, NUMBER ##
####################
from node import Node
from lexer import LexList, Types

# expects the openeing quotation mark of a string literal
def string(lexed: LexList) -> Node:

    # expect a quotation mark
    lexed.expect(Types.STRSEP)
    # this is to make sure that the string ends with the same mark that it began with
    # for example: "Hello World' would not work
    quotation = lexed.val()

    # to check if the current string is terminated or not. ie \n \t
    terminated = False
    output = ""
    while not lexed.eof() and lexed.canRetrieve():
        # move up
        lexed.step()

        # chars could be a whole token so loop through everything
        chars = lexed.val()

        if lexed.type() == "NEWLINE" and not terminated:
            # this could have more space
            if '\n' in chars:
                # error
                pass

        if terminated:
            if chars == "n":
                # new line:
                output += "\\n"
            elif chars == "t":
                # tab
                output += "\\t"
            else:
                # everything else
                output += chars

        elif lexed.val() == "\\":
            # an escape sequence
            terminated = True
            continue

        elif lexed.type() == Types.STRSEP and quotation == lexed.val():
            # the string has ended
            break
        else:
            output += chars
        terminated = False
    # wrap up output in node and return
    node = Node(Node.STRING)
    # stops with lexer on top of STRSEP
    node.value = output
    return node



# expects lexed to be pointing to the number.
def number(lexed: LexList) -> Node:
    lexed.expect(Types.NUM)

    # if this literal is a int or not
    decimal = False

    value = lexed.val()

    lexed.step()
    
    if lexed.type() == Types.PERIOD:
        decimal = True
        value += lexed.val()
        # the literal could just be 42. (making it a float)
        lexed.step()
        if lexed.type() == Types.NUM:
            value += lexed.val()
    
    node = Node(Node.NUMBER)
    node.value = value
    return node