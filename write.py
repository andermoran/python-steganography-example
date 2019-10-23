#!/usr/bin/python

# https://en.wikipedia.org/wiki/Netpbm_format
# http://netpbm.sourceforge.net/doc/ppm.html
# https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa

# PPM header format: P6->(2 bytes) WIDTH->(3 bytes) HEIGHT->(3 bytes) 255->(3 bytes) then RGB data->(3 bytes)

import binascii
import sys

def print_usage():
    print "Usage: write.py file.PPM 'your secret message'"

def set_bit(v, index, x):
  """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
  mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
  v &= ~mask          # Clear the bit indicated by the mask (if x is False)
  if x:
    v |= mask         # If x was True, set the bit indicated by the mask.
  return v            # Return the result, we're done.
  
def set_last_two_bits(c,b1,b0):
  char = set_bit(ord(c), 1, b1)
  char = set_bit(ord(chr(char)), 0, b0)
  return chr(char)
  
  
if len(sys.argv) != 3:
  print_usage()
  exit(1)

with open(sys.argv[1]) as f:
  content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line

i = 4
while i < len(content):
  content[3] += content[i]
  i += 1

#secret_message = "HELLO THIS IS A SECRET MESSAGE" # 01-00-00-01 * 01-00-11-10 * 01-00-01-00 * 01-00-01-01 * 01-01-00-10
secret_message = sys.argv[2] # 01-00-00-01 * 01-00-11-10 * 01-00-01-00 * 01-00-01-01 * 01-01-00-10
secret_message_length_binary = bin(len(secret_message))[2:]
while len(secret_message_length_binary) < 32:
  secret_message_length_binary = '0' + secret_message_length_binary[0:]

# WANT TO SET FIRST
# 2^20 bytes = 1MB
# 2^20 bytes = 1MB
# use 32 bits or 4 bytes to store the file size encrypted (MAX: 4294967296-1 bits or 536.870912 MB)
# first 12 segments of 2 bits will be read and stored as the size (in bits) to be read (not including those bits)
# use next 16 bits to declare the offset of where the encrypted message will be placed (0-65535)

# this is to clear any contents in the file in case it already exists
fh = open('sten_output.PPM','w')
fh.write('')
fh.close()

fh = open('sten_output.PPM','a')
fh.write(content[0] + content[1] + content[2])

for i in range(0,32,2):
  first_index = False
  zeroth_index = False
  if int(secret_message_length_binary[i]) == 1:
    first_index = True
  if int(secret_message_length_binary[i+1]) == 1:
    zeroth_index = True
  
  c = set_last_two_bits(content[3][i/2], first_index, zeroth_index)
  fh.write(c)


i = 16
message_index = 0
while message_index < len(secret_message):
  c = set_last_two_bits(content[3][i], ord(secret_message[message_index])&128 != 0, ord(secret_message[message_index])&64 != 0)
  fh.write(c)
  i += 1
  c = set_last_two_bits(content[3][i], ord(secret_message[message_index])&32 != 0, ord(secret_message[message_index])&16 != 0)
  fh.write(c)
  i += 1
  c = set_last_two_bits(content[3][i], ord(secret_message[message_index])&8 != 0, ord(secret_message[message_index])&4 != 0)
  fh.write(c)
  i += 1
  c = set_last_two_bits(content[3][i], ord(secret_message[message_index])&2 != 0, ord(secret_message[message_index])&1 != 0)
  fh.write(c)
  i += 1
  message_index += 1

while i < len(content[3]):
  fh.write(content[3][i])
  i += 1

print 'Succesfully placed your message in sten_output.PPM'

fh.close()
