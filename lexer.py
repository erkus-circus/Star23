from lib2to3.pytree import Base
from traceback import TracebackException, print_tb
import traceback


class Type:
    def __init__(self, a: str, b: str, c=False):
        self.name = a
        self.values = b
        self.stackable = c

    def isOfType(self, type: str) -> bool:
        return self.values.find(type) >= 0

    name = ""
    values = ""
    stackable: bool

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class LexList:
    def __init__(self) -> None:
        self.index: int = -1
        self.length: int = 0
        self.types: list[Type] = []
        self.vals: list[str] = []


    def add(self, type: Type, val: str):
        self.types.append(type)
        self.vals.append(val)
        self.length += 1
    

    def getLineOfCurrentToken(self) -> int:
        # returns the line the current token is on
        
        # get index before stepping down
        indexBeforeStepDown = self.index

        # go back to the start
        self.index = 0

        numberOfLines = 1

        # go through the list until you reach the current token, counting how many \n there are
        while self.index <= indexBeforeStepDown:
            if self.type() == "NEWLINE":
                numberOfLines += len(self.val())
            self.step()

        self.index = indexBeforeStepDown
        
        return numberOfLines

    def expect(self, *types: Type):
        typeFound = False
        for i in types:
            if self.type() == i:
                typeFound = True
                break
        if not typeFound:
            #error
            print(traceback.format_exc())
            print(bcolors.UNDERLINE + bcolors.BOLD + bcolors.FAIL + "An Error occured on line " + str(self.getLineOfCurrentToken()) + bcolors.ENDC + bcolors.HEADER + " Expected:", [j.name for j in types], bcolors.OKCYAN + "Token Index:", self.index, bcolors.ENDC + '\n')
            
            # print the line that the error occured on

            # get index before stepping down
            indexBeforeStepDown = self.index

            # print the start of the line that the error occured on
            while not self.type() == "NEWLINE":
                self.step(-1)

            self.step()

        
            # print the end of the line that the error occured on
            while not self.type() == "NEWLINE" and not self.type() == "EOF":
                if self.index == indexBeforeStepDown:
                    print(bcolors.FAIL + self.val() + bcolors.ENDC, end="")
                else:
                    print(bcolors.WARNING + self.val(), end="" + bcolors.ENDC)
                self.step()

            print("\n")
            exit(-1)


    def type(self) -> Type:
        return self.types[self.index] if self.canRetrieve() else Types.EOF

    def val(self) -> str:
        return self.vals[self.index] if self.canRetrieve() else "EOF"

    def step(self, steps: int = 1):
        self.index += steps

    # skips whitespace, whitespace must be on top
    # down is false, unless true then skip downwards instead of upwards
    def skipSpace(self, down: bool = False):
        if not self.canRetrieve() or self.type() == "EOF":
            return
        while self.type() == "SPACE" or self.type() == "NEWLINE":
            self.step(-1 if down else 1)
        # check for comment type here
        # then skip comment
        if self.type() == "EXPONENT":
            while not '\n' in self.val():
                self.step()
            # skip the last space
            self.skipSpace()
    
    # print out all of the lexed list
    def printOut(self):
        for i in range(self.length):
            if self.types[i] == "NEWLINE" or self.types[i] == "SPACE":
                continue
            print("(" + str(i) + ")" + self.vals[i] + ": " + self.types[i].name)
    

    # checks if you are able to retrieve a token
    def canRetrieve(self) -> bool:
        return self.index < self.length
    
    # checks if the current value is EOF
    def eof(self) -> bool:
        return self.type() == "EOF"


class Types:
    ID = Type("ID", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", True)
    STRSEP = Type("STRSEP", "\"`'")
    NUM = Type("NUM", "1234567890", True)
    SPACE = Type("SPACE", " \t", True)
    QMARK = Type("QMARK", "?")
    COMMA = Type("COMMA", ",")
    EXPOMARK = Type("EXPOMARK", "!")
    PARENTH = Type("PARENTH", "()")
    CURLY_PAREN = Type("CURLY_PAREN", "{}")
    BRACKET = Type("BRACKET", "[]")
    # adding the = sign here to make my life much easier.
    COMPOPERATOR = Type("COMPOPERATOR", "<>=", True)
    OPERATOR = Type("OPERATOR", "/*+-")
    PERIOD = Type("PERIOD", ".")
    USCORE = Type("USCORE","_")
    BSLASH = Type("BSLASH","\\")
    SEMICOL = Type("SEMICOL",";")
    AT = Type("TYPEOPER","@")
    TILDE = Type("TILDE","~")
    EXPONENT = Type("EXPONENT", "^")
    # this is a special case, not included in list types
    STATEMENT = Type("STATEMENT", "")
    # maybe should add EOF type?]
    NEWLINE = Type("NEWLINE", "\n", True)

    EOF = Type("EOF", "")

types = [
	Types.ID,
	Types.STRSEP,
	Types.NUM,
	Types.SPACE,
	Types.QMARK,
    Types.COMMA,
	Types.EXPOMARK,
	Types.PARENTH,
	Types.CURLY_PAREN,
	Types.BRACKET,
    Types.COMPOPERATOR,
	Types.OPERATOR,
	Types.PERIOD,
	Types.USCORE,
	Types.BSLASH,
	Types.SEMICOL,
	Types.TILDE,
	Types.EXPONENT,
    Types.AT,
    Types.NEWLINE,
    Types.EOF
]

statements = [
    "func",
	"var",
	"if",
    "else",
	"return",
    "include",
    "while",
    "for"
]

def lex(text: str, linenum=0) -> LexList:
    index = 0

    lexed = LexList()

    lastType = Types.EOF
    lastVal = "NULL"
    first = False

    length = len(text)

    done = False

    for i in range(length):
        c = text[i]

        theType = getCharType(c)

        if theType == lastType and theType.stackable:
            lastVal += c
        else:
            if first:
                for j in range(len(statements)):
                    if statements[j] == lastVal:
                        lastType = Types.STATEMENT
                lexed.add(lastType, lastVal)
            else:
                first = True
            
            lastType = theType
            lastVal = c
    for i in range(len(statements)):
        if statements[i] == lastVal:
            lastType = Types.STATEMENT
    
    lexed.add(lastType, lastVal)

    lexed.add(Types.EOF, "EOF")

    return lexed

def getCharType(char: str) -> Type:
    for i in range(len(types)):
        if types[i].isOfType(char):
            return types[i]
    return Type("NULL", "^")


