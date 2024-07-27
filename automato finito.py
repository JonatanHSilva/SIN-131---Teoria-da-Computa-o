#import pynput

#Entrada de dados do Automato
def entradaDados():
    while ValueError:
        try:
            estados = int(input('Digite quantos estados possui o automato:\n'))
            for i in range (estados):
                if i == 0:
                    estadosGerados = "q{}".format(i)
                else:
                    estadosGerados += ",q{}".format(i)
            estadosGerados = estadosGerados.split(',')
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
        except ValueError:
            print('Entrada inválida, digite apenas números.\n')
    
    #print(estadosGerados)
   


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


'''def conversao(parametrosEstados, transicoesConversao, estadosGerados):
    atualizarIndice = 0
    vezes = (2 ** len(estadosGerados)) - 1
    #print(vezes)
    i = 0
    k = 0
    j = 0

    while i < vezes:
        teste = transicoesConversao[atualizarIndice].split(', ')
        print(teste)
        ultimoIndiceTeste = len(teste) - 1
        j = 0
        indiceEstado = 0
        while j < len(estadosGerados):
            if estadosGerados[j] == teste[ultimoIndiceTeste]:
                indiceEstado = j
            #print(estadosGerados[j]) 
            j += 1
            #print(teste[ultimoIndiceTeste])
            #print(ultimo)
            #print(achou)
        k = indiceEstado + 1
        while k < len(estadosGerados):
            transicoesConversao.append(transicoesConversao[atualizarIndice] + ', ' + estadosGerados[k])
            k += 1
            #print(achou)
        i += 1
        
        if atualizarIndice != len(transicoesConversao) - 1:
            atualizarIndice += 1
        #print(transicoesConversao)
        #print(atualizarIndice)'''
    
def conversaoAFN(parametrosEstados):
    transicoesExistentes = parametrosEstados[3].copy()
    transicoesConvertidas = []
    estadosGerados = parametrosEstados[3].copy()
    
    atualizarIndice = 0
    vezes = (2 ** len(estadosGerados)) - 1
    i = 0
    k = 0
    j = 0

    while i < vezes:
        teste = transicoesExistentes[atualizarIndice].split(', ')
        #print(teste)
        ultimoIndiceTeste = len(teste) - 1
        j = 0
        indiceEstado = 0
        while j < len(estadosGerados):
            if estadosGerados[j] == teste[ultimoIndiceTeste]:
                indiceEstado = j
            j += 1
        k = indiceEstado + 1
        while k < len(estadosGerados):
            transicoesExistentes.append(transicoesExistentes[atualizarIndice] + ', ' + estadosGerados[k])
            k += 1
        i += 1
        
        if atualizarIndice != len(transicoesExistentes) - 1:
            atualizarIndice += 1

    for alfabeto in parametrosEstados[1]:
        i = 0
        while i < len(transicoesExistentes):
            conversoesInicial = []
            conversoesFinal = []
            teste = transicoesExistentes[i].split(', ')
            #print(teste)
            j = 0
            while j < len(teste):
                contagem = 0
                for transicoes in parametrosEstados[4]:
                    if teste[j] == transicoes[0] and alfabeto == transicoes[1] and contagem == 0:
                        conversoesInicial.append(transicoes[0])
                        conversoesFinal.append(transicoes[2])
                        contagem += 1
                    elif teste[j] == transicoes[0] and alfabeto == transicoes[1] and contagem != 0:
                        if teste[j] not in transicoes[0]:
                            conversoesInicial[0] = conversoesInicial[0] + ', ' + transicoes[0]
                            if transicoes[2] not in conversoesFinal:
                                conversoesFinal[0] = conversoesFinal[0] + ', ' + transicoes[2]
                            else:
                                conversoesFinal[0] = transicoes[2]
                        else:
                            conversoesInicial[0] = transicoes[0]
                            if transicoes[2] not in conversoesFinal:
                                conversoesFinal[0] = conversoesFinal[0] + ', ' + transicoes[2]
                            else:
                                conversoesFinal[0] = transicoes[2]
                finalNaoDupla = set(conversoesFinal)
                conversoesFinal = list(finalNaoDupla)  
                j += 1
            #print(conversoesFinal)   
            i += 1
            transicoesConvertidas.append([conversoesInicial, alfabeto, conversoesFinal])
    #print(transicoesConvertidas)
        


conversaoAFN(entradaDados())



