#!/usr/bin/python3
class netutils:
  def __init__(self,hostname):
    self.hostname = hostname 

  def resolve(self):
    import socket # ?
    try:
      return socket.gethostbyname(self.hostname)
    except Exception as error:
       return False

    def get_whois(self):
      print("whois function")
