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
    ultimoAlternativo = ordenado(ultimoAdicionado) #atribuição de conjunto de estados ordenado para o último que foi adicionado na função de transição que está sendo convertida
    #print(ultimoAlternativo)

    for transicoes in transicoesConvertidas: #loop para verificar se de todas as transições possíveis, há aquelas que não são transições vazias ou que não levam a uma transição(transições inúteis)
        if ultimoAlternativo == transicoes[0]: #verifica se o último adicionado nas transições que não são inúteis leva a uma outra transição não inútil
            transicoes[2] = ordenado(transicoes[2]) #chama a função de ordenação de string para ordenar o estado resultante
            conjTransicoes.append(transicoes) #adiciona a função de transição não inútil 
            jaAdicionou = False #variável para controle de transições que já foram (ou não) adicionadas para caso haja transição que leva para o próprio estado
            for transicoes1 in conjTransicoes: #loop para verificar se já foi adicionado transições que levam para o próprio estado
                if transicoes1[0] == transicoes[2]:
                    jaAdicionou = True 
            if not jaAdicionou: 
                if ultimoAlternativo != transicoes[2]:
                    conversao(conjTransicoes, transicoesConvertidas, alfabeto, transicoes[2]) #chamada recursiva com o último estado resultante adicionado para verificar se há outro estado que não seja inútil
    
    return conjTransicoes #após a adição de todos estados não inúteis, retorna o conjunto de transições que possui estados não inúteis

