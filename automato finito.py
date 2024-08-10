#import pynput
import re

#Entrada de dados do Automato
def entradaDados():
    while ValueError:
        try:    #tratamento de exceção para entrada inválida
            estados = int(input('Digite quantos estados possui o automato:\n')) #entrada e armazenamento com a quantidade de estados do AFN ou AFD
            for i in range (estados):   #geração dos estados conforme a entrada da quantidade
                if i == 0:
                    estadosGerados = "q{}".format(i)
                else:
                    estadosGerados += ",q{}".format(i)
            estadosGerados = estadosGerados.split(',')  #dividindo os estados que foram gerados
            alfabeto = str(input('Digite o alfabeto:\n')).split(', ')   #entrada e armazenamento dos simbolos que compõem o alfabeto
            transicoes = []
            ambiguidade = []
            for i in estadosGerados:    #geração das funções de transição conforme o simbolo
                for j in alfabeto:
                    qtdTransicoes = int(input(f'Quantas transições existem quando o estado é "{i}" e a entrada for "{j}"?\n'))  #entrada de quantidade de estados resultantes para uma função de transição
                    ocorrencia = 0
                    for m in range(qtdTransicoes):
                        ocorrencia += 1 #indicador de ocorrencia de estados resultantes, ou seja, indica se há um estado que há mais de um resultante 
                        transicoes.append([i, j, str(input('Para o estado "{}", qual é a sua transição quando a entrada for "{}"?\n'.format(i, j))), ocorrencia])   #entrada de dados do estado resultante da função de transição e armazenamento das funções com o estado de ativação de função, o simbolo correspondente, o estado resultante e o indice de ocorrencia deste estado resultante para o estado de ativação definindo "caminhos" para seguir
                    ambiguidade.append([i, j, qtdTransicoes - 1]) #armazenamento das informações dos estados, sinalizando se há ou não, mais de um resultante e o simbolo na qual ocorre
                    #print(transicoes)
            estadoInicial = str(input(f'Dentre {estadosGerados}, qual estado seria o inicial? ')) #entrada e armazenamento do estado inicial
            estadoFinal = str(input(f'Dentre os estados {estadosGerados}, qual(is) seria(m) o(s) estado(s) de aceitação? ')).split(', ')    #entrada e armazenamento do(s) estado(s) final(is)
            print('Automato Salvo!!!')
            return estadoInicial, alfabeto, estadoFinal, estadosGerados, transicoes, estados, ambiguidade #retorno com as informações do automato para simulação, conversão, minimização, etc.
        except ValueError:
            print('Entrada inválida, digite apenas números.\n')
   

