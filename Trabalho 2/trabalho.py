import random
import math
import heapq

# Função para calcular a distância entre duas cidades
def distancia(cidade1, cidade2):
    return math.sqrt((cidade1[0] - cidade2[0])**2 + (cidade1[1] - cidade2[1])**2)

# Função para ler as coordenadas das cidades
# Retorna as coordenadas das cidades e os pesos (distâncias) entre cada duas cidades
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

# função heurística do custo da árvore geradora mínima
def h(caminho, numero_cidades, pesos, comPartida):
    # determina quais as cidades disponíveis (as que não estão no circuito)
    abertos = set()
    for cidade in range(numero_cidades):
        if cidade not in caminho:
            abertos.add(cidade)

    custo = 0 
    circuito = []
    heap_aux = [] # criando heap para ordenar os pesos
    for cidade1 in range(numero_cidades):
        for cidade2 in range(numero_cidades):
            if (cidade1 != cidade2 and cidade2 in abertos):
                # insere somente os pesos das cidades destino que ainda estão disponíveis para visitar
                heapq.heappush(heap_aux,(pesos[cidade1][cidade2], (cidade1, cidade2)))

    ultimo = caminho[len(caminho) - 1] # pega a ultima cidade do caminho
    circuito.append(ultimo)
    # laço para calcular o custo e qual o caminho de menor custo para completar o circuito
    while len(abertos) > 0:
        copia_heap = heap_aux[:] # copia de segurança
        ultimo = circuito[len(circuito) - 1] # pega a ultima cidade do circuito
        # encontra a ultima cidade do circuito e pega a menor aresta para alguma outra cidade
        atual = heapq.heappop(copia_heap)  
        # pega o menor peso e quais são as cidades com base na ultima cidade do circuito
        while True:
            if ultimo == atual[1][0] and atual[1][1] not in circuito:
                break
            atual = heapq.heappop(copia_heap)  
        custo += atual[0] # aumenta o custo
        abertos.discard(atual[1][1]) # remove a cidade do conjunto de cidades não visitadas
        circuito.append(atual[1][1]) # adiciona a cidade no circuito 
    if comPartida:
        custo += pesos[circuito[len(circuito) - 1]][caminho[0]]
    return custo

# função que calcula custo real do estado inicial até n
def g(caminho, pesos):
    custo = 0
    for cidade in range(len(caminho) - 1):
        custo += pesos[cidade][cidade + 1]
    return custo

# função principal que põe em prática o algoritmo A*
def a_star(cidades, pesos, cidade_inicial, comPartida):
    # Auxiliares para imprimir os resultados
    str_saida = []
    saida = (f"Cidade inicial - cidade {cidade_inicial}\n")
    str_saida.append(saida)
    abertos = set(range(len(cidades))) # cidades não visitadas
    abertos.discard(cidade_inicial)
    circuito = [cidade_inicial] # circuito atual
    it = 0 # variavel para saber a interação
    #enquanto todas as cidades não forem visitadas, executa o laço
    while len(abertos)>0: 
        heap_min = []    
        for cidade in abertos:
            # auxiliares para imprimir os resultados
            saida = ("----------------------------------------------------------\n")
            str_saida.append(saida)
            saida = (f"interacao {it} \n")
            str_saida.append(saida)
            saida = (f"Cidade visitada: {cidade} \n")
            str_saida.append(saida)

            circuito_temp = circuito + [cidade] # armazena o circuito temporário
            
            # auxiliares para imprimir os resultados
            saida =  (f"Circuito atual: {circuito} \n" )  
            str_saida.append(saida)

            funcao_g = g(circuito_temp, pesos) # armazena a função g (o custo real do circuito atual)

            # auxiliares para imprimir os resultados
            saida = (f"Funcao g: {funcao_g} \n")
            str_saida.append(saida)

            # armazena a função f (o custo segundo a função heurística que calcula o custo de um tal nó até o objetivo)
            # a cidade de partida vai ser a ultima do circuito temporario, o objetivo é usar todas as cidades no novo circuito (usando todos, fecharemos um ciclo) 
            custo_h= h(circuito_temp, len(cidades), pesos, comPartida) 

            # auxiliares para imprimir os resultados
            saida = (f"Funcao h: {custo_h}\n")
            str_saida.append(saida)
            saida = (f"Funcao f (g + h): {(custo_h + funcao_g)} \n")
            str_saida.append(saida)

            # adiciona o valor de f (g + h) na heap-min
            heapq.heappush(heap_min, ((funcao_g + custo_h), cidade))
            it += 1
        _, cidade = heapq.heappop(heap_min) # pega a cidade de menor custo
        abertos.discard(cidade) # retira a cidade do set de cidades não visitadas
        circuito.append(cidade) # adiciona a cidade no circuito atual
        
    # auxiliares para imprimir os resultados 
    saida = (f"\nPara a cidade inicial {cidade_inicial}, o circuito de menor custo foi: {circuito}\n" )
    str_saida.append(saida)
    saida = ("----------------------------------------------------------\n")
    str_saida.append(saida)
    return str_saida

def main ():
    def escrita(matriz_resultados, nomeArquivo): # escreve no arquivo de saida
        fout = open(nomeArquivo, "w") # arquivo de saida
        for linha in range(len(matriz_resultados)): 
            for coluna in range(len(matriz_resultados[0])) :
                fout.write(matriz_resultados[linha][coluna] )
            fout.write("\n")
        fout.close()

    # Cidades lidas do arquivo de entrada
    cidades, pesos = leitura()

    tamanho_cidades = len(cidades)
    # Questão 1: estado inicial arbritário ou não
    # se tiver mais de 10 cidades, é arbitrário, senão segue a ordem de cidades da entrada
    matriz1 = [] # matriz contendo os resultados da variação com a cidade de partida na estimativa
    matriz2 = [] # matriz contendo os resultados da variação sem a cidade de partida na estimativa
    if (tamanho_cidades > 10):
        iniciais = set()
        
        while(len(iniciais) <= 10): #aciona elementos no set até o tamanho ser igual a 10
            cidade = random.choice(range(tamanho_cidades)) # escolhe uma cidade aleatoria para ser a cidade inicial
            if cidade not in iniciais: 
                iniciais.add(cidade)
                saida = a_star(cidades, pesos, cidade, True)
                matriz1.append(saida)
                saida = a_star(cidades, pesos, cidade, False)
                matriz2.append(saida)
        escrita(matriz1, "variacao1.txt") 
        escrita(matriz2, "variacao2.txt") 
    else:
        for cidade in range(len(cidades)): # para cidade da entrada, chama o algoritmo passando ela como cidade inicial 
            saida = a_star(cidades, pesos, cidade, True)
            matriz1.append(saida)
            saida = a_star(cidades, pesos, cidade, False)
            matriz2.append(saida)
        escrita(matriz1, "variacao1.txt") 
        escrita(matriz2, "variacao2.txt") 
         
if __name__ == "__main__":
    main()