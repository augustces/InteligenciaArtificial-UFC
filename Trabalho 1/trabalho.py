import random
import math

# Função para gerar um vizinho trocando dois pontos na rota
def operador1(rota):
    vizinho = rota[:]
    i, j = random.sample(range(len(rota)), 2)
    vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
    return vizinho

# Função para inverter trechos das permutações entre dois pontos da rota
def operador2(rota):
    vizinho = rota[:]
    i, j = random.sample(range(len(rota)), 2)
    if i > j:
        i, j = j, i
    vizinho[i:j+1] = reversed(vizinho[i:j+1])
    return vizinho

# Função para calcular a distância entre duas cidades
def distancia(cidade1, cidade2):
    return math.sqrt((cidade1[0] - cidade2[0])**2 + (cidade1[1] - cidade2[1])**2)

# Função para calcular o custo total de uma rota
def calcular_custo(rota, pesos):
    custo = 0.0
    for i in range(len(rota) - 1):
        cidade_atual = rota[i]
        proxima_cidade = rota[i + 1]
        custo += pesos[cidade_atual][proxima_cidade]
    return custo

# Função que calcula o fatorial
def fatorial(n):
    if n == 1 :
        return 1
    return n*(n-1)

# Função para gerar vizinhos com base em uma rota
def calcular_vizinhos (cidades, rota, f):
    vizinhos = []
    possivel = rota[:]
    possivel = f(possivel)
    for _ in range(fatorial(len(cidades))):
        possivel = f(possivel)
        if ((possivel not in vizinhos) or len(vizinhos) == 0): 
            vizinhos.append(possivel)
    return vizinhos

# Subida de Encosta
def subida_de_encosta(cidades, iteracoes,f, pesos,  inicialRandom = True, randomizar = True):
    coluna = []
    inicial = list(range(len(cidades))) # estado inicial é a sequencia lida no arquivo
    if (inicialRandom): # caso o estado inicial seja gerado aleatoriamente, embaralhamos a sequencia lida no arquivo
        random.shuffle(inicial)
    melhor_rota = inicial
    melhor_custo = calcular_custo(inicial, pesos) 
    coluna.append((melhor_custo, melhor_rota))
    for _ in range(iteracoes-1):
        vizinhos = calcular_vizinhos(cidades, melhor_rota, f) 
        if (randomizar):
            random.shuffle(vizinhos)
        for vizinho in vizinhos :
            custo_vizinho = calcular_custo(vizinho, pesos)
            if custo_vizinho < melhor_custo:
                melhor_rota = vizinho
                melhor_custo = custo_vizinho
                break 
        melhores = ((melhor_custo, melhor_rota)) 
        coluna.append(melhores)

    return coluna

# Função para escrever a matriz de resultados de cada interação de cada varização
def escrever(matriz, interacoes, variacoes):
    fout = open("saida.txt", "w")
    fout.write("Interacao \t \t 1 \t \t 2 \t\t 3 \t\t 4\t \t 5\t \t 6 \t\t 7 \t\t 8 \n")
    for interacao in range(interacoes):
        msg = f"{interacao + 1} \t\t"
        fout.write(msg)
        for variacao in range(variacoes):
            msg = f"{ matriz[variacao][interacao] } \t\t" 
            fout.write(msg)
        fout.write("\n")
    fout.close()

# Função para ler as coordenadas das cidades
def leitura():
    fin = open("entrada.txt", "r")
    x = list(map(float, fin.readline().split())) 
    y = list(map(float, fin.readline().split()))
    fin.close()
    cidades = [ (x[i], y[i])  for i in range (len(x))]
    pesos = []
    for cidade1 in cidades:
        coluna = []
        for cidade2 in cidades:
            coluna.append(distancia(cidade1, cidade2)) 
        pesos.append(coluna)
    return cidades, pesos


def main ():
    # Cidades lidas do arquivo de entrada
    cidades, pesos = leitura()
    # Número de iterações
    iteracoes = 30
    #Matriz que será gerada no arquivo de saída
    matriz = []

    # Estado Inicial 1 com Operador 1 sem randomização da vizinhança
    coluna = subida_de_encosta(cidades, iteracoes, operador1,pesos, False, False)
    matriz.append(coluna)

    # Estado Inicial 1 com Operador 1 com randomização da vizinhança
    coluna = subida_de_encosta(cidades, iteracoes, operador1,pesos, False)
    matriz.append(coluna)

    # Estado Inicial 1 com Operador 2 sem randomização da vizinhança
    coluna = subida_de_encosta(cidades, iteracoes, operador2,pesos, False, False)
    matriz.append(coluna)

    # Estado Inicial 1 com Operador 2 com randomização da vizinhança
    coluna = subida_de_encosta(cidades, iteracoes, operador2,pesos, False)
    matriz.append(coluna)

    # Estado Inicial 2 com Operador 1 sem randomização da vizinhança
    coluna = subida_de_encosta(cidades, iteracoes, operador1,pesos, True, False)
    matriz.append(coluna)

    # Estado Inicial 2 com Operador 1 com randomização da vizinhança
    coluna = subida_de_encosta(cidades, iteracoes, operador1,pesos)
    matriz.append(coluna)

    # Estado Inicial 2 com Operador 2 sem randomização da vizinhança
    coluna = subida_de_encosta(cidades, iteracoes, operador2,pesos, True, False)
    matriz.append(coluna)

    # Estado Inicial 2 com Operador 2 com randomização da vizinhança
    coluna = subida_de_encosta(cidades, iteracoes, operador2,pesos)
    matriz.append(coluna)

    # Chamada de função para escrever a matriz no arquivo de saída 
    escrever(matriz, 30, 8)

if __name__ == "__main__":
    main()