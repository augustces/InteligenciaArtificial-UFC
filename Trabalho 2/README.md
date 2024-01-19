# Trabalho 3 - Algoritmo A\*

## Desenvolvedores

- [Augusto César](https://github.com/augustces)

## Arquivos Importantes

O enunciado do problema está no arquivo [Enunciado - A-Star.pdf](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%202/Enunciado%20-%20A-Star.pdf).

Os testes foram executados no arquivo [Testes_02.ipynb](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%202/Teste_02.ipynb). O arquivo contém a aplicação do algoritmo para dois conjuntos de entrada, um com 7 cidades e o outro com 12. Existem duas variações do algortimo, um considerando a cidade de partida no cálculo da função heurística e o outro não a inserindo. Os resultados são mostrados por um dataframe para cada cidade inicial, tendo campos de número de cidades visitadas, cidades geradas, o melhor circuito encontrado para aquela cidade inicial e o custo total.
Também são calculadas as médias de cidades visitadas e geradas.

O algoritmo está no arquivo [trabalho.py](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%202/trabalho.py). Após definir as coordenadas das cidades de entrada, o algoritmo é executado verificando a vizinha do nó atual e calculando o custo, comparando-o com os demais nós encontrados. Quando todas as cidades forem percorridas, o melhor circuito, isto é, o de menor custo, é retornado. O custo é calculado com a soma das funções g e h, em que a função g calcula o custo real entre as cidades de um caminho e a função h calcula o custo estimado até o nó objetivo, isto é, o caminho que contém todas as cidades percorridas.

O arquivo de entrada, contendo as cidades que serão consideradas para o cálculo estão no arquivo [entrada.txt](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%202/entrada.txt).

Os arquivos de saída estão em divididos em 3:

1. [resultados.txt](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%202/resultados.txt). Esse arquivo contém a cidade inicial, os números de cidades visitadas e geradas e versão da heurística utilizada para cada cidade inicial considerada (executado no arquivo [trabalho.py](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%202/trabalho.py)) .

2. [variacao1.txt](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%202/variacao1.txt). Esse arquivo contém de cada iteração do algoritmo A\* (executado no arquivo [trabalho.py](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%202/trabalho.py)) utilizando a cidade de partida no cálculo da função heurística. Inicialmente, é informado a cidade inicial e depois os blocos de iteração para a cidade inicial em questão. Cada bloco contém as seguintes informações:

- Número da iteração
- Número da cidade visitada
- Caminho atual
- Valor da função g (custo real)
- Valor da função h (custo estimado até o nó objetivo)
- Valor da função f (funções g e h somadas)

No fim dos blocos de cada cidade inicial, são informados o caminho de menor custo e o custo final.

3. [variacao2.txt](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%202/variacao2.txt). Esse arquivo contém de cada iteração do algoritmo A\* (executado no arquivo [trabalho.py](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%202/trabalho.py)) utilizando a cidade de partida no cálculo da função heurística. Inicialmente, é informado a cidade inicial e depois os blocos de iteração para a cidade inicial em questão. Cada bloco contém as seguintes informações:

- Número da iteração
- Número da cidade visitada
- Caminho atual
- Valor da função g (custo real)
- Valor da função h (custo estimado até o nó objetivo)
- Valor da função f (funções g e h somadas)

No fim dos blocos de cada cidade inicial, são informados o caminho de menor custo e o custo final.

As instruções de execução estão no arquivo [help.txt](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%202/help.txt).

O relatório final está no arquivo [Relatório - Trabalho 2 - IA.pdf](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%202/Relat%C3%B3rio%20-%20Trabalho%202%20-%20IA.pdf).
