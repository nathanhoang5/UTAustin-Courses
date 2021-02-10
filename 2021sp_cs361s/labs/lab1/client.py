import socket
s = socket.socket()
try:
  s.connect(('127.0.0.1', 8900)) #replace 6116 with forwarded port from forward command (forward 6116 nathanhsocket)
  s.send(b'message from nathans client - hello :)')
  print(s.recv(1024))
  # s.close()

except:
  # s.close()
  pass