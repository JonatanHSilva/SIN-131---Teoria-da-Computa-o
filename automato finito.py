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
            conversoesInicial = ''
            conversoesFinal = ''
            teste = transicoesExistentes[i].split(', ')
            j = 0
            contagem = 0
            while j < len(teste):
                for transicoes in parametrosEstados[4]:
                    if teste[j] == transicoes[0] and alfabeto == transicoes[1] and contagem == 0:
                        conversoesInicial = transicoes[0]
                        conversoesFinal = transicoes[2]
                        contagem += 1
                    elif teste[j] == transicoes[0] and alfabeto == transicoes[1] and contagem != 0:
                        
                        if teste[j] not in conversoesInicial:
                            conversoesInicial = conversoesInicial + ', ' + transicoes[0]
                            #print('inicial:' + conversoesInicial)

                            if transicoes[2] not in conversoesFinal:
                                conversoesFinal = conversoesFinal + ', ' + transicoes[2]
                            else:
                                conversoesFinal = transicoes[2]
                        else:
                            conversoesInicial = transicoes[0]
                            if transicoes[2] not in conversoesFinal:
                                conversoesFinal = conversoesFinal + ', ' + transicoes[2]
                            else:
                                conversoesFinal = transicoes[2]
                j += 1
            i += 1
            transicoesConvertidas.append([conversoesInicial, alfabeto, conversoesFinal])
    #print(transicoesConvertidas)

    transicoesCopia = transicoesConvertidas.copy()
    transicoesModTempo = []
    transicoesModificados = []

    for alfabeto in parametrosEstados[1]:
        for i in transicoesCopia:
            if i[1] == alfabeto and i[0] == parametrosEstados[0]:
                transicoesModTempo.append(i)
            #print(i)
            for j in transicoesConvertidas:
                if i[2] == j[0] and i[1] == alfabeto and j[1] == alfabeto:
                    transicoesModTempo.append(j)
    #print(transicoesModTempo)
    
    for alfabeto in parametrosEstados[1]:
        indice = 0
        for temporario in transicoesModTempo:
            if indice == 0 and temporario[1] == alfabeto:
                transicoesModificados.append(temporario)
                #print(transicoesModificados)
                indice += 1
            i = 0
            adicionou = False
            while i < len(transicoesModificados):
                if temporario[0] not in transicoesModificados[i][0] and transicoesModificados[i][1] == alfabeto and temporario[1] == alfabeto:
                    adicionou = True
                elif temporario[0] in transicoesModificados[i][0] and transicoesModificados[i][1] == alfabeto and temporario[1] == alfabeto:
                    adicionou = False
                #print(temporario[0])
                #print(transicoesModificados[i])
                #print(i)
                i += 1
                
            if adicionou:
                transicoesModificados.append(temporario)
    #print(transicoesModificados)
    
    estadosFinaisModificados = []
    i = 0
    while i < len(transicoesModificados):
        for finais in parametrosEstados[2]:
            if finais in transicoesModificados[i][0]:
                estadosFinaisModificados.append(transicoesModificados[i][2])
            #print(transicoesModificados[i])
        i += 1

    i = 0 

    estadoModificados = []
    
    while i < len(transicoesModificados):
        estadoModificados.append(transicoesModificados[i][0])
        i += 1
    estadosSemRepeticao = set(estadoModificados)
    estadoModificados = list(estadosSemRepeticao)
    #print(estadosSemRepeticao)
    

    minimizacao(parametrosEstados, transicoesModificados, estadoModificados, estadosFinaisModificados)
        
    #print(transicoesModificados)
    #print(indices)
    #return transicoesModificados, indices        
                
def minimizacao(parametrosEstados, transicoesModificados, estadoModificados, estadoFinalModificado):
    transicoesT = transicoesModificados.copy()
    transicoesMinInicial = []
    transicoesMinFinal = []
    transicoesEliminar = transicoesT
    j = 0
    i = 0
    #print(transicoesT)
    while j < len(transicoesT):
        i = j + 1
        while i < len(transicoesT):
            for final in estadoFinalModificado:
                if final in transicoesT[i][0] and final in transicoesT[j][0] or final not in transicoesT[i][0] and final not in transicoesT[j][0]:
                    if final in transicoesT[i][2] and final in transicoesT[j][2] or final not in transicoesT[i][2] and final not in transicoesT[j][2]:
                        if transicoesT[i][1] == transicoesT[j][1]:
                            transicoesMinInicial.append([transicoesT[i][0], transicoesT[j][0]])
                            transicoesMinFinal.append([transicoesT[i][2], transicoesT[j][2]])
            i += 1
        j += 1
    
    j = 0
    i = 0
    
    while i < len(transicoesMinInicial):
        while j < len(transicoesMinFinal):
            k = 0
            for l in transicoesMinFinal:
                while k < len(l):
                    testeFinal = l[k]
                    #print(l[0])
                    k += 1
                o = 0
                for m in transicoesMinInicial:
                    while o < len(m):
                        testeInicial = m[o]
                        if testeInicial == testeFinal:
                            for t in transicoesT:
                                if t[0] == testeInicial:
                                    transicoesEliminar.remove(t)
                        o += 1
                        
            j += 1
        i += 1
    
    #print(transicoesMinInicial)
    #print(transicoesMinFinal)
    #print(transicoesEliminar)                  
    
    estadoNovo = 'F'
    indiceTransicoes = 0
    #
    #transicoesNulas = []
    #teste = parametrosEstados[1]
    i = 0
    achou = 0
    diferente = 0
    simbolo = ''
    while i < len(estadoModificados):
        for alfabeto in parametrosEstados[1]:
            for j in transicoesModificados:
                if estadoModificados[i] == j[0] and alfabeto == j[1]:
                    achou += 1
                    simbolo = alfabeto
        #print('estado: '+estadoModificados[i])
        #print('simbolo: '+ simbolo)
        if achou < len(parametrosEstados[1]):
            for alfabeto in parametrosEstados[1]:
                for j in transicoesModificados:
                    #print('alfabeto: '+ alfabeto)
                    #print(j[0])
                    #print(j[1])
                    if estadoModificados[i] == j[0] and alfabeto != simbolo and j[1] != alfabeto:
                        transicoesModificados.append([j[0], alfabeto, estadoNovo])
                        #print('entrou')
        
        i += 1
        achou = 0
    #print(transicoesModificados)
    for alfabeto in parametrosEstados[1]:
       transicoesModificados.append([estadoNovo, alfabeto, estadoNovo])
    estadoModificados.append(estadoNovo)

conversaoAFN(entradaDados())



