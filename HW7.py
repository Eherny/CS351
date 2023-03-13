#Tucker Shaw, Abraham Gomez, and Eric Hernandez
#Import required libraries for GUI and RegEx
from tkinter import *
from tkinter import ttk
import re
#Global variables
inToken = ("empty","empty") #Tuple for parsing
output_tokens = [] #List for tokens
msg = "" #String for parse tree output
"""""""""""""""""""""""""""""""""""""""""
This class defines the GUI for the Lexer
"""""""""""""""""""""""""""""""""""""""""
class LexerGUI:
def __init__(self, root):
#Create title and change background color
root.title("Lexical Analyzer for TinyPie")
root.configure(bg="#3F3F3F")
self.counter = 0 #Create the counter for line numbers
#Create and place Labels
self.input_Lbl = Label(root, text="Source Code Input:", borderwidth=2,
relief="solid",
bg="black", fg="#0FFF50", highlightthickness=1,
highlightbackground="#0FFF50")
self.input_Lbl.grid(sticky=W, row=0, column = 0, padx=(20, 50), pady=(20,
0))
self.output_Lbl = Label(root, text="Lexical Analyzed Result:",
borderwidth=2, relief="solid",
bg="black", fg="#0FFF50", highlightthickness=1,
highlightbackground="#0FFF50")
self.output_Lbl.grid(sticky=W, row=0, column=1, pady=(20,0), padx=(9, 0))
self.parse_Lbl = Label(root, text="Parse Tree:", borderwidth=2,
relief="solid",
bg="black", fg="#0FFF50", highlightthickness=1,
highlightbackground="#0FFF50")
self.parse_Lbl.grid(sticky=W, row=0, column=2, pady=(20,0), padx=(50, 0))
self.process_Lbl = Label(root, text="Current Processing Line:\t\t\t\t",
borderwidth=2, relief="solid",
bg="black", fg="#0FFF50", highlightthickness=1,
highlightbackground="#0FFF50")
self.process_Lbl.grid(sticky=W, row=2, column=0, padx=(20, 0))
self.counter_Lbl = Label(root, text=str(self.counter), borderwidth=2,
relief="solid", padx=20,
bg="black", fg="#0FFF50", highlightthickness=1,
highlightbackground="#0FFF50")
self.counter_Lbl.grid(sticky=E, row=2, column=0, padx=(20, 50))
#Create a ttk style for the Scrollbars
self.style = ttk.Style()
self.style.theme_use('clam')
self.style.configure('Vertical.TScrollbar', troughcolor="black",
background="#3F3F3F",
bordercolor="#3F3F3F", arrowcolor="#3F3F3F")
#Create and place Scrollbars
self.input_scroll_y = ttk.Scrollbar(root, orient='vertical')
self.input_scroll_y.grid(sticky=N+S+W, row=1, column=0, padx=(10, 50))
self.output_scroll_y = ttk.Scrollbar(root, orient='vertical')
self.output_scroll_y.grid(sticky=N+S+E, row=1, column=1, padx=(450, 0))
self.parse_scroll_y = ttk.Scrollbar(root, orient='vertical')
self.parse_scroll_y.grid(sticky=N+S+E, row=1, column=2, padx=(0, 10))
#Create and place Text boxes
self.input_Box = Text(root, wrap=WORD, height=20, width=55, bg="black",
fg="#0FFF50",
insertbackground="white", highlightbackground="#0FFF50",
yscrollcommand=self.input_scroll_y.set)
self.input_Box.grid(row=1, column=0, padx=(20, 50))
self.output_Box = Text(root, wrap=WORD, height=20, width=55, bg="black",
fg="#0FFF50",
insertbackground="white", highlightbackground="#0FFF50",
yscrollcommand=self.output_scroll_y.set)
self.output_Box.grid(row=1, column=1)
self.parse_Box = Text(root, wrap=WORD, height=20, width=55, bg="black",
fg="#0FFF50",
insertbackground="white", highlightbackground="#0FFF50",
yscrollcommand=self.parse_scroll_y.set)
self.parse_Box.grid(row=1, column=2, padx=(50, 20))
#Create and place Buttons
self.next_line = Button(root, text="Next Line", padx=20, bg="black",
fg="#0FFF50",
highlightbackground="#0FFF50", command=self.nextLine)
self.next_line.grid(sticky=E, row=3, column=0, padx=(20, 50), pady=(10,
20))
self.quit = Button(root, text="Quit", padx=20, bg="black", fg="#0FFF50",
highlightbackground="#0FFF50", command=self.exitProgram)
self.quit.grid(sticky=E, row=3, column=2, padx=(0, 20), pady=(10, 20))
#Configure Scrollbars for Text Boxes
self.input_scroll_y.configure(command=self.input_Box.yview)
self.output_scroll_y.configure(command=self.output_Box.yview)
self.parse_scroll_y.configure(command=self.parse_Box.yview)
self.style.configure('Vertical.TScrollbar', background="#3F3F3F",
bordercolor="#3F3F3F", arrowcolor="#3F3F3F")
#This function quits the GUI (quit Button)
def exitProgram(self):
root.destroy()
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This function will analyze the source code box line-by-line
It will highlight the line as it analyzes and prints out a
line number along with the source code onto the output box
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def nextLine(self):
global output_tokens, msg
msg = ""
if self.counter > 0:
self.input_Box.tag_remove("start", f"{self.counter}.0",
f"{self.counter}.end") #Remove previous highlight if there is one
#self.parse_Box.delete("1.0", "end")
input_txt = self.input_Box.get(f"1.0", END).split('\n') #Get a list of all
input
#Check if there is still more input to process
if self.counter < len(input_txt) - 1 and input_txt[0] != '':
self.counter += 1 #Add one to the input processing line
input_txt = self.input_Box.get(f"{self.counter}.0",
f"{self.counter}.end") #Get the line of input
#Add a highlight to the current line
self.input_Box.tag_add("start", f"{self.counter}.0",
f"{self.counter}.end")
self.input_Box.tag_config("start", background="#ff0000")
output_tokens = CutOneLineTokens(input_txt) #Get the token list from
HW3 functions
self.output_Box.insert(f"{self.counter}.0", f"{self.counter}. ")
#Display the line number
index = 3 #Start inserting after the line number
#Loop through token list and print out tokens
for i in range(len(output_tokens)):
if i < len(output_tokens) - 1:
self.output_Box.insert(f"{self.counter}.{index}",
f"{output_tokens[i]}, ")
else:
self.output_Box.insert(f"{self.counter}.{index}",
f"{output_tokens[i]}")
index += len(output_tokens[i]) + 2 #Update starting point for
insertion based on token length
self.counter_Lbl.config(text=str(self.counter)) #Update counter
self.output_Box.insert(f"{self.counter}.{index}", f"\n") #Add a new
line for next input line
parser(self.counter) #Parse the output of the lexer
self.parse_Box.insert(END, f"{msg}") #Output the parse tree into the
output box
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This function will parse a string of input and separate tokens by type
It will return a list of tokens by type
one_line is the input string being parsed
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def CutOneLineTokens(one_line):
#Define variables:
output_Lis, token = [], [] #Initialize output and token list
tk_type = "" #Initialize pattern and token type variables
choice = 0 #Initialize a counter for pattern matching
#Loop through input string until empty
while one_line != "":
#Check for whitespace characters and remove
if one_line[0] == ' ' or one_line[0] == '\t':
one_line = one_line.lstrip()
if one_line == "": #If string is now empty, leave function
break
token, tk_type = confirmPattern(one_line, choice) #Get the current token
and type
#Add the result to the output list and remove the token
output_Lis.append(f"<{tk_type},{token[0]}>")
one_line = one_line.lstrip(token[0])
#Check if the token is a string, add string and closing " then remove
if token[0] == '\"' or token[0] == '\'':
pattern = token[0]
elif token[0] == '“':
pattern = '”'
token = re.match(r'.*(?=\"|”|\')', one_line)
if token is not None: #Checking if string literal existed
output_Lis.append(f"<str_literal,{token[0]}>")
one_line = one_line.lstrip(token[0])
output_Lis.append(f"<{tk_type},{pattern}>")
one_line = one_line.lstrip(pattern)
choice = 0 #Reset the counter for next token
return output_Lis #Return the token list
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This function will choose a regEx pattern based on the input choice
It will return a regEx pattern and token type
choice is the pattern number
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def getPattern(choice):
if choice == 0: #Keywords
return r'[i,e,f]\w+', "keyword"
elif choice == 1: #Separators
return r'[(,),:,“,”,",\',;]', "separator"
elif choice == 2: #Identifiers
return r'[a-zA-Z]+\d*', "identifier"
elif choice == 3: #Operators
return r'[=, +, >, *]', "operator"
elif choice == 4: #Literals (int)
return r'\b\d+\b(?![\.])', "int_literal"
elif choice == 5: #Literals (float)
return r'\d+\.\d*', "float_literal"
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This function will confirm the correct pattern for the token
It will return the token and the type
one_line is the input string
choice is the current pattern number
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def confirmPattern(one_line, choice):
#Get the pattern and type, check for a match
pattern, tk_type = getPattern(choice)
result = re.match(pattern, one_line)
#Match not found, loop until token matches
while result is None:
choice += 1
pattern, tk_type = getPattern(choice)
result = re.match(pattern, one_line)
#Return the token and the type
return result, tk_type
"""""""""""""""""""""""""""""""""""""""""""""""""""""
This function will accept a token from the list and
get the next token
"""""""""""""""""""""""""""""""""""""""""""""""""""""
def accept_token():
#Define global variables
global inToken, output_tokens, msg
inToken = output_tokens.pop(0) #Get next type, token
split_token() #Split list and convert to tuple
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This function will parse the math node and find all multi
nodes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def math():
#Define global variables
global inToken, msg
#Start building math tree nodes
msg += "\n\nParent node math, finding children nodes:"
#Check for multi
msg += "\n child node (internal): multi"
multi()
if msg.find("Error") == -1: #Check if errors building tree
#Check for operator +
msg += "\n\nParent node math, finding children nodes:"
if inToken[1]=="+":
msg += f"\n child node (token): {inToken[1]}"
accept_token()
#Check for next multi
msg += "\n child node (internal): multi"
multi()
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This function will parse the multi node and find all children
nodes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def multi():
#Define global variables
global inToken, msg
#Start building multi tree nodes
msg += "\n\nParent node multi, finding children nodes:"
#Check for float literals and print output
if inToken[0]=="float_literal":
msg += "\n child node (internal): float_literal"
msg += f"\n float_literal has child node (token): {inToken[1]}"
accept_token()
elif inToken[0]=="int_literal": #Check for integer literals
msg += "\n child node (internal): int_literal"
msg += f"\n int_literal has child node (token): {inToken[1]}"
accept_token()
#Check for multiplication
if inToken[1]=="*":
msg += f"\n child node (token): {inToken[1]}"
accept_token()
else:
msg = "Error: multi expects * after the int_literal in the math!\n\n"
#Run the multi function again for floats
msg += "\n child node (internal): multi"
multi()
else:
msg = "Error: multi expects int_literal * multi or float_literal!\n\n"
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This function will parse a math expression and find all children nodes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def exp():
#Define global variables
global inToken, msg
#Start building the tree
msg += "Parent node exp, finding children nodes:"
#Check for keyword as first token
if(inToken[0] == "keyword"):
msg += "\n child node (internal): keyword"
msg += f"\n keyword has child node (token): {inToken[1]}"
accept_token()
else:
msg = "Error: exp expects keyword as the first element of the expression!\
n\n"
return
#Check for identifier as second token
if(inToken[0] == "identifier"):
msg += "\n child node (internal): identifier"
msg += f"\n identifier has child node (token): {inToken[1]}"
accept_token()
else:
msg = "Error: exp expects identifier as the second element of the
expression!\n\n"
return
#Check for operator = as third token
if(inToken[1] == "="):
msg += f"\n child node (token): {inToken[1]}"
accept_token()
else:
msg = "Error: exp expects = as the third element of the expression!\n\n"
return
#Build tree for math tokens
msg += "\n child node (internal): math"
math()
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This function will parse the if comparison and find all children nodes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def comparison_exp():
#Define global variables
global inToken, msg
#Start building comparison exp tree nodes
msg += "\n\nParent node comparison_exp, finding children nodes:"
#Check for identifier and print output
if inToken[0] == "identifier":
msg += "\n child node (internal): identifier"
msg += f"\n identifier has child node (token): {inToken[1]}"
accept_token()
#Check for >
if inToken[1] == '>':
msg += f"\n child node (token): {inToken[1]}"
accept_token()
else:
msg = "Error: comparison_exp expects > after the identifier in the
comparison_exp!\n\n"
#Check for identifier and print output
if inToken[0]=="identifier":
msg += "\n child node (internal): identifier"
msg += f"\n identifier has child node (token): {inToken[1]}"
accept_token()
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This function will parse the if expression and find all children nodes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def if_exp():
#Define global variables
global inToken, msg
#Start building the tree
msg += "Parent node if_exp, finding children nodes:"
#Check for keyword:if as first token
if(inToken[1] == "if"):
msg += "\n child node (internal): keyword"
msg += f"\n keyword has child node (token): {inToken[1]}"
accept_token()
else:
msg = "Error: if_exp expects keyword:if as the first element of the
expression!\n\n"
return
#Check for ( as second token
if(inToken[1] == '('):
msg += f"\n child node (token): {inToken[1]}"
accept_token()
else:
msg = "Error: if_exp expects ( as the second element of the expression!\n\
n"
return
#Build comparison tree
msg += "\n child node (internal): comparison_exp"
comparison_exp()
if msg.find("Error") == -1: #Check for errors building tree
msg += "\n\nParent node if_exp, finding children nodes:"
#Check for operator ) as fourth token
if(inToken[1] == ')'):
msg += f"\n child node (token): {inToken[1]}"
accept_token()
else:
msg = "Error: if_exp expects ) as the fourth element of the
expression!\n\n"
return
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This function will parse the print expr and find all children nodes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def print_exp():
#Define global variables
global inToken, msg
#Start building the tree
msg += "Parent node print_exp, finding children nodes:"
#Check for keyword:if as first token
if(inToken[1] == "print"):
msg += "\n child node (internal): identifier"
msg += f"\n keyword has child node (token): {inToken[1]}"
accept_token()
else:
msg = "Error: print_exp expects keyword:print as the first element of the
expression!\n\n"
return
#Check for ( as second token
if(inToken[1] == '('):
msg += f"\n child node (token): {inToken[1]}"
accept_token()
else:
msg = "Error: print_exp expects ( as the second element of the expression!\
n\n"
return
#Build tree for str_literal
msg += "\n child node (internal): string_exp"
string_exp()
if msg.find("Error") == -1: #Check for errors building tree
msg += "\n\nParent node print_exp, finding children nodes:"
#Check for ) as fourth token
if(inToken[1] == ')'):
msg += f"\n child node (token): {inToken[1]}"
accept_token()
else:
msg = "Error: print_exp expects ) as fourth element of the expression!\
n\n"
return
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This function will parse the string expr and find all children nodes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def string_exp():
#Define global variables
global inToken, msg
#Start building string exp tree nodes
msg += "\n\nParent node string_exp, finding children nodes:"
#Check for separator "
if(inToken[1] == '\"' or inToken[1] == '“' or inToken[1] == '\''):
msg += f"\n child node (token): {inToken[1]}"
accept_token()
else:
msg = "Error: string_exp expects \" as the first element of the
expression!\n"
return
#Check for string token
if inToken[0] == "str_literal":
msg += "\n child node (internal): str_literal"
msg += f"\n str_literal has child node (token): {inToken[1]}"
accept_token()
else:
msg = "Error: string_exp expects str_literal as second element of the
expression!\n\n"
#Check for separator "
if inToken[1] == '\"' or inToken[1] == '”' or inToken[1] == '\'':
msg += f"\n child node (token): {inToken[1]}"
accept_token()
else:
msg = "Error: string_exp expects \" as the third element of the
expression!\n\n"
return
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This function splits the type, token string into a tuple
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def split_token():
#Define global variable
global inToken
#Split the string into just type, token
inToken = inToken[1:]
inToken = inToken[:-1]
inToken = inToken.split(',')
tuple(inToken) #Convert the list into a tuple
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This function will create a parse tree using the token list from
cutOneLineTokens
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def parser(line):
#Define global variables
global output_tokens, inToken, msg
#Begin building the tree
msg += f"---Building parse tree for line #{line}---\n\n"
inToken = output_tokens.pop(0) #Get first type, token
split_token() #Split into tuple
#Check for BNF algorithms
if inToken[1] == "float": #Math expressions
exp()
elif inToken[1] == "if": #If Statements
if_exp()
elif inToken[1] == "print": #Print statements
print_exp()
else: #Invalid expression
msg += f"Could not find BNF for line #{line}!\n\n"
error = msg.find("Error") #Check for error in parsing
#Display appropriate msg for complete tree or error
if (inToken[1] == ';' or inToken[1] == ':') and error == -1: #Done building
tree
msg += "\n\nparse tree building success!\n\n"
elif error != -1: #Error in building
msg = f"---Building parse tree for line #{line}---\n\n" + msg
return #Leave recursive loop
if __name__ == '__main__':
root = Tk() #Create main window
gui = LexerGUI(root) #Create GUI
root.mainloop() #Main loop