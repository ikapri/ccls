import requests
from bs4 import BeautifulSoup

HOME_URL = 'http://www.codechef.com'
LOGIN_URL = 'http://www.codechef.com/node?destination=node'
SUBMIT_URL = 'http://www.codechef.com/submit/%s'
UA = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'
headers = {
		'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'		
		}
def login(username, password):
	try:
		r = requests.get(HOME_URL,headers=headers)
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
			headers['Referer'] = 'http://www.codechef.com'
			cookies = None
			url = LOGIN_URL
			for i in range(6):
				r = s.post(url,headers=headers,data=data,allow_redirects=False)
				if r.status_code in [301,302]:
					url = r.headers['Location']
				elif r.status_code == 200:
					cookies = s.cookies
					break
			return cookies.get_dict()
	except Exception as e:
		print e

def submit(cookies,pname='HS08TEST'):
	url = SUBMIT_URL % pname
	try:
		r = requests.get(url,headers=headers,cookies=cookies)
		if r.ok:
			soup = BeautifulSoup(r.text)
			form = soup.find('form')
			print form
			form_build_id = form.find('input',{'name':'form_build_id'}).get('value')
			print form_build_id
			form_token = form.find('input',{'name':'form_token'}).get('value')
			print form_token
			form_id = form.find('input',{'name':'form_id'}).get('value')
			print form_token
			unique_id = form.find('input',{'name':'submission_unique_id'}).get('value')
			print unique_id
			title = form.find('input',{'name':'title'}).get('value')
			print title
			problem_code = pname
			body = """import java.io.BufferedReader;\n\nimport java.io.InputStreamReader;\n\n\npublic class Main {\n\n\tpublic static void main(String[] args) throws Exception {\nBufferedReader br=new BufferedReader(new InputStreamReader(System.in));\nString b[];\nint x;\n double y;\n\nb=br.readLine().split(" ");\nx=Integer.parseInt(b[0]);\ny=Double.parseDouble(b[1]);\nif(x%5==0 && y-x>=.50)\n\tSystem.out.println(y-x-0.50d);\nelse\t\nSystem.out.println(y);\n\t}\n\n}"""
			submission_language = '10'
			data = {
					'form_build_id':form_build_id,
					'form_token':form_token,
					'form_id':form_id,
					'submission_unique_id':unique_id,
					'problem_code':problem_code,
					'title':title,
					'body':body.replace('\t','?'),
					'files[program_file]':'',
					'submission_language':submission_language,
					'changed':''
			}
			proxies = {'http':'http://192.168.1.7:8080','https':'http://192.168.1.7:8080'}
			headers['Referer'] = url
			r = requests.post(url,headers=headers,files=data,cookies=cookies,proxies=proxies)
			return r
	except Exception as e:
		print e

c = login('','')
r = submit(c)