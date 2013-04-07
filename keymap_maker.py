import os
from subprocess import Popen, PIPE
from sys import argv
from tempfile import mkstemp

CPP = "arm-none-eabi-cpp"
START_MARKER = "===begin==="
END_MARKER = "===end==="

if (len(argv) != 3):
	print "Make a device tree keymap"
	print "Usage:"
	print "\tkeymap_maker.py input.txt /path/to/kernel_src/"
	quit()

include_path = os.path.join(argv[2], "include", "uapi", "linux", "input.h")
include_path = include_path.replace('\\', '\\\\')
include_path = include_path.replace('"', '\"')

file_contents = '#include "{0:s}"\n'.format(include_path)

with open(argv[1]) as f:
	file_contents += f.read()

p = Popen([CPP, "-E", "-D__KERNEL__"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
stdout, stderr = p.communicate(file_contents)

if (p.returncode != 0):
	print "C preprocessor returned error!"
	print stderr
	quit()

file_contents = str(stdout)
index_start = file_contents.find(START_MARKER)
index_end = file_contents.find(END_MARKER)

if (index_start == -1 or index_end == -1 or index_start >= index_end):
	print "Syntax error. Missing beginning or end"
	quit()

index_start += len(START_MARKER)

file_contents = file_contents[index_start:index_end].strip()

print "keymap = <"

rows = file_contents.splitlines()
x, y = 0, 0
counter = 0

for row in rows:
	cols = row.split()
	for col in cols:
		col = int(col)
		if (col != 0):
			print "\t0x{0:02x}{1:02x}{2:04x}".format(y, x, col),
			counter += 1
			if (counter % 3 == 0): print
		x += 1
	x = 0
	y += 1

print "\t>;"
