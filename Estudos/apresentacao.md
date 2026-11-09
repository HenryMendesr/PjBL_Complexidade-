# Apresentação: roteiro explicado e preparação para a defesa

**Integrantes:** Henry Rodrigues, Rafael Maluf e Matheus.

Este documento serve para ensaiar a apresentação e entender a razão de cada afirmação. As falas são sugestões: a equipe deve explicá-las com as próprias palavras. Todos precisam conhecer as duas implementações e a análise das outras oito estratégias. A divisão entre os integrantes pode ser feita depois do ensaio, sem deixar uma pessoa responsável por saber apenas uma parte.

A versão principal abaixo ocupa aproximadamente 12 a 15 minutos, dependendo da demonstração. Ajustar ao tempo informado pelo professor. As perguntas e os aprofundamentos no final são material de reserva, não precisam ser lidos integralmente na apresentação.

## Antes de começar

Na raiz do repositório, verificar os comandos:

```sh
python3 projeto/src/main.py heap 3 1 3 0 65535
python3 projeto/src/main.py bitmap 3 1 3 0 65535
python3 projeto/tests/test.py
```

Deixar abertos o relatório, os seis gráficos e os arquivos heap.py e bitmap.py. Os testes pequenos são rápidos; **não executar a coleta inteira durante a apresentação**, a menos que haja tempo reservado. No computador usado na coleta, cada rodada de Heap Sort com dez milhões de leituras levou cerca de 70 segundos, e a coleta de tempo faz aquecimento mais três rodadas por combinação. O coletor também realiza rodadas separadas de memória: a última do heap levou cerca de 15 minutos com tracemalloc ativo. Isso não substitui o tempo de desempenho de aproximadamente 70 s.

Preparar a explicação a partir dos [dados reais](../projeto/dados/resumo.json). Se houver uma nova coleta, atualizar as falas numéricas a partir desse arquivo. Os valores deste roteiro correspondem à coleta Python atualmente entregue.

## Visão geral do tempo

| Momento | Conteúdo | O que precisa ficar claro |
|---|---|---|
| 0–1 min | Problema e dois clientes | Mesmo problema, restrições diferentes |
| 1–2 min | Exemplo e contrato | O retorno u delimita a saída válida |
| 2–4 min | Heap Sort e compactação | Como funciona, por que está correto e seu custo |
| 4–6 min | Bitmap | Como um bit identifica um valor e por que é linear |
| 6–8 min | Resultados e gráficos | Medição real, hipótese e limitações são coisas diferentes |
| 8–11 min | Quatro estratégias exageradas | Rejeitar com contas e recursos específicos |
| 11–13 min | Força bruta, hash, árvore e Bloom | Comparar escolhas e explicar o domínio limitado |
| 13–15 min | Recomendação e pendências | Concluir somente o que as evidências permitem |

## 1. Abertura: qual problema estamos resolvendo?

**Fala sugerida:**

> Nosso problema é eliminar leituras repetidas de sensores. Cada leitura está entre zero e 65535. São 65536 valores possíveis. O cliente Embarca permite só 256 bytes além do vetor de entrada. O cliente Datacenter quer processar dez milhões de leituras em menos de dois segundos na máquina da disciplina. Vamos mostrar como as restrições orientam a escolha e o que a implementação Python efetivamente conseguiu demonstrar.

Escrever ou mostrar:

```text
n = quantidade total de leituras
u = quantidade de valores diferentes que apareceram
D = quantidade de valores possíveis = 65536
u ≤ min(n,D)
```

**Raciocínio:** n e u não são a mesma coisa. Se cem mil posições só podem receber 65536 valores, alguma repetição é inevitável. Isso não significa que todos os valores aparecem: dez milhões de zeros têm u=1.

A implementação está toda em Python, a linguagem escolhida pela equipe. A restrição Embarca continua sendo 256 bytes; a escolha da linguagem não altera o teto do enunciado.

## 2. Demonstrar a entrada, a saída e o contrato

Executar os dois comandos do exemplo. A entrada é:

```text
[3, 1, 3, 0, 65535]
n=5, u=4
```

| Algoritmo | Saída válida esperada |
|---|---|
| Heap Sort | [0,1,3,65535] |
| Bitmap | [3,1,0,65535] |

