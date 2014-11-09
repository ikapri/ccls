import util, getpass, argparse, os
from config import LANG_CODES
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument('-p', help="The Problem Name")
parser.add_argument('-f', help="The source code file")
parser.add_argument('-c', help="The Contest Name")
parser.add_argument('-l', help="The Programming Language.", choices=LANG_CODES.keys())
args = parser.parse_args()

if not (args.p and args.f and args.l):
    parser.error("Please provide problem name(-p) and source file location(-f) and Programming Language(-l)")
if not os.path.exists(args.f):
    parser.error("The source code file does not exist")

username = raw_input("Username:")
passwd = getpass.getpass()
pname = args.p.upper()
if args.c:
    contest = args.c.upper()
else:
    contest = ''
file = args.f
lang_code = LANG_CODES[args.l]

cookies = util.login(username, passwd)
if not cookies:
    exit("Could not login")
print "Successfully Logged in!"

print "Submitting Your source code..."
r = util.submit(cookies, pname, file, lang_code, contest)
if not r:
    print "Could not submit the problem.Please check if problem name and/or contest name are correct"
    util.logout(cookies)
    exit()

s_id = util.get_submission_id(r.text)
if not s_id:
    print "There was some problem in retrieving your submission id.Please try again."
    util.logout(cookies)
    exit()
print "Your submission id is %s" % s_id

status = util.get_submission_status(s_id)
if not status:
    print "Could not get submission status."
print "Your submission status :"
pprint(status)
util.logout(cookies)