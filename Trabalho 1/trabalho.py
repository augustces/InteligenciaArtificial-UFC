import random
import math


# Função para gerar um vizinho trocando dois pontos na rota
def operador1(rota, i, j):
    vizinho = rota[:]  # cópia da rota
    vizinho[i], vizinho[j] = (
        vizinho[j],
        vizinho[i],
    )  # troca a cidade que estava no índice i para o índice j, e vice-versa
    return vizinho


# Função para inverter trechos das permutações entre dois pontos da rota
def operador2(rota, i, j):
    tam = len(rota)  # tamanho da rota
    vizinho = rota[:]  # cópia da rota
    if i > j:  # caso i seja maior que j (propriedade circular da lista)
        for c in vizinho[
            : j - i
        ]:  # aumenta a lista para auxiliar na inversão de trechos
            vizinho.append(c)
        while j >= 0:  # realiza a troca de cidades (garante a inversão)
            vizinho[j], vizinho[i] = vizinho[i], vizinho[j]
            i += 1
            j -= 1
        vizinho = vizinho[:tam]  # transforma de volta a lista para seu tamanho original
    else:
        while i < j:  # caso i menor que j (trecho interno da rota)
            vizinho[i], vizinho[j] = (
                vizinho[j],
                vizinho[i],
            )  # faz troca de cidades (garante a inversão)
            i += 1
            j -= 1
            if i == tam:  # garante índices dentro do intervalo
                i == 0
            if j < 0:  # garante índices dentro do intervalo
                j = tam - 1
    return vizinho


# Função para calcular a distância entre duas cidades
def distancia(cidade1, cidade2):
    return math.sqrt((cidade1[0] - cidade2[0]) ** 2 + (cidade1[1] - cidade2[1]) ** 2)


# Função para calcular o custo total de uma rota
def calcular_custo(rota, pesos):
    custo = 0.0
    # percorre toda a rota somando os custos de uma cidade a outra
    # ainda calcula o custo da última cidade para a cidade de origem
    for i in range(len(rota)):
        cidade_atual = rota[i]
        proxima_cidade = rota[
            (i + 1) % len(rota)
        ]  # garante que o índice não saia do invervalo
        custo += pesos[cidade_atual][proxima_cidade]
    return custo


# Função para gerar vizinhos com base em uma rota
def calcular_vizinhos(cidades, rota, operador):
    vizinhos = []  # lista de vizinhos
    for i in range(
        len(cidades)
    ):  # para cada cidade, calcula novos vizinhos com base na rota e no operador escolhido
        for j in range(len(cidades)):
            vizinhos.append(operador(rota, i, j))
    return vizinhos


# Subida de Encosta
def subida_de_encosta(cidades, operador, pesos, inicialRandom=True, randomizar=True):
    inicial = list(range(len(cidades)))  # estado inicial é a sequencia lida no arquivo
    if (
        inicialRandom
    ):  # caso o estado inicial seja gerado aleatoriamente, embaralhamos a sequencia lida no arquivo
        random.shuffle(inicial)
    melhor_rota = inicial[:]  # melhor rota atual é a inicial
    melhor_custo = calcular_custo(inicial, pesos)  # melhor custo atual

    condicao = True  # condição de parada do loop
    # executa até não haver um vizinho com custo melhor
    while condicao:
        condicao = False  # Até agora nenhum vizinho foi melhor
        vizinhos = calcular_vizinhos(
            cidades, melhor_rota, operador
        )  # encontra os vizinhos possíveis

        if randomizar:  # se a variação for para randomizar os vizinhos, randomiza
            random.shuffle(vizinhos)
        # ver o primeiro vizinho com custo menor
        for vizinho in vizinhos:
            custo_vizinho = calcular_custo(vizinho, pesos)  # calcula o custo do vizinho
            if (
                custo_vizinho < melhor_custo
            ):  # verifica se o custo do vizinho é menor que o melhor custo
                melhor_rota = vizinho  # atualiza o valor da melhor rota
                melhor_custo = custo_vizinho  # atualiza o valor do melhor custo
                condicao = True  # deixa True para verificar os próximos vizinhos
                break

    return melhor_custo, melhor_rota


# Função para ler as coordenadas das cidades
def leitura():
    fin = open("entrada.txt", "r")  # lê as cidades do arquivo de entrada
    x = list(map(float, fin.readline().split()))  # guarda os valores de x
    y = list(map(float, fin.readline().split()))  # guarda os valores de y
    fin.close()  # fecha o arquivo
    cidades = [(x[i], y[i]) for i in range(len(x))]  # organiza as cidades
    pesos = []
    # calcula os pesos (a distância) de uma cidade para outra
    for cidade1 in cidades:
        coluna = []
        for cidade2 in cidades:
            coluna.append(distancia(cidade1, cidade2))
        pesos.append(coluna)
    # retorna as coordenadas das cidades e os pesos de cada cidade
    return cidades, pesos


def main():
    # Cidades lidas do arquivo de entrada
    cidades, pesos = leitura()

    print(
        "Cidades lidas, informe qual operador usar \n 1 (troca duas cidades de posição em um circuito) \n 2 (inverte o trajeto entre duas cidades em um circuito) \n"
    )
    operador = int(input())

    print("Os vizinhos serão comparados randomicamente? Sim = 1, Não = 0")
    yes = int(input())

    print("A cidade inicial é arbitrária? Sim = 1, Não = 0")
    inicialRandom = int(input())

    if operador == 1:
        melhor_custo, melhor_rota = subida_de_encosta(
            cidades, operador1, pesos, inicialRandom == 1, yes == 1
        )
        print(f"Melhor custo: {melhor_custo}")
        print(f"Melhor rota: {melhor_rota}")
    else:
        melhor_custo, melhor_rota = subida_de_encosta(
            cidades, operador2, pesos, inicialRandom == 1, yes == 1
        )
        print(f"Melhor custo: {melhor_custo}")
        print(f"Melhor rota: {melhor_rota}")


if __name__ == "__main__":
    main()
