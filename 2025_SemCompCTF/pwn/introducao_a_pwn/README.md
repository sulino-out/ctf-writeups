# Introdução a Pwn

### Descricao
> Esse chall não é para ser complexo, mas apenas uma introdução às ferramentas necessárias para pwn como um geral, para quem nunca teve contato com a área.
>
> Dito isso, divirta-se!
>
> `nc ganesh.icmc.usp.br 5550`

<details><summary>Hint</summary>

> Decompilou? Está confuso mesmo, decompilador não é perfeito, mas é só mandar os endereços das duas funções

</details>

<details><summary>Flag</summary>

> SEMCOMP{W3lc0me_70_7h3_jUNgl3!--pWn_1s_4_den53_f0Re5t}

</details>



---

### Arquivo

[intro.zip](../../assets/files/intro.zip)

---

### Analise inicial

Ao extrair o arquivo, recebemos um único binário `intro`. Como este é um chall introdutório, a primeira coisa a se fazer é executá-lo:

```
[user@hostname] ./intro
Olá!
Esse chall busca ser nada além de uma introdução às ferramentas à sua disposição para serem usadas em pwn
Se você não tem o código-fonte do programa e nem a paciência para ler Assebmly, existem decompiladores que tentam reverter do Assembly para C
	Sugestão: IDA Free / Ghidra
Para uma análise de toda a memória do programa durante sua execução, sugere-se o GBD, mais especificamente, sua extensão voltada para pwning, pwndbg (procure no github)
E, por fim, caso você não saiba escrever algo além de ASCII com seu teclado, existe a biblioteca pwntools para Python, que permite sua interação com o programa e o envio de bytes não ASCII
O como usar cada um fica a cargo do leitor
E um spoiler dos challs de pwn: muitos envolvem chamar uma shell. Boa sorte!

Insira a resposta para merecer a flag: 
```

Vemos entao uma mensagem do criador do chall nos dizendo para instalar as ferramentas úteis, vamos utilizá-las entao a partir de agora. Para uma breve referência das utilidades, recomendo o [Gitbook do Ganesh](https://gitbook.ganeshicmc.com/engenharia-reversa/gdb), bem como nosso [Amigo de Três Letras](https://chatgpt.com/). 

Além das ferramentas citadas, é necessario a instalacao da biblioteca `pwntools` do python, para isso utilize o comando no terminal:

```sh
pip install pwntools
```

---

### Decompilando

Abrindo o executável com o IDA, pressionamos `f5` para decompilá-lo. 

![Executável Decompilado](../../assets/img/intro_decompilado.png)

> Arquivo decompilado com o IDA. Perceba que as variáveis estao com nomes estranhos, isso é uma limitacao do decompilador

Vamos entao renomear as variáveis para que o funcionamento do programa fique mais claro:

![Executável Decompilado com Variáveis Nomeadas](../../assets/img/intro_renomeado.png)

> Arquivo decompilado e com as variáveis renomeadas.

Basicamente, o programa compara se a string que passamos no input é igual ao endereco da funcao win (em little endian) concatenado ao endereco da funcao main (também em little endian) e entao abre uma shell, entao a única coisa que precisamos fazer é descobrir qual o endereco dessas duas funcoes.

---

### Usando o GDB

Apesar de existirem outras formas de se descobrir o endereco das funcoes, como por exemplo usando `objdump -D intro`, utilizaremos o GDB por ser a ferramenta citada pelo autor do chall.

Rodamos entao no terminal `gdb intro` ou `pwndbg intro` para abrir o GDB e em seguida `info functions` para mostrar as funcoes do programa.

![Funcoes no GDB](../../assets/img/functions.png)
> Funcoes que aparecem no GDB

Vemos entao que o endereco da funcao `random_useless_function_lol` é `0x401150` e da funcao `main` é `0x40115d`

<details><summary>Um pequeno detalhe</summary>

Só podemos pegar os enderecos brutos porque o arquivo nao é `PIE (Position Independent Code)`, podemos checar isso usando:

```
[user@hostname] pwn checksec intro

Arch:       amd64-64-little
RELRO:      Partial RELRO
Stack:      No canary found
NX:         NX enabled
PIE:        No PIE (0x400000) <-------
Stripped:   No
```

O que significa que o endereco base do programa nao é randomizado a cada execucao. Voce pode entender melhor sobre isso [aqui](https://ir0nstone.gitbook.io/notes/binexp/stack/pie)

</details>

---

### Resolvendo o chall

Temos todas as informacoes que precisamos para resolver o chall, mas falta entao mandarmos o input correto para o processo remoto, para isso usaremos o `pwntools` com o seguinte script:

```python
#solve.py
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
```

Com isso, rodando `python3 solve.py`, abrimos uma shell no servidor remoto

```
[user@hostname] python3 solve.py
[+] Opening connection to ganesh.icmc.usp.br on port 5550: Done
[*] Switching to interactive mode
Olá!
Esse chall busca ser nada além de uma introdução às ferramentas à sua disposição para serem usadas em pwn
Se você não tem o código-fonte do programa e nem a paciência para ler Assebmly, existem decompiladores que tentam reverter do Assembly para C
	Sugestão: IDA Free / Ghidra
Para uma análise de toda a memória do programa durante sua execução, sugere-se o GBD, mais especificamente, sua extensão voltada para pwning, pwndbg (procure no github)
E, por fim, caso você não saiba escrever algo além de ASCII com seu teclado, existe a biblioteca pwntools para Python, que permite sua interação com o programa e o envio de bytes não ASCII
O como usar cada um fica a cargo do leitor
E um spoiler dos challs de pwn: muitos envolvem chamar uma shell. Boa sorte!

Insira a resposta para merecer a flag: 

Well done!
I'm to lazy to compile twice with different flags, so here is a shell for you!
$ ls
flag.txt
intro
run
$ cat flag.txt
SEMCOMP{W3lc0me_70_7h3_jUNgl3!--pWn_1s_4_den53_f0Re5t}
```
