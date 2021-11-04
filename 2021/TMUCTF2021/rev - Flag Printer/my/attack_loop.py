data = []

def loop(index):
	v3 = 0
	for i in range(1, index):
		v3 = (index + (v3 ^ i))% 10
	v2 = v3*data[index-1]
	return (index + v2 + v3*data[index-2])%1000000

def main():
	for i in range(1370):
		data.append(0)
	#print(data)
	
	data[1] = 0xa
	data[2] = 0x20
	
	#print(hex(loop(3)))
	
	for i in range(3, len(data)):
		data[i] = loop(i)

	note = [0x0000002e	,0x00000022	,0x00000983	,0x000bce11,0x000b6612	,0x0009fd20	,0x0000007f	,0x0007dc23,0x00031372	,0x00000045	,0x000a15e5	,0x00013985,0x0009431a	,0x000000b2	,0x000000a6	,0x000d929b,0x0008e5c9	,0x0004b1ba	,0x000de169	,0x00019268,0x000bcf55	,0x0006c58f	,0x00030131	,0x0006ec86,0x000639e5	,0x000c306f	,0x000002c0	,0x000002f3,0x00078b1d	,0x0002433f	,0x000d2034	,0x000003e8,0x000315e1	,0x000c2163	,0x000004f5	,0x0001ec35,0x00003736	,0x00000525	]
	
	flag = "T"

	for i in range(1, len(note)):
		tmp = (data[i*i] ^ note[i]) - i + 38
		flag += chr(tmp)
		print(flag)
	


if(__name__ == "__main__"):
	main()