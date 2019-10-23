#!/usr/bin/python

import sys
import binascii

def print_usage():
  print 'Usage: read.py file.PPM'
      
def last_two_bits(f):
  content = f.readlines()
  i = 4
  while i < len(content):
    content[3] += content[i]
    i += 1
  bytes = content[3]
  for b in bytes:
    for i in reversed(xrange(2)):
      yield (ord(b) >> i) & 1
      
      
if len(sys.argv) != 2:
  print_usage()
  exit(1)

input_file = sys.argv[1]
bit_index = 0
buffer = '0b'
buffer_size = -1

try:
  open(input_file, 'r')
except:
  print 'Unable to read ' + input_file
  print_usage()
  exit(1)
  

for b in last_two_bits(open(input_file, 'r')):
  if bit_index == 32:
    buffer_size = int(buffer, 2)
#    print "buffer_size: " + str(buffer_size)
    buffer = '0b'
  if bit_index < 32:
    buffer += str(b)
  else:
    if bit_index % 8 == 0 and bit_index != 32:
      n = int(buffer, 2)
      if n == 10:
        print # this is for '\n', acts weird withbinascii.unhexlify
      else:
        sys.stdout.write("%s" %binascii.unhexlify('%x' % n))
      buffer = '0b' + str(b)
      #sys.stdout.write("%s" %b)
    else:
      #print "b = " + str(b)
      buffer += str(b)
    if bit_index == buffer_size*8+32:
      break
  bit_index += 1

print # this is to make a new line in the terminal after the message prints