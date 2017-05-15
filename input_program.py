#Purpose: command line arguments and standard input handling

from collections import OrderedDict
import getopt
import sys

print("Standard Input:")

# get the command line arguments

try:
	opts,args = getopt.getopt(sys.argv[1:],'o:t:h')
except getopt.GetoptError as err:
	# print help information and exit:
	print(err) # will print something like "option -a not recognized"
	sys.exit(2) # Unix programs generally use 2 for command line syntax errors and 1 for all other kind of errors.

optionlst = {}
for o,a in opts:
	if o == "-o":
		optionlst[1] = (o,a)
	elif o == "-t":
		optionlst[2] = (o, a)
	elif o == "-h":
		optionlst[3] = (o, a)

OrderedDict(sorted(optionlst.items(),key=lambda t:t[0]))

# read from standard input
#text= input() # requires exception processing!

text = sys.stdin.readline() # leaves the newline char at the end

print(text,end='')
lines= []
while text:
	lines.append( text )
	text= sys.stdin.readline()
	print(text, end='')

print("Command line arguments:")


for i in optionlst:
	if i == 1:
		print("option 1:" + optionlst[i][1])
	elif i == 2:
		print("option 2:" + optionlst[i][1])
	elif i == 3:
		print("option 3")


