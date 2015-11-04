import sys
import time
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

def clock(func):
	@functools.wraps(func)
	def inner(args):
		start = time.clock()
		func(args)
		tm = time.clock() - start
		print("Time taken: %f" % tm)
	return inner

def memoize(func):
	results = {}
	@functools.wraps(func)
	def inner(*args):
		if args not in results:
			results[args] = func(*args)
		return results[args]
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
def spell(args):
	if current_user != "rosuav":
		print("You may not use that command.")
		return
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
def fire_missiles(args):
	if current_user != "rosuav":
		print("You may not use that command.")
		return
	print("BOOOOM! Missiles fired at latitude %s longitude %s" % (args[0], args[1]))

@cmd
def reboot_server(args):
	if current_user != "rosuav":
		print("You may not use that command.")
		return
	print("This is a very destructive command.")
	confirm = input("To confirm, enter 'Yes, do as I say!': ")
	if confirm != 'Yes, do as I say!':
		print("Cancelled.")
		return
	print("Shutting down the server for reboot... nah, just kidding!")

def call_count(func):
	@functools.wraps(func)
	def inner(n):
		inner.count += 1
		return func(n)
	inner.count = 0
	return inner

# Helper for fib()
@call_count
# @memoize
def stupid_fibonacci(n):
	if n < 2: return n
	return stupid_fibonacci(n-1) + stupid_fibonacci(n-2)

@cmd
@clock
def fib(args):
	stupid_fibonacci.count = 0
	n = int(args[0])
	print("Fibonacci number %d is: %d" % (n, stupid_fibonacci(n)))
	print("Took %d calls" % stupid_fibonacci.count)

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
