inputs = "print(open('flag', 'r').read())"

inputs = inputs.encode("utf-8").hex()

#inputs = "7072696e74286f70656e2827666c6167272c20277227292e72656164282929"

result = ""

for i in range(len(inputs)//2):
	result += "chr(0x" + inputs[i*2:i*2+2] + ")+"
print(result[:-1])