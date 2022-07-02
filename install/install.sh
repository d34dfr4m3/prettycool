#!/bin/bash
function basic_packages(){
  apt-get install git python3-pip pwgen -y
}
function configure_database(){
  apt-get update -y
  apt-get install mariadb-server -y
  systemctl start mariadb-server
  systemctl enable mariadb-server
  # mysql_secure_installation
  ./database/build_db.sh ./database/database-latest.sql 
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

function installAquatone(){
  sudo apt install chromium -y 
  mkdir /opt/aquatone 
  cd /opt/aquatone
  wget "https://github.com/michenriksen/aquatone/releases/download/v1.7.0/aquatone_linux_amd64_1.7.0.zip"
  unzip aquatone*
  cd - 
}

basic_packages
configure_database
requirementsPython
installMasscan
installAquatone