#Conversão de AFN para AFD
def conversaoAFN(parametrosEstados):
    estadosGerados = parametrosEstados[3].copy() #realiza uma cópia do conjunto de transições que foi gerado inicialmente
    transicoesConvertidas = []
    estados = parametrosEstados[3].copy() #realiza uma cópia para servir de variável auxiliar na concatenação
    
    atualizarIndice = 0 #variável auxiliar para atualizar o índice da lista de estados que foram gerados e poder por meio dela fazer as concatenações
    vezes = (2 ** len(estadosGerados)) - 1 #conceito de produção das concatenações de estados da conversão em que matematicamente seria 2 elevado a quantidade de estados menos o estado vazio (...- 1)
    i = 0
    k = 0
    j = 0

    while i < vezes: #loop para realizar as concatenações 
        teste = estadosGerados[atualizarIndice].split(', ') #transformação da "string" com os estados em uma lista para que passe por cada estado existente
        ultimoIndiceTeste = len(teste) - 1 #variável que pega o último índice do estado concatenado que foi adicionado para que por meio dele, seja adicionados os outros que serão concatenados, podendo ser feita uma espécie de agrupamento
        j = 0
        indiceEstado = 0 #variável auxiliar para indicar onde está o estado na qual possui o último estado concatenado (ou agrupado)
        while j < len(estados): #loop para achar o estado que foi último a ser agrupado
            if estados[j] == teste[ultimoIndiceTeste]:
                indiceEstado = j
            j += 1
        k = indiceEstado + 1 #variável que recebe o índice do último estado que foi agrupado e que servirá para procurar outros estados restantes que não foram agrupados
        while k < len(estados): #loop para agrupar outros estados restantes
            estadosGerados.append(estadosGerados[atualizarIndice] + ', ' + estados[k]) #adiciona a uma das cópias dos estados existentes, o estado concatenado que também servirá para adicionar estados concatenados dos estados concatenados
            k += 1
        i += 1
        
        if atualizarIndice != len(estadosGerados) - 1: #assim que foram feitas todas as concatenações possíveis com o estado que está em evidência para armazenar sua concatenação, é verificado se não atingiu o fim da lista de estados concatenados
            atualizarIndice += 1
    
    conjEstados = []
    for alfabeto in parametrosEstados[1]: #loop auxiliar de controle que passa por todos símbolos do alfabeto
        i = 0
        while i < len(estadosGerados): #loop auxiliar que passa por todos os estados concatenados
            conversoesInicial = '' #variável auxiliar que servirá para concatenação dos estados de ativação da função de transição 
            conversoesFinal = '' #variável auxiliar que servirá para concatenação dos estados resultantes da função de transição
            teste = estadosGerados[i].split(', ') #variável que divide a concatenação dos estados concatenados
            j = 0
            contagem = 0 #variável auxiliar que indica se houve o armazenamento da primeira parte do estado concatenado
            while j < len(teste): #loop que passa pela divisão dos estados concatenados
                for transicoes in parametrosEstados[4]: #loop que passa por todas as transições para achar a função de transição que corresponde à parte atual do estado concatenado
                    if teste[j] == transicoes[0] and alfabeto == transicoes[1] and contagem == 0: #verifica se os estado de ativação e a parte do estado concatenado coincidem e se na função de transição se trata de apenas um símbolo na qual está no momento atual do loop do alfabeto e se trata-se da primeira parte a ser adicionada
                        conversoesInicial = transicoes[0]
                        conversoesFinal = transicoes[2]
                        contagem += 1
                    elif teste[j] == transicoes[0] and alfabeto == transicoes[1] and contagem != 0: #se não for a primeira parte a ser adicionada, faz-se apenas a concatenação
                        
                        if teste[j] not in conversoesInicial: #verifica se já não foi adicionada a parte atual do estado concatenado
                            conversoesInicial = conversoesInicial + ', ' + transicoes[0]
                            if transicoes[2] not in conversoesFinal: #verifica se estado resultante da função de transição já não foi adicionado
                                conversoesFinal = conversoesFinal + ', ' + transicoes[2]
                            else: #se já foi adicionado, apenas atribui
                                conversoesFinal = transicoes[2]
                        else: #se já foi adicionado, apenas atribui (sem concatenar)
                            conversoesInicial = transicoes[0]
                            if transicoes[2] not in conversoesFinal:
                                conversoesFinal = conversoesFinal + ', ' + transicoes[2]
                            else:
                                conversoesFinal = transicoes[2]
                j += 1
            i += 1
            transicoesConvertidas.append([conversoesInicial, alfabeto, conversoesFinal]) #adiciona as transições que foram concatenadas em outra variável
    #print(transicoesConvertidas)

    conjTransicoes = []
    for alfabeto in parametrosEstados[1]:
        i = 0
        while i < len(transicoesConvertidas):
            if parametrosEstados[0] == transicoesConvertidas[i][0] and alfabeto == transicoesConvertidas[i][1]:
                conjTransicoes.append(transicoesConvertidas[i]) #adiciona o primeiro estado de ativação da função de transição para quaisquer símbolos que exista no alfabeto, este que servirá de guia para eliminar os estados inúteis
            i += 1
    
    
    indice = len(conjTransicoes) #variável que armazena a última função de transição com o último símbolo possível em relação estados iniciais de ativação da função de transição
    i = 0
    while i < indice: #loop com a chamada da função recursiva que passará por todos estados úteis
        conjTransicoes = conversao(conjTransicoes, transicoesConvertidas, parametrosEstados[1], conjTransicoes[i][2])
        i += 1
    #print(conjTransicoes)

    i = 0
    while i < len(conjTransicoes): #loop para remoção de funções de transição repetidas
        j = i + 1
        while j < len(conjTransicoes): #loop auxiliar para fazer comparação
            if conjTransicoes[i][0] == conjTransicoes[j][0] and conjTransicoes[i][1] == conjTransicoes[j][1]: #verifica se o estado de ativação da função coincide e possuem o mesmo símbolo, efetuando a remoção 
                conjTransicoes.remove(conjTransicoes[j]) 
                i -= 1 #ação que mantém o índice atual da função de transição
            j += 1
        i += 1
    #print(conjTransicoes)

    estadoNovo = 'F'
    transicoesPont = conjTransicoes #variável que serve como ponteiro para o "conjunto" de funções de transição
    
    for transicoes in conjTransicoes: #loop para verificar se possui alguma função de transição que leva à transição nula (transição vazia) "eliminando" a transição vazia dando lugar a um estado de rejeição
        destino = transicoes[2].split(', ') #efetua a separação da concatenação do estado resultante para verificar se há um "estado vazio"
        resultado = ''
        indice = 0
        for d in destino: #loop para passar sobre todos os estados concatenados que foram separados
            if d == '': #verifica se já no primeiro estado separado é vazio, se sim, atribui um estado novo
                d = estadoNovo
            if indice == 0: #verifica se trata-se da primeira parte do estado concatenado separado, atribuindo-o
                resultado = d
            else: #se não, apenas concatena 
                resultado = resultado + ', ' + d
            indice += 1
        transicoes[2] = resultado #atribui à transição que há "estado vazio" o estado novo (estado de rejeição)
    
    
    novoEstado = False #variável que libera (ou não) a inclusão do estado de rejeição como um dos estados que faz parte do conjunto de estados
    for j in conjTransicoes: #loop para verificar se foi incluído o estado de rejeição na transição vazia
        if estadoNovo in j[2]: 
            novoEstado = True
    
    if novoEstado: #se foi incluído na transição vazia, inclui as funções de transição em relação a cada simbolo para o estado de rejeição
        for alfabeto in parametrosEstados[1]:
            transicoesPont.append([estadoNovo, alfabeto, estadoNovo])
     
    
    for alfabeto in parametrosEstados[1]: 
        for transicoes in conjTransicoes:
            if transicoes[1] == alfabeto: #verificação por meio de loops auxiliares de transição e do símbolos do alfabeto para armazenar os estados que compõem o conjunto de estados depois que foram convertidos
                conjEstados.append(transicoes[0])
    conjEstados.append(parametrosEstados[0])
    copia = set(conjEstados) #variável que "converte" o conjunto de estados do tipo lista para o tipo set, pois o tipo set é um tipo de lista que não admite duplicações, portanto, eliminando quaisquer tipo de duplicações de estados
    conjEstados = list(copia) #convertendo de volta os estados
    print(conjEstados)
     
    #print(conjTransicoes)

    return minimizacao(parametrosEstados, conjTransicoes, conjEstados) #retorno com a chamada da função de minimização que também retornará as transições minimizadas

