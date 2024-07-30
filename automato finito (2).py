#import pynput

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
            qtdTransicoes = int(input(f'Quantas transições existem quando o estado é "{i}" e a entrada for "{j}"?\n'))
            for m in range(qtdTransicoes):
                transicoes.append([i, j, str(input('Para o estado "{}", qual é a sua transição quando a entrada for "{}"?\n'.format(i, j)))])
            #print(transicoes)
    estadoInicial = str(input(f'Dentre {estadosGerados}, qual estado seria o inicial? '))
    estadoFinal = str(input(f'Dentre os estados {estadosGerados}, qual(is) seria(m) o(s) estado(s) de aceitação? ')).split(', ')
    print('Automato Salvo!!!')
    return estadoInicial, alfabeto, estadoFinal, estadosGerados, transicoes, estados

def definirSimulacao(parametrosEstados):
    qtdEstados = 0
    mudou = True
    for estados in parametrosEstados[3]:
        for transicoes in parametrosEstados[4]:
            if estados == transicoes[0]:
                qtdEstados += 1
    
    if (qtdEstados/len(parametrosEstados[1])) > parametrosEstados[5]:
        simulacaoAFN(parametrosEstados)
    else:
        simulacaoAFD(parametrosEstados)


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
                break


    if estadoAtual in parametrosEstados[2]:
        print('Palavra Aceita!!!')
    else:
        print('Palavra Rejeitada!!!')

def simulacaoAFN(parametrosEstados):
    palavra = str(input('Digite a palavra:'))
    estadoAtual = parametrosEstados[0]
    estadoTeste = ''
    estadoTemporario = []
    estadoInicial = parametrosEstados[0]

    sinal = False
    for i in palavra:
        for j in parametrosEstados[1]:
            if i == j:
                break
        else:
            print('Palavra rejeitada, pois ela não faz parte do alfabeto')

        
        ocorrencia = False
        contagem = 0
        entrou = False
        for k in parametrosEstados[4]:
            if k[0] != estadoTeste and k[2] != estadoInicial and not ocorrencia and estadoTeste != estadoInicial:
                estadoTeste = k[0]
                estadoInicial = estadoTeste
                ocorrencia = True
            
            if ocorrencia:
                if k[0] == estadoInicial and i == k[1]:
                    if contagem < 1:
                        estadoAtual = k[2]
                        contagem += 1
                        print('estado atual: ' + estadoAtual)
                        print('transicoes: ')
                        print(k)
                        #print('palavra: '+ i)
                    else:
                        estadoTemporario.append(k[2])
                        #print(estadoInicial)
                        sinal = True
            
                if sinal and not entrou and k[0] == estadoInicial:
                    #print('b')
                    #contagem = 0
                    if len(estadoTemporario) < 2:
                        #print(i)
                        if k[0] in estadoTemporario and i == k[1]:
                            estadoTemporario[0] = k[2]
                            #print('b')
                            #contagem = 0
                            entrou = True
                            print('estado temporario:' + estadoTemporario[0])
                    else:
                        #print(estadoTemporario)
                        h = 0
                        while h < len(estadoTemporario): 
                            if k[0] in estadoTemporario[h] and i == k[1]:
                                estadoTemporario[h] = k[2]
                                #print(estadoTemporario[h])
                            h += 1
                        entrou = True
                    
    h = 0   
    while h < len(estadoTemporario):
        #print(estadoTemporario)
        if estadoTemporario[h] in parametrosEstados[2]:
            estadoAtual = estadoTemporario[h]
            #print('entrou')
            #print(estadoAtual)
        h += 1
                   
    if estadoAtual in parametrosEstados[2]:
        print('Palavra Aceita!!!')
    else:
        print('Palavra Rejeitada!!!')
                        

definirSimulacao(entradaDados())

