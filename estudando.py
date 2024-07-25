#precisava praticar um pouco aqui no python então decidi criar um codigo novo :D
#[] {} + / = ? meu teclado não tem esses caracteres então tenho q ficar dando ctrlc ctrlv

#estruturas
estados = [] 
alfabeto = [] 
estadoInicial = ""
estadoFinal = []
transicao = {}

#inserindo o conjunto de estados
print("insira o conjunto de estados: ", end= "") #o end é só pro python não quebrar a linha automaticamente
estados = input().split()

#inserindo o alfabeto
print("insira o alfabeto: ", end= "")
alfabeto = input().split()

#inserindo o estado inicial
print("insira o estado inicial: ", end= "")
estadoInicial = input()

#inserindo os estados finais
print("insira os estados finais: ", end= "")
estadoFinal = input().split()

#inserindo as funções de transição
print("insira as funções de transição:\t ('n' para vazio) ", end= "")


for estado in estados:
    for simbolo in alfabeto:
        print(f"\n\t {simbolo}")
        print(f"{estado}\t--->\t", end="")
        proximoEstado = input()

        if proximoEstado == " ":
            transicao[(estado, simbolo)] = None
        else:
            transicao[(estado, simbolo)] = proximoEstado

#inserindo linguagem
print("insira a linguagem a ser reconhecida: ")
entrada = input()

estadoAtual = estadoInicial
#[] {} + / = ?
for simbolo in entrada:
    print(f"estado atual: {estadoAtual}")
    print(f"entrada: {simbolo}")

    print(f"proximo: {transicao[(estadoAtual, simbolo)]}")

    estadoAtual = transicao[(estadoAtual, simbolo)]

    if estadoAtual == None:
        print(f"linguagem não reconhecida >:P")
        break

if estadoAtual in estadoFinal:
    print(f"palavra aceita")
else:
    print(f"palavra não aceita")