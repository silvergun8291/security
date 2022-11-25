import subprocess
import shlex
import os
import random

def getFileName(length=16):
  return ''.join([random.choice('0123456789abcdef') for i in range(length)])

filename = f'/tmp/{getFileName()}'
data = input('your vm (hex encode) >>> ')

try:
  fileData = bytes.fromhex(data)
except:
  print('Plz hex input')
  exit(1)

f = open(filename, 'wb')
f.write(fileData)
f.close()

print(subprocess.check_output(['md5sum', filename]))
try:
  print(subprocess.check_output(['./vm', filename]))
except subprocess.CalledProcessError as e:
  print(e.output)
finally:
  os.remove(filename)