#Simulação de aceitação de palavras
def simulacao(parametrosEstados): #apenas um parametro para acessar as variáveis que retornaram, pois elas estão em formato de tuplas
    palavra = str(input('Digite a palavra:'))   #entrada com a palavra para teste de aceitação
    estadoAtual = parametrosEstados[0]  #a variável armazena o estado inicial conforme a posição que corresponde ao estado inicial para fazer o movimento entre estados
    estadoTemporario = []
    estadoTeste = []
   
    sinal = False #variável para sinalizar se existe uma ambiguidade que é presente nos AFNs
    for i in palavra: #loop para passar por cada simbolo da palavra que será testada
        for j in parametrosEstados[1]: #loop para verificar se existe um simbolo na palavra que não faz parte do alfabeto
            if i == j:
                break
        else:   #condição para que caso haja algum simbolo que não faça parte do alfabeto, não fazendo a leitura dos simbolos
            print('Palavra rejeitada, pois ela não faz parte do alfabeto')
            break
        
        tamanho = 0
        while tamanho < len(estadoTemporario): #loop para que quando houver alguma ambiguidade de estados resultantes poder retirar a sinalização de estado que foi adicionado recente
            estadoTemporario[tamanho][3] = False #"variável" dentro da lista de estados que houveram ambiguidades para marcar que o estado não foi adicionado recentemente
            tamanho += 1
        ocorrencia = False #variável que delimita se houve modificação no estado atual para AFD
        ambiguidades = 0
        entrou = False #variável que delimita se foi feita alguma modificação na lista de estados que houveram ambiguidade
        contagem = 0 #variável que servirá para delimitar o armazenamento do resultante do estado que há ambiguidade
        entrada = 0 #variável que servirá para verificar se houve modificações para todos os estados que depararam com alguma ambiguidade e que foram armazenadas
        for k in parametrosEstados[4]:  #loop que passará por todas as funções de transição para achar o que corresponde ao simbolo atual e ao(s) estado(s) atual(is) que se encontra(m)
            for ambiguidade in parametrosEstados[6]:    #loop que passa por todos estados que foram armazenados baseando-se no estado atual da função de transição e retornando a quantidade de ambiguidade (0 ou mais)
                if not ocorrencia: #verifica se continua sem modificação no estado atual
                    if k[0] == ambiguidade[0] and i == ambiguidade[1] and i == k[1]: #verifica se o estado de ativação da função possui ambiguidade e se também tanto o simbolo do estado de ativação quanto o simbolo que foi armazenado junto com as outras informações do estado são compatíveis com o simbolo que está sendo lido
                        ambiguidades = ambiguidade[2] #se compatível, armazena quantas ambiguidades o estado possui (0 ou mais)
            if k[0] == estadoAtual and i == k[1]: #verifica se o estado de ativação é o estado atual de leitura e se o simbolo do estado de ativação é compatível com o simbolo de leitura atual
                if not ocorrencia and ambiguidades == 0: #verifica se não houve a modificação para o estado atual e se não há ambiguidades para o estado "atual"
                    estadoAtual = k[2] #k[0] é o estado de ativação, k[1] é o símbolo, k[2] é o estado resultante e k[3] é a ocorrência para casos de haver ambiguidade
                    ocorrencia = True
                elif ambiguidades >= 1: #se há mais de uma ambiguidade para o estado atual e ativa os estados atuais "paralelos"
                    if len(estadoTemporario) < ambiguidades + 1: #verifica se ainda não adicionou todos os estados na qual houve a "ambiguidade"
                        if contagem < ambiguidades + 1: #verifica se ainda pode armazenar mais uma função de transição ambígua 
                            estadoTemporario.append([k[0], k[3], k[2], True]) #armazenamento de uma parte da "maquina" com um dos estados que possuem ambiguidade com apenas o estado de ativação que houve ambiguidade, o indice de ocorrencia, o estado resultante e a variável que determina se ele foi armazenado recentemente, sendo 'True' como que armazenou recentemente
                            contagem += 1 #contagem de armazenamento de estados
                    else: 
                        if estadoTemporario[len(estadoTemporario) - 1][0] != k[0]: #se adicionou todos os estados que houveram ambiguidade, verifica se o estado que houve ambiguidade já não foi armazenado 
                            if contagem < ambiguidades + 1: 
                                estadoTemporario.append([k[0], k[3], k[2], True]) 
                                #print(contagem)
                                contagem += 1
                    sinal = True
                    
                
            
            if sinal and not entrou: #por meio da variável "sinal" é liberado (ou não) as modificações no estados ambiguos e a variável "entrou" é para a modificação feita nos estados ambíguos
                if len(estadoTemporario) < 2:   #se existe apenas um estado que seja ambíguo, apenas sua modificação será feita
                    if k[0] == estadoTemporario[0][2] and i == k[1] and not estadoTemporario[0][3]: #verifica se o estado resultante é o mesmo do estado de ativação da função e o simbolo corresponde ao simbolo atual da palavra e também se o estado não foi adicionado recentemente
                        if k[0] != estadoTemporario[0][0]: #verifica se o estado de ativação não é o estado que houve a ambiguidade
                            estadoTemporario[0][2] = k[2]
                        else:
                            if estadoTemporario[0][1] == k[3]: #se não for o estado que houve ambiguidade, verifica se o indice de ocorrência é compatível para seguir pelo "caminho" que foi definido 
                                estadoTemporario[0][2] = k[2]
                        entrou = True #modificação feita
                else:
                    h = 0
                    while h < len(estadoTemporario): #se existir mais de um estado ambiguo armazenado, passará por todos os estados armazenados
                        if k[0] == estadoTemporario[h][2] and i == k[1] and not estadoTemporario[h][3]: #verificando se o é o mesmo estado resultante com o estado de ativação da função atual
                            if k[0] != estadoTemporario[h][0]:
                                estadoTemporario[h][2] = k[2]
                                entrada += 1 #uma das modificações foram feitas
                            else:
                                if ambiguidades > 0: #verifica se o estado de ativação da função atual possui ambiguidades, tendo que escolher o caminho definido, caso haja ambiguidades, ou apenas continuar seguindo.
                                    if estadoTemporario[h][1] == k[3]:
                                        estadoTemporario[h][2] = k[2]
                                        entrada += 1
                                else: 
                                    estadoTemporario[h][2] = k[2]
                                    entrada += 1
                        h += 1
                    if entrada == len(estadoTemporario): #feita todas as modificações dos estados armazenados
                        entrou = True
    h = 0   
    while h < len(estadoTemporario): #loop para verificar se alguma das maquinas que foram dividas para os estados ambíguos chegou em um estado de aceitação
        for finais in parametrosEstados[2]: #verifica se alguma delas está no estado de aceitação(estado final)
            if estadoTemporario[h][2] == finais and estadoAtual != finais: 
                estadoAtual = estadoTemporario[h][2] 
        h += 1
                   
    if estadoAtual in parametrosEstados[2]: #se estiver no estado final, palavra aceita
        print('Palavra Aceita!!!')
    else:   #senão, é rejeitada
        print('Palavra Rejeitada!!!')
                

