import requests
from bs4 import BeautifulSoup
from config import *
import time, json


def login(username, password):
    print "Logging in...."
    try:
        r = requests.get(HOME_URL, headers=headers)
        if r.ok:
            soup = BeautifulSoup(r.text)
            form = soup.find('form', {'id': 'user-login-form'})
            form_build_elem = form.find('input', {'name': 'form_build_id'})
            form_build_id = form_build_elem.get('value')
            data = {
            'name': username,
            'pass': password,
            'submit.x': 14,
            'submit.y': 9,
            'form_build_id': form_build_id,
            'form_id': 'user_login_block'
            }
            s = requests.Session()
            headers['Referer'] = 'http://www.codechef.com'
            cookies = None
            url = LOGIN_URL
            for i in range(6):
                r = s.post(url, headers=headers, data=data, allow_redirects=False)
                if r.status_code in [301, 302]:
                    url = r.headers['Location']
                elif r.status_code == 200:
                    cookies = s.cookies
                    break
            if 'Hello ' + username in r.text:
                return cookies.get_dict()
    except Exception as e:
        print e


def submit(cookies, pname, file, lang_code, contest=''):
    if contest:
        url = SUBMIT_URL % (contest + '/', pname)
    else:
        url = SUBMIT_URL % ('', pname)
    try:
        r = requests.get(url, headers=headers, cookies=cookies)
        if r.ok:
            soup = BeautifulSoup(r.text)
            form = soup.find('form')
            form_build_id = form.find('input', {'name': 'form_build_id'}).get('value')
            form_token = form.find('input', {'name': 'form_token'}).get('value')
            form_id = form.find('input', {'name': 'form_id'}).get('value')
            unique_id = form.find('input', {'name': 'submission_unique_id'}).get('value')
            title = form.find('input', {'name': 'title'}).get('value')
            problem_code = pname
            submission_language = lang_code
            data = {
            'form_build_id': (None, form_build_id, None),
            'form_token': (None, form_token, None),
            'form_id': (None, form_id, None),
            'submission_unique_id': (None, unique_id, None),
            'problem_code': (None, problem_code, None),
            'title': (None, title, None),
            'body': (None, '', None),
            'files[program_file]': (pname, open(file, 'rb'), 'application/octet-stream'),
            'submission_language': (None, submission_language, None),
            'changed': (None, '', None)
            }
            headers['Referer'] = url
            r = requests.post(url, headers=headers, files=data, cookies=cookies)
            if r.ok:
                return r
    except Exception as e:
        print e
    return False


def logout(cookies):
    print "Logging out..."
    try:
        r = requests.get(LOGOUT_URL, headers=headers, cookies=cookies)
        return r.ok
    except Exception as e:
        print e
        return False


def get_submission_id(response):
    soup = BeautifulSoup(response)
    scripts = soup.find_all('script', {'src': None})
    sc = None
    for s in scripts:
        if 'submission_id' in s.text:
            sc = s
    if not sc:
        return False
    text = sc.text
    ind1 = text.find('submission_id =')
    ind2 = text.find(';')
    s_id = text[ind1 + 16:ind2]
    return s_id


def get_submission_status(s_id):
    try:
        for i in range(5):
            r = requests.get(SUBMISSION_STATUS_URL % s_id)
            if r.ok:
                data = json.loads(r.text)
                if data['result_code'] == 'wait':
                    print "Your code is being executed.Please wait..."
                    time.sleep(5)
                    continue
                else:
                    return data
    except Exception as e:
        print e