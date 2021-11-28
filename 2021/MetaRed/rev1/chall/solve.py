import math 
import requests
import hashlib
from Crypto.Cipher import AES
import base64


def main():
	#a = requests.get('https://cdimage.kali.org/kali-2020.4/kali-linux-2020.4-installer-amd64.iso')
	#m = hashlib.sha256()
	#m.update(a.content)
	mhexdigest = "50492d761e400c2b5e22c8f253dd6f75c27e4bc84e33c2eff272476a0588fb02"
	a = int(mhexdigest, 16)	
	limit = a // 2941460046203168433808698735326701052265551841195155278226402
	print("limit: " + str(limit))
	# limit = 12345678987654320
	n1 = 0 
	#for i in range(limit):
	#	n1 += i*2 - 1
	
	# (0 + 1 + 2 + .. + (limit-1)) * 2 - limit

	n1 = (limit-1)*limit - limit

	print("n1:" + str(n1))
	
	
	n2 = 0 
	#for i in range(n1):
	#	n2 += math.floor(i/2) * 2
	
	n1 = n1//2
	# 0 + 1 + 2 + ... n1/2
	n2 = (n1-1)*n1 * 2   

	print("n2: " + str(n2))
	

	
	key = hex(n2)[2:][:16]   # 12313
	print("key: " + key)
	cipher = AES.new(key, AES.MODE_ECB)


	b64ecrypt = 'zoCeKfVqUw66ErPWhOWnPSmHq5h6rnofsrLkkwgQcDnEnvJMtWgaXSg6KYOSFG+i'
	b64decrypt = base64.b64decode(b64ecrypt)

	msg = cipher.decrypt(b64decrypt)
	print(msg)

	#raw = open("flag.txt").read().encode('utf-8')
	#encrypted = cipher.encrypt(raw)
	#encoded = base64.b64encode(encrypted)

	#print(encoded)
	#if(encoded.decode() == 'zoCeKfVqUw66ErPWhOWnPSmHq5h6rnofsrLkkwgQcDnEnvJMtWgaXSg6KYOSFG+i' ):
	#	print("correct")
	
main()