#Minimização do autômato convertido para AFD
def minimizacao(parametrosEstados, conjTransicoes, conjEstados):
    conjEstIniciais = []
    conjEstFinais = []
    
    for estados in conjEstados: #loop para verificar quais estados do conjunto de estados é(são) final(is)
        for finais in parametrosEstados[2]: #loop para passar pelo(s) estado(s) final(is) 
            if finais in estados: #verifica se o estado atual do conjunto de estados é final
                conjEstFinais.append(estados) #armazena no conjunto de estados finais
    copia = set(conjEstFinais) #conversão para retirada de duplicados
    conjEstFinais = list(copia) #conversão de volta
    #print(conjEstFinais)
    
    i = 0
    while i < len(conjEstados): #loop para verificar quais estados são não-finais
        final = False #variável para delimitar o armazenamento de estados não-finais
        for finais in parametrosEstados[2]: 
            if finais in conjEstados[i]: #se algum dos estados forem finais, delimita o armazenamento mudando a variável para True
                final = True
        if not final: #verifica se é um estado final, se não, armazena.
            conjEstIniciais.append(conjEstados[i])
        i += 1
    estadosSemRepeticao = set(conjEstIniciais)
    conjEstIniciais = list(estadosSemRepeticao)
    #print(conjEstIniciais)
    
    pares = []
    transicoesCopia = conjTransicoes #variável que recebe a cópia do conjunto de transições que veio como parametro   
    
    indice = 0 #variável que servirá para marcar a posição do par no conjunto de pares que farão a verificação de minimização
    i = 0
    while i < len(conjEstIniciais): #loop para fazer os pares dos estados não-finais
        j = i + 1
        while j < len(conjEstIniciais): #loop auxiliar para seja feita pares diferentes
            if conjEstIniciais[i] != conjEstIniciais[j]: #verifica se os pares são diferentes
                indice += 1 
                pares.append([conjEstIniciais[i], conjEstIniciais[j], False, indice]) #adiciona os pares diferentes, com uma "variável" que servirá para caso seja True não haja a fusão dos estados e False para que haja a fusão de estados, além do índice que marca a posição do par
            j += 1
        i += 1

    i = 0
    while i < len(conjEstFinais): #loop para fazer os pares de estados finais
        j = i + 1
        while j < len(conjEstFinais): #loop auxiliar para que seja feita para pares finais diferentes
            if conjEstFinais[i] != conjEstFinais[j]: #verifica se são pares diferentes
                indice += 1
                pares.append([conjEstFinais[i], conjEstFinais[j], False, indice]) #adiciona os pares diferentes, com uma variável False que poderá ser modificada caso não seja necessária uma fusão(True) e o índice
            j += 1
        i += 1
        
    #print(pares)

    for par in pares: #loop para que passe por todos os pares e verifique a possibilidade de fusão ou não         
        pares = minimizar(par[3] - 1, -1, pares, conjTransicoes, parametrosEstados[1], parametrosEstados[2]) #função recursiva que verifica cada par, com o seu respectivo índice, o índice anterior ao atual(inicializado com -1), os pares, as funções de transições convertidas, o alfabeto e os estados finais de antes da conversão

    #print(pares)

    for i in pares: #loop para verificar quais pares foram "marcados" com False
        for alfabeto in parametrosEstados[1]: #loop para controle sob quais simbolos farão a alteração
            for transicoes in transicoesCopia: #loop para controle sob quais transições que farão a alteração
                if not i[2]: #verifica se o par foi "marcado" com False, assim fazendo a fusão de transições
                    if transicoes[0] == i[0] and alfabeto == transicoes[1]:  #verifica se um dos pares é compatível com a transição e o simbolo correspondente ao loop de controle
                        #print(transicoes[0] + ', ' + i[0])
                        for t in transicoesCopia: #loop para verificar o outro par
                            if t[0] == i[1] and alfabeto == t[1]: #verifica se o outro par é compatível com a transição e o simbolo correspondente ao loop de controle
                                transicoesCopia.append([i[0] + ', ' + i[1], alfabeto, transicoes[2] + ', ' + t[2]]) #adiciona a transição com os pares fundidos
                                transicoesCopia.remove(t) #remove a transição de um dos pares que farão fusão, dando lugar aos pares fundidos
                                transicoesCopia.remove(transicoes) #remove a transição do outro par
        

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


