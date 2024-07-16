import pynput

#Entrada de dados do Automato
def entradaDados():
    estados = str(input('Digite quais estados possui o automato:\n')).split(', ')
    alfabeto = str(input('Digite o alfabeto:\n')).split(', ')
    transicoes = []
    for i in estados:
        for j in alfabeto:
            transicoes.append([i, j, str(input('Para o estado "{}", qual é a sua transição quando a entrada for "{}"?\n'.format(i, j)))])
            print(transicoes)
    estadoInicial = str(input(f'Dentre {estados}, qual estado seria o inicial? '))
    estadoFinal = str(input(f'Dentre os estados {estados}, qual(is) seria(m) o(s) estado(s) de aceitação? ')).split(', ')
    print('Automato Salvo!!!')
    return estadoInicial, alfabeto, estadoFinal, estados, transicoes


#Simulação de aceitação de palavras
def simulacao(parametrosEstados):
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

simulacao(entradaDados())