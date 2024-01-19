import random
import math
import heapq

# Função para calcular a distância entre duas cidades
def distancia(cidade1, cidade2):
    return math.sqrt((cidade1[0] - cidade2[0])**2 + (cidade1[1] - cidade2[1])**2)

# Função para ler as coordenadas das cidades
# Retorna as coordenadas das cidades e os pesos (distâncias) entre cada duas cidades
def leitura():
    fin = open("entrada.txt", "r") # abre o arquivo de leitura
    x = list(map(float, fin.readline().split())) # guarda as coordenadas x das cidades
    y = list(map(float, fin.readline().split())) # guarda as coordenadas y das cidades
    fin.close() # fecha o arquivo de leitura
    cidades = [ (x[i], y[i])  for i in range (len(x))] # organiza as cidades lidas
    pesos = [] 
    # calcula os pesos (distâncias) das cidades
    for cidade1 in cidades:
        coluna = []
        for cidade2 in cidades:
            coluna.append(distancia(cidade1, cidade2)) 
        pesos.append(coluna)
    return cidades, pesos

# Função auxiliar para encontrar a raiz de uma cidade e retorná-la
def encontrar(subconjuntos, cidade):
    if subconjuntos[cidade] == -1:
        return cidade
    return encontrar(subconjuntos, subconjuntos[cidade])

# Função auxiliar que liga a raiz de duas cidades
def unir(subconjuntos, cidade1, cidade2):
    raizCidade1 = encontrar(subconjuntos, cidade1)
    raizCidade2 = encontrar(subconjuntos, cidade2)
    subconjuntos[raizCidade1] = raizCidade2

# função heurística do custo da árvore geradora mínima
# a função por default não considera o retorno para a cidade de início do circuito,
# por isso, pode-se decidir deixando o parâmetro comPartida como True
def h(caminho, numero_cidades, pesos, comPartida):
    ultimo = caminho[len(caminho) - 1] # pega a ultima cidade do caminho

    abertos = [] # lista de cidades disponíveis para visitar
    # caso a variação permitir a cidade de partida no cálculo da estimativa, adiciona à lista de abertos
    if comPartida:
        abertos.append(ultimo)
    # determina quais as cidades disponíveis (as que não estão no caminho)
    for cidade in range(numero_cidades):
        if cidade not in caminho:
            abertos.append(cidade)

    custo = 0 
    heap_aux = [] # criando heap para ordenar os pesos
    # organiza em uma heap min os pesos de uma cidade para outra
    for cidade1 in abertos:
        for cidade2 in abertos:
            if (cidade1 != cidade2):
                # insere somente os pesos das cidades destino que ainda estão disponíveis para visitar
                heapq.heappush(heap_aux,(pesos[cidade1][cidade2], (cidade1, cidade2)))
    
    # cria matriz zerada para representar a árvore geradora mínima
    # se celula continuar 0, não há uma aresta entre as cidades (linha = cidade de origem, coluna = cidade de destino)
    agm = []
    for _ in range(numero_cidades):
        vetor = [0] * numero_cidades
        agm.append(vetor)

    # cria vetor que organiza as cidades interligadas
    subconjuntos = [-1] * numero_cidades
    
    while len(heap_aux) > 0:
        peso, aresta = heapq.heappop(heap_aux) # pega a menor aresta
        raizCidade1 = encontrar(subconjuntos, aresta[0]) # encontra a raiz
        raizCidade2 = encontrar(subconjuntos, aresta[1]) # encontra a raiz

        if raizCidade1 != raizCidade2: # adiciona à AGM o peso das cidades não interligadas
            agm[aresta[0]][aresta[1]] = peso
            unir(subconjuntos, raizCidade1, raizCidade2) # une as cidades

    # soma as arestas da AGM
    for linha in agm:
        custo += sum(linha)
    
    return custo

