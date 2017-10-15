import socket 
ip = 'localhost'
port = 7000 
addr = ((ip,port)) 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client_socket.connect(addr)
while True: 
  mensagem = raw_input("digite uma mensagem para enviar ao servidor") 
  client_socket.send(mensagem) 
  print 'mensagem enviada'   
client_socket.close()