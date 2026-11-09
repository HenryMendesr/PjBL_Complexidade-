# Contas e raciocínio do trabalho

Este material explica como chegar aos resultados, para que os integrantes consigam refazer as contas e defendê-las. A análise que faz parte da entrega permanece em [analise_teorica.md](../projeto/docs/analise_teorica.md). 

## 1. O que estamos contando?

| Símbolo | Significado | Exemplo |
|---|---|---|
| n | Quantidade de leituras recebidas, incluindo repetições | Em [3,1,3,0,65535], n=5 |
| u | Quantidade de valores diferentes que aparecem | Nesse vetor, u=4 |
| D | Quantidade de valores possíveis no domínio | D=65536, pois a faixa vai de 0 até 65535 |

O zero também conta. Por isso o tamanho do domínio é 65535−0+1=65536.

Sempre vale **0≤u≤min(n,D)**. Há dois limites: não podemos ter mais distintos do que leituras, nem mais distintos do que valores possíveis. No vetor vazio, n=u=0. Se n>0, u≥1.

Para n=100000 ou n=10000000, é impossível todas as leituras serem distintas: existem mais posições do que valores possíveis. É o princípio das gavetas. Isso não obriga todos os 65536 valores a aparecerem: um vetor com dez milhões de zeros continua tendo u=1.

## 2. Como saber que uma saída está correta?

Para a entrada [3,1,3,0,65535], o conjunto esperado é {0,1,3,65535}. A saída deve cumprir três condições:

1. Não pode inventar valor que não estava na entrada.
2. Não pode perder nenhum dos valores que apareceram.
3. Não pode repetir um valor na parte válida da saída.

Só conferir u não basta. [0,1,3,99] tem quatro elementos distintos, mas perdeu 65535 e inventou 99.

Nossas funções modificam o vetor e retornam u. **A resposta está apenas em a[0:u].** A cauda pode continuar com leituras repetidas e não faz parte da resposta. Heap Sort entrega os únicos crescentes. Bitmap entrega na ordem das primeiras ocorrências. Para comparar as duas soluções, conferimos conjunto e quantidade; para conferir o contrato completo, verificamos também a ordem de cada uma.

Nos testes, set, sorted e dict são referências independentes. Eles não são usados pelas duas funções de deduplicação de produção.

## 3. O, Θ e a diferença entre tempo e segundos

O(f(n)) é um limite superior assintótico. Θ(f(n)) diz que, sob as hipóteses declaradas, a ordem de crescimento também é um limite inferior, a menos de fatores constantes.

Se uma análise prova no máximo n log₂n operações, ela fornece O(n log n). Para afirmar Θ(n log n), também precisamos justificar o limite inferior no caso estudado. Não podemos usar o pior caso para descrever automaticamente todas as entradas.

Melhor caso é a entrada mais favorável; pior é a mais desfavorável; caso médio exige dizer qual distribuição de entradas ou escolhas aleatórias está sendo considerada. Sem essa hipótese, uma média universal não está definida.

Big-O não fornece segundos. Um modelo T=c·f(n) só vira uma estimativa numérica quando declaramos c. Nos gráficos das oito alternativas, c=10⁻⁹ s por operação nominal é uma hipótese otimista de representação compacta. Não é uma medição de C ou Python e não foi calibrado por benchmark dessas oito estratégias.

## 4. Força bruta: de onde vem o quadrático?

Imagine ler cada valor e procurá-lo no prefixo dos únicos já emitidos. Se todas as n leituras forem diferentes, as buscas fazem:

```text
1ª leitura: 0 comparações, porque o prefixo está vazio
2ª leitura: 1 comparação
3ª leitura: 2 comparações
...
nª leitura: n−1 comparações
```

A soma é 0+1+…+(n−1)=n(n−1)/2. Para n=1000, são 1000×999/2=499500 comparações. O termo dominante é n², portanto o pior caso genérico é Θ(n²), quando o domínio permite n distintos.

