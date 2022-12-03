#!/usr/bin/python3

import subprocess
import sys
import signal
import re
from shlex import quote

def alarm_handler(signum, frame):
  try:
    p.kill()
  except:
    pass
  print('Timeout!')
  exit(1)

def checkIp(ip):
  regex = '(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}'
  if(re.search(regex, ip)):
    return False
  else:
    return True
 
def checkMail(email):
  regex = '^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$'
  if(re.search(regex, email)):
    return False
  else:
    return True

signal.signal(signal.SIGALRM, alarm_handler)
signal.alarm(120)

binaryPath = '/home/ctf/ms' # change

ip       = input('ip > ').replace('\n', '')
port     = input('port > ').replace('\n', '')
email    = input('email > ').replace('\n', '')
password = input('password > ').replace('\n', '')
content  = input('content > ').replace('\n', '')

try:
  port = int(port)
except:
  print('port is int')
  exit(-1)

if checkIp(ip):
  print('Not valid ip')
  exit(-1)

if checkMail(email):
  print('Not valid email')
  exit(-1)

blackList = '''`!#$&*(){}[];|<>?_+ '''

for i in blackList:
  if i in ip:
    print('NO!')
    exit(1)
  elif i in email:
    print('NO!')
    exit(1)
  elif i in password:
    print('NO!')
    exit(1)
  elif i in content:
    print('NO!')
    exit(1)


cmd = f'{binaryPath} --ip {ip} --port {port} --email {email} --password {password} --message {content}'

p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.wait(timeout=60)
print(p.stdout.read())
print('END')
