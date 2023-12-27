#Importing the lexer needed for lexical analysis
from lexer import *
#Importing the parser for parsing the tokenized source code
from parsercomponent import *
#Importing the interpreter used to Interprete the AST and execute the corresponding actions
from interpreter import *
#Imports the sys module, which provides access to some variables maintained by the Python interpreter and to functions that interact with the interpreter.
import sys

#Entry point for the script
def main():
#Retrieving the source code file from the command line arguments

    source = sys.argv[1]
    new_lexer = Lexer(source)

    tokens = new_lexer.getTokens()

    new_parser = Parser(tokens)
    asts = new_parser.runParse()

    new_interpreter = Interpreter(asts)
    new_interpreter.execute()

main()