#Função que realiza a ordenação de estados
def num_sort(test_string): 
    return list(map(int, re.findall(r'\d+', test_string))) #retorna a lista ordenada pelo número dentro da string

#Função para ordenar os estados
def ordenado(string):
    teste = string.split(', ') #transformando a string em lista para fazer a ordenação
    teste.sort(key=num_sort)    #chamada da função da realização de ordenação de estados para ordenar pelo número do estado na string
    concatenacao = ''
    i = 0
    while i < len(teste): #loop para concatenar os elementos da string que foram separados em uma lista para string novamente
        if concatenacao == '':
            concatenacao = teste[i]
        else:
            concatenacao = concatenacao + ', ' + teste[i]
        i += 1
    
    return concatenacao


#Função recursiva para a realização da conversão
def conversao(conjTransicoes, transicoesConvertidas, alfabeto, ultimoAdicionado):
    ultimoAlternativo = ordenado(ultimoAdicionado)
    #print(ultimoAlternativo)

    for transicoes in transicoesConvertidas:
        if ultimoAlternativo == transicoes[0]:
            transicoes[2] = ordenado(transicoes[2])
            conjTransicoes.append(transicoes)
            jaAdicionou = False
            for transicoes1 in conjTransicoes:
                if transicoes1[0] == transicoes[2]:
                    jaAdicionou = True 
            if not jaAdicionou:   
                if ultimoAlternativo != transicoes[2]:
                    conversao(conjTransicoes, transicoesConvertidas, alfabeto, transicoes[2])
    
    return conjTransicoes