# função que calcula custo real do estado inicial até n
def g(caminho, pesos, numero_cidades):
    custo = 0
    for cidade in range(len(caminho) - 1): # percorre todas as cidades somando as distâncias de uma para outra 
        custo += pesos[caminho[cidade]][caminho[cidade + 1]]
    # caso todas as cidades tenham sido percorridas, fecha o ciclo (soma o custo da última cidade com a primeira)
    if (len(caminho) == numero_cidades):
        custo += pesos[caminho[numero_cidades - 1]][caminho[0]] # fecha o ciclo
    return custo

# Classe que guarda as informações de um caminho
class Caminho:
    def __init__(self, caminho) -> None:
        self.caminho = caminho # caminho de cidades percorridas
        self.g = 0 # custo da função g
        self.h = 0 # custo da função h
        self.f = self.g + self.h # custo da função f

    def calcularF(self):
        self.f = self.g + self.h # custo da função f

    def ultima(self): # retorna a última cidade do caminho
        return self.caminho[len(self.caminho) - 1]

# função para calcular o custo de um caminho
def funcaoCusto(caminhoLista, pesos, cidades, comPartida):
    caminho = Caminho(caminhoLista)
    caminho.g = g(caminho.caminho, pesos, len(cidades)) # armazena a função g (o custo real do caminho atual)

    # armazena a função f (o custo segundo a função heurística que calcula o custo de um tal nó até o objetivo)
    # a cidade de partida vai ser a ultima do caminho temporario, o objetivo é usar todas as cidades no novo circuito (usando todos, fecharemos um ciclo) 
    caminho.h= h(caminho.caminho, len(cidades), pesos, comPartida) 

    caminho.calcularF() # calcula o custo da função f 
    return caminho

# função principal que põe em prática o algoritmo A*
# a função por default não considera o retorno para a cidade de início do circuito,
# por isso, pode-se decidir deixando o parâmetro comPartida como True
def a_star(cidades, pesos, cidade_inicial, comPartida):
    visitadas = 0 # guarda o número de cidades visitadas
    gerados = 0 # guarda o número de cidades geradas

    # Auxiliares para imprimir os resultados
    str_saida = []
    saida = (f"Cidade inicial - cidade {cidade_inicial}\n")
    str_saida.append(saida)

    visitadas += 1 # incrementa cidade visitada
    circuito = Caminho([cidade_inicial]) # caminho atual (já com a cidade de origem)
    gerados += 1 # incrementa cidade gerada
    it = 0 # variavel para saber a iteração
    heap_min = []  # guarda os custos de todos os caminhos visitados (percorridos) 
    #enquanto o circuito não tiver com todas as cidades, executa
    while len(circuito.caminho) < len(cidades):
        abertos = set()
        # guarda as cidades abertas (disponíveis para visita)
        for cidade in range(len(cidades)):
            if cidade not in circuito.caminho:
                abertos.add(cidade) 
        # visita todas as cidades em aberto, calcula seus custos e adiciona na heap min 
        for cidade in abertos:
            visitadas += 1 # adiciona 1 em cidades visitadas
            # auxiliares para imprimir os resultados
            saida = ("----------------------------------------------------------\n")
            str_saida.append(saida)
            saida = (f"iteracao {it} \n")
            str_saida.append(saida)
            saida = (f"Cidade visitada: {cidade} \n")
            str_saida.append(saida)

            caminho_temp = Caminho(circuito.caminho + [cidade]) # armazena o caminho temporário

            # auxiliares para imprimir os resultados
            saida =  (f"Caminho atual: {circuito.caminho} \n" )  
            str_saida.append(saida)

            caminho_temp.g = g(caminho_temp.caminho, pesos, len(cidades)) # armazena a função g (o custo real do caminho atual)

            # auxiliares para imprimir os resultados
            saida = (f"Funcao g: {caminho_temp.g} \n")
            str_saida.append(saida)

            # armazena a função f (o custo segundo a função heurística que calcula o custo de um tal nó até o objetivo)
            # a cidade de partida vai ser a ultima do caminho temporario, o objetivo é usar todas as cidades no novo circuito (usando todos, fecharemos um ciclo) 
            caminho_temp.h= h(caminho_temp.caminho, len(cidades), pesos, comPartida) 

            # auxiliares para imprimir os resultados
            saida = (f"Funcao h: {caminho_temp.h}\n")
            str_saida.append(saida)

            caminho_temp.calcularF() # calcula o custo da função f

            # auxiliares para imprimir os resultados
            saida = (f"Funcao f (g + h): {(caminho_temp.f)} \n")
            str_saida.append(saida)

            # adiciona o valor de f (g + h) na heap-min
            heapq.heappush(heap_min, (caminho_temp.f, caminho_temp.caminho))
            it += 1 # incrementa a iteração
        _, caminhoLista = heapq.heappop(heap_min) # pega o caminho de menor custo
        caminho = funcaoCusto(caminhoLista, pesos, cidades, comPartida)
        gerados += 1 # incrementa o valor de cidades geradas
        circuito = caminho # atualiza o valor do circuito com o caminho de menor custo
    # auxiliares para imprimir os resultados 
    # Formatação do custo com 12 casas decimais
    texto_formatado = "{:.{precisao}f}".format(circuito.f, precisao=12)
    saida = (f"\nPara a cidade inicial {cidade_inicial}, o circuito de menor custo foi: {circuito.caminho}, com custo {texto_formatado}\n" )
    str_saida.append(saida)
    saida = ("----------------------------------------------------------\n")
    str_saida.append(saida)
    return str_saida, visitadas, gerados