**Fala sugerida:**

> As duas respostas contêm exatamente os mesmos valores únicos. Heap Sort os entrega em ordem crescente. Bitmap mantém a ordem em que cada valor apareceu pela primeira vez. As funções alteram o próprio vetor e retornam quatro. Só as primeiras quatro posições são a resposta; o conteúdo que sobra depois disso não faz parte da saída.

Explicar que a entrada é `array('H')`, com dois bytes por elemento na máquina avaliada. Não é uma lista de inteiros Python como armazenamento de entrada, embora índices e temporários das funções sejam objetos Python.

**Critério de corretude:** a saída não pode inventar valor, perder valor nem repetir um valor dentro do prefixo válido. Os testes verificam essas propriedades com set e a ordem com sorted/dict, somente na infraestrutura de teste.

## 3. Heap Sort: mostrar a lógica antes de mostrar os laços

Abrir [heap.py](../projeto/src/heap.py). Identificar três etapas: construir max-heap, retirar máximos, compactar os únicos.

**Fala sugerida:**

> Um max-heap garante que cada pai é maior ou igual aos filhos. Assim o máximo fica na raiz. Ainda não é uma ordenação completa. Tiramos esse máximo, colocamos na última posição que ainda não era definitiva e restauramos o heap do prefixo. Repetindo isso, o sufixo vai ficando ordenado.

### Exemplo de construção

Usar a mesma entrada para evitar trocar de problema durante a explicação:

| Etapa | Vetor | Por que aconteceu? |
|---|---|---|
| Entrada | [3,1,3,0,65535] | Valores originais |
| Ajustar pai no índice 1 | [3,65535,3,0,1] | O maior filho de 1 era 65535 |
| Ajustar raiz | [65535,3,3,0,1] | 65535 sobe; a possível violação desce e é corrigida |

No heap resultante, a raiz é o maior valor. Para a primeira extração, trocar a raiz com a última posição produz [1,3,3,0,65535]. Restaurar o prefixo de tamanho quatro produz [3,1,3,0,65535]. O 65535 já está na posição final e não participa mais do heap.

Após todas as extrações, obtemos [0,1,3,3,65535]. Não é preciso narrar todas as trocas se o tempo for curto; o essencial é explicar a propriedade que se repete.

### Por que isso é correto?

Antes de cada extração, o prefixo é um heap e o sufixo está ordenado, com valores maiores ou iguais aos do prefixo. A raiz é o máximo restante, então colocá-la na fronteira do sufixo mantém essa propriedade. O prefixo diminui a cada passo, garantindo término.

No sift, escolher o maior filho é necessário: trocar com o menor poderia deixar o pai abaixo do outro filho. A possível violação só desce pela árvore, cuja altura é finita. O laço é iterativo e não cria uma cadeia recursiva de chamadas.

### Compactar depois de ordenar

| Leitura no vetor ordenado | Decisão | Prefixo válido |
|---|---|---|
| 0 | Primeiro valor | [0] |
| 1 | Diferente do último emitido | [0,1] |
| 3 | Diferente do último emitido | [0,1,3] |
| 3 | Igual ao último emitido; pular | [0,1,3] |
| 65535 | Diferente; escrever na próxima posição de saída | [0,1,3,65535] |

A escrita fica na região já lida. No último passo, o valor lido na posição 4 vai para a posição 3. Isso não destrói nenhuma leitura futura. A cauda pode ficar com outro 65535, mas está fora de a[0:u].

### Conta para explicar oralmente

> Construir o heap custa Θ(n), porque a maioria dos nós está perto das folhas. A soma das alturas é limitada por n/2+n/4+n/8+…, que é menor que n. Depois temos n−1 extrações, cada uma de custo no máximo O(log n). A ordenação tem limite O(n log n), e a compactação final é linear. Com todos iguais, as descidas param cedo e essa implementação tem melhor caso Θ(n).

O detalhe de soma de alturas está em [Matematica.md](Matematica.md). Não afirmar que a construção do heap é Θ(n log n), nem que toda entrada necessariamente leva Θ(n log n).

## 4. Bitmap: explicar a conta e acompanhar os bits

Abrir [bitmap.py](../projeto/src/bitmap.py).

