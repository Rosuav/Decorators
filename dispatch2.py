import sys
import traceback

# Python 2/3 compatibility
try: input = raw_input
except NameError: pass

dispatch = {}

def cmd(name):
	def inner(func):
		dispatch[name] = func
		return func
	return inner

@cmd("add")
@cmd("+")
def add(args):
	print("Sum: %d" % sum(int(arg) for arg in args))

@cmd("mul")
@cmd("*")
def mul(args):
	product = 1
	for arg in args: product *= int(arg)
	print("Product: %d" % product)

@cmd("splel") # oops, what a stroke of irony
def spell(args):
	with open("/usr/share/dict/words") as dict:
		words = {line.strip() for line in dict}
	correct = 0
	for word in args:
		if word in words:
			correct += 1
		else:
			print("Misspelled: "+word)
	print("%d correctly spelled words." % correct)

@cmd("quit")
def quit(args):
	print("Bye!")
	sys.exit()

while "moar commands":
	try: line = input("Command> ").split()
	except EOFError: line = ["quit"]
	if not line: continue
	if line[0] not in dispatch:
		print("Unrecognized command - type 'quit' to end")
		continue
	try: dispatch[line[0]](line[1:])
	except Exception: traceback.print_exc()
