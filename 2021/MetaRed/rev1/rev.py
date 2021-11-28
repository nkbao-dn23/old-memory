# ref: https://docs.python.org/3/library/dis.html

import math
import requests
import hashlib
from Crypto.Cipher import AES
import base64



def main():
	#a = requests.get('https://cdimage.kali.org/kali-2020.4/kali-linux-2020.4-installer-amd64.iso')
	#m = hashlib.sha256()
	#m.update(a)
	#a = int(m.hexdigest(), 16)
	#limit = a//2941460046203168433808698735326701052265551841195155278226402
	
	limit = 12345678987654320
	n1 = 0
	#for i in range(limit):
	#	n1 += i*2 - 1
	
	n1 = (limit*(limit-1)) - limit

	#n1 = 2*n1 - limit
	print("n1:" + str(int(n1)))
	n2 = 0
	#for i in range(int(n1)):
	#	n2 += math.floor(i/2) * 2
	
	n1 = int(n1//2)
	n2 = (n1*(n1-1)) * 2

	print("n2: " + str(n2))

	key = hex(n2)[2:]
	#print(b"key: " + key[:16])
	

	key = key[:16]
	print("key: " + key)
	cipher = AES.new(key, AES.MODE_ECB)

	bb = 'zoCeKfVqUw66ErPWhOWnPSmHq5h6rnofsrLkkwgQcDnEnvJMtWgaXSg6KYOSFG+i'
	#bb = "LJdRO21paI4uFymXza2nig=="

	encrypted = base64.b64decode(bb)

	msg = cipher.decrypt(encrypted)

	print(msg)

	#raw = open("flag.txt").read().encode("utf-8")
	#raw = b'flag{is_here_pd}'
	#encrypted = cipher.encrypt(raw)
	#encoded = base64.b64encode(encrypted)
	#print(encoded)
	#if(encoded == b'zoCeKfVqUw66ErPWhOWnPSmHq5h6rnofsrLkkwgQcDnEnvJMtWgaXSg6KYOSFG+i'):
	#	print("win")

main()