**Fala sugerida:**

> Como conhecemos o domínio, podemos reservar um bit para cada leitura possível. Um bit zero significa que o valor ainda não apareceu; um bit um significa que já foi emitido. São 65536 bits, ou 8192 bytes, porque um byte tem oito bits.

Mostrar a conta:

```text
65536 ÷ 8 = 8192 B = 8 KiB
8192 ÷ 256 = 32 vezes o orçamento da Embarca, só em bits
```

A versão Python usa bytearray. Para localizar um valor x:

```text
byte = x // 8
bit dentro do byte = x % 8
máscara = 1 << bit
```

No código, `>> 3` equivale à divisão inteira por oito e `& 7` ao resto, pois x é não negativo. Não confundir com a versão antiga baseada em palavras de 64 bits: a implementação atual usa bytes.

### Acompanhar a mesma entrada

| Valor lido | Byte e máscara | Estado anterior | Ação e saída |
|---|---|---|---|
| 3 | Byte 0, máscara 00001000 | Bit zero | Marcar e emitir: [3] |
| 1 | Byte 0, máscara 00000010 | Bit zero | Marcar e emitir: [3,1] |
| 3 | Byte 0, máscara 00001000 | Bit um | Pular: [3,1] |
| 0 | Byte 0, máscara 00000001 | Bit zero | Marcar e emitir: [3,1,0] |
| 65535 | Byte 8191, máscara 10000000 | Bit zero | Marcar e emitir: [3,1,0,65535] |

O teste com `&` verifica o bit. A atualização com `|=` marca o bit sem apagar os outros. Todos os 65536 valores têm posições diferentes, então não há colisões como numa tabela hash.

**Por que é correto?** Antes de cada iteração, os bits representam exatamente os valores já lidos, e o prefixo de saída contém suas primeiras ocorrências. Se o bit era zero, o valor não tinha sido emitido; se era um, já tinha sido. A escrita ocorre atrás da leitura, como na compactação do heap.

**Conta de tempo:** inicializar os bytes custa Θ(ceil(D/8)); percorrer as leituras custa Θ(n). Total Θ(n+ceil(D/8)). Com D fixo, é linear em n para n≥1. A inicialização está incluída no benchmark.

## 5. Mostrar resultados reais e ler os gráficos

### Começar pelo gráfico mais simples

Abrir [tempo_medido.png](../projeto/graficos/tempo_medido.png). Ele contém só as duas implementações reais.

**Fala sugerida:**

> A coleta usou um aquecimento e três rodadas medidas por algoritmo e tamanho. Copiar e gerar a entrada, validar a resposta e imprimir ficaram fora do tempo. Inicializar as estruturas e compactar ficaram dentro. Os pontos mostram as medianas; as barras mostram mínimo e máximo, não intervalo de confiança.

Para dez milhões de leituras:

| Algoritmo | Mediana local | Mínimo–máximo |
|---|---|---|
| Heap Sort | 70,117608 s | 67,930714–72,476764 s |
| Bitmap | 1,041611 s | 0,973067–1,057751 s |

A razão 70,117607581/1,041610970≈67,32 descreve esta coleta: tempo mediano do bitmap cerca de 67 vezes menor. O bitmap consulta um bit por leitura; o heap faz descidas e trocas. Essa comparação não demonstra sozinha a causa de cada variação de cache ou escalonamento, nem uma razão universal para qualquer entrada/máquina.

### Depois, apresentar as oito alternativas

Abrir [tempo_comparativo.png](../projeto/graficos/tempo_comparativo.png).

> Só Heap Sort e bitmap foram implementados. As outras oito linhas são modelos teóricos com constantes explícitas, não benchmarks. Usamos custos nominais otimistas de operações compactas, sem calibração para Python. Big-O sozinho não fornece segundos.

Abrir [tempo_completo.png](../projeto/graficos/tempo_completo.png). Explicar:

> O eixo vertical mostra o expoente E de tempo=10^E segundos. E=3 significa mil segundos. E=1000 significa 10 elevado a mil segundos. O eixo comprime esses expoentes para não apagar Bogosort e subconjuntos por overflow ou por saírem da faixa prática.

Não ler E=1000 como mil segundos. Não afirmar que uma alternativa Python teria exatamente o tempo da linha hipotética.

### Memória e armazenamento

Abrir [memoria_algoritmos.png](../projeto/graficos/memoria_algoritmos.png), que mostra só as medições reais nas três escalas. A comparação com modelos compactos está em [memoria_comparativa.png](../projeto/graficos/memoria_comparativa.png); entrada, disco e processo estão em [armazenamento.png](../projeto/graficos/armazenamento.png).

> A memória Python foi medida separadamente com tracemalloc nas três escalas, em uma execução completa por algoritmo e tamanho, sem usar a duração rastreada como tempo de desempenho. Em n=1000, heap apresentou 380 B rastreados e bitmap 8553 B; os seis registros estão na tabela do relatório e em memoria.json. A amostra do heap já ultrapassa os 256 B. Ter três escalas medidas não representa uma contagem completa da memória do interpretador nem prova todas as entradas.

Fazer a conta pequena: 380−256=124 B acima do teto. O vetor de dez milhões ocupa 2n=20000000 B de payload, aproximadamente 19,07 MiB; ele é a entrada, separada dos extras. RSS é o pico do processo inteiro, com infraestrutura, não o consumo isolado do algoritmo.

## 6. Rejeitar as quatro estratégias exageradas com números

Aqui o objetivo é explicar uma conta de cada estratégia, não decorar uma sequência enorme de algarismos. Se necessário, deixar as fórmulas detalhadas abertas em [Matematica.md](Matematica.md).

### Bogosort — probabilidade e fatorial

> Embaralhar até ordenar tem probabilidade minúscula quando os valores são distintos. Para n=1000, válido no domínio, há 1000! permutações; log₁₀(1000!)≈2567,6. Mesmo supondo um custo extremamente favorável de um microssegundo por tentativa, o tempo esperado seria da ordem de 10²⁵⁶¹ segundos.

Explicar o exemplo menor [1,1,2]: há seis permutações rotuladas, mas duas levam à mesma sequência ordenada de valores. Então q=2/6 e a espera é três tentativas independentes, partindo de uma entrada desordenada. A fórmula geral é n!/∏cⱼ!. Com n>D, é obrigatório considerar repetições; não usar n! como se todos fossem distintos.

### Subconjuntos — folhas e materialização

> Enumerar todos os subconjuntos dá 2ⁿ folhas. Se guardar todos os elementos, cada posição aparece em metade dos subconjuntos: n2ⁿ⁻¹ elementos no total. Com dois bytes por elemento, só o payload ocupa n2ⁿ bytes.

Para n=1000, isso é aproximadamente 1,07×10³⁰⁴ B. A pilha também tem profundidade n+1; sob uma hipótese nominal de 16 B/frame, já seriam 16016 B. Streaming evita guardar todas as folhas, mas continua com tempo exponencial e pilha linear. Frames de 16 B são hipótese didática, não uma medição de Python.

### Unário — armazenamento e releituras

> Nosso formato grava x símbolos '1' e um delimitador '0'. Cada registro ocupa x+1 bytes. Como x≤65535, o total gravado está entre n e 65536n: é linear em n neste domínio. A representação pode ser exponencial nos bits de um valor, que é outra variável.

Para dez milhões de valores com média uniforme, o arquivo esperado tem 327,685 GB. Só escrever isso a 1 GB/s hipotético leva 327,685 s. A variante de deduplicação ainda relê registros anteriores; o tráfego esperado é 32768,5n(n+1)/2, de ordem quadrática para D fixo. Não confundir o custo de gravar com o de deduplicar.

### Matriz — todas as comparações

> Uma matriz de dez milhões por dez milhões tem 10¹⁴ células. São 100 TB se cada célula usar um byte ou 12,5 TB empacotando bits. Mesmo a um nanossegundo por célula, levaria 100000 segundos. O problema não exigiu guardar a auditoria de todas as comparações.

Lembrar que o PDF não impõe teto numérico de disco nem prazo para Embarca. Nesses recursos, distinguir inviabilidade prática de violação de uma restrição formal. O prazo formal de dois segundos pertence a Datacenter; a memória extra de 256 B pertence a Embarca.

## 7. Comparar força bruta, hash, árvore e Bloom

Explicar em uma frase a utilidade de cada uma e em outra o motivo da escolha atual.

| Estratégia | Raciocínio para a fala |
|---|---|
| Força bruta | Não precisa de uma estrutura grande, mas pode buscar entre até u únicos por leitura. Custo máximo de comparações: u(u−1)/2+(n−u)u. Com iguais é linear; com distintos permitidos pelo domínio pode ser quadrático |
| Hash | Processa n leituras e guarda só u chaves. Esperado linear com boa dispersão, mas colisões e alocação adicionam custo. Não foi implementado para o trabalho |
| Árvore balanceada | Guarda u nós e dá limite de busca logarítmico em u; útil para ordenação dinâmica em domínio amplo. Aqui não foi exigido esse serviço e temos acesso direto por bit |
| Bloom | Permite falsos positivos; na deduplicação pode descartar um valor inédito. Para capacidade D e 1% aproximado com k=7, o filtro exige 78586 B, maior que o bitmap exato de 8192 B |

Se perguntarem pela média, declarar a distribuição: a palavra «médio» não é sinônimo de «sempre» nem de «qualquer entrada». Se perguntarem pelo espaço, distinguir quantidade de chaves guardadas, pilha, heap, disco e entrada.

## 8. Encerramento: o que concluímos?

**Fala sugerida:**

> O domínio de 16 bits permite ao bitmap resolver exatamente o problema com trabalho linear e uma estrutura pequena para Datacenter. A mediana local para dez milhões ficou abaixo de dois segundos, mas precisamos da máquina da disciplina para confirmar esse requisito. Heap Sort mostra ordenação e compactação sem vetor auxiliar, porém a versão Python excedeu os 256 B na amostra rastreada. Portanto não declaramos a solução Embarca aprovada. A equipe escolheu Python para compreender e defender a implementação, mantendo explícitas as limitações e as confirmações pendentes com o professor.

Encerrar com a recomendação e as evidências, não com «todos os requisitos foram cumpridos». Permanecem pendentes aprovação do par, aceitação da linguagem diante das menções a Pascal e teste na referência.

## Perguntas prováveis e raciocínio para responder

**Por que a entrada pode ter dez milhões de posições se só há 65536 valores?** O domínio limita quais valores podem aparecer, não quantas vezes aparecem. Repetições permitem n muito maior que D; u continua limitado por D.

**Por que não basta comparar os dois algoritmos entre si?** Eles poderiam compartilhar um erro. Os testes usam uma referência independente e verificam conjunto, quantidade, unicidade e ordem. Além dos exemplos conhecidos, há enumeração de entradas pequenas sobre {0,64,65535} e casos com o domínio completo.

**Por que só retornar u, sem devolver um vetor novo?** A resposta já está no prefixo do vetor alterado. Evitar outro vetor é uma decisão importante quando se estuda espaço auxiliar.

**A cauda repetida significa erro?** Não. O contrato define a[0:u] como saída. Mostrar os n elementos como se fossem a resposta seria usar a função incorretamente.

**Por que não Quick Sort?** A versão recursiva usual tem pilha dependente de n e pior tempo quadrático. Escolhemos Heap Sort iterativo para estudar uma estrutura de chamadas de profundidade constante. Isso, por si só, não resolveu os 256 B em Python.

**O(1) significa zero bytes ou 256 bytes?** Não. Significa que a quantidade de palavras não cresce com n no modelo adotado. Uma constante de 8192 B continua sendo O(1) em n, e ainda assim é 32 vezes o teto. Em Python há também objetos e execução interna; com índices arbitrariamente grandes é preciso considerar seus bits.

**O bitmap tem colisões?** Não neste domínio: cada valor tem um bit exclusivo. O valor 65535 usa o último byte, índice 8191, bit 7. Essa conta também explica por que o extremo não acessa fora do vetor.

**Bloom a 1% mantém todos os únicos com 99% de chance?** Essa interpretação não decorre da taxa por consulta. O falso positivo pode ocorrer em uma das várias consultas inéditas e causar perda na saída. A fórmula é aproximada sob hipóteses de hashes e ocupação; não é uma garantia determinística da saída inteira.

**Por que u, não n, no tamanho do hash e da árvore?** Leituras repetidas não acrescentam novas chaves. Processamos n elementos, mas armazenamos no máximo u distintos, limitado por D.

**Bogosort sempre leva n! tentativas?** Não. Repetições dividem o resultado por ∏cⱼ!, e uma entrada já ordenada termina na checagem inicial. A espera geométrica exige tentativas uniformes independentes e não é limite de pior caso.

**Power set precisa guardar tudo?** Não. Streaming evita a materialização, mas não o número exponencial de visitas. A nossa curva escolhe materializar e inclui custos nominais adicionais ao payload; a análise distingue as variantes.

**Unário é exponencial?** Pode ser exponencial no número de bits de um valor. Com valores limitados a 16 bits, seu volume é no máximo 65536n bytes no formato estudado, linear em n. A variante de releituras torna o tráfego de deduplicação quadrático.

**O(n) é sempre mais rápido que O(n log n)?** Não para todo tamanho e ambiente: constantes, distribuição e implementação importam. Aqui há também uma razão estrutural para o bitmap e medições que sustentam a comparação local.

**Por que os modelos de hash/árvore podem parecer rápidos perto do Python medido?** Os custos dos modelos são nominais e otimistas, de representação compacta; não são benchmarks dessas alternativas em CPython. O gráfico não autoriza prometer esses segundos numa implementação futura.

**Os 380 B incluem o vetor?** O vetor foi criado antes de iniciar o rastreamento da rodada de memória. O pico registra alocações rastreadas durante a função e não representa toda a memória interna do interpretador. Há uma execução completa rastreada em cada uma das três escalas, separada dos tempos. Ainda não é uma contagem de toda a RAM ou de toda a pilha. A capacidade dos frames foi calculada separadamente para o CPython instalado e não deve ser somada diretamente ao pico rastreado.

**A mediana de 1,04 s comprova o prazo?** Comprova esse resultado local na coleta apresentada. O enunciado pede a máquina da disciplina; a confirmação formal continua pendente.

## Ensaio final da equipe

Cada integrante deve conseguir, sem ler uma resposta pronta:

1. Diferenciar n, u e D com um exemplo.
2. Explicar por que construir o heap é linear e por que extrair máximos pode custar n log n.
3. Localizar os bits de 0, 8 e 65535 no bytearray.
4. Refazer uma conta de cada estratégia exagerada.
5. Dizer o que foi medido, o que foi modelado e o que não foi comprovado.
6. Demonstrar as duas funções e explicar a região a[0:u].

Usar a [Checklist](Checklist.md) para conferir a situação da entrega e [Matematica.md](Matematica.md) para revisar os passos das contas.

## Como responder à crítica dos 256 bytes

**Fala sugerida:**

> A revisão está correta: nossa versão Python não cumpre os 256 bytes e nós não devemos anunciá-la como pronta para Embarca. Corrigimos a cobertura da coleta de memória, executando as duas funções completas nas três escalas. Além do pico rastreado, verificamos separadamente o espaço dos frames do CPython. A equipe optou por manter Python, então a limitação permanece registrada em vez de ser escondida ou dispensada por conta própria.

Se o professor pedir a conta da pilha, mostrar 72+8×(6+6)=168 B para heap_unique e 72+8×(5+4)=144 B para sift. Como ficam ativos juntos, somam 312 B de capacidade no layout do interpretador usado. Não são frames de uma versão C anterior nem um número de RSS. O cálculo não inclui todos os objetos ou toda a pilha nativa e não deve ser somado diretamente aos 380 B de tracemalloc.

Se perguntarem se «o algoritmo está errado», separar corretude e adequação: os testes e invariantes sustentam a deduplicação exata, mas uma solução correta pode descumprir um orçamento de memória. Se perguntarem se «o professor aceitar Python resolve», explicar que aprovação da linguagem e cumprimento do limite são requisitos diferentes. Uma dispensa de requisito precisaria ser explicitamente dada pelo professor; não existe tal confirmação nesta entrega.

O resultado de 1,04 s do bitmap também deve ser apresentado como mediana local. A frase «cumpre a meta na máquina testada» descreve a coleta; a frase «cumpre a exigência da disciplina» dependeria da máquina de referência.
