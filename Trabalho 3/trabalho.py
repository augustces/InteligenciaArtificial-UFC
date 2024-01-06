import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Matriz:
    # construtor da classe, contém número de enfermeiros, número de turnos e a matriz (zerada)
    def __init__(self, nenfermeiros, nturnos, matriz=[]):
        self.nenfermeiros = nenfermeiros  # númeo de enfermeiros
        self.nturnos = nturnos  # número de turnos
        self.enfermeiros = self.criaMatriz(nenfermeiros, nturnos)  # própria matriz
        self.turnos = self.criaMatriz(
            nturnos, nenfermeiros
        )  # representação diferente da matriz

    # método para fazer uma matriz
    def criaMatriz(self, l, c):
        matriz = []
        for _ in range(l):
            linha = []
            for _ in range(c):
                linha.append(0)
            matriz.append(linha)
        return matriz

    # retorna matriz como uma cadeia de 0s e 1s
    def printMatriz(self):
        string = ""
        for enf in range(self.nenfermeiros):
            for turno in range(self.nturnos):
                string += str(self.enfermeiros[enf][turno])
        return string

    def stringParaMatriz(self, string):
        it = 0
        for enf in range(self.nenfermeiros):
            for turno in range(self.nturnos):
                self.enfermeiros[enf][turno] = int(string[it])
                self.turnos[turno][enf] = int(string[it])
                it += 1


# função referente à restrição 1: min 1 enfermeiro e max 3 enfermeiros por turno
#  calcula o valor da penalidade e retorna
def r1(matriz):
    penalidade = 0  # armazena a penalidade

    # olha cada turno e checa se a quantidade de enfermeiros é menor que 1 ou maior que 3 para penalizar
    for turno in matriz.turnos:
        soma = sum(turno)
        if soma < 1 or soma > 3:
            penalidade += -1

    return penalidade


# função referente à restrição 2: Cada enfermeiro deve ser alocado em 5 turnos por semana
# calcula o valor da penalidade e retorna
def r2(matriz):
    penalidade = 0  # armazena a penalidade

    # olha cada enfermeiros e checa se a quantidade de turnos que ele está é menor ou maior que 5 para penalizar
    for enfermeiro in matriz.enfermeiros:
        soma = sum(enfermeiro)
        if soma < 5 or soma > 5:
            penalidade += -1

    return penalidade


# função referente à restrição 3: Nenhum enfermeiro pode trabalhar mais que 3 dias seguidos sem folga
# calcula o valor da penalidade e retorna
def r3(matriz):
    penalidade = 0  # armazena a penalidade
    diasTrabalhados = []  # auxiliar que verifica os dias trabalhados consecutivos
    nturno = 1  # auxiliar que verifica qual o turno

    # olha para cada turno de cada enfermeiro (em sequencia) e verifica se foi trabalhado em dias consecutivos
    for enfermeiro in matriz.enfermeiros:
        turnos = (
            []
        )  # auxiliar para verificar se o enfermeiro trabalhou naquele dia ou não
        for turno in enfermeiro:
            # guarda cada turno (a cada 3 turnos forma um dia)
            if nturno <= 3:
                turnos.append(turno)

            # incrementa os dias
            if nturno == 3:
                nturno = 0  # garante que não passa de 3

                if sum(turnos) > 0:
                    diasTrabalhados.append(1)
                else:
                    diasTrabalhados.append(0)
                    if sum(diasTrabalhados) > 3:
                        penalidade += -1
                    diasTrabalhados.clear()
                turnos.clear()
            nturno += 1
        if sum(diasTrabalhados) > 3:
            penalidade += -1

    return penalidade


# função referente à restrição 4
# calcula o valor da penalidade e retorna
def r4(matriz):
    penalidade = 0  # valor da penalidade
    turnos = 3  # turnos por dia
    enfermeiros = matriz.enfermeiros  # recebe a matriz separada por enfermeiros
    for enf in range(matriz.nenfermeiros):
        for turno in range(matriz.nturnos):
            if enfermeiros[enf][turno] == 1:
                for turnoExtra in range(matriz.nturnos):
                    # verifica se dado um turno ocupado, outros turnos no mesmo horário possuem enfermeiros trabalhando
                    if (turno % turnos) != (turnoExtra % turnos) and enfermeiros[enf][
                        turnoExtra
                    ] == 1:
                        penalidade += -1
    return penalidade


# função que calcula o fitness de determinada matriz
def fitness(matriz, restricoes):
    fit = 0
    if 1 in restricoes:
        fit += r1(matriz)
    if 2 in restricoes:
        fit += r2(matriz)
    if 3 in restricoes:
        fit += r3(matriz)
    if 4 in restricoes:
        fit += r4(matriz)
    return fit


# Cruzamento (crossover)
# contem o parâmetro var que indica qual variação está sendo usada
def crossover(tampopulacao, populacao, melhores_indices, restricoes, var=1):
    # a partir dos melhores individuos, pegamos 2 e realizamos o crossover para criar 2 novos filhos
    novos_individuos = []
    for _ in range(
        tampopulacao - len(melhores_indices)
    ):  # conta sem os melhores individuos
        index1 = random.choice(range(tampopulacao))
        index2 = random.choice(range(tampopulacao))
        while index1 == index2:
            index2 = random.choice(range(tampopulacao))
        pai1 = populacao[index1].printMatriz()
        pai2 = populacao[index2].printMatriz()
        ponto_corte = random.randint(1, len(pai1))  # seleciona o ponto de corte
        # realiza o crossover (troca as partes de cada pai)
        filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
        filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
        if var == 1:
            matriz = Matriz(
                nenfermeiros=populacao[index1].nenfermeiros,
                nturnos=populacao[index1].nturnos,
            )
            matriz.stringParaMatriz(filho1)
            novos_individuos.append(matriz)
        elif var == 2:
            matriz = Matriz(
                nenfermeiros=populacao[index1].nenfermeiros,
                nturnos=populacao[index1].nturnos,
            )
            matriz.stringParaMatriz(filho2)
            novos_individuos.append(matriz)
    return novos_individuos


# Mutação
def mutacaoF(mutacao, novos_individuos):
    # realiza a mutação alterando um caractere em uma cadeia (se é 0, muda para 1 e vice-versa)
    for novo in novos_individuos:
        # aplica a mutação de acordo com a taxa de mutação
        if random.random() < mutacao:
            novoStr = novo.printMatriz()
            index = random.randint(0, len(novoStr) - 1)
            string = ""
            if novoStr[index] == "0":
                if index == 0:
                    string = "1" + novoStr[index + 1 :]
                elif index == (len(novoStr) - 1):
                    string = novoStr[:index] + "1"
                else:
                    string = novoStr[:index] + "1" + novoStr[index + 1 :]
            else:
                if index == 0:
                    string = "0" + novoStr[index + 1 :]
                elif index == (len(novoStr) - 1):
                    string = novoStr[:index] + "0"
                else:
                    string = novoStr[:index] + "0" + novoStr[index + 1 :]
            novoStr = string
            novo.stringParaMatriz(novoStr)
    return novos_individuos


def algGenetico(
    nenfermeiros, nturno, restricoes, tampopulacao, interacoes, elitismo, mutacao, var
):
    # cria strings aleatorias que representam um cromossomo (uma possivel configuração)
    def string_aleatoria(tamanho):
        return "".join(random.choice("01") for _ in range(tamanho))

    # armazena a população (inicialmente vazia)
    populacao = []
    for _ in range(tampopulacao):
        matriz = Matriz(nenfermeiros=nenfermeiros, nturnos=nturno)
        matriz.stringParaMatriz(
            string_aleatoria(nenfermeiros * nturno)
        )  # preenche a matriz
        populacao.append(matriz)

    for _ in range(interacoes):
        # armazena o fitness de cada elemento da população
        fitnessPopulacao = []
        fitnesspositivo = []
        for matriz in populacao:
            value = fitness(matriz, restricoes)
            fitnessPopulacao.append(value)
            fitnesspositivo.append(value * (-1))
        novos_individuos = populacao
        melhores_individuos = []
        if elitismo > 0:
            # escolha dos melhores indivíduos (elitismo)
            melhores_indices = np.argsort(fitnesspositivo)[
                : int(elitismo * tampopulacao)
            ]  # pega os indices dos melhores fitness

            for indice in melhores_indices:
                melhores_individuos.append(
                    populacao[indice]
                )  # pega os elementos correspondentes aos indices

            # realiza o crossover
            novos_individuos = crossover(
                tampopulacao=tampopulacao,
                melhores_indices=melhores_indices,
                restricoes=restricoes,
                var=1,
                populacao=populacao,
            )

        # realiza a mutação
        novos_individuos = mutacaoF(mutacao=mutacao, novos_individuos=novos_individuos)
        for individuo in novos_individuos:
            melhores_individuos.append(individuo)
        populacao = melhores_individuos

    # Encontrando a melhor solução
    melhor_indice = np.argmax(fitnessPopulacao)
    melhor_solucao = populacao[melhor_indice]
    return melhor_solucao.printMatriz(), fitness(melhor_solucao, restricoes)


def main():
    # leitura dos dados
    print("informe o numero de enfermeiros")
    nenfermeiros = int(input())

    print("Os turnos por semana sao 21, 3 turnos de 8 horas por dia\n")
    nturnos = 21

    print(
        "informe quais as restriçoes que devem compor a funçao fitness? (separe o numero das restriçoes por espaço em branco)"
    )
    entrada = input()
    restricoes = [int(x) for x in entrada.split()]

    print("informe o tamanho da populaçao")
    tampopulacao = int(input())

    print("informe o numero de geraçoes (interaçoes) da simulaçao")
    interacoes = int(input())

    print("informe a taxa de elitismo")
    elitismo = float(input())

    print("informe a taxa de mutaçao")
    mutacao = float(input())

    print("informe a variaçao do algoritmo do crossover (explicado no relatorio)")
    print("escolha de 1 a 3")
    var = int(input())

    cadeia, fit = algGenetico(
        nenfermeiros=nenfermeiros,
        nturno=nturnos,
        restricoes=restricoes,
        tampopulacao=tampopulacao,
        interacoes=interacoes,
        elitismo=elitismo,
        mutacao=mutacao,
        var=var,
    )
    print(cadeia)
    print(fit)


if __name__ == "__main__":
    main()
