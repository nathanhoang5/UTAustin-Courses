import socket
s = socket.socket()
try:
  s.bind(('', 8686)) #replace 6113 with port number for list_servers command (nathanh:6113 (alias: nathanhsocket))
  s.listen(5)
  data = s.accept()
  print(data[0].recv(1024)) 
  data[0].send(b'message from nathans server (nathanhserver)')
  s.close()
except:
  s.close()
  pass