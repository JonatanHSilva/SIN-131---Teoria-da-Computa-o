import pynput

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
            return estadoInicial, alfabeto, estadoFinal, estados, transicoes
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


def conversao(parametrosEstados):
    contagem = 0
    primeiroLoop = False
    transicoesConversao = []

    for alfabeto in parametrosEstados[1]:
        for l in parametrosEstados[4]:
            if contagem == 0:
                transicoesConversao.append(l)
                contagem += 1
            else:
                concatenou = False
                for i in transicoesConversao:
                    if i[0] == l[0] and i[1] == alfabeto and i[1] == l[1] and i[2] != l[2]:
                        i[2] = i[2] + ', ' + l[2]
                        concatenou = True
                if not concatenou and not primeiroLoop:
                    transicoesConversao.append(l)                   
            #print(transicoesConversao)
        
        primeiroLoop = True

    conversaoTemporario = len(transicoesConversao)
    k = 0
    
    while k < conversaoTemporario:
        j = k + 1
        while j < conversaoTemporario:
            if transicoesConversao[k][1] == transicoesConversao[j][1] and transicoesConversao[k][0] not in transicoesConversao[j][0]:
                if transicoesConversao[k][2] in transicoesConversao[j][2]:
                    transicoesConversao.append([transicoesConversao[k][0] + ', ' + transicoesConversao[j][0], transicoesConversao[j][1], transicoesConversao[k][2]])
                else:
                    transicoesConversao.append([transicoesConversao[k][0] + ', ' + transicoesConversao[j][0], transicoesConversao[j][1], transicoesConversao[k][2] + ', ' + transicoesConversao[j][2]])
            j += 1       
        k += 1
    k = 0
    indiceTemporario = conversaoTemporario
    atualizarIndice = conversaoTemporario
    conversaoTemporario = len(transicoesConversao)
    while k < indiceTemporario:
        j = atualizarIndice
        while j < conversaoTemporario:
            if transicoesConversao[k][1] == transicoesConversao[j][1] and transicoesConversao[k][0] not in transicoesConversao[j][0]:
                if transicoesConversao[k][2] in transicoesConversao[j][2]:
                    transicoesConversao.append([transicoesConversao[k][0] + ', ' + transicoesConversao[j][0], transicoesConversao[j][1], transicoesConversao[k][2]])
                    atualizarIndice = j
                else:
                    transicoesConversao.append([transicoesConversao[k][0] + ', ' + transicoesConversao[j][0], transicoesConversao[j][1], transicoesConversao[k][2] + ', ' + transicoesConversao[j][2]])
                    atualizarIndice = j
            j += 1
        k += 1
    print(transicoesConversao.sort())
        

estados = int(input('Digite quantos estados possui o automato:\n'))
for i in range (estados):
    if i == 0:
        estadosGerados = "q{}".format(i)
    else:
        estadosGerados += ",q{}".format(i)
estadosGerados = estadosGerados.split(',')

transicoesConversao = estadosGerados.copy()
indiceTemporario = 0
i = 0
while i < len(estadosGerados):
    k = i
    while k < len(estadosGerados):
        if estadosGerados[i] not in transicoesConversao[k]:
            transicoesConversao.append(estadosGerados[i] + ', ' + transicoesConversao[k])
        k += 1
        #
    i += 1
    #print(estadosGerados)
#print(transicoesConversao)
atualizarIndice = len(estadosGerados)
vezes = (2 ** len(estadosGerados)) - 1
print(vezes)
i = 0
mudou = i
contador = len(estadosGerados) - 1
j = 0
while j < vezes:
    while i < len(estadosGerados):
        k = atualizarIndice
        while k < (len(transicoesConversao)):
            if estadosGerados[i] in transicoesConversao[k]:
                if i + 1 != len(estadosGerados):
                    i += 1
                    k -= 1
                    indice = i
                    #print('entrou')
                '''else:
                    if k + 1 < len(transicoesConversao):
                        if estadosGerados[i - 1] or estadosGerados[i] not in transicoesConversao[k + 1]:
                            i -= 1
                            #print("mudou indice")'''
            else:
                transicoesConversao.append(transicoesConversao[k] + ', ' + estadosGerados[i])
                if i + 1 != len(estadosGerados):
                    i += 1
                    k -= 1
                else:
                    i = indice
                
            k += 1
                
            #print(mudou)
            print(k)
            print(estadosGerados[i])
            print(transicoesConversao)
            print(indice)
        
        atualizarIndice += contador
        contador -= 1
        
        if(contador > 2):
            contador = 2
            mudou = 2
        #print(atualizarIndice)
        mudou += 1
        i = mudou
        #
    j += 1
    
    
    #print(estadosGerados)