Se só existem u distintos, introduzi-los custa u(u−1)/2. Cada uma das n−u repetições pode exigir até u comparações. Logo:

**Cmax=u(u−1)/2+(n−u)u.**

Esse máximo é atingível: introduza os u valores primeiro e depois repita sempre o último valor do prefixo. Exemplo n=5, u=3: 0+1+2+3+3=9 comparações.

O custo completo inclui ler e emitir, então é Θ(n+C). Com todos iguais, depois da primeira leitura basta uma comparação por leitura restante: Θ(n). Com domínio fixo, u≤D implica O(nD); não podemos fingir que u continua crescendo até dez milhões.

Para n=10⁷ e u≈65536, a aproximação nu/2 dá 327680000000 comparações. A 1 ns/comparação hipotético, seriam 327,68 s. A aproximação pressupõe posições médias; não é o número exato para qualquer entrada.

## 5. Heap Sort: por que construir o heap não custa n log n?

Um max-heap é uma árvore binária armazenada no próprio vetor em que cada pai é maior ou igual aos filhos. Isso não significa que o vetor todo esteja ordenado. A garantia útil é que o máximo está na raiz.

Para uma posição i, os filhos são 2i+1 e 2i+2. A rotina sift compara os filhos existentes, escolhe o maior e troca com o pai se necessário. Se houver troca, a possível violação desce. A altura restante diminui, então o procedimento termina.

Uma descida a partir da raiz pode custar O(log n). Mas, na construção, quase todos os nós estão perto das folhas e não descem essa altura toda. Há no máximo floor(n/2ʰ) nós com altura pelo menos h. Somando o trabalho por nível:

```text
Soma das alturas ≤ n/2 + n/4 + n/8 + ... < n
```

A construção visita os nós internos e custa Θ(n). Multiplicar n pela altura da raiz seria um limite superior frouxo para essa etapa, não a análise justa.

Depois fazemos n−1 extrações. Trocamos o máximo da raiz com a última posição ainda não definitiva e restauramos o heap reduzido. Cada extração custa no máximo O(log n), portanto a ordenação tem limite O(n log n). A varredura final de compactação custa Θ(n) e não muda esse limite.

Com chaves distintas, o caso médio sobre permutações uniformes e o pior caso genérico têm Θ(n log n). Com todos iguais, a descida para cedo e o total dessa implementação é Θ(n). Não se deve apresentar Θ(n log n) como tempo de toda entrada, nem aplicar o argumento de n chaves distintas quando n>D.

A profundidade de chamadas é constante porque sift usa laço, não recursão. Na versão atual em C, o compilador fornece frames static de 48 B e 32 B. Somar o caminho e a margem de 16 B dá 96 B. O significado de O(1) não forneceu sozinho esse número: o build foi auditado.

## 6. Bitmap: a conta dos 8192 bytes e os índices

Há um bit para cada valor possível. Um byte tem oito bits:

**65536 bits ÷ 8=8192 bytes=8 KiB.**

O código atual usa bytearray e trabalha por bytes. Não usa palavras de 64 bits. Para o valor x:

```text
índice do byte = x // 8 = x >> 3
posição dentro do byte = x % 8 = x & 7
máscara = 1 << posição
```

Exemplos:

| x | Byte | Posição do bit | Máscara binária |
|---|---|---|---|
| 0 | 0 | 0 | 00000001 |
| 3 | 0 | 3 | 00001000 |
| 7 | 0 | 7 | 10000000 |
| 8 | 1 | 0 | 00000001 |
| 65535 | 8191 | 7 | 10000000 |

O teste `seen[index] & mask` verifica se o bit já estava marcado. A operação `seen[index] |= mask` marca o bit sem apagar os outros.

Antes de ler a posição i, os bits representam exatamente os valores já lidos. Se o bit de x estava zero, x é inédito: marcamos e emitimos. Se estava um, x já foi emitido e é descartado. Esse invariante explica por que não se perde um único nem se emite duplicata.

