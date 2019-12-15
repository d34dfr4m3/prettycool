#!/bin/bash
#set -x 
DB='db_data'
FILE='../db_creds'
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
  echo "[+] User:prettycool\n Password:$password" >> $FILE
  echo "[-] Credentials saved at $FILE"
  echo "[+] Granting Privileges"
  echo "grant all privileges ON $DB.* to 'prettycool'@'localhost';" | mysql -u root
else
	echo "[!!] Error: You need to run with root user"
fi
