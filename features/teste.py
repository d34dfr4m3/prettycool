credential = open('../keys/db_creds','r')
for line in credential:
  password=(line.replace('\n',''))
  print(password)

