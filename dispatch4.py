import sys
import traceback
import functools

# Python 2/3 compatibility
try: input = raw_input
except NameError: pass

dispatch = {}
current_user = ""

def cmd(name_or_func):
	if isinstance(name_or_func, str):
		# Parameterized decorator
		def inner(func):
			dispatch[name_or_func] = func
			return func
		return inner
	# Else we have no parameter - use the function name.
	dispatch[name_or_func.__name__] = name_or_func
	return name_or_func

def login_required(func):
	@functools.wraps(func)
	def inner(args):
		if current_user != "rosuav":
			print("You may not use that command.")
			return
		return func(args)
	return inner

@cmd
def login(args):
	global current_user
	current_user = args[0] if args else ""
	print("Now logged in as " + current_user)

@cmd
@cmd("+")
def add(args):
	print("Sum: %d" % sum(int(arg) for arg in args))

@cmd
@cmd("*")
def mul(args):
	product = 1
	for arg in args: product *= int(arg)
	print("Product: %d" % product)

@cmd
@login_required
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

@cmd
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
