#======================================================================================================================
# Program: elfscrow_crack.py
#
# Description: Python implementation to bruteforce weak DES keys in HHC Objective 10
#
# Date: 12/2019
#
# Author: deckerXL
#
# Examples:
#
# python3 ./elfscrow_crack.py --epoch_start=1575658800 --epoch_end=1575666000 --encrypted_file=./ElfUResearchLabsSuperSledOMaticQuickStartGuideV1.2.pdf.enc --plaintext_file=./ElfUResearchLabsSuperSledOMaticQuickStartGuideV1.2.pdf --magicbyte_sentinel=PDF
#
#======================================================================================================================
import sys
from Crypto.Cipher import DES
from Crypto.Cipher import PKCS1_OAEP
import time
import binascii
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--epoch_start", help="Start time in Unix epoch time {}", required=True)
parser.add_argument("--epoch_end", help="End time in Unix epoch time {12}", required=True)
parser.add_argument("--encrypted_file", help="Encrypted file {encrypted.enc}", required=True)
parser.add_argument("--plaintext_file", help="Plaintext filename to output {plaintext.ext}", required=True)
parser.add_argument("--magicbyte_sentinel", help="String to look for {PDF}", required=True)
parser.add_argument("--debug", action="store_true", help="Enable debugging output")
args = parser.parse_args()

def gen_key(seed):
	
	val1 = "000343fd"   # Multiply value (214013 int) taken from dissembled code - (01351DC8 | IMUL EAX,EAX,343FD)
	val2 = "00269ec3"   # Add value (2531011 int) taken from dissembled code - (01351DCE | ADD EAX,269EC3)
	val3 = "00000010"   # Shift right value (16 int) taken from dissembled code - (01351DDD | SAR EAX,10)
	val4 = "00007fff"   # AND value (0111 1111 1111 1111i binary) taken from dissembled code - (01351DE0 | AND EAX,7FFF)
	val5 = "000000ff"   # Keep the low order byte - build key byte by byte with these - (01351E3F | AND ECX,0FF)

	if args.debug:
		print("Val1 Hex:"+str(format(int(val1,16),'#010x'))+" = Int:"+str(int(val1,16)))
		print("Val2 Hex:"+str(format(int(val2,16),'#010x'))+" = Int:"+str(int(val2,16)))
		print("Val3 Hex:"+str(format(int(val3,16),'#010x'))+" = Int:"+str(int(val3,16)))
		print("Val4 Hex:"+str(format(int(val4,16),'#010x'))+" = Int:"+str(int(val4,16)))

	if args.debug:
		print("Seed: "+str(seed))

	# The initial value for state is the seed
	state = seed

	key = ""
	for i in range(0,8):

		# Step 1 - Multiply val1 with the current state value
		step1 = state * int(val1,16)
		if args.debug:
			print("Step1 state*val1: "+str(format(int(str(step1),16),'#010x')))

		# Step 2 - Add val2 to the current state value
		step2 = step1 + int(val2,16)
		if args.debug:
			print("Step2 step1+val2: "+str(format(int(str(step2),16),'#010x')))

		# Save State - this now becomes the saved state value for the next iteration of the loop
		state = step2
		if args.debug:
			print("Save State:       "+str(format(int(str(state),16),'#010x')))

		# Step 3 - Do a bitwise shift right 16 bits
		step3 = step2>>16
		if args.debug:
			print("Step3 step2>>16:  "+str(format(int(str(step3),16),'#010x')))

		# Step 4 - Do a bitwise AND with val4
		step4 = step3 & int(val4,16)
		if args.debug:
			print("Step4 step3&val4: "+str(format(int(str(step4),16),'#010x')))

		# Step 5 - Do a bitwise AND with val5 - this will retain the least significant/low-order byte
		lsb = hex(int(step4) & int(val5,16))
		if args.debug:
			print ("Key:"+str(format(int(step4),'#010x'))+" -- Least Significant Byte:"+str(lsb))

		# Concatenate this least significant byte to become part of the key
		key = key + str(format(int(lsb,16),'02x'))

		step1 = step2 = step3 = step4 = lsb = 0

	if args.debug:
		print ("Key:  "+key)

	return key

# ===================================================
# Main
# ===================================================

start_seed = int(args.epoch_start)
end_seed   = int(args.epoch_end)

infile  = args.encrypted_file
outfile = args.plaintext_file

ciphertext = open(infile, "rb").read()  
cipher_len = len(ciphertext)
if cipher_len % 8 != 0:
	for i in range(0, 8 -cipher_len%8):
		ciphertext += " "

#iv = str(bytearray(8)) 
iv = bytearray(8) 

plaintext = ""
found = False
for s in range(start_seed,end_seed+1):
	key_hex = gen_key(s)

	if args.debug:
		print ("Seed: "+str(s)+" -- Key: "+str(key_hex))

	key = binascii.unhexlify(key_hex)
	cipher = DES.new(key, DES.MODE_CBC, iv)
	plaintext = cipher.decrypt(ciphertext)
	plaintext_header = plaintext[0:8]

	print ("Seed:"+str(s)+" -- Key: "+str(key_hex)+" -- Bytes: ["+str(plaintext_header)+"]")

	filetype = plaintext_header.find(args.magicbyte_sentinel.encode())
	if filetype > 0:
		print ("\nFOUND IT! - Seed:"+str(s)+" -- Key: "+str(key_hex)+" -- Bytes: ["+str(plaintext_header)+"]\n")
		found = True
		break

if found:
	print ("Writing plaintext output ["+args.plaintext_file+"]")
	f = open(outfile, "wb")
	f.write(plaintext)
	f.close()
else:
	print ("ERROR: Did not find a key that decrypted ciphertext to magic bytes.")
	sys.exit(1)

sys.exit(0)