def main ():
    def escrita(matriz_resultados, nomeArquivo): # escreve no arquivo de saida
        fout = open(nomeArquivo, "w") # arquivo de saida
        for linha in (matriz_resultados): 
            for coluna in linha:
                fout.write(coluna)
            fout.write("\n")
        fout.close()

    # Cidades lidas do arquivo de entrada
    cidades, pesos = leitura()

    tamanho_cidades = len(cidades)
    # Questão 1: estado inicial arbritário ou não
    # se tiver mais de 10 cidades, é arbitrário, senão segue a ordem de cidades da entrada
    matriz1 = [] # matriz contendo os resultados da variação com a cidade de partida na estimativa
    matriz2 = [] # matriz contendo os resultados da variação sem a cidade de partida na estimativa
    fout = open("resultados.txt", "w") 
    if (tamanho_cidades > 10):
        iniciais = set()
        while(len(iniciais) <= 10): #aciona elementos no set até o tamanho ser igual a 10
            cidade = random.choice(range(tamanho_cidades)) # escolhe uma cidade aleatoria para ser a cidade inicial
            if cidade not in iniciais: 
                iniciais.add(cidade)
                saida, visitados, gerados = a_star(cidades, pesos, cidade, True)
                fout.write(f"Cidade inicial: {cidade} \nVersao da Heuristica: Com a cidade inicial na estimativa \nCidades visitadas: {visitados} \nCidades geradas: {gerados}\n\n")
                matriz1.append(saida)
                saida, visitados, gerados = a_star(cidades, pesos, cidade, False)
                fout.write(f"Cidade inicial: {cidade} \nVersao da Heuristica: Sem a cidade inicial na estimativa \nCidades visitadas: {visitados} \nCidades geradas: {gerados}\n\n")
                matriz2.append(saida) 
    else:
        for cidade in range(len(cidades)): # para cidade da entrada, chama o algoritmo passando ela como cidade inicial 
            saida, visitados, gerados  = a_star(cidades, pesos, cidade, True)
            fout.write(f"Cidade inicial: {cidade} \nVersao da Heuristica: Com a cidade inicial na estimativa \nCidades visitadas: {visitados} \nCidades geradas: {gerados}\n\n")
            matriz1.append(saida)
            saida, visitados, gerados = a_star(cidades, pesos, cidade, False)
            fout.write(f"Cidade inicial: {cidade} \nVersao da Heuristica: Sem a cidade inicial na estimativa \nCidades visitadas: {visitados} \nCidades geradas: {gerados}\n\n")
            matriz2.append(saida)
    fout.close()
    escrita(matriz1, "variacao1.txt") 
    escrita(matriz2, "variacao2.txt") 
        
         
if __name__ == "__main__":
    main()