O algoritmo inicializa os 8192 bytes e percorre as n leituras. Seu custo, no modelo de operações por byte, é Θ(n+ceil(D/8)). Para D fixo, é Θ(n+1), incluindo a chamada vazia. A forma usual Θ(n) considera n≥1.

A inicialização entra no cronômetro. Só os bits já usam 8192/256=32 vezes o orçamento da Embarca. Em Python ainda há cabeçalho e outros objetos. Portanto «constante em n» não significa «cabe em 256 B».

## 7. Hash e árvore: por que armazenam u, não n?

Um conjunto hash guarda apenas chaves diferentes. Ele processa n leituras, mas tem no máximo u chaves armazenadas. Com boa dispersão e carga controlada, uma consulta tem custo esperado O(1), e redimensionamentos são cobertos por amortização: total esperado Θ(n). Colisões adversas podem exigir buscas longas, chegando a O(nu), ou Θ(n²) no cenário genérico de n chaves distintas colidentes.

A árvore balanceada também armazena só u nós. Sua altura é O(log(u+1)); por isso o limite de tempo é O(n log(u+1)+u). Com todos iguais, as consultas podem ser constantes e o total Θ(n). Para buscas uniformes entre u chaves, o custo esperado por busca é Θ(log(u+1)). É preciso declarar a distribuição para falar de média.

As duas estruturas usam heap proporcional a u, mais administração. Árvores recursivas também usam pilha O(log(u+1)); uma versão com ponteiros de pais pode ser iterativa. Nenhuma delas garante os 256 B para qualquer u. No domínio pequeno conhecido, bitmap evita colisões e o custo de nós/ponteiros.

## 8. Bloom: como se calcula 1% e o que esse erro significa?

Um filtro de Bloom tem m bits e usa k hashes por valor. Se todos os k bits consultados estão marcados, responde «provavelmente presente». Um falso positivo na deduplicação significa considerar uma leitura inédita como repetida e **perder esse valor na saída**.

No modelo de hashes uniformes independentes e aproximação de independência entre os bits consultados:

**p≈(1−exp(−ku/m))ᵏ.**

A intuição é: exp(−ku/m) aproxima a chance de um bit ainda estar zero; um menos isso aproxima a chance de estar marcado; elevar a k aproxima a chance de os k bits estarem marcados.

No ótimo contínuo:

```text
k=(m/u)ln2
m=−u·ln(p)/(ln2)²
```

Para u=65536 e p=0,01, m≈628166,386 bits. Porém k precisa ser inteiro. Fixando k=7, recalculamos:

**m≥−7u/ln(1−p^(1/7)).**

Arredondar a bytes resulta em 78586 B, ou 628688 bits. Substituir na aproximação dá p≈0,0099996885, isto é, aproximadamente 0,99996885%. Usar 78521 B e somente arredondar k para sete daria aproximadamente 1,0039%, ligeiramente acima da meta.

O filtro dos modelos é dimensionado para capacidade D, não para n=10⁷, porque nunca haverá mais de D distintos. Quando u=D não há valor inédito restante dentro do domínio; a capacidade máxima é uma escolha conservadora para os estados anteriores.

A taxa p é uma aproximação por consulta sob hipóteses. Ela não garante que a saída inteira tenha só 1% de chance de erro. O filtro não foi implementado: não existe taxa empírica dele neste projeto. O bitmap é menor e exato neste domínio, por isso foi escolhido.

## 9. Bogosort: de onde vem o fatorial e como as repetições mudam a conta?

Com n objetos rotulados, há n! permutações. Se os valores são todos distintos, só uma ordenação de valores serve: a probabilidade de sucesso por embaralhamento uniforme é q=1/n!.

Com repetições, trocar objetos de mesmo valor não muda a sequência de valores. Se as multiplicidades são c₁,…,cᵤ, há ∏cⱼ! permutações rotuladas que resultam na sequência ordenada. Assim:

```text
q=∏cⱼ!/n!
E[tentativas]=1/q=n!/∏cⱼ!
```

Exemplo [1,1,2]: n!=6, produto de fatoriais=2!×1!=2; q=2/6=1/3 e a espera é três tentativas para embaralhamentos independentes de uma entrada inicialmente desordenada. Se já ordenada, a checagem inicial termina sem embaralhar.

Para n=1000 distintos, log₁₀(1000!)≈2567,604644222, então 1000!≈4,02×10²⁵⁶⁷. Se cada tentativa custasse n×10⁻⁹=10⁻⁶ s, o tempo esperado seria ≈4,02×10²⁵⁶¹ s. Trata-se de uma hipótese extremamente favorável, não benchmark.

Em n>D, não podemos usar «todos distintos». Os modelos usam contagens balanceadas e o multinomial correspondente. O pior número de tentativas não tem teto finito quando q<1; «tempo esperado» não é garantia de terminar em um prazo.

## 10. Power set: contar subconjuntos não é contar elementos armazenados

Cada posição pode entrar ou não entrar. São duas escolhas por posição: 2ⁿ subconjuntos. Uma árvore binária completa de decisões tem 2ⁿ folhas e 2ⁿ⁺¹−1 nós.

Para n=3, os oito subconjuntos das posições são vazio, três singletons, três pares e o trio. A soma dos tamanhos é 0+3×1+3×2+1×3=12.

Em geral, cada posição aparece em metade dos subconjuntos: n×2ⁿ⁻¹ elementos armazenados no total. Com dois bytes por elemento, o payload é:

**2×n×2ⁿ⁻¹=n2ⁿ bytes.**

Só enumerar sem copiar exige Θ(2ⁿ) visitas e pode trabalhar em streaming, sem guardar todas as folhas. Materializar todos os elementos exige Θ(n2ⁿ) tempo e payload, mais descritores. A recursão mantém n+1 níveis, portanto pilha linear.

Para n=1000: 2¹⁰⁰⁰≈1,0715×10³⁰¹ subconjuntos; payload ≈1,0715×10³⁰⁴ B. Com hipótese nominal de 16 B/frame, 1001 níveis usam 16016 B, já acima de 256 B. Não são frames medidos de Python. A curva soma ainda descritores e trabalho, com as hipóteses da análise. Não há como endereçar tais volumes numa máquina comum de 64 bits.

## 11. Unário: por que não é exponencial em n neste trabalho?

O formato estudado grava x bytes '1' seguidos de um byte '0'. Por exemplo, x=3 vira `1110`; x=0 vira `0`. O delimitador permite representar zero e distinguir registros. O tamanho de cada registro é Lⱼ=xⱼ+1.

Logo S=ΣLⱼ. Como 0≤xⱼ≤65535:

**n≤S≤65536n bytes.**

Com domínio fixo, o armazenamento é linear em n. O crescimento pode ser exponencial em b, o número de bits de um único valor: se x pode chegar a 2ᵇ−1, seu unário pode ter 2ᵇ símbolos. São variáveis diferentes.

Gravar não deduplica. Na variante analisada, cada registro é comparado com todos os anteriores, sem encerrar cedo. O registro j é escrito uma vez e relido n−j vezes. Por isso:

**V=Σ(j=1..n)(n−j+1)Lⱼ.**

Exemplo de comprimentos [1,2,3]: gravar custa 6 B; as buscas anteriores leem 0+1+(1+2)=4 B. Total 10 B, igual a 3×1+2×2+1×3.

Se cada comprimento tem média μ=32768,5, a linearidade da esperança dá E[V]=μn(n+1)/2. Para n=10⁷:

```text
E[S]=32768,5×10000000=327685000000 B
E[V]=32768,5×10000000×10000001/2
    =1638425163842500000 B
```

A 10⁹ B/s hipotético, só escrever E[S] leva 327,685 s; o tráfego completo leva aproximadamente 1,638×10⁹ s, cerca de 51,9 anos. Não foram incluídos seeks e CPU. Esse tempo é condicional à taxa assumida, não medição real. O PDF não define teto de disco, portanto falamos em inviabilidade prática de armazenamento e em tempo do modelo, sem inventar uma restrição formal de capacidade.

## 12. Matriz: converter células para bytes

Uma matriz n×n tem n² células. Em um byte por célula, ocupa n² B; empacotada em bits, ceil(n²/8) B. O ceil arredonda para cima porque não podemos alocar uma fração de byte.

Para n=10⁷:

```text
n²=10¹⁴ células
em bytes: 10¹⁴ B=100 TB decimais
em bits: 10¹⁴/8=12500000000000 B=12,5 TB
```

12,5 TB decimais correspondem a aproximadamente 11,37 TiB, pois 1 TiB=2⁴⁰ B. Mesmo n=1000 exige 1000000/8=125000 B empacotados, muito além de 256 B.

Construir todas as comparações custa Θ(n²), inclusive com todos os valores iguais, porque a variante exige preencher a auditoria inteira. A 1 ns/célula hipotético: 10¹⁴×10⁻⁹=100000 s, ou 27,78 h. Em n=10, o payload em bits seria ceil(100/8)=13 B e pode fazer sentido se uma auditoria pequena for necessária.

## 13. Como ler nossos números reais

Os dados estão em [resumo.json](../projeto/dados/resumo.json), a memória e evidências em [memoria.json](../projeto/dados/memoria.json) e o ambiente em [ambiente.json](../projeto/dados/ambiente.json). A versão atual é mista: Heap Sort em C e bitmap em Python. Para n=10⁷:

| Medida | Heap Sort C | Bitmap Python |
|---|---|---|
| Mediana de tempo | 2,092282 s | 1,017508 s |
| Menor tempo | 2,000067 s | 0,986792 s |
| Maior tempo | 2,513517 s | 1,092296 s |

A mediana é o valor central dos três tempos ordenados. Os extremos mostram dispersão observada, não intervalo de confiança. Há um aquecimento antes das três rodadas. A razão das medianas é aproximadamente 2,06: nesta coleta grande, o bitmap levou cerca de 2,06 vezes menos tempo. Isso não é uma razão universal nem isola o efeito do algoritmo, porque as linguagens são diferentes. Nos vetores menores, Heap Sort C foi mais rápido; constantes e custo do interpretador também importam.

O payload da entrada em n=10⁷ é 2n=20000000 B, aproximadamente 19,07 MiB. O array do teste compartilha seu buffer com a função C sem copiar; a preparação do ponteiro acontece antes do cronômetro. O tempo C inclui a chamada via ctypes e seu custo de conversão/retorno, relevante nas escalas pequenas. Não se subtrai uma estimativa desse custo. Geração, cópia, validação e impressão ficam fora; inicialização do bitmap e compactação ficam dentro.

| n | Heap C: limite GCC + margem (B) | Bitmap Python: pico rastreado (B) |
|---|---|---|
| 1000 | 96 | 8553 |
| 100000 | 96 | 8553 |
| 10000000 | 96 | 8553 |

Os métodos são diferentes: para C, 96 B é um limite estático do objeto com margem, que independe de n e foi acompanhado de execução correta nos três tamanhos; não é pico de tracemalloc. Para Python, 8553 B é o pico observado em uma execução completa rastreada por tamanho, não toda a RAM do interpretador. Nenhum dos valores é o RSS do processo inteiro.

A recomendação Embarca agora se refere ao núcleo C, capaz de executar sem Python. A ponte de testes heap.py não faz parte do firmware. O limite 96≤256 foi comprovado no GCC/x86-64 e flags registrados. Para outro compilador/ABI, repetir a auditoria. O tempo de dois segundos pertence a Datacenter; o Heap Sort C ter mediana acima de dois segundos não viola um prazo inexistente da Embarca.

## 14. O que significa o eixo E dos gráficos completos?

Na faixa prática, o eixo mostra segundos em escala logarítmica. No gráfico completo, o número no eixo é o expoente E da relação tempo=10^E segundos:

| E | Tempo correspondente |
|---|---|
| −6 | 0,000001 s |
| 0 | 1 s |
| 3 | 1000 s |
| 1000 | 10¹⁰⁰⁰ s, não 1000 s |

O eixo de expoentes é comprimido para mostrar curvas astronomicamente grandes sem overflow. Memória usa a mesma ideia com bytes. Linhas tracejadas são modelos nominais; pontos e linhas contínuas identificam tempos das implementações C/Python medidos. As constantes dos modelos não autorizam dizer que hash ou árvore em Python executariam naqueles segundos.

## 15. Como concluir sem exagerar a evidência

O bitmap é a recomendação Datacenter pelo domínio conhecido, exatidão e trabalho linear; a mediana local ficou abaixo de dois segundos. A confirmação formal depende da máquina da disciplina. Heap Sort C ordena e compacta no próprio vetor e tem limite conservador local de 96 B, abaixo dos 256 B da Embarca. O programa C nativo de testes executa sem interpretador; a demonstração Python é apenas infraestrutura.

Aprovação do par, confirmação da interpretação de linguagem diante das menções a Pascal e defesa oral dos integrantes são questões externas. Um alvo embarcado diferente do build avaliado também precisa de auditoria própria. Não se inventa aprovação ou teste de uma placa não fornecida.

## 16. Pilha de C: como provar 96 B incluindo chamadas?

O compilador pode guardar uma variável em registrador, fazer spill na pilha ou reservar espaço de alinhamento. Por isso somar sizeof das variáveis do texto não basta. Usamos GCC com -fstack-usage nos objetos realmente ligados ao teste nativo e à biblioteca.

| Função | Frame reportado | Profundidade simultânea |
|---|---|---|
| heap_unique | 48 B, static | Ativo enquanto sift executa |
| sift | 32 B, static | Não chama outra função e não é recursivo |

O caminho mais profundo é heap_unique → sift: 48+32=80 B. Acrescentamos uma margem conservadora de 16 B na fronteira de chamada/ABI: 80+16=96 B. A folga para o requisito é 256−96=160 B. Esse cálculo já inclui os frames das duas funções e o contexto que o compilador efetivamente guardou na pilha; variáveis mantidas em registradores não alocam RAM extra.

O objeto não tem símbolos externos em nm -u. A fonte e a desmontagem não contêm chamadas de alocação ou recursão; não há vetor auxiliar nem cópia da entrada no algoritmo. O heap dinâmico é zero. As saídas brutas de .su e objdump, hashes e flags estão em memoria.json, e os artefatos podem ser regenerados pelo script de compilação.

`static` no relatório .su significa que o tamanho do frame é determinado estaticamente: ele não cresce com n. Não significa que medimos apenas n=1000 e supusemos o restante. O mesmo caminho de chamadas e os mesmos frames valem para os três tamanhos e para qualquer vetor válido suportado por esse build.

O alvo da prova é somente o núcleo C. A infraestrutura Python/ctypes, o programa de testes com suas referências e a memória do chamador ficam fora da função embarcada. O núcleo também foi ligado a um executável C de testes sem Python, usando o mesmo heap.o, para mostrar essa separação. No firmware real, o chamador e interrupções precisam de reserva própria; o enunciado já pressupõe o vetor de entrada residente.

A comprovação é local ao GCC/x86-64 e flags registrados. Com outro alvo, não transportar automaticamente o número 96: recompilar, inspecionar os novos frames e verificar novamente o caminho. O código de máquina do algoritmo e arquivos de programa não são tratados como RAM auxiliar de trabalho.

