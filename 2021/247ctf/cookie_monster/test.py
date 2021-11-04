for i in range(1, 0xffffff):
	canary = i << 8
	print(hex(canary))
