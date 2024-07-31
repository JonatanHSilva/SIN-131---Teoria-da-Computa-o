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
            ambiguidade = []
            for i in estadosGerados:
                for j in alfabeto:
                    qtdTransicoes = int(input(f'Quantas transições existem quando o estado é "{i}" e a entrada for "{j}"?\n'))
                    for m in range(qtdTransicoes):
                        transicoes.append([i, j, str(input('Para o estado "{}", qual é a sua transição quando a entrada for "{}"?\n'.format(i, j)))])
                    ambiguidade.append([i, j, qtdTransicoes - 1])
                    #print(transicoes)
            estadoInicial = str(input(f'Dentre {estadosGerados}, qual estado seria o inicial? '))
            estadoFinal = str(input(f'Dentre os estados {estadosGerados}, qual(is) seria(m) o(s) estado(s) de aceitação? ')).split(', ')
            print('Automato Salvo!!!')
            return estadoInicial, alfabeto, estadoFinal, estadosGerados, transicoes, estados, ambiguidade
        except ValueError:
            print('Entrada inválida, digite apenas números.\n')
   

#Simulação de aceitação de palavras
def simulacao(parametrosEstados):
    palavra = str(input('Digite a palavra:'))
    estadoAtual = parametrosEstados[0]
    estadoTemporario = []
    estadoTeste = []
   
    sinal = False
    for i in palavra:
        for j in parametrosEstados[1]:
            if i == j:
                break
        else:
            print('Palavra rejeitada, pois ela não faz parte do alfabeto')
        tamanho = 0
        while tamanho < len(estadoTemporario):
            estadoTemporario[tamanho][3] = False
            tamanho += 1
        ocorrencia = False
        proximaPalavra = False
        ambiguidades = 0
        entrou = False
        contagem = 0
        entrada = 0
        for k in parametrosEstados[4]:
            for ambiguidade in parametrosEstados[6]:
                if not ocorrencia:
                    if k[0] == ambiguidade[0] and i == ambiguidade[1] and i == k[1]:
                        ambiguidades = ambiguidade[2]
            if k[0] == estadoAtual and i == k[1]:
                if not ocorrencia and ambiguidades == 0:
                    estadoAtual = k[2]
                    ocorrencia = True
                elif ambiguidades >= 1:
                    if len(estadoTemporario) < ambiguidades + 1:
                        if contagem  < ambiguidades + 1:
                            estadoTemporario.append([k[0], k[3], k[2], True])
                            contagem += 1
                    else:
                        if estadoTemporario[len(estadoTemporario) - 1][0] != k[0]:
                            if contagem < ambiguidades + 1:
                                estadoTemporario.append([k[0], k[3], k[2], True]) 
                                print(contagem)
                                contagem += 1
                    sinal = True
                    
                
            
            if sinal and not entrou:
                if len(estadoTemporario) < 2:
                    if k[0] == estadoTemporario[0][2] and i == k[1] and not estadoTemporario[0][3]:
                        if k[0] != estadoTemporario[0][0]:
                            estadoTemporario[0][2] = k[2]
                        else:
                            if estadoTemporario[0][1] == k[3]:
                                estadoTemporario[0][2] = k[2]
                        entrou = True
                else:
                    h = 0
                    while h < len(estadoTemporario): 
                        if k[0] == estadoTemporario[h][2] and i == k[1] and not estadoTemporario[h][3]:
                            if k[0] != estadoTemporario[h][0]:
                                estadoTemporario[h][2] = k[2]
                                entrada += 1
                            else:
                                if ambiguidades > 0:
                                    if estadoTemporario[h][1] == k[3]:
                                        estadoTemporario[h][2] = k[2]
                                        entrada += 1
                                else:
                                    estadoTemporario[h][2] = k[2]
                                    entrada += 1
                        h += 1
                    if entrada == len(estadoTemporario):
                        entrou = True
    h = 0   
    while h < len(estadoTemporario):
        for finais in parametrosEstados[2]:
            if estadoTemporario[h][2] == finais and estadoAtual != finais:
                estadoAtual = estadoTemporario[h][2]
        h += 1
                   
    if estadoAtual in parametrosEstados[2]:
        print('Palavra Aceita!!!')
    else:
        print('Palavra Rejeitada!!!')
                

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
    
    for estados in estadosGerados:
        for alfabeto in parametrosEstados[1]:
            for transicoes in transicoesConvertidas:
                if estados == transicoes[2] and transicoes[0] != transicoes[2] and transicoes[1] == alfabeto:
                    conjEstFinais.append(estados)
    conjEstFinais.append(parametrosEstados[0])
    copia = set(conjEstFinais)
    conjEstFinais = list(copia)

    conjTransicoes = []
    for finais in conjEstFinais:
        for transicoes in transicoesConvertidas:
            if finais == transicoes[0]:
                conjTransicoes.append(transicoes)
    
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
    

    minimizacao(parametrosEstados, conjTransicoes, conjEstIniciais, conjEstFinais)    
                
'''def minimizacao(parametrosEstados, transicoesModificados, estadoModificados, estadoFinalModificado):
    transicoesT = transicoesModificados.copy()
    transicoesMinInicial = []
    transicoesMinFinal = []
    transicoesEliminar = transicoesT
    transicoesCopia = transicoesT.copy()
    j = 0
    i = 0
    

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
        aceitacao()'''

def minimizacao(parametrosEstados, conjTransicoes, conjEstIniciais, conjEstFinais):
    estadosIniciais = conjEstIniciais
    estadosFinais = conjEstFinais
    pares = []
    transicoesCopia = conjTransicoes
    
    resultante = []
    indices = []
    
    
    indice = 0
    for iniciais in estadosIniciais:
        for estados in estadosIniciais:
            if estados != iniciais:
                indice += 1
                pares.append(iniciais, estados, False, indice)

    indice = 0
    for finais in estadosFinais:
        for estados in estadosFinais:
            if estados != finais:
                indice += 1
                pares.append(finais, estados, False, indice)

    resultado = ''
    for par in pares:
        for alfabeto in alfabeto:
            for transicoes in conjTransicoes:
                if transicoes[0] == par[0] and transicoes[1] == alfabeto:
                    if resultado == '':
                        resultado = transicoes[2]
                    else:
                        resultado = resultado + ', ' + transicoes[2]
                elif transicoes[0] == par[1] and transicoes[1] == alfabeto:
                    if resultado == '':
                        resultado = transicoes[2]
                    else:
                        resultado = resultado + ', ' + transicoes[2]
        resultante.append(resultado, False, par[3])

    contagem = 0
    for inicial in resultante:
        teste = inicial[0].split(', ')
        for par in pares:
            if (par[0] == teste[0] and par[1] == teste[1]) or (par[0] == teste[1] and par[1] == teste[0]):
                contagem += 1

        if contagem != inicial[2]:
            indices.append(inicial[2])
    
    for i in indices:
        for resultado in resultante:
            if i == resultado[2]:
                resultado[1] = True


    for inicial in resultante:
        teste = inicial[0].split(', ')
        for par in pares:
            if inicial[1]:
                if par[3] == inicial[2]:
                    par[2] = True
                   
    pares = minimizacaoRecursao(0, pares, conjTransicoes, parametrosEstados[1])

    for i in pares:
        for alfabeto in alfabeto:
            for transicoes in transicoesCopia:
                if not i[2]:
                    if transicoes[0] == i[0] and alfabeto == transicoes[1]:
                        for t in parametrosEstados:
                            if t[0] == i[1] and alfabeto == t[1]:
                                transicoesCopia.append([i[0] + ', ' + i[1], alfabeto, transicoes[2] + ', ' + t[2]])
                                transicoesCopia.remove(t)
                                transicoesCopia.remove(transicoes)
    
    


def minimizacaoRecursao(index, peer, transitions, simbolos):
    indice = index
    pares = peer
    transicoes = transitions
    resultado = ''
    achou = False

    for alfabeto in simbolos:
        for transicoes in transicoes:
            if transicoes[0] == pares[indice][0] and transicoes[1] == alfabeto:
                if resultado == '':
                    resultado = transicoes[2]
                else:
                    resultado = resultado + ', ' + transicoes[2]
            elif transicoes[0] == pares[indice][1] and transicoes[1] == alfabeto:
                if resultado == '':
                    resultado = transicoes[2]
                else:
                    resultado = resultado + ', ' + transicoes[2]

    resultante = resultado.split(', ')

    for par in pares:
        if (resultante[0] == par[0] and resultante[1] == par[1]) or (resultante[0] == par[1] and resultante[1] == par[0]):
            achou = True
            indice = par[3]
    
    if achou and indice != 0:
        pares[indice][2] = minimizacaoRecursao(indice, pares, transicoes, simbolos)
        return pares[indice][2]
    elif achou and indice == 0:
        pares[indice][2] = minimizacaoRecursao(indice, pares, transicoes, simbolos)
        return pares
    elif not achou:
        return True
        

    

parametros = entradaDados()
while True:
    simulacao(parametros)
#conversaoAFN(parametros)



