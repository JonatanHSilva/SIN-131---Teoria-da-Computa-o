#import pynput
import re

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
                    ocorrencia = 0
                    for m in range(qtdTransicoes):
                        ocorrencia += 1
                        transicoes.append([i, j, str(input('Para o estado "{}", qual é a sua transição quando a entrada for "{}"?\n'.format(i, j))), ocorrencia])
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

def num_sort(test_string):
    return list(map(int, re.findall(r'\d+', test_string)))

def ordenado(string):
    teste = string.split(', ')
    teste.sort(key=num_sort)
    concatenacao = ''
    i = 0
    while i < len(teste):
        if concatenacao == '':
            concatenacao = teste[i]
        else:
            concatenacao = concatenacao + ', ' + teste[i]
        i += 1
    
    return concatenacao

def conversao(conjTransicoes, transicoesConvertidas, alfabeto, ultimoAdicionado):
    ultimoAlternativo = ordenado(ultimoAdicionado)
    print(ultimoAlternativo)

    for transicoes in transicoesConvertidas:
        if ultimoAlternativo == transicoes[0]:
            transicoes[2] = ordenado(transicoes[2])
            conjTransicoes.append(transicoes)
            if ultimoAlternativo != transicoes[2]:
                conversao(conjTransicoes, transicoesConvertidas, alfabeto, transicoes[2])
    
    return conjTransicoes

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
    conjEstados = []
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
    #print(transicoesConvertidas)

    for estados in estadosGerados:
        for alfabeto in parametrosEstados[1]:
            for transicoes in transicoesConvertidas:
                for finais in parametrosEstados[2]:
                    if estados == transicoes[2] and transicoes[0] != transicoes[2] and transicoes[1] == alfabeto and finais in estados:
                        conjEstFinais.append(estados)
    #conjEstFinais.append(parametrosEstados[0])
    copia = set(conjEstFinais)
    conjEstFinais = list(copia)
    #print(conjEstFinais)

    for estados in estadosGerados:
        for alfabeto in parametrosEstados[1]:
            for transicoes in transicoesConvertidas:
                if estados == transicoes[2] and transicoes[0] != transicoes[2] and transicoes[1] == alfabeto:
                    conjEstados.append(estados)
    conjEstados.append(parametrosEstados[0])
    copia = set(conjEstados)
    conjEstados = list(copia)

    print(transicoesConvertidas)
    conjTransicoes = []
    for alfabeto in parametrosEstados[1]:
        i = 0
        while i < len(transicoesConvertidas):
            if parametrosEstados[0] == transicoesConvertidas[i][0] and alfabeto == transicoesConvertidas[i][1]:
                conjTransicoes.append(transicoesConvertidas[i])
            i += 1
    
    
    indice = len(conjTransicoes)
    i = 0
    while i < indice: 
        conjTransicoes = conversao(conjTransicoes, transicoesConvertidas, parametrosEstados[1], conjTransicoes[i][2])
        i += 1
   # print(conjTransicoes)

    i = 0
    while i < len(conjTransicoes):
        j = i + 1
        while j < len(conjTransicoes):
            if conjTransicoes[i][0] == conjTransicoes[j][0] and conjTransicoes[i][1] == conjTransicoes[j][1]:
                conjTransicoes.remove(conjTransicoes[j])
                i -= 1
            j += 1
        i += 1
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
    
    
    novoEstado = False
    for j in conjTransicoes:
        if estadoNovo in j[2]:
            novoEstado = True
    
    if novoEstado:
        for alfabeto in parametrosEstados[1]:
            transicoesPont.append([estadoNovo, alfabeto, estadoNovo])
     
    #print(conjTransicoes)
    i = 0
    while i < len(conjEstados):
        for finais in parametrosEstados[2]:
            if finais not in conjEstados[i]:
                conjEstIniciais.append(conjEstados[i])
        i += 1
    estadosSemRepeticao = set(conjEstIniciais)
    conjEstIniciais = list(estadosSemRepeticao)
    #print(conjEstIniciais)
    

    return minimizacao(parametrosEstados, conjTransicoes, conjEstIniciais, conjEstFinais)    
                
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
    
    indices = []
    
    
    indice = 0
    i = 0
    while i < len(estadosIniciais):
        j = i + 1
        while j < len(estadosIniciais):
            if estadosIniciais[i] != estadosIniciais[j]:
                indice += 1
                pares.append([estadosIniciais[i], estadosIniciais[j], False, indice])
            j += 1
        i += 1

    i = 0
    while i < len(estadosFinais):
        j = i + 1
        while j < len(estadosFinais):
            if estadosFinais[i] != estadosFinais[j]:
                indice += 1
                pares.append([estadosFinais[i], estadosFinais[j], False, indice])
            j += 1
        i += 1
        
    #print(pares)

                   
    pares = minimizacaoRecursao(0, -1, pares, conjTransicoes, parametrosEstados[1], 0)

    #print(pares)

    if type(pares) != bool:
        for i in pares:
            for alfabeto in parametrosEstados[1]:
                for transicoes in transicoesCopia:
                    if not i[2]:
                        if transicoes[0] == i[0] and alfabeto == transicoes[1]:
                            #print(transicoes[0] + ', ' + i[0])
                            for t in transicoesCopia:
                                if t[0] == i[1] and alfabeto == t[1]:
                                    transicoesCopia.append([i[0] + ', ' + i[1], alfabeto, transicoes[2] + ', ' + t[2]])
                                    transicoesCopia.remove(t)
                                    #if transicoes != None:
                                    transicoesCopia.remove(transicoes)

    #print(transicoesCopia)
    for transicoes in transicoesCopia:
        entradaSRepeticao = ''
        saidaSRepeticao = ''
        entrada = transicoes[0].split(', ')
        saida = transicoes[2].split(', ')
        i = 0
        while i < len(entrada):
            j = i + 1
            removeu = False
            while j < len(entrada):
                if entrada[i] == entrada[j]:
                    entrada.remove(entrada[j])
                    removeu = True
                j += 1
            if not removeu:
                i += 1
        
        i = 0
        while i < len(entrada):
            if entradaSRepeticao == '':
                entradaSRepeticao = entrada[i]
            else:
                entradaSRepeticao = entradaSRepeticao + ', ' + entrada[i]
            i += 1
        #print(entradaSRepeticao)
        transicoes[0] = entradaSRepeticao

        
        i = 0
        while i < len(saida):
            removeu = False
            j = i + 1
            #print(saida[i])
            while j < len(saida):
                
                if saida[i] == saida[j]:
                    saida.remove(saida[j])
                    removeu = True
                #elif saida[i] == saida[j] and i == 0:
                    #saida.remove(saida[i])
                j += 1
            if not removeu:
                i += 1
      
        i = 0
        while i < len(saida):
            if saidaSRepeticao == '':
                saidaSRepeticao = saida[i]
            else:
                saidaSRepeticao = saidaSRepeticao + ', ' + saida[i]
            i += 1
        #print(saidaSRepeticao)
        transicoes[2] = saidaSRepeticao
    #print(transicoesCopia)

    for alfabeto in parametrosEstados[1]:
        for transicoes in transicoesCopia:
            achou = False
            for t in transicoesCopia:
                if transicoes[2] == t[0]:
                    achou = True
            
            if not achou:
                transicoes[2] = transicoes[0]

    
    estadoFinal = ''
    for transicoes in transicoesCopia:
        for finais in parametrosEstados[2]:
            if finais in transicoes[0]:
                estadoFinal = transicoes[0]
    
    estadosGerados = []
    for alfabeto in parametrosEstados[1]:
        for transicoes in transicoesCopia:
            if alfabeto == transicoes[1]:
                estadosGerados.append(transicoes[0])
    estadosCopia = set(estadosGerados)
    estadosGerados = list(estadosCopia)

    ambiguidade = []
    for estados in estadosGerados:
        for alfabeto in parametrosEstados[1]:
            ambiguidade.append([estados, alfabeto, 0])
    
    #print(estadosGerados)
    #print(estadoFinal)
    #print(transicoesCopia)
    
    return parametrosEstados[0], parametrosEstados[1], estadoFinal, estadosGerados, transicoesCopia, len(estadosGerados), ambiguidade
    


