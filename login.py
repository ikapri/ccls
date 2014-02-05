import requests
from bs4 import BeautifulSoup

HOME_URL = 'http://www.codechef.com'
LOGIN_URL = 'http://www.codechef.com/node?destination=node'
UA = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'
headers = {
		'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
		'Referer':'http://codechef.com'
}
def login(username, password):
	try:
		proxies = {'http':'http://192.168.1.7:8080','https':'http://192.168.1.7:8080'}
		r = requests.get(HOME_URL,headers=headers,proxies=proxies)
		if r.ok:
			soup = BeautifulSoup(r.text)
			form = soup.find('form',{'id':'user-login-form'})
			form_build_elem = form.find('input',{'name':'form_build_id'})
			form_build_id = form_build_elem.get('value')
			data = {
					'name':username,
					'pass':password,
					'submit.x':14,
					'submit.y':9,
					'form_build_id':form_build_id,
					'form_id':'user_login_block'
			}
			s = requests.Session()
			cookies = None
			url = LOGIN_URL
			for i in range(6):
				r = s.post(url,headers=headers,data=data,proxies=proxies,allow_redirects=False)
				if r.status_code in [301,302]:
					url = r.headers['Location']
				elif r.status_code == 200:
					cookies = s.cookies
					break
			return cookies.get_dict()
	except Exception as e:
		print e