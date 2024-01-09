# Trabalho 3 - Algoritmos Genéticos

## Desenvolvedores

- [Augusto César](https://github.com/augustces)

## Arquivos Importantes

O enunciado do problema está no arquivo [Enunciado - Algoritmos Genéticos.pdf](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%203/Enunciado%20-%20Algoritmos%20Gen%C3%A9ticos.pdf).

Os testes foram executados no arquivo [Testes.ipynb](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%203/Testes.ipynb). O arquivo contém a aplicação do algoritmo para um tamanho de população determinado em cada bloco de experimentação, a população é gerada arbitrariamente. O primeiro bloco de experimentação executa o algoritmo 10 vezes para 5 valores distintos de elitismo. Já o segundo bloco de experimentação executa o algoritmo 10 vezes para 6 valores distintos de população. O algoritmo retorna o fitness (a penalidade) para aquele indivíduo. É mostrando um dataframe contendo os melhores fitness para cada execução do bloco. Para a execução dos blocos de experimentação, o primeiro bloco demora cerca de 36 minutos, e o segundo demora duas horas e 36 minutos. Existem duas variações de crossover, uma com o primeiro filho gerado, e a outra com o segundo.

O algoritmo está no arquivo [trabalho.py](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%203/trabalho.py). Após definir os parâmetros de entrada (exceto o número de turnos, que é fixo), o algoritmo cria a população arbitrariamente e calcula os fitness de cada um dos indivíduos, guarda os melhores (os de maior fitness) e os mantêm na próxima geração de filhos conforme a taxa de elitismo. Após isso, é realizado o crossover da população, que terá novos indivíduos como produto (o tamanho é a quantidade da população menos a quantidade de indivíduos preservados pelo elitismo). O crossover combina partes de dois pais, que são separadas em um ponto arbitrário. Com o produto do crossover, alguns indivíduos são modificados (a quantidade é conforme a taxa de mutação). Após a junção dos novos indivíduos com os preservados, uma nova geração é feita, essa que terá o fitness calculado para iniciar novamente o algoritmo. Esse ciclo ocorre seguindo um número de iterações (valor que diz quantas gerações serão produzidas). Ao fim, é retornado o melhor fitness e o indivíduo que o possui.

As instruções de execução estão no arquivo [help.txt](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%203/help.txt).

O relatório final está no arquivo [Trabalho 3 - IA.pdf](https://github.com/augustces/InteligenciaArtificial-UFC/blob/main/Trabalho%203/Trabalho%203%20-%20IA.pdf).