def minimizacaoRecursao(index, prevIndex, peer, transitions, simbolos, contagem):
    indice = index
    pares = peer
    indiceAnterior = prevIndex
    transicoes = transitions
    resultado = []
    achou = False

    for alfabeto in simbolos:
        for estados in transicoes:
           for t in transicoes:
                if estados[0] == pares[indice][0] and t[0] == pares[indice][1] and estados[1] == alfabeto and t[1] == alfabeto:
                    resultado.append([estados[2], t[2]])
                    break

    #print(pares[indice])
    #print(resultado)
    #print(pares[indice])

    for par in pares:
        for r in resultado:
            if (r[0] == par[0] and r[1] == par[1]) or (r[0] == par[1] and r[1] == par[0]):
                achou = True
                indiceAnterior = indice
                indice = par[3] - 1
                #print(indice)
                break
            #print(par)
            #print(r)
  
    #print(resultado)
    #print(len(resultado))
    #print(contagem)
    #print(indice)
    #print(achou)
    if achou and contagem == 0:
        pares[indice][2] = minimizacaoRecursao(indice, indiceAnterior, pares, transicoes, simbolos, contagem + 1)
        return pares
    elif achou and contagem < len(resultado) and contagem != 0:
        pares[indice][2] = minimizacaoRecursao(indice, indiceAnterior, pares, transicoes, simbolos, contagem + 1)
        return pares[indice][2]
    elif achou and contagem == len(resultado) or indice == indiceAnterior:
        return True
    elif not achou and contagem == 0:
        pares[indice][2] = minimizacaoRecursao(indice + 1, indiceAnterior, pares, transicoes, simbolos, contagem + 1)
        return pares
    elif not achou and contagem != 0:
        return True

    

parametros = entradaDados()
parametrosMinimizados = conversaoAFN(parametros)
#while True:
simulacao(parametros)
simulacao(parametrosMinimizados)



