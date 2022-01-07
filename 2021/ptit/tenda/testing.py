import requests

url_home = "http://pishcm.club/"
url_login = "http://pishcm.club/login"
url_setting = "http://pishcm.club/settings"
url_change = "http://pishcm.club/api/v1/users/me"


payload1 = {
    'name': 'connan23343@gmail.com',
    'password': 'heapme'
}

payload2 = {
	"name":"connan23343@gmail.com",
	"email":"connan23343@gmail.com",
	"confirm":"heapme",
	"password":"lolstat",
	"fields":[
	]
}


with requests.Session() as s:
	# init session to get cookie(not nesessary) and nonce 
    p = s.get(url_home)
    nonce = p.text.split('csrfNonce\': \"')[1].split('\"')[0]
    #print(nonce)

    coki = "session=" + p.cookies["session"]

    header = {
		"Host": "pishcm.club",
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
		"Accept": "application/json",
		"Referer": "http://pishcm.club/settings",
		"Content-Type": "application/json",
		"CSRF-Token": nonce,
		"Origin": "http://pishcm.club",
		"Cookie": coki
	}

    # add nonce to payload 
    payload1["nonce"]=nonce

    # login
    p = s.post(url_login, data=payload1)
    #print(p.text)

    # change password 
    r = s.patch(url_change, data=payload2, headers=header)
    print(r.text)
