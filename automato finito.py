import pynput

#Entrada de dados do Automato
def entradaDados():
    estados = int(input('Digite quantos estados possui o automato:\n'))
    for i in range (estados):
        if i == 0:
            estadosGerados = "q{}".format(i)
        else:
            estadosGerados += ",q{}".format(i)
    estadosGerados = estadosGerados.split(',')
    #print(estadosGerados)
    alfabeto = str(input('Digite o alfabeto:\n')).split(', ')
    transicoes = []
    for i in estadosGerados:
        for j in alfabeto:
            qtdTransicoes = int(input(f'Quantas transições existem quando o estado é "{i}" e a entrada for "{j}"?'))
            for m in range(qtdTransicoes):
                transicoes.append([i, j, str(input('Para o estado "{}", qual é a sua transição quando a entrada for "{}"?\n'.format(i, j)))])
            #print(transicoes)
    estadoInicial = str(input(f'Dentre {estados}, qual estado seria o inicial? '))
    estadoFinal = str(input(f'Dentre os estados {estados}, qual(is) seria(m) o(s) estado(s) de aceitação? ')).split(', ')
    print('Automato Salvo!!!')
    return estadoInicial, alfabeto, estadoFinal, estados, transicoes


#Simulação de aceitação de palavras
def simulacaoAFD(parametrosEstados):
    palavra = str(input('Digite a palavra:'))
    estadoAtual = parametrosEstados[0]

    for i in palavra:
        for j in parametrosEstados[1]:
            if i == j:
                break
        else:
            print('Palavra rejeitada, pois ela não faz parte do alfabeto')

        
        for k in parametrosEstados[4]:
            if k[0] == estadoAtual and i == k[1]:
                estadoAtual = k[2]
                #print(k)
                #print(estadoAtual)
                break


    if estadoAtual == parametrosEstados[2][0]:
        print('Palavra Aceita!!!')
    else:
        print('Palavra Rejeitada!!!')

def simulacaoAFN(parametrosEstados):
    palavra = str(input('Digite a palavra:'))
    estadoAtual = parametrosEstados[0]

    for i in palavra:
        for j in parametrosEstados[1]:
            if i == j:
                break
        else:
            print('Palavra rejeitada, pois ela não faz parte do alfabeto')

        contagem = 0
        estadoTemporario = []
        for k in parametrosEstados[4]:
            if k[0] == estadoAtual and i == k[1]:
                if contagem < 1:
                    estadoAtual = k[2]
                    contagem += 1
                else:
                    estadoTemporario.append(k[2])
                    sinal = True
           
            if sinal:
                contagem = 0
                if len(estadoTemporario) < 2:
                    if k[0] == estadoTemporario[0] and i == k[1]:
                        estadoTemporario[0] = k[2]
                else: 
                    h = 0
                    while h < len(estadoTemporario): 
                        if k[0] == estadoTemporario[h] and i == k[1]:
                            estadoTemporario[h] = k[2]
                            


simulacaoAFN(entradaDados())

