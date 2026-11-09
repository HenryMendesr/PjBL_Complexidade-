# PjBL: deduplicação de leituras de sensores

**Integrantes:** Henry Rodrigues, Rafael Maluf e Matheus.

O projeto elimina leituras repetidas de sensores que recebem valores entre 0 e 65535. Implementamos duas soluções para clientes com necessidades diferentes:

- **Embarca:** Heap Sort iterativo seguido de compactação, em C. O algoritmo ordena o próprio vetor e mantém uma ocorrência de cada valor. Na compilação avaliada, o limite conservador de memória extra é de **96 bytes**, incluindo a pilha e uma margem para a chamada.
- **Datacenter:** bitmap em Python. Cada valor possível tem seu próprio bit, o que permite reconhecer repetições em uma única passagem pelo vetor. O bitmap usa 8192 bytes de bits, além dos objetos do interpretador.

A pasta `projeto/` reúne a entrega. A pasta `Estudos/` contém as contas explicadas, o roteiro de apresentação e a checklist. Os seis gráficos estão em arquivos individuais.

## Preparar o ambiente

A versão entregue foi avaliada em Linux x86-64, com GCC, binutils e Python 3.12.14. Para reproduzir também os gráficos e o PDF com as dependências fixadas, use Python 3.11 ou mais recente da série 3. No Windows, use um ambiente Linux ou WSL com essas ferramentas. O script de compilação usa uma biblioteca `.so` e opções do GCC próprias de x86-64.

Os algoritmos e os testes Python usam apenas a biblioteca padrão. Para gerar os gráficos e o relatório, instale os pacotes de [requirements.txt](projeto/requirements.txt):

```sh
python3 -m pip install -r projeto/requirements.txt
```

| Pacote | Versão conferida | Uso no projeto |
|---|---|---|
| NumPy | 2.3.5 | Montar a sequência de tamanhos usada nas curvas teóricas |
| Matplotlib | 3.10.8 | Gerar os seis gráficos em PNG |
| ReportLab | 4.4.9 | Gerar o relatório PDF a partir dos textos e resultados |

GCC e binutils são ferramentas do sistema, não pacotes instalados por pip. A geração do PDF também usa a fonte DejaVu Sans em `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`. Esse arquivo faz parte do pacote `fonts-dejavu-core` em sistemas Debian e Ubuntu.

## Compilar, testar e demonstrar

Execute os comandos abaixo a partir da raiz do repositório:

```sh
python3 projeto/scripts/compilar.py --sanitizers
python3 projeto/tests/test.py
python3 projeto/src/main.py heap 3 1 3 0 65535
python3 projeto/src/main.py bitmap 3 1 3 0 65535
```

O primeiro comando compila o código C e executa os testes nativos. Depois, repete os testes em uma compilação separada com AddressSanitizer e UndefinedBehaviorSanitizer, que ajudam a detectar acessos inválidos à memória e comportamento indefinido. Os objetos e executáveis ficam em `projeto/build/`, fora do controle de versão.

Para executar o teste C sem Python, depois da compilação:

```sh
./projeto/build/test_nativo
```

A solução embarcada está em [heap.c](projeto/src/heap.c). Sua função pública é `size_t heap_unique(uint16_t *a, size_t n)`. Ela pode ser ligada diretamente a um programa C e não depende de um interpretador.

O arquivo `heap.py` é apenas a ponte usada nos testes e nas demonstrações do computador. Ele compartilha o vetor com a função C, sem copiar os elementos. Python e ctypes não fazem parte do programa proposto para o sensor, e sua memória não é apresentada como parte dos 96 bytes do algoritmo embarcado.

## Refazer as medições

```sh
python3 projeto/scripts/experimentos.py
```

A coleta usa 1.000, 100.000 e 10.000.000 de leituras. Para cada algoritmo e tamanho, há um aquecimento e três rodadas medidas. Os dois algoritmos recebem os mesmos dados, gerados com a semente 20261108.

Gerar a entrada, copiar o vetor, preparar o ponteiro C, validar a resposta e imprimir ficam fora do tempo medido. A chamada C inclui o custo de ctypes. O bitmap também passa por uma execução completa com rastreamento de memória para cada tamanho, separada dos tempos de desempenho.

Uma nova coleta substitui os dados atuais. Para repetir apenas a verificação de memória e preservar os tempos já registrados:

```sh
python3 projeto/scripts/experimentos.py --somente-memoria
```

Essa opção exige que as fontes e o binário ainda correspondam à versão medida. Se houve mudança, refaça a coleta completa.

## Gerar novamente os gráficos e o PDF

```sh
MPLCONFIGDIR=/tmp/pjbl-mpl python3 projeto/scripts/documentos.py
```

O comando lê os dados existentes, refaz as oito curvas teóricas, gera os seis gráficos e atualiza o relatório em Markdown e PDF. Ele não executa novos benchmarks. Para mudar o texto do relatório, edite `projeto/docs/analise_teorica.md` ou as frases definidas em `projeto/scripts/documentos.py`; alterações feitas apenas em `relatorio.md` serão substituídas na próxima geração.

## Entender os dados e a memória

| Arquivo | Conteúdo |
|---|---|
| [resultados_empiricos.csv](projeto/dados/resultados_empiricos.csv) | Os 18 tempos individuais, com algoritmo, linguagem, tamanho e quantidade de únicos |
| [resumo.json](projeto/dados/resumo.json) | Mediana, mínimo e máximo das seis combinações |
| [ambiente.json](projeto/dados/ambiente.json) | Sistema, versões, compilador, opções de compilação, semente e hashes das fontes |
| [memoria.json](projeto/dados/memoria.json) | Evidências de memória C e Python, com o método identificado em cada registro |
| [previsoes.csv](projeto/dados/previsoes.csv) | Os 808 pontos calculados das oito estratégias não implementadas, em logaritmo de base dez |
| [testes.txt](projeto/dados/testes.txt) | Registro dos testes C, da execução com sanitizadores e da integração Python |

Para C, o GCC informa 48 bytes de pilha para `heap_unique` e 32 bytes para `sift`. As duas funções ficam ativas juntas durante uma descida. Somando 16 bytes de margem, temos **48 + 32 + 16 = 96 bytes**, abaixo dos 256 permitidos. O código não usa recursão, cópia da entrada ou alocação dinâmica. O arquivo de memória preserva o relatório bruto do compilador, a desmontagem e os hashes do objeto e da biblioteca.

Esse limite independe de n para o objeto avaliado. Ele foi conferido na mesma compilação usada pela biblioteca e pelo teste C. Se o compilador, as opções ou o alvo mudarem, a análise precisa ser refeita. O programa chamador e as interrupções precisam de suas próprias reservas no sistema embarcado real. O enunciado já considera o vetor de entrada residente na memória.

Para Python, os valores são picos observados por tracemalloc. Eles não representam toda a memória do interpretador. Por isso, os gráficos distinguem o limite de pilha C dos picos rastreados do bitmap. Nenhum desses valores deve ser confundido com o RSS, que é o consumo residente do processo inteiro.

## Consultar a entrega e o material de estudo

[Relatório PDF](projeto/relatorio.pdf) · [Fonte do relatório](projeto/docs/relatorio.md) · [Análise teórica](projeto/docs/analise_teorica.md) · [Roteiro de apresentação](Estudos/apresentacao.md) · [Contas e introdução ao C](Estudos/Matematica.md) · [Checklist](Estudos/Checklist.md)

As funções modificam a entrada e retornam a quantidade de únicos, chamada u. Apenas o prefixo a[0:u] é a resposta. Heap Sort C entrega ordem crescente; bitmap Python preserva a ordem das primeiras ocorrências. A função C aceita NULL quando n=0. Na infraestrutura Python, o vetor vazio é um array('H') sem elementos. Conjuntos e ordenação nativa aparecem apenas na validação.

O limite de memória Embarca foi demonstrado na compilação local, mas nenhuma placa específica foi fornecida para teste. O bitmap teve mediana local abaixo de dois segundos; ainda é necessário executar na máquina de referência da disciplina. O prazo de dois segundos pertence à Datacenter, não à Embarca.

Também continuam pendentes a aprovação do par e a confirmação da interpretação de linguagem, pois o enunciado recomenda C e Python, mas menciona Pascal em outros trechos. Essas confirmações dependem do professor.

O Git contém as fontes, as evidências e os documentos necessários. Arquivos de compilação e caches ficam fora. Se a entrega for compactada, exclua `projeto/build` e `__pycache__` da cópia enviada. O repositório Git também é uma forma de entrega permitida pelo PDF.
