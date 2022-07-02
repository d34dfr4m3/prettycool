#!/bin/bash
#set -x 
DB='db_data'
FILE='../keys/db_creds' 

mkdir ../keys

systemctl start mysql
if [ $(id -u) -eq 0 ];then
  db_version=`echo  'select version();' | mysql -u root  | tail -n1 `

  echo "Database Version: $db_version"
  echo "drop database $DB;" | mysql -u root
  echo "revoke all privileges on db_data.* from 'prettycool'@'localhost';" | mysql -u root 
  echo "drop user prettycool@localhost;" | mysql -u root 
  echo "drop database db_data;":| mysql -u root 
  echo "[+] Creating Database"
  mysql -u root   < $1 
  password=`pwgen -sy 12`
  echo "[+] Creating user"
  echo "create user 'prettycool'@'localhost' IDENTIFIED BY '$password';"| mysql -u root 
  echo "[+] User:prettycool Password:$password"
  echo -e "Password:$password" >> $FILE
  sed -i  "s/FRESHINSTALL/$password/g" ../features/db_controler.py
  sed -i  "s/FRESHINSTALL/$password/g" ../features/report_maker.py
  echo "[-] Credentials saved at $FILE"
  echo "[+] Granting Privileges"
  echo "grant all privileges ON $DB.* to 'prettycool'@'localhost';" | mysql -u root
else
	echo "[!!] Error: You need to run with root user"
fi