## 17. Introdução ao código C para quem conhece Python

O código de produção tem duas funções pequenas em [heap.c](../projeto/src/heap.c). A estrutura lógica é a mesma já estudada no roteiro; o que muda são os tipos e algumas formas de escrever os laços.

| Escrita em C | Como entender |
|---|---|
| uint16_t | Inteiro sem sinal de 16 bits, adequado aos valores 0–65535 |
| size_t | Tipo sem sinal usado para tamanhos e índices; no build atual tem 64 bits. u pode chegar a 65536, que não caberia em uint16_t |
| uint16_t *a | Ponteiro ao primeiro elemento de um vetor de leituras; a[i] acessa o elemento i |
| size_t n | Quantidade de elementos, não quantidade de bytes |
| static void sift(...) | Função auxiliar interna ao arquivo; modifica o vetor e não devolve valor |
| size_t heap_unique(...) | Função pública que modifica o vetor e devolve a quantidade de únicos |
| ++i / --i | Incrementar/decrementar o índice |
| a[u++] = a[i] | Escrever no índice u atual e depois incrementar u |
| return u | Devolver a quantidade; os elementos da resposta já estão no vetor |

### Ler sift em quatro passos

1. `root < end/2` identifica um nó que ainda tem filho. end é o tamanho exclusivo do heap ativo. A condição também mantém o cálculo do filho dentro do intervalo, sem overflow para um vetor válido.
2. `child = 2*root+1` localiza o filho esquerdo. Só acessamos o direito se `child+1 < end`; se ele for maior, passamos a escolhê-lo.
3. Se `a[root] >= a[child]`, a propriedade de heap já vale e o laço termina. Caso contrário, um temporário uint16_t permite trocar os valores sem perder nenhum.
4. `root = child` continua a descida. A possível violação só desce, então o procedimento termina quando encontra posição correta ou folha.

### Ler heap_unique em quatro passos

1. Se n<2, retorna imediatamente n. Isso permite NULL quando n=0, sem acessar a[0].
2. O laço de construção começa em n/2 e chama sift para i−1. O teste i>0 ocorre antes da subtração. Isso evita o erro clássico de usar i>=0 com um inteiro sem sinal, que nunca se torna negativo.
3. O laço de extração diminui end, troca raiz e última posição ativa e restaura o heap do prefixo. O sufixo ordenado cresce.
4. A compactação começa com u=1 porque sabemos que n≥2. Compara cada leitura ao último emitido a[u−1], escreve só se for diferente e devolve u.

Não há malloc, conjunto, tabela ou recursão nessas duas funções. Em testes/nativo.c há malloc e referências para conferir respostas: esse programa é infraestrutura, não a função sob orçamento. O mesmo vale para o adaptador Python: ele cria uma visão sobre o buffer para chamar C, mas não executa outra deduplicação.

### Compilar e demonstrar

```sh
python3 projeto/scripts/compilar.py --sanitizers
./projeto/build/test_nativo
python3 projeto/tests/test.py
python3 projeto/src/main.py heap 3 1 3 0 65535
```

O script de compilação é Python e mostra um caminho único para quem ainda está aprendendo GCC. `-O3` ativa otimização; `-Wall -Wextra -Wpedantic -Werror` exigem compilação sem avisos; `-fstack-usage` gera a evidência de pilha. As demais opções fixam condições de auditoria no ambiente x86-64, como não usar red zone e não inlinear funções. `-fPIC` permite usar o mesmo objeto na biblioteca compartilhada do teste. Essas flags não são uma receita universal para toda placa embarcada.

O build com sanitizadores é separado e serve para procurar acessos inválidos e comportamento indefinido. Seus frames e tempos não são usados para provar os 96 B do build otimizado. `heap.py` usa ctypes para ligar a demonstração ao C; o dispositivo pode ligar diretamente heap.o a um programa C e não precisa de Python.
