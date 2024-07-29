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
   

'''def simulacaoAFN(parametrosEstados):
    caminhoAceitacao = []
    for alfabeto in parametrosEstados[1]:
        contagem = 0
        for transicoes in parametrosEstados[4]:
            if transicoes[0] == parametrosEstados[0]:
                caminhoAceitacao.append(transicoes)
                contagem += 1
            elif transicoes[2] '''
                

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

    
def conversaoAFN(parametrosEstados):
    estadosGerados = parametrosEstados[3].copy()
    transicoesConvertidas = []
    estados = parametrosEstados[3].copy()
    
    atualizarIndice = 0
    vezes = (2 ** len(estadosGerados)) - 1
    i = 0
    k = 0
    j = 0

    while i < vezes:
        teste = estadosGerados[atualizarIndice].split(', ')
        #print(teste)
        ultimoIndiceTeste = len(teste) - 1
        j = 0
        indiceEstado = 0
        while j < len(estados):
            if estados[j] == teste[ultimoIndiceTeste]:
                indiceEstado = j
            j += 1
        k = indiceEstado + 1
        while k < len(estados):
            estadosGerados.append(estadosGerados[atualizarIndice] + ', ' + estados[k])
            k += 1
        i += 1
        
        if atualizarIndice != len(estadosGerados) - 1:
            atualizarIndice += 1
    #print(transicoesExistentes)
    conjEstIniciais = []
    conjEstFinais = []
    for alfabeto in parametrosEstados[1]:
        i = 0
        while i < len(estadosGerados):
            conversoesInicial = ''
            conversoesFinal = ''
            teste = estadosGerados[i].split(', ')
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
    
    for estados in estadosGerados:
        for alfabeto in parametrosEstados[1]:
            for transicoes in transicoesConvertidas:
                if estados == transicoes[2] and transicoes[0] != transicoes[2] and transicoes[1] == alfabeto:
                    conjEstFinais.append(estados)
    conjEstFinais.append(parametrosEstados[0])
    copia = set(conjEstFinais)
    conjEstFinais = list(copia)
    #print(conjEstFinais)

    conjTransicoes = []
    for finais in conjEstFinais:
        for transicoes in transicoesConvertidas:
            if finais == transicoes[0]:
                conjTransicoes.append(transicoes)
    #print(conjTransicoes)
    
    estadoNovo = 'F'
    transicoesPont = conjTransicoes
    
    for transicoes in conjTransicoes:
        destino = transicoes[2].split(', ')
        resultado = ''
        indice = 0
        for d in destino:
            if d == '':
                d = estadoNovo
            if indice == 0:
                resultado = d
            else:
                resultado = resultado + ', ' + d
            indice += 1
        transicoes[2] = resultado
    print(conjTransicoes)
    
    novoEstado = False
    for j in conjTransicoes:
        if estadoNovo in j[2]:
            novoEstado = True
    
    if novoEstado:
        for alfabeto in parametrosEstados[1]:
            transicoesPont.append([estadoNovo, alfabeto, estadoNovo])
     
     
    i = 0
    while i < len(conjTransicoes):
        conjEstIniciais.append(conjTransicoes[i][0])
        i += 1
    estadosSemRepeticao = set(conjEstIniciais)
    conjEstIniciais = list(estadosSemRepeticao)
    #print(conjEstIniciais)
    #print(estadosSemRepeticao)
    

    minimizacao(parametrosEstados, conjTransicoes, conjEstIniciais, conjEstFinais)
        
    #print(transicoesModificados)
    #print(indices)
    #return transicoesModificados, indices        
                
def minimizacao(parametrosEstados, transicoesModificados, estadoModificados, estadoFinalModificado):
    transicoesT = transicoesModificados.copy()
    transicoesMinInicial = []
    transicoesMinFinal = []
    transicoesEliminar = transicoesT
    transicoesCopia = transicoesT.copy()
    j = 0
    i = 0
    #print(transicoesT)
    #print(estadoFinalModificado)
    #print(transicoesCopia)
    

    while j < len(transicoesT):
        i = j + 1
        while i < len(transicoesT):
            for final in parametrosEstados[2]:
                if final in transicoesT[i][0] and final in transicoesT[j][0] or final not in transicoesT[i][0] and final not in transicoesT[j][0]:
                    if final in transicoesT[i][2] and final in transicoesT[j][2] or final not in transicoesT[i][2] and final not in transicoesT[j][2]:
                        if transicoesT[i][1] == transicoesT[j][1]:
                            transicoesMinInicial.append([transicoesT[i][0], transicoesT[j][0]])
                            transicoesMinFinal.append([transicoesT[i][2], transicoesT[j][2]])
                            break
            i += 1
        j += 1

    j = 0
    i = 0
    
    while i < len(transicoesMinInicial):
        while j < len(transicoesMinFinal):
            
            for l in transicoesMinFinal:
                k = 0
                while k < len(l):
                    testeFinal = l[k]
                    #print(l[0])
                    k += 1
                
                for m in transicoesMinInicial:
                    o = 0
                    while o < len(m):
                        testeInicial = m[o]
                        if testeInicial == testeFinal:
                            #print(testeInicial)
                            #print(testeFinal)
                            for t in transicoesT:
                                for alfabeto in parametrosEstados[1]:
                                    if t[0] == testeInicial and t[0] != parametrosEstados[0] and t[2] == testeFinal and t[1] != alfabeto:
                                        #print(testeInicial)
                                        #print(t)
                                        transicoesEliminar.remove(t)
                                        
                        o += 1
                        
            j += 1
        i += 1
    
    #print(transicoesMinInicial)
   # print(transicoesMinFinal)
    #print(transicoesEliminar)

    

    #
    
    
    #print(transicoesEliminar)
    
    #
    #transicoesNulas = []
    #teste = parametrosEstados[1]
    
                        #print('entrou')
        
      
    
    #for alfabeto in parametrosEstados[1]:
       #transicoesEliminar.append([estadoNovo, alfabeto, estadoNovo])
    #print(transicoesEliminar)
    

conversaoAFN(entradaDados())