#Conversão de AFN para AFD
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
    #print(conjTransicoes)

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
     
    
    for alfabeto in parametrosEstados[1]:
        for transicoes in conjTransicoes:
            if transicoes[1] == alfabeto:
                conjEstados.append(transicoes[0])
    conjEstados.append(parametrosEstados[0])
    copia = set(conjEstados)
    conjEstados = list(copia)
    #print(conjEstados)
     
    print(conjTransicoes)

    return minimizacao(parametrosEstados, conjTransicoes, conjEstados)    


def minimizacao(parametrosEstados, conjTransicoes, conjEstados):
    conjEstIniciais = []
    conjEstFinais = []
    
    for estados in conjEstados:
        for alfabeto in parametrosEstados[1]:
            for transicoes in conjTransicoes:
                for finais in parametrosEstados[2]:
                    if estados == transicoes[2] and transicoes[0] != transicoes[2] and transicoes[1] == alfabeto and finais in estados:
                        conjEstFinais.append(estados)
    
    copia = set(conjEstFinais)
    conjEstFinais = list(copia)
    #print(conjEstFinais)
    
    i = 0
    while i < len(conjEstados):
        final = False
        for finais in parametrosEstados[2]:
            if finais in conjEstados[i]:
                final = True
        if not final:
            conjEstIniciais.append(conjEstados[i])
        i += 1
    estadosSemRepeticao = set(conjEstIniciais)
    conjEstIniciais = list(estadosSemRepeticao)
    #print(conjEstIniciais)
    
    pares = []
    transicoesCopia = conjTransicoes
    
    #indices = []
    
    
    indice = 0
    i = 0
    while i < len(conjEstIniciais):
        j = i + 1
        while j < len(conjEstIniciais):
            if conjEstIniciais[i] != conjEstIniciais[j]:
                indice += 1
                pares.append([conjEstIniciais[i], conjEstIniciais[j], False, indice])
            j += 1
        i += 1

    i = 0
    while i < len(conjEstFinais):
        j = i + 1
        while j < len(conjEstFinais):
            if conjEstFinais[i] != conjEstFinais[j]:
                indice += 1
                pares.append([conjEstFinais[i], conjEstFinais[j], False, indice])
            j += 1
        i += 1
        
    #print(pares)

    for par in pares:          
        pares = minimizar(par[3] - 1, -1, pares, conjTransicoes, parametrosEstados[1], parametrosEstados[2])

    #print(pares)

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
    
def minimizar(indice, indiceAnterior, pares, conjTransicoes, alfabeto, estadoFinal):
    resultado = []
    achou = False
    
    #print(pares[indice])
    
    for simbolo in alfabeto:
        for estado1 in conjTransicoes:
            for estado2 in conjTransicoes:
                if estado1[0] == pares[indice][0] and estado2[0] == pares[indice][1] and estado1[1] == simbolo and estado2[1] == simbolo:
                    resultado.append([estado1[2], estado2[2]])
                    break
    #print(resultado)
    for r in resultado:
        for par in pares:
            if (r[0] == par[0] and r[1] == par[1]) or (r[0] == par[1] and r[1] == par[0]):  
                #print(r)
                if indice != indiceAnterior:
                    achou = True
                    pares = minimizar(par[3] - 1, indice, pares, conjTransicoes, alfabeto, estadoFinal)
                    if par[2]:
                        achou = False
    
    
    if not achou:
        contagem = 0
        finais = False
        pares[indice][2] = True
        for r in resultado:
            if r[0] == r[1]:
                contagem += 1
            if contagem >= 1:
                for final in estadoFinal:
                    if final in r[0] and final in r[1] and r[0] != r[1]:
                        finais = True
                        #print('a')
        #print(contagem)
        if contagem == len(resultado) or (contagem >= len(resultado) / 2 and finais):
            pares[indice][2] = False
    return pares
    
    
parametros = entradaDados()
parametrosMinimizados = conversaoAFN(parametros)
#while True:
simulacao(parametros)
simulacao(parametrosMinimizados)

'''def simulacaoAFD(parametrosEstados):
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
        print('Palavra Rejeitada!!!')'''


