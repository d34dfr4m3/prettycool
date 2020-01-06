#!/bin/bash
function basic_packages(){
  apt-get install git pip pwgen -y
}
function configure_database(){
  apt-get update -y
  apt-get install mariadb-server -y
  systemctl start mariadb-server
  systemctl enable mariadb-server
  # mysql_secure_installation
  ./database/build_db.sh database/databasev1.sql
}

function requirementsPython(){
  pip3 install -r requirements.txt
}

function installMasscan(){
  apt-get install git gcc make libpcap-dev -y 
  git clone https://github.com/robertdavidgraham/masscan.git /opt/masscan
  cd /opt/masscan
  make -j 

}

function installNode(){
  echo "[+] Installing node"
  curl -sL https://deb.nodesource.com/setup_13.x | bash -
  apt-get install -y nodejs
  echo '[-] Loading enviroment for node'
  . ~/.bashrc
  NODE_VERSION=$(node --version)
  echo "[*] Node instalation is done, version $NODE_VERSION"
}

function installOrq(){
  echo "[+] Orquestrator goin up"
  git clone https://github.com/g4rcez/prowler.git 
  npm i -g ts-node yarn
  cd PROJETO
  #yarn
  #ts-node src —url dominio.com
}

basic_packages
configure_database
requirementsPython
installMasscan
#installNode
#installOrq
