from pwn import *

r = remote('challenge.ctf.games',31090)

r.recvline()
r.recvline()
r.recvline()
r.recvline()
r.recvline()
r.recvline()
r.recvline()
u = r.recvline()
print(u)
nhap_play = "play"
r.sendline(nhap_play.encode())
for l_30 in range(0,30):
	u = r.recvline() # repear #1
	print(u)
	u = r.recvline()
	print(u)
	u = r.recvline()
	print(u)
	ls = []
	tmp_set=set()
	for i in range(0,16):
		u = r.recvline()
		print(u)
	#	if(i==0):
	#		print(u)
	#		print("ok",len(u))
	#		for i in range(0,len(u)):
	#		        print("{0}--{1}".format(i,chr(u[i])))
		for j in range(0,len(u)):
			_ = u[j]
			if(j%4==0 and j>=8):
				ls.append(_)	
				tmp_set.add(_)
	#uu=""
	#for i in range(0,17):
	#	uu = uu + chr(ls[i])
	#print(uu)
	di = {}
	for _ in tmp_set:
		di[_]=[]	
	print(len(ls))
	#print(chr(ls[0]))
	#print("kiem tra")
	dem=0
	for i in range(0,16):
		for j in range(0,16):
			#pp = (j,i)
	#		print("{0}--{1}".format(chr(ls[dem]),pp))
			di[ls[dem]].append((j,i))
			dem+=1
	#print("ket thuc kiem tra")
	#for p in di:
	#	print("{0}--{1}".format(p,di[p]))
	r.recvline()
	r.recvline()
	for l_5 in range(0,5):
		u = r.recvuntil('>')
		tap_ki_tu = []
		print(u)
		for _ in u:
			if _ in tmp_set:
				tap_ki_tu.append(_)
				print("{0}--{1}".format(chr(_),di[_]))
#		print(tap_ki_tu)
		#y tuong check 8 huong 
		# Dung 1 ky tu dau roi check 8 huong, xem thu co huong nao thoa man thi add vao 
		# tao mang luu 8 huong
		huong = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
		answer = []
		for _ in di[tap_ki_tu[0]]:
			x = _[0]
			y = _[1]
			x_0 = _[0]
			y_0 = _[1]
			answer.append((x,y))
			check=0
			for hu in range(0,8):
				dau=0
				dx = huong[hu][0]
				dy = huong[hu][1]
				for i in range(1,len(tap_ki_tu)):
					p = (x+dx,y+dy)	
					dai_dien_x = 0
					dai_dien_y = 0
					if(p[0]<0):
						dai_dien_x = p[0]+16
					else:
						dai_dien_x = p[0]
					if(p[1]<0):
						dai_dien_y = p[1]+16
					else:
						dai_dien_y = p[1]
					daidien = (dai_dien_x,dai_dien_y)
					if daidien in di[tap_ki_tu[i]]:
						answer.append(p)
						x=daidien[0]
						y=daidien[1]
					else:
						dau=1
						break
				if(dau==0):
					dauu = 0
					#for _ in answer:
					#	if(_[0]<0 or _[1]<0):
					#		dauu=1
					#		break
					if(dauu==0):
						check=1
						break
				else:
					answer = [(x_0,y_0)]
					x=x_0
					y=y_0
			if(check==1):
				break
			else:
				continue
		#print("haha",answer)
		answer1 = []
		dd = len(answer)-len(tap_ki_tu)
		print("dd",dd)
		for i in range(dd,len(answer)):
			answer1.append(answer[i])
			
		res="["
		for i in range(0,len(answer1)):
			if(i==len(answer1)-1):
				res = res + "(" + str(answer1[i][0]) + ", " + str(answer1[i][1]) + ")]"
			else:
				res = res + "(" + str(answer1[i][0]) + ", " + str(answer1[i][1]) + "), "

#		print("ok",res)
		r.sendline(res.encode())
	#r.sendline(res.encode()))
	u = r.recvline()
	print(u)
	u = r.recvline()
	print(u)
	r.recvline()
	#u = r.recvline() # ket thuc repeat 2
	#print(u)
u = r.recvline()
print(u)		




#	# sang phai 
#	demm=1
#	for i in range(y+1,16):
#		toado_x=x
#		toado_y=i
#		p = (toado_x,toado_y)	
#		dau=0
#		if p in di[tap_ki_tu[demm]]:
#			dau=1
#			demm+=1
#			answer.append(p)
#		if(dau==0):
#			break
#	if(len(answer)==len(tap_ki_tu)):
#		break
#	else:
#		answer = [(x,y)]
	
		






#print("test di ",di[ls[0]])

#dem_u=0
#ans_u = 0
#res = "["
#for i in range(0,len(u)):
#	if(u[i] in ls):
#		ans_u+=1
#for i in range(0,len(u)):
#	_ = u[i]
#	if(_ in ls):
#		dem_u+=1
#		#print("{0}--{1}".format(di[_][0],di[_][1]))
#		res = res + "(" + str(di[_][0])+", "+str(di[_][1])+")"
#		if(dem_u!=ans_u):
#			res = res + ", "
#		else:
#			res = res + "]."
#print(res)
#r.sendline(res.encode())
#r.recvline()
#u = r.recvline()
#print(u)
