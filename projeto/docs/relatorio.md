# PjBL: Duas empresas, duas restrições

Deduplicação de leituras de sensores — relatório técnico.

Integrantes: Henry Rodrigues, Rafael Maluf e Matheus.



# Fundamentação matemática

Este capítulo organiza a defesa do trabalho: primeiro o que precisa ser provado, depois quanto custa. Resultados empíricos complementam a análise; eles não substituem uma prova, e uma função assintótica não determina segundos.

## 1. Especificação como propriedade matemática

Para o vetor original A=(a₀,…,aₙ₋₁), defina S(A)={aᵢ : 0≤i<n}. A saída é um prefixo B de comprimento u. Exigimos simultaneamente: (i) todo elemento de B pertence a S(A); (ii) cada elemento de S(A) aparece em B; (iii) os elementos de B são dois a dois distintos. Essas três propriedades implicam u=|S(A)|. Acertar apenas u não prova corretude: uma saída de tamanho correto pode trocar um valor por outro.

Para n=0, S é vazio e u=0. Para n>0, 1≤u≤min(n,D), D=65536. O princípio das gavetas prova que n>D implica ao menos uma repetição; não prova que todos os D valores ocorreram. No modelo uniforme independente, E[u]=D[1-(1-1/D)ⁿ], mas esse valor é uma esperança, não o u de uma entrada concreta. Prova: o indicador Iₓ de presença de x tem esperança 1-(1-1/D)ⁿ; somar sobre os D valores e usar linearidade da esperança. Independência entre os indicadores não é necessária.

A leitura de n elementos é necessária no pior caso para qualquer algoritmo exato, sem certificação prévia da entrada. Considere a entrada toda igual a zero: se uma posição não for inspecionada, pode-se alterá-la para um e mudar a resposta. Esse argumento usa D≥2 e uma entrada que não cobre o domínio; não diz que toda instância obriga ler tudo, pois uma vez encontrados todos os D valores seria possível encerrar. Portanto há limite inferior Ω(n) no modelo geral de acesso às leituras. Isso situa o bitmap em Θ(n) com domínio fixo, assintoticamente ótimo nesse modelo; não afirma que sua constante seja a melhor em todo hardware.

## 2. Prova de corretude do Heap Sort e da compactação

**Invariante do sift.** As subárvores dos filhos já são max-heaps; uma eventual violação está na raiz corrente. Se a raiz é maior ou igual ao maior filho, a propriedade foi restaurada. Caso contrário, trocar com o maior filho faz a nova raiz dominar os dois filhos e desloca a única violação possível para a subárvore escolhida. A altura restante diminui, logo o laço termina. Escolher o maior filho é essencial.

**Construção.** Folhas são heaps triviais. Ao processar nós internos em ordem decrescente de índice, as subárvores dos filhos já são heaps. Pelo argumento anterior, cada passo torna um heap a subárvore atual. Ao fim, o vetor todo é um max-heap.

**Extração.** Antes de cada extração, o prefixo é um max-heap e o sufixo está ordenado, com elementos maiores ou iguais aos do prefixo. A raiz é o máximo restante. Movê-la ao início do sufixo e restaurar o heap mantém o invariante. O prefixo diminui em um até terminar. Trocas conservam o multiconjunto de valores; o vetor resultante é uma permutação ordenada da entrada.

**Compactação.** Antes de ler o índice i, o prefixo a[0..u) contém exatamente um representante de cada valor do prefixo ordenado já lido. Se a[i] coincide com o último emitido, não surge um valor novo. Se difere, a ordenação garante que ele não apareceu em nenhum bloco anterior; anexá-lo mantém as três propriedades da saída. Como u≤i na entrada de cada passo, escrever em a[u] não altera a região futura. O caso n<2 é tratado antes de acessar qualquer posição.

**Tempo.** Uma descida custa O(h) para altura h. Na construção, o número de nós de altura pelo menos h é no máximo floor(n/2ʰ); por isso a soma dos trabalhos é limitada por n Σ(h≥1)1/2ʰ=O(n), além de Ω(n) visitas. As extrações somam no máximo Σ(m=2..n)O(log m)=O(n log n). Com todos iguais, cada sift interrompe após uma comparação local e o total é Θ(n). Para ordens adversas com muitas chaves distintas, Θ(n log n) é atingido; com D fixo esse limite superior permanece válido, mas não se usa o limite inferior de ordenação de n chaves distintas quando n>D. O custo completo soma Θ(n) de compactação.

**Espaço.** Há apenas o frame da função externa e um frame de sift simultâneo, sem cadeia recursiva. O número de variáveis não cresce com n; o tamanho depende da ABI. A prova estrutural é O(1); os 96 B são evidência do build local, não consequência numérica da notação O(1).

## 3. Prova de corretude e custo do bitmap

Antes da iteração i: (a) o bit de x está marcado se e somente se x ocorreu no prefixo original A[0..i); (b) a[0..u) contém exatamente esses valores, nas primeiras ocorrências; (c) a região ainda não lida não foi modificada. A inicialização estabelece o invariante para i=0. Se o bit está marcado, não há valor novo e não se emite. Se está desmarcado, emitir x e marcar o bit acrescenta exatamente o novo valor. A escrita ocorre no máximo na posição i; o valor corrente já foi carregado. Assim o invariante avança e, em i=n, prova as propriedades da saída e sua ordem.

O índice x>>6 varia de 0 a 1023; o deslocamento x&63 varia de 0 a 63. UINT64_C(1) torna válido o deslocamento de 63 bits. Há 1024 palavras de 8 B: 8192 B. Em modelo de palavra w=64, T(n,D)=Θ(ceil(D/w)+n), incluindo zerar a estrutura. Para D fixo, Θ(n+1), inclusive a chamada vazia da implementação. O espaço é Θ(ceil(D/w)) palavras; com w constante, Θ(D) bits. A notação Θ(1) em n não autoriza chamar 8192 B de memória desprezível.

## 4. Contagem precisa da força bruta

Na versão que busca apenas entre únicos já emitidos, introduzir os u valores pela primeira vez custa 0+1+…+(u-1)=u(u-1)/2 comparações, independentemente das buscas de repetidos. Cada uma das n-u repetições custa no máximo u. O máximo para n e u fixos é exatamente Cmax=u(u-1)/2+(n-u)u: introduzir os u valores primeiro e repetir sempre o último do prefixo atinge esse valor. O trabalho total é Θ(n+C), incluindo laço e emissão. Para u=n, Cmax=n(n-1)/2; para u=1, Cmax=n-1.

A aproximação nu/2 para a curva é um cenário de buscas com posições aproximadamente uniformes após estabilizar u, não uma identidade universal. Num cenário de primeira formação dos únicos, há o termo triangular acima. Não se substitui u por n quando n>D. O pior caso limitado ao domínio é O(nD), linear em n se D é constante, embora a constante possa torná-lo impraticável.

## 5. Fatoriais, subconjuntos e I/O: contagens verificáveis

**Bogosort.** Há n! permutações de objetos rotulados, mas ∏cⱼ! delas produzem a sequência de valores ordenada. Portanto q=∏cⱼ!/n!. Embaralhamentos uniformes independentes dão distribuição geométrica: E[tentativas]=1/q. Para uma entrada inicialmente desordenada, esse é o número esperado de embaralhamentos até o primeiro sucesso; a checagem inicial acrescenta apenas uma verificação. Se já ordenada, a função hipotética termina imediatamente. Tempo esperado cn/q é modelo de custo por tentativa, não garantia. Com n=1000 distintos, log₁₀(1/q)=2567,604644222. Para n>D usar n! sem dividir pelas multiplicidades superestima o número de tentativas; usamos lgamma para calcular o logaritmo sem overflow.

**Subconjuntos.** Cada posição tem duas decisões independentes, logo 2ⁿ folhas e 2ⁿ⁺¹-1 nós na árvore binária completa. Cada posição pertence a exatamente metade dos subconjuntos: Σ(t=0..n)t binom(n,t)=n2ⁿ⁻¹. Com 2 B por elemento, a materialização exige n2ⁿ B só de payload. Assim, materializar e copiar todos os elementos custa Θ(n2ⁿ) tempo e espaço, além de descritores e pilha Θ(n). Somente enumerar em streaming custa Θ(2ⁿ) visitas e pode usar heap zero; não confundir as duas variantes. As curvas do relatório usam materialização para tempo e RAM; a RAM soma ao payload descritores e frames nominais, conforme docs/modelos.md. Em n=1000, log₁₀(bytes)=304,029995664, e não apenas log₁₀(2¹⁰⁰⁰)=301,029995664.

**Unário.** Seja Lⱼ=xⱼ+1 o tamanho em bytes do registro j, com j=1,…,n. Gravar todos os registros custa S=ΣLⱼ. Consultar todos os registros anteriores para cada posição, sem parar cedo, relê o registro j exatamente n-j vezes. O tráfego idealizado total é V=Σ(n-j+1)Lⱼ. Essa identidade não exige independência. Para comprimentos de mesma esperança μ=32768,5, a linearidade dá E[V]=μn(n+1)/2, e E[S]=μn. A expressão inclui a gravação inicial e todas as releituras, sem contar novamente um registro corrente que já está disponível no vetor. Para n=10⁷: E[V]=1638425163842500000 B, aproximadamente 1,638425164×10¹⁸ B, e E[V]/10⁹≈1,638×10⁹ s a 1 GB/s. Não estão incluídos syscalls, seeks, comparar contadores e outros custos; esse throughput é hipótese otimista. O custo completo de CPU inclui Ω(n) acessos ao vetor e o custo de contar símbolos; no domínio fixo, o modelo de varredura completa tem Θ(n²) tempo de I/O em melhor e pior caso, com constantes dependentes dos comprimentos.

## 6. Probabilidade do Bloom e o significado dos arredondamentos

Com ku marcações uniformes independentes, a probabilidade de um bit particular continuar zero é exatamente (1-1/m)^(ku). Aproximá-la por exp(-ku/m) e supor independência entre os k bits consultados leva a p≈(1-exp(-ku/m))^k. As ocupações dos bits não são rigorosamente independentes; trata-se do modelo clássico aproximado. O modelo de dupla hash, hashes não uniformes e consultas adversariais podem alterar a taxa. Não se apresenta p como limite determinístico garantido.

No ótimo contínuo, k=(m/u)ln2 e m=-u ln p/(ln2)². Porém k é inteiro. Para u=D e p-alvo=0,01, escolher k=7 exige ajustar m≥-7u/ln(1-p^(1/7)). Arredondando para bytes, 78586 B dão p≈0,0099996885 pela aproximação. Usar 78521 B e simplesmente arredondar k para 7 dá p≈0,010039, ligeiramente acima da meta. Essa correção foi aplicada. Como Bloom não foi implementado, não há taxa empírica observada; uma implementação escolhida precisaria medir a taxa e avaliar as hipóteses. Ambas as soluções entregues são exatas.

Uma taxa p por consulta não implica saída inteira correta com probabilidade 1-p: para r consultas inéditas, a desigualdade da união limita a probabilidade de algum falso positivo por min(1,Σpᵢ), quando limites marginais válidos estão disponíveis. Os eventos não precisam ser independentes para essa desigualdade. A taxa admissível do PDF não é necessária às nossas implementações exatas.

## 7. Decisão por restrição e interpretação dos gráficos

Embarca: provar espaço constante não basta; a constante precisa caber em 256 B. Heap Sort tem prova de correção e evidência local de 96 B. Bitmap usa 8192 B de dados, impossíveis sob o teto, mesmo antes dos escalares. Datacenter: bitmap tem tempo linear e domínio conhecido; medições locais apoiam sua recomendação, mas não provam o prazo na máquina externa.

Curvas hipotéticas misturam limites, esperanças e cenários declarados: não são oito benchmarks. As multiplicidades balanceadas de Bogosort são uma escolha pessimista de multiplicidades, não a esperança das entradas uniformes medidas. Tempos nominais a 1 ns/op e I/O a 1 GB/s são condições de modelos; não são constantes inferidas de O. As transformações dos eixos preservam os expoentes astronômicos sem converter previsões em evidência empírica.

As verificações numéricas deste capítulo estão em scripts/validar_matematica.py, com registro em dados/revisao_matematica.txt. Elas conferem identidades e arredondamentos em casos pequenos por contagem independente; não implementam uma terceira solução de deduplicação.

O multinomial de Bogosort é máximo entre multiplicidades balanceadas. Se duas contagens satisfazem a≥b+2, transferir um elemento da maior para a menor altera o produto de fatoriais pelo fator (b+1)/a<1; portanto aumenta o número de permutações distintas. Repetir essa operação chega às contagens floor(n/D) e ceil(n/D). Isso justifica o cenário extremo escolhido, sem confundi-lo com a média de uma amostra uniforme.


# Análise teórica — Duas empresas, duas restrições

## Escopo, interpretação e hipóteses

O projeto compara Heap Sort iterativo e bitmap para deduplicação de leituras de 16 bits. As duas implementações utilizam C; Python é empregado na automação dos experimentos e dos documentos. A seção 6 do enunciado permite a escolha da linguagem, enquanto os objetivos e o critério 3 da rubrica mencionam Pascal. A confirmação da linguagem e a aprovação do par são requisitos acadêmicos registrados na checklist.

Seja n o número de leituras, u o número de valores distintos e D=65536. Temos 0≤u≤min(n,D). Para n=100000 e n=10000000, duplicatas são inevitáveis. O vetor usa 2n bytes com uint16_t; n=10000000 ocupa 20000000 bytes. O limite Embarca é de 256 bytes EXTRAS ao vetor, mesmo que esse vetor não caiba num sensor real; essa residência é premissa do enunciado. A Datacenter exige tempo estritamente menor que 2 s na máquina da disciplina. A Embarca não tem prazo numérico explícito. Não atribuímos a ela o limite de 2 s.

Modelo RAM: leitura, comparação, acesso por índice e operação de palavra de 64 bits custam O(1); índices cabem em size_t. Nos limites físicos reais não se considera n além da memória endereçável. As análises genéricas permitem D crescer; com D fixo, muitas expressões em u se tornam lineares em n com constantes grandes. Pilha, heap e disco serão separados. O espaço de saída está no prefixo do vetor sempre que possível, sem cobrar outro vetor de saída.

## 1. Força bruta

Para cada leitura, procurar no prefixo de únicos; se não existir, anexar nesse prefixo. A escrita fica atrás da leitura, portanto é exata e preserva primeiras ocorrências. O trabalho é a soma das posições percorridas nas buscas. Melhor caso Θ(n), com todos iguais. Pior genérico Θ(n²), pois 0+1+…+(n-1)=n(n-1)/2 quando distintos. Para u limitado, limite O(nu); configurações que mantêm muitas buscas longas atingem Θ(nu). No modelo médio de posições equiprováveis, cerca de nu/2 comparações após formar o conjunto. Sem distribuição não há uma média universal. Com D fixo, pior O(nD), não crescimento quadrático indefinido.

Pilha Θ(1), heap 0, disco 0. Pequeno número de índices pode caber nos 256 B, mas qualquer implementação exigiria verificação da ABI. Embarca: candidata, porém escolhida a ordenação para evitar até 65536 buscas por leitura. Datacenter: rejeitada como recomendação para lote geral. Em n=10⁷ e u≈D, nu/2≈3,28×10¹¹ comparações; a 1 ns/comparação seriam 328 s. Isso é hipótese, não benchmark. Todos iguais podem ser rápidos. A observação de que seria o único candidato seguro é excessiva: Heap Sort iterativo também tem espaço constante.

## 2. Ordenação e varredura

Ordenar agrupa iguais; manter o primeiro de cada bloco e compactar. O(n) da varredura soma-se ao custo da ordenação. Na implementação, construir heap custa Θ(n): a soma de alturas é O(n), pois há menos nós em níveis altos. Cada uma de n-1 extrações pode percorrer log₂n níveis: O(n log n). Para chaves distintas e ordem não favorável, tempo médio (permutações uniformes de chaves distintas) e pior Θ(n log n); com todos iguais, o sift encerra imediatamente e o melhor é Θ(n). O limite superior continua válido com repetições; não se deve prometer Θ(n log n) em toda entrada.

Heap Sort iterativo usa pilha Θ(1), heap 0, disco 0, altera ordem para crescente. A prova de corretude combina: sift restaura o heap; a raiz máxima vai à extremidade definitiva; após ordenar, valores diferentes do último emitido são exatamente os únicos. Quick Sort usual tem média Θ(n log n), pior Θ(n²), pilha média Θ(log n) e pior Θ(n), sem garantir 256 B. Merge Sort usual tem Θ(n log n) em todos os casos e vetor auxiliar Θ(n), além de pilha Θ(log n). Não são implementados aqui. Embarca: Heap Sort atende espaço neste build; Datacenter: possível, mas trabalho e acessos são maiores que os do bitmap, sem benefício exigido pelo problema.

## 3. Tabela hash/conjunto

Consultar cada x; inserir e emitir apenas quando ausente. Com fator de carga controlado, boa dispersão e hash universal/randomizado, consultas esperadas O(1) e inserções amortizadas O(1), total esperado Θ(n); melhor Θ(n). Redimensionar ocasiona operação individual Θ(u), coberta pela análise amortizada. Colisões adversas com listas ou sondagem podem levar a O(nu), O(n²) genérico; não se supõe árvore nos buckets. Domínio fixo dá O(nD) nesse pior caso.

Heap Θ(u+1) entradas (incluindo buckets e fator de carga), pilha Θ(1) na versão iterativa, disco 0. Modelo dos gráficos: 16 B por distinto, hipótese otimista de chave, estado, alinhamento e folga; bibliotecas podem usar mais. Com D cheio, cerca de 1 MiB, contra 8 KiB do bitmap. Embarca: não garante 256 B para todos n/u. Datacenter: plausível, mas não há razão para aceitar colisões, alocações e overhead neste domínio. Para u muito pequeno cabe um conjunto diminuto; isso não garante o limite geral.

## 4. Árvore balanceada (AVL/Red-Black)

Buscar x e inserir somente se ausente; emitir no prefixo ou percorrer em ordem. Altura O(log(u+1)), pelo invariante de balanceamento; logo O(n log(u+1)+u) no limite superior. Com u≈n, a construção por inserções exige Θ(n log n) no modelo usual de comparações; para acessos uniformes entre u chaves numa árvore de altura logarítmica, o custo esperado por busca é Θ(log(u+1)). Sem distribuição de acessos, o caso médio não é definido. Melhor Θ(n) com todos iguais; uma entrada com muitos acertos na raiz também pode custar Θ(n). Não se afirma limite inferior log u para toda distribuição. Rotações custam O(1) por ajuste; manutenção do caminho cabe no limite da altura.

Heap Θ(u+1) bytes no modelo de palavra fixa, com Θ(u) nós e administração constante; modelo de 32 B/nó para dois ponteiros, pai/balanceamento, chave e alinhamento, cerca de 2 MiB no domínio completo. Pilha Θ(log(u+1)) se recursiva; iterativa pode usar pai e Θ(1) de pilha. Disco 0. Embarca: nós e possível pilha violam a garantia para u grande. Datacenter: determinística e exata, mas perseguição de ponteiros e log u são desnecessários frente ao acesso direto. Quando se precisa de consultas ordenadas dinâmicas em domínio amplo, ela tem utilidade.

## 5. Bitmap

Associar um bit a cada valor. Inicializar D bits em zero, ler cada x, testar bit e emitir/marcar somente se zero. No código, cada palavra tem 64 bits; índice x>>6 e máscara 1<<(x&63). Invariante: o bit representa exatamente os valores já visitados. Como u≤i+1, compactar não sobrescreve elementos futuros. Retorna únicos na ordem das primeiras ocorrências.

Tempo Θ(n+ceil(D/w)), w=64, nos três casos, pois sempre inicializa 1024 palavras e lê n elementos. Com D fixo, Θ(n+1); o atalho usual O(n) pressupõe n≥1. A variante que primeiro marca todos e depois percorre o domínio devolve ordem crescente em Θ(n+D), mas NÃO é o código entregue. Espaço D/8=8192 B mais escalares: aqui automático, na pilha; heap 0 e disco 0. Ser constante em n não significa caber em 256 B. Embarca: rejeitado, 32 vezes o orçamento só em bits. Datacenter: escolha exata, linear, sem colisões, com conjunto de trabalho pequeno. Os dados locais apoiam a escolha, mas a máquina de referência ainda precisa ser testada.

## 6. Filtro de Bloom

m bits, k funções de hash; um valor é considerado presente se todos seus k bits estiverem marcados. Se algum estiver zero, emitir e marcar. Após u inserções, com hashes uniformes independentes, p≈(1-exp(-ku/m))^k. O ótimo k≈(m/u)ln2, m≈-u ln p/(ln2)². Para u=65536 e p=0,01: m≈628167 bits (arredondar a bytes), cerca de 78521 B no ótimo contínuo. Com k inteiro igual a 7, deve-se aumentar para 628684 bits, arredondados a 78586 B (628688 bits), para p≈0,99997% na fórmula aproximada. A fórmula de dimensionamento com k fixo é m≥-ku/ln(1-p^(1/k)); arredondar k sem ajustar m pode passar ligeiramente de 1%. Para u=1000: cerca de 1199 B, ainda acima de 256 B. Dimensionar por n=10⁷ desperdiçaria memória: só existem D chaves. Com m=2048 bits e u=D, k ótimo seria menor que 1; k=1 já dá p≈1-exp(-32), quase 100%.

Melhor/médio/pior Θ(nk+m/w) numa variante que avalia sempre os k hashes; com interrupção antecipada o custo varia entre Ω(n+m/w) e O(nk+m/w). Para k fixo é linear. Pilha Θ(1) escalares se bitset no heap, heap Θ(m) bits, disco 0; um bitset automático transfere esse custo para a pilha. Falso positivo significa descartar uma leitura inédita e perder um valor na saída; não é duplicata remanescente. Não há falso negativo na consulta ao filtro para valores inseridos sob essas hipóteses. Quando u=D, não há consulta inédita possível dentro do domínio; o dimensionamento por D é uma capacidade conservadora para os estados anteriores. p por consulta inédita não é chance de saída inteira correta, nem um limite determinístico em toda sequência. O PDF admite probabilístico com taxa declarada ≤1%; aqui preferimos exatidão. Embarca não comporta o dimensionamento; Datacenter pode aceitar aproximação em outros problemas, mas neste domínio o bitmap é menor e exato. Não implementado.

## 7. Bogosort e varredura

Checar se está ordenado; se não, embaralhar uniformemente (Fisher-Yates in-place) e repetir. Depois compactar vizinhos. Para multiplicidades c₁,…,cᵤ, a probabilidade de uma permutação de elementos rotulados estar não decrescente é q=∏cⱼ!/n!. O número esperado de tentativas geométricas é 1/q=n!/∏cⱼ!. Com distintos, n!; com todos iguais, 1. Se embaralhar e checar custam Θ(n), tempo esperado Θ(n/q) para uma entrada inicialmente desordenada, sob embaralhamentos uniformes independentes; se já ordenado, melhor Θ(n). Quando q<1, o número de tentativas tem suporte ilimitado, portanto não há teto finito para o pior tempo. Se todos iguais, a checagem inicial custa Θ(n) e não há embaralhamento. Para modelo médio é preciso declarar a distribuição das multiplicidades e a aleatoriedade dos embaralhamentos.

Pilha Θ(1), heap 0 e disco 0 se embaralhamento e gerador forem iterativos de estado fixo. RNG e ABI devem caber no orçamento, não basta dizer O(1). Sem garantia temporal; não há orçamento explícito Embarca, mas o tempo geral é impraticável. Datacenter não tem garantia de 2 s. Domínio fixo não salva o método: com frequências balanceadas, o multinomial continua crescendo aproximadamente como Dⁿ dividido por fator polinomial para D fixo. Casos ordenados ou minúsculos podem terminar rápido.

## 8. Enumeração recursiva de subconjuntos

Para tornar a estratégia definida: decidir incluir/excluir cada posição, percorrer as 2ⁿ folhas e examinar os subconjuntos de cardinalidade 1 para recuperar seus elementos, emitindo apenas primeiras ocorrências por uma busca no prefixo de únicos. É um modo correto, mas extremamente redundante, de resolver um problema mais geral. Identidade de posições evita ambiguidade quando valores se repetem. Nada exige que subconjuntos de valores coincidentes sejam armazenados uma única vez.

A árvore tem 2ⁿ⁺¹-1 nós: visitar sem copiar é Θ(2ⁿ) tempo em melhor/médio/pior para essa variante que não poda nem encerra cedo, mais O(nu) para as emissões de singletons. Recursão tem profundidade n+1 e pilha Θ(n) frames; uma seleção corrente ocupa O(n) se não couber no próprio caminho. Heap pode ser 0 em enumeração por streaming, portanto Θ(2ⁿ) de heap não é obrigatório. Materializar listas de todos os subconjuntos exige Θ(n2ⁿ) tempo e bytes de elementos: cada uma das n posições participa de 2ⁿ⁻¹ subconjuntos. Acrescentam-se até Θ(2ⁿ) descritores. Copiar/examinar cada folha inteira também custa Θ(n2ⁿ). Disco 0, salvo armazenamento externo que transfira o mesmo volume. Embarca: pilha viola 256 B em n grande, mesmo sem materializar; Datacenter: explosão de tempo. É útil para busca combinatória com n pequeno, não para deduplicação em lote.

## 9. Codificação unária em disco

A tabela do PDF descreve serialização, mas não especifica como comparar e remover duplicatas. Apenas escrever os valores não resolve o problema. Definimos uma variante exata e de RAM constante para análise: gravar cada leitura x como x bytes '1' seguidos de um byte '0'; para cada registro, comparar seu comprimento com os registros anteriores, emitindo o x original somente se não houver igual. Comparações e navegação usam contadores de largura fixa e I/O sem buffer grande; o disco continua contendo todos os registros, inclusive os repetidos. A saída é compactada no vetor de entrada. Essa variante não é implementada.

Volume S=Σ(xᵢ+1), entre n e 65536n bytes; zero precisa do delimitador. Só codificar custa Θ(n+Σxᵢ), NÃO tempo exponencial em n para domínio fixo. Comparar por varredura física dos registros anteriores pode custar O(nS), com Θ(n²D) no cenário de comprimentos longos e busca que não encerra cedo. Média depende de ordem e multiplicidades; modelo pessimista dos gráficos lê metade do arquivo para cada consulta, sem atalhos, mesmo após encontrar duplicata. O tráfego exato dessa auditoria é V=Σ(j=1..n)(n-j+1)(xⱼ+1), independentemente de duplicatas; Θ(nS) é atingível, mas não é identidade para comprimentos arbitrários quando D também varia. Melhor Θ(n²) quando todos os comprimentos são 1 nesse modelo; com D fixo todos esses limites são quadráticos em n, com constantes distintas. Uma versão que encerra cedo seria mais rápida. Não atribuímos Θ(S) ao deduplicador completo.

Pilha/heap de trabalho podem ser constantes e inferiores a 256 B numa implementação de baixo nível com buffers mínimos, mas libc, FILE e buffers do kernel precisam ser contabilizados conforme a plataforma. Disco Θ(S). Não há medição nem garantia de RAM para essa estratégia hipotética. Se um valor tem b bits e chega a 2ᵇ-1, representá-lo em unário exige Θ(2ᵇ) símbolos; é exponencial em b, não em n quando b=16 fixo. Codificar bits em vez de bytes reduz volume até 8 vezes, mantendo necessidade de delimitadores e a análise de crescimento. Embarca pode falhar no armazenamento, disponibilidade de disco, buffers e tempo prático; não existe restrição numérica de disco no enunciado, portanto o volume de disco caracteriza uma limitação prática, sem teto formal de capacidade especificado. Datacenter: o modelo de I/O abaixo excede 2 s. Unário serve em exemplos minúsculos, contagens pequenas e formatos didáticos.

## 10. Matriz n×n de auditoria

Construir Mᵢⱼ=(aᵢ=aⱼ) para todos os pares; uma posição i é primeira ocorrência se nenhum j<i tem igualdade. A construção é Θ(n²) em melhor/médio/pior mesmo com todos iguais, pois a variante exige auditar todos os pares. A leitura e compactação adicionais não dominam. Usar somente metade altera constante, não ordem. NaN não existe no domínio inteiro, logo igualdade é bem definida.

Heap Θ(n²) células, pilha Θ(1), disco 0 na versão residente; em disco há o mesmo crescimento em outro recurso. Em bytes n² B; empacotada ceil(n²/8) B, além de escalares. Embarca: mesmo n=1000 usa 125000 B em bits, muito além de 256 B. Datacenter: sem teto de memória formal, mas exigir 12,5 TB ou 100 TB em n=10⁷ é operacionalmente oneroso; tempo também é impeditivo sob o modelo quantitativo. Não afirmar que viola só memória. Matriz pode servir a uma auditoria exigida para n pequeno; auditoria de todos os pares não foi pedida aqui.

## Exemplos quantitativos das quatro estratégias exageradas

**Bogosort:** n=1000 com todos distintos é válido no domínio. log₁₀(1000!)≈2567,604644; cerca de 4,02×10²⁵⁶⁷ tentativas. Supondo, de modo extremamente favorável, 1 ns por elemento para embaralhar e verificar, cada tentativa custa 10⁻⁶ s: tempo ≈4,02×10²⁵⁶¹ s. Todos iguais têm q=1, logo esse número não vale para qualquer entrada. Para n>D usa-se o multinomial das multiplicidades, jamais n! sem correção.

**Power set:** n=1000 implica 2¹⁰⁰⁰≈1,072×10³⁰¹ subconjuntos. Materializar elementos uint16_t custa 2×1000×2⁹⁹⁹=1000×2¹⁰⁰⁰≈1,072×10³⁰⁴ B, sem contar descritores. Mesmo uma representação otimista de 16 B/frame já usa 16016 B para profundidade 1001, violando Embarca. A 10⁹ folhas/s, apenas enumerar requer cerca de 1,072×10²⁹² s. Em n=10⁷ a pilha desse modelo seria aproximadamente 160 MB antes da materialização. Para n≤10, enumeração pode ser razoável em outro problema.

**Unário:** com n=10⁷ e média uniforme E[x]=32767,5, S esperado=327685000000 B (327,685 GB decimais). Só gravar a 1 GB/s sustentado custa 327,685 s; ler novamente soma esse custo. Pior S=655360000000 B, 655,36 GB. No deduplicador definido, tráfego esperado do modelo 32768,5×n(n+1)/2≈1,638425164×10¹⁸ B, ou 1,638×10⁹ s à mesma taxa otimista, cerca de 51,9 anos. São hipóteses de throughput, sem latência de seek ou CPU; não medições. Um buffer pequeno evita grande RAM de usuário, mas não elimina disco/I/O. Em n=1, x=0, apenas um byte basta.

**Matriz:** n=10⁷ produz 10¹⁴ células: 100 TB em bytes ou 12,5 TB em bits (≈11,37 TiB). A 1 ns/célula, construção idealizada leva 100000 s (27,78 h), sem alocação nem tráfego de memória. n=1000 já pede 1 MB ou 125 kB; mesmo n=100 pede 1250 B em bits. n=10 pede 13 B em bits mais escalares e pode caber. Só para Datacenter existe teto temporal formal de 2 s; rejeição temporal da Embarca é julgamento de viabilidade prática.

## Escolha e contrato

Implementamos exatamente duas estratégias do catálogo: ordenação Heap Sort seguida de compactação e bitmap. A infraestrutura de testes usa histograma de frequências exclusivamente como oráculo, não como terceira solução entregue ao cliente. A geração, validação, cópia e impressão estão fora do tempo do algoritmo.

Ambas recebem uint16_t *a e size_t n, permitem NULL somente se n=0, alteram a e retornam size_t u. Apenas a[0..u) é saída; a cauda não tem contrato. Heap devolve crescente; bitmap mantém primeiras ocorrências. Ambas são determinísticas e exatas. Nenhuma exige estabilidade no PDF; a diferença está documentada e validada.

Heap supera força bruta em previsibilidade de trabalho para u alto, não exige estruturas do hash/árvore, nem bits além de 256 B. A pilha de Quick Sort recursivo não foi presumida segura. Bitmap aproveita o domínio: custa menos que Bloom a 1%, evita colisões de hash e ponteiros de árvore. A compactação integrada evita uma segunda varredura por todo o vetor ou domínio para emissão.

## Referências verificáveis

- Cormen, Leiserson, Rivest e Stein. Introduction to Algorithms, 4ª edição. MIT Press, 2022. Heap Sort, tabelas hash e árvores balanceadas. https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/
- Bloom, Burton H. Space/Time Trade-offs in Hash Coding with Allowable Errors. Communications of the ACM, 13(7), 1970, pp. 422–426. https://doi.org/10.1145/362686.362692
- Broder, A.; Mitzenmacher, M. Network Applications of Bloom Filters: A Survey. Internet Mathematics 1(4), 2004, pp. 485–509. https://doi.org/10.1080/15427951.2004.10129096
- GCC, Developer Options: -fstack-usage. https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html
- POSIX, clock_gettime. https://pubs.opengroup.org/onlinepubs/9799919799/functions/clock_gettime.html
- Linux man-pages, getrusage(2), ru_maxrss em KiB no Linux. https://man7.org/linux/man-pages/man2/getrusage.2.html


# Metodologia e evidências de memória

Compilação C11 com GCC, -O3, -Wall -Wextra -Wpedantic -Werror. Para tornar os frames auditáveis: -fno-inline -fno-omit-frame-pointer -mno-red-zone -fno-tree-loop-distribute-patterns -fstack-usage. Flags completas e hardware reportado por lscpu estão em dados/ambiente.json. São flags para GCC/x86-64, não uma configuração portátil de microcontrolador. Não se utilizou -march=native. A comparação é entre builds de mesmas opções, não entre bibliotecas com otimizações distintas.

Cada combinação algoritmo/n roda em um processo separado. Entradas uniformes aproximadas são os 16 bits baixos do xorshift32 de semente decimal 20261108, reiniciada para cada processo. O gerador não é criptográfico. Mesmos dados são usados nos dois algoritmos. Executa-se um aquecimento e sete rodadas medidas; o vetor original é copiado antes de cada rodada. O relógio CLOCK_MONOTONIC fornece tempo de parede com nanossegundos na representação; isso não promete precisão de 1 ns. A janela inclui chamada e retorno da deduplicação, construção do heap ou limpeza do bitmap e compactação. Exclui malloc dos vetores, geração, memcpy, oráculo e printf. Para n pequeno o overhead do relógio é relevante e não foi artificialmente subtraído. Estatística: mediana; dispersão por mínimo/máximo e quartis exclusivos de statistics.quantiles. Não são intervalos de confiança.

Corretude: testes manuais, domínio completo crescente e decrescente, 200 casos pseudoaleatórios menores, e quatro distribuições em cada escala obrigatória (iguais, globalmente ordenados, globalmente inversos, pseudoaleatória). A grade exaustiva acrescenta 3280 sequências sobre {0,64,65535} de tamanho 0 a 7, e há sentinelas antes/depois do vetor. São 3502 casos para cada algoritmo, além das chamadas NULL/0. O histograma de teste verifica existência de cada saída, ausência de repetição, contagem exata e ordem contratada. Validação também é feita após cada rodada do benchmark. Asserções permanecem ativas, sem -DNDEBUG. AddressSanitizer e UndefinedBehaviorSanitizer são executados em build separado: seus tempos e frames não são usados como benchmark.

A memória de trabalho foi auditada por -fstack-usage nos objetos realmente usados na medição, não pela soma de sizeof de variáveis. Frames reportados neste GCC: heap_unique 48 B e sift 32 B, simultâneos no caminho mais profundo: 80 B. Adiciona-se margem conservadora de 16 B de fronteira de chamada/ABI, total 96 B. bitmap_unique tem frame de 8208 B, mais a mesma margem: 8224 B. Os frames incluem ponteiros/argumentos salvos, temporários, alinhamento e salvamento de registradores conforme gerados pelo compilador. Arquivos .su são preservados em dados/evidencias/; desmontagem está em dados/desmontagem.txt. O compilador classifica todos os frames como static. Não há recursão nem chamadas de sift para outras funções. nm -u confirma ausência de símbolos externos nos dois objetos; inspeção da fonte e desmontagem confirma heap dinâmico de 0 B. Esse zero é evidência estática do binário, não amostragem de RSS nem profiler de malloc.

O limite de 96 B independe de n, incluindo os três tamanhos testados. A verificação automatizada falha se a soma mais margem superar 256 B. Isso demonstra a restrição no build local x86-64, mas não em qualquer ABI ou compilador. Interrupções, pilha do sistema operacional, rotina chamadora/gerador e redirecionamentos de runtime não fazem parte da subárvore do algoritmo. Em firmware real, medir novamente com o compilador do alvo e reservar a pilha de interrupções conforme requisitos do dispositivo. Com sanitizadores ou instrumentação diferente, os frames mudam.

O bitmap foi posto na pilha por simplicidade e reentrância; 8 KiB são adequados ao ambiente local e proibidos para Embarca. Transferi-lo para heap não reduziria memória EXTRA. O vetor original e sua cópia usam 4n B na infraestrutura; o cliente precisa apenas do vetor de 2n B. O oráculo usa histograma e auxiliares exclusivamente nos testes. getrusage fornece ru_maxrss em KiB no Linux, pico do processo incluindo essa infraestrutura; não é o consumo instantâneo do algoritmo. Dados calculados (2n, D/8), reportados pelo compilador (frames) e observados pelo SO (RSS) são identificados separadamente.

A coleta atual registra instante UTC e hashes das fontes e do binário em ambiente.json. Os CSVs da versão anterior à auditoria estão em dados/historico/pre_auditoria/, identificados pelo commit de origem. Alterações de dados não são preenchidas manualmente: gráficos e tabelas são regenerados a partir da execução.

Os índices, ponteiros e temporários que o compilador mantém em registradores não alocam RAM adicional. A desmontagem de heap.o não contém registradores vetoriais; mesmo contabilizando conservadoramente todos os 16 registradores gerais de 64 bits como armazenamento adicional, 96+16×8=224 B permanece abaixo de 256 B. Os 96 B apresentados nos resultados são o limite de RAM de pilha com margem, não essa contabilidade ampliada calculada.


## Resultados locais efetivamente medidos

CPU informada ao ambiente: AMD EPYC 9V74 80-Core Processor. Sistema: Linux-6.18.57-x86_64-with-glibc2.41. Compilador: gcc (Debian 14.2.0-19) 14.2.0.

| Algoritmo | n | u | Mediana (s) | Mín–máx (s) | Q1–Q3 (s) | Extra conservador (B) | RSS pico (KiB) |
|---|---|---|---|---|---|---|---|
| heap | 1000 | 996 | 0.000032508 | 0.000018718–0.000208229 | 0.000019359–0.000052508 | 96 | 12800 |
| bitmap | 1000 | 996 | 0.000001012 | 0.000000992–0.000001051 | 0.000001002–0.000001031 | 8224 | 12800 |
| heap | 100000 | 51485 | 0.008981933 | 0.008230120–0.010595884 | 0.008499539–0.010453874 | 96 | 12800 |
| bitmap | 100000 | 51485 | 0.000331160 | 0.000325181–0.000374215 | 0.000329898–0.000363298 | 8224 | 12800 |
| heap | 10000000 | 65536 | 1.794285846 | 1.612656371–1.925955623 | 1.688465706–1.877988920 | 96 | 40192 |
| bitmap | 10000000 | 65536 | 0.006632755 | 0.006483575–0.006843317 | 0.006522121–0.006760154 | 8224 | 40192 |

O RSS é o máximo residente de cada processo Linux, inclui dois vetores, oráculo, runtime e páginas tocadas. Não é memória extra do algoritmo e não deve ser subtraído do vetor para inferir a pilha. A inicialização do bitmap está dentro do cronômetro.


# Extrapolações: hipóteses, unidades e limites

As oito estratégias não foram programadas nem cronometradas. Seus pontos são previsões ilustrativas, não afirmações de que executariam nesses tempos. Para tempo, usa-se custo nominal c=10⁻⁹ s por operação abstrata; não há calibração independente dessas operações. Um hash ou nó de árvore é modelado com 5 operações e Bloom com 7 hashes de custo c, escolha didática otimista. Não se derivou c de Big-O nem se ajustaram as curvas para garantir uma classificação. Multiplicar essas constantes por 0,1 ou 10 desloca os log₁₀ dos tempos em -1 ou +1, sem remover a explosão combinatória. Tráfego unário supõe 10⁹ B/s. Cache, branches, largura de banda e latência estão ausentes desses modelos; a incerteza é grande e não é expressa como erro estatístico.

Nas curvas força bruta/hash/árvore, u(n)=D[1-(1-1/D)ⁿ], esperança sob amostragem uniforme independente. O gerador real é determinístico e só aproxima essa hipótese. Os u reais são registrados, não substituídos pela esperança. Para Bogosort, as multiplicidades são balanceadas: q=floor(n/D), r=n mod D, com D-r contagens q e r contagens q+1. Quando n≤D, isso é uma entrada distinta (pior cenário de multiplicidades), diferente da distribuição empírica; não se pretende que todas as curvas sejam o tempo da mesma instância. Usar n! em n>D seria incorreto. O Bloom usa um filtro fixo de 78586 B, dimensionado para D distintos, tanto para o tempo de limpeza como para a RAM. O modelo de subconjuntos materializa todos os elementos para tempo e memória, com fator n em ambas as curvas. A variante de streaming é discutida separadamente na análise.

Modelos de tempo em segundos:

- Força bruta: c n max(1,u/2), busca média no prefixo de únicos.
- Hash: 5cn, esperança com boa dispersão; não descreve colisões adversas.
- Árvore: 5cn log₂(u+1), limite de buscas em árvore balanceada.
- Bloom: 7cn + 78586c, limpeza conservadora por byte do filtro máximo mais hashes.
- Bogosort: cn n!/[(q!)^(D-r)((q+1)!)^r], checagem/embaralhamento nominal de cn.
- Subconjuntos: n2ⁿc, custo nominal proporcional aos elementos materializados (um fator constante 2 é absorvido por c).
- Unário: [32768,5×n×(n+1)/2]/10⁹, gravar e varrer em média metade do arquivo por consulta; sem seeks e com comprimentos médios uniformes.
- Matriz: cn², uma operação nominal por célula; não inclui alocação.

RAM extra hipotética em bytes (não medidas): força bruta/Bogosort/unário 128 B de trabalho nominal; hash 16u+128; árvore 32u+128; Bloom 78586+128, com k=7 e capacidade de D distintos; subconjuntos (n+16)2ⁿ+16(n+1)+128 (payload n2ⁿ B, descritor nominal de 16 B por subconjunto, frames nominais de 16 B em n+1 níveis e 128 B de trabalho); matriz ceil(n²/8)+128, empacotada. Os descritores e frames dos subconjuntos são hipóteses de layout, não tamanhos medidos. A análise também apresenta o limite mínimo de payload n2ⁿ B; a curva soma os outros termos, sem misturá-los à variante de streaming. Unário usa disco separado n×32768,5 B esperado. Os 128 B são hipótese ilustrativa de escalares e buffer, não garantia de ABI. Comparações no relatório consideram também matrizes em bytes.

O módulo scripts/modelos.py usa lgamma para fatoriais e expoentes em log₁₀ para 2ⁿ. dados/previsoes_log10.csv contém as oito curvas sem overflow e com unidade explícita. Em graficos/tempo.png, o painel esquerdo mostra segundos em escala log de 10⁻⁸ a 10⁶; as curvas fora dessa janela são continuadas integralmente no painel direito. O painel direito mostra o número log₁₀(segundos) sobre eixo symlog: valor 6 representa um milhão de segundos, valor 3000000 representa 10 elevado a três milhões de segundos, não três milhões de segundos. Essa segunda transformação permite ver simultaneamente números negativos (tempos <1 s), valores próximos de zero e expoentes enormes. Nenhuma curva inviável é removida.

As duas linhas sólidas com pontos são medianas medidas; barras no painel prático são mínimo/máximo. As outras oito linhas são modelos. graficos/memoria.png usa o mesmo tratamento de expoentes para RAM e outro painel em bytes para disco, entrada e RSS. O frame GCC mais a margem é constante para os dois algoritmos, e não uma medição dinâmica de pico a cada n. Sobreposições em curvas de RAM constante são esperadas; legenda e CSV permitem identificá-las.

O domínio dos modelos é n inteiro positivo. A substituição de E[u] nas fórmulas de custo não calcula automaticamente E[T]: em particular, log(E[u]+1) difere de E[log(u+1)]. Para a árvore, a concavidade do log fornece E[log(u+1)]≤log(E[u]+1); para a força bruta, nu/2 é heurística de posição média, não esperança exata da fase de formação. Essas aproximações não são garantias de tempo.

Nos volumes astronômicos, descritores de 16 B não significam que um computador de 64 bits conseguiria endereçar a estrutura. São custos nominais otimistas para evidenciar a inviabilidade. Endereçar um payload de ordem n2ⁿ requer Θ(n+log n) bits de endereço; uma máquina teórica de palavra crescente também teria de rever o custo das operações. O payload n2ⁿ B é uma contagem combinatória independente desses detalhes e já basta para a rejeição física. As previsões fora do espaço endereçável não são promessas de execução.



![Tempo](graficos/tempo.png)

![Memória](graficos/memoria.png)



# Discussão crítica e recomendação

Os resultados locais indicam que Heap Sort atende ao orçamento de memória com 96 B conservadores e bitmap oferece forte vantagem de tempo no maior lote. O bitmap tem 8192 B só de bits e não serve à Embarca. Para Datacenter, recomenda-se bitmap, condicionado à repetição na máquina da disciplina. Um resultado local menor que 2 s não cumpre sozinho a validação exigida na referência.

A taxa por elemento do bitmap não é constante entre as escalas: enquanto ainda surgem muitos inéditos, a função realiza mais escritas, decisões e atualizações de bits. Em n=10⁷, há no máximo 65536 emissões; a maior parte das leituras apenas consulta bits. Já o heap percorre caminhos e faz trocas em regiões cada vez maiores do vetor. O vetor de 20 MB muda a localidade frente aos 2 kB da menor escala, enquanto o bitmap mantém somente 8 kB de bits. Esses mecanismos são compatíveis com as diferenças observadas, mas não foram isolados por contadores de cache ou um experimento causal. Não atribuímos uma diferença especificamente a cache, compilador ou SO sem medi-los.

Há efeitos de aquecimento, escalonamento, compartilhamento da CPU virtual, frequência e resolução efetiva do relógio. As sete rodadas e dispersões documentam variação local; não eliminam essas fontes. A cópia anterior aquece páginas e faz parte da condição experimental, embora esteja fora da janela de tempo. O oráculo também toca dados entre rodadas. Comparar tempos de modelos a 1 ns/op com esses pontos não é medir as oito alternativas. A teoria oferece tendências e limites, e os benchmarks oferecem evidências apenas das duas implementações.

O Heap Sort também pode atender ao prazo local, mas isso não o torna a melhor recomendação Datacenter: bitmap faz menos trabalho e explora uma garantia do domínio. Se o domínio crescer ou a estabilidade for obrigatória para o cliente embarcado, a escolha precisará ser revista. Se surgir requisito de manter a entrada intacta, ambos os contratos atuais deixam de atendê-lo sem cópia externa.

Pendências reais: aprovação do par, confirmação de C diante da rubrica que menciona Pascal e reprodução no hardware da disciplina. A checagem de pilha precisa ser refeita em qualquer novo alvo.


# Auditoria técnica da entrega

## Escopo e critério de verificação

Versão examinada inicialmente: acb938d. Referência: PDF «PjBL: Duas Empresas, Duas Restrições — Deduplicação de Leituras de Sensores», lido integralmente. A auditoria confrontou fontes C, scripts, somatórios, probabilidades, CSVs, gráficos e relatório. Os estados de atendimento ao enunciado estão em docs/checklist.md. A existência de um texto explicativo não foi considerada evidência de execução.

## Erros e insuficiências encontrados

| Item | Constatação na versão anterior | Correção e consequência |
|---|---|---|
| Modelo de Bloom | O tempo cobrava zerar 78586 B em todo n, mas a RAM dimensionava um filtro variável por E[u] | Adotado filtro fixo de 78586 B para D distintos em ambos os recursos; RAM nominal total 78714 B, incluindo 128 B de trabalho. Curva de RAM regenerada; a dedução do dimensionamento não mudou |
| RAM de subconjuntos | A figura rotulada pilha + heap mostrava só payload n2ⁿ B, embora o texto apontasse descritores e pilha | Curva soma payload, descritores nominais de 16 B por subconjunto, pilha nominal de 16(n+1) B e 128 B de trabalho. O payload mínimo continua identificado separadamente; não se trata de memória medida |
| Esperanças e substituições | As curvas por E[u] podiam ser lidas como E[T], apesar de funções não lineares e da fase de formação do conjunto | Documentada a distinção: log(E[u]+1) não é E[log(u+1)]; nu/2 é aproximação de posição média, não a esperança exata de toda a força bruta |
| Entrada da demonstração | A combinação de strtoull com teste apenas do primeiro caractere aceitava ` -18446744073709551615` como n=1 | Falha reproduzida: retorno 0 e CSV na versão anterior; agora retorno 1 e nenhuma rodada. Exigidos tokens decimais sem sinal/espaços e verificado errno também nas repetições |
| Verificação da entrega | O verificador não conferia Q1/Q3, unicidade dos seis grupos, rodadas 0–6, frames dos .su contra o resumo, tabela do relatório ou proveniência dos gráficos | Esses vínculos são verificados; manifesto associa hashes dos dados/modelos às figuras e registra os pontos medidos plotados. Cálculos combinatórios independentes complementam a comparação do modelo com seu próprio CSV |
| Checklist | O contrato era atribuído ao cabeçalho dedup.h após a remoção de seus comentários; «concluído» misturava comprovação local e exigência externa | Evidência do contrato corrigida para README, análise e testes. Checklist passou a separar requisito, evidência e estado: atendido, parcial, ausente ou não verificável |

Nenhum erro de deduplicação foi encontrado nas duas funções C. Não houve alteração de heap.c ou bitmap.c nesta auditoria. As afirmações de limite inferior de leitura, caso médio e pior tempo do Bogosort foram delimitadas com as hipóteses necessárias; elas não são garantias para toda entrada.

## Rededução das dez estratégias

A tabela resume o resultado da conferência; os argumentos completos permanecem em fundamentacao_matematica.md e analise_teorica.md. Expressões com Θ de tempo desconsideram n=0, salvo indicação contrária. n é o tamanho da entrada; u é a quantidade de distintos; D=65536; m é o número de bits do Bloom; k é o número de hashes; w=64. Uma implementação com memória em palavras não implica a mesma contagem em bits sob aritmética de precisão ilimitada.

| Estratégia | Resultado da dedução e hipótese | Espaço extra e limite |
|---|---|---|
| Força bruta | Cmax=u(u−1)/2+(n−u)u; trabalho Θ(n+C). Melhor Θ(n); pior genérico Θ(n²) com D≥n; O(nD) com domínio limitado. Médio depende da distribuição | Pilha O(1), heap 0, disco 0; contadores de palavra fixa |
| Ordenar e varrer | Heap: construção Θ(n), extrações O(n log n), compactação Θ(n). Melhor Θ(n) com iguais; médio de permutações de chaves distintas e pior genérico Θ(n log n) | Pilha constante sem recursão; heap/disco 0. 96 B conservadores no build local |
| Hash | Esperado Θ(n) com dispersão e carga controladas; amortização cobre redimensionamentos. Colisões podem causar Θ(nu); não é garantia de Θ(n) | Heap O(u+1), inclusive folga e pico de redimensionamento; pilha O(1), disco 0 |
| Árvore balanceada | Limite O(n log(u+1)+u); melhor Θ(n) com iguais; buscas uniformes entre u nós têm média Θ(log(u+1)); sem distribuição não há média única | Nós O(u+1) no heap; pilha O(log(u+1)) recursiva ou O(1) iterativa com pais; disco 0 |
| Bitmap | Θ(n+ceil(D/w)) incluindo inicialização; com D fixo, Θ(n+1) | 8192 B de bits mais escalares na pilha; frame GCC 8208 B, mais margem 16 B; heap/disco 0 |
| Bloom | Variante de k hashes sempre avaliados: Θ(nk+ceil(m/w)); p≈(1−exp(−ku/m))^k sob o modelo clássico aproximado | m bits no heap ou pilha, não ambos; escalares O(1); disco 0. Não oferece exatidão e um falso positivo pode perder um único |
| Bogosort | Para multiplicidades cⱼ, E[tentativas]=n!/∏cⱼ!. Entrada inicialmente desordenada e embaralhamentos independentes: Θ(n/q); já ordenada Θ(n). Para q<1 não há teto finito do número de tentativas | Pilha/RNG O(1) em variante iterativa; heap/disco 0; o orçamento em bytes exigiria implementação |
| Subconjuntos | Visitar 2ⁿ folhas sem copiar: Θ(2ⁿ) tempo; materializar elementos: Θ(n2ⁿ). Não se confunde contagem de subconjuntos com soma de seus tamanhos | Pilha Θ(n); streaming pode ter heap 0; materialização exige payload n2ⁿ B para uint16_t, mais descritores; disco 0 |
| Unário | S=Σ(xⱼ+1). Serialização Θ(S). Deduplicador por varreduras completas: V=Σ(n−j+1)(xⱼ+1); E[V]=32768,5n(n+1)/2 se cada comprimento tem essa média. Com D fixo, tráfego Θ(n²) nesta variante | RAM de contadores/buffer O(1) hipotética; disco Θ(S), no máximo 65536n B no formato de um byte por símbolo. Exponencial em bits do valor, não em n para domínio fixo |
| Matriz | Todas as n² comparações são exigidas pela auditoria de pares: Θ(n²) nos três casos | Heap n² B ou ceil(n²/8) B empacotados, mais escalares; pilha O(1); disco 0 na variante residente |

Não há teto temporal numérico para Embarca no PDF. Rejeições por tempo para esse cliente são de viabilidade prática; para Datacenter, a meta formal é menor que 2 s na máquina da disciplina. Tampouco há teto de disco no enunciado: volumes unários gigantescos não demonstram uma violação formal de capacidade que não foi estipulada.

## Contas quantitativas refeitas

Em dados/calculos_quantitativos.csv estão as três escalas para as quatro estratégias exageradas, com unidades nos nomes dos campos. São cálculos de modelos, separados do CSV empírico.

- Bogosort, n=1000 distinto: log₁₀(1000!)=2567,604644222; a 1 ns por elemento/tentativa, log₁₀(tempo em s)=2561,604644222. Para n>D, o cálculo usa multiplicidades balanceadas e divide os fatoriais; a soma independente de logaritmos confirma o resultado de lgamma.
- Subconjuntos, n=1000: 2¹⁰⁰⁰≈1,071508607×10³⁰¹ folhas; payload 1000×2¹⁰⁰⁰≈1,071508607×10³⁰⁴ B; profundidade 1001 e pilha nominal de 16016 B. O modelo completo de RAM da curva adiciona descritores e trabalho. Streaming evita materializar, mas não elimina a explosão de tempo nem a pilha linear.
- Unário, n=10⁷ uniforme em média: armazenamento esperado 327685000000 B, pior 655360000000 B; tráfego esperado 1638425163842500000 B. A 10⁹ B/s, só a gravação esperada custa 327,685 s e a varredura completa cerca de 1,638×10⁹ s. São tempos condicionais à taxa assumida, sem seeks ou CPU.
- Matriz, n=10⁷: 10¹⁴ células, 100 TB em bytes ou 12,5 TB em bits (11,3687 TiB). A 1 ns/célula, 100000 s. Mesmo n=1000 exige 125000 B empacotados, acima de 256 B. Não se afirma um limite formal de memória para Datacenter, pois ele não foi dado.

## Corretude, limites de índices e medição

No sift, root<end/2 implica 2root+1<end e evita overflow do cálculo do filho sob um vetor válido; o filho direito só é lido se child+1<end. Laços decrescentes testam o limite antes de subtrair. Na compactação ordenada, n<2 retorna antes de acessar a[0]; o índice u−1 é válido porque u começa em 1. No bitmap, x>>6≤1023 e x&63≤63; o literal deslocado é uint64_t. Em ambos, a saída nunca escreve à frente da região já consumida. O contrato aceita NULL apenas com n=0.

Os 3502 casos por algoritmo incluem 222 casos dirigidos/pseudoaleatórios e todas as 3280 sequências de comprimento 0 a 7 sobre {0,64,65535}. O histograma independente verifica cada valor, unicidade, contagem e ordem; sentinelas verificam as posições imediatamente antes/depois do vetor. As três escalas incluem vetores globalmente crescentes/decrescentes, também com repetições quando n>D; ciclos do domínio não foram considerados equivalentes a ordem global. AddressSanitizer e UndefinedBehaviorSanitizer passaram. Isso é evidência forte de corretude e complementa os invariantes; não é uma prova por enumeração de todo o domínio de entradas possíveis.

O benchmark foi executado novamente após a correção da rotina principal. Houve um aquecimento e sete medições por combinação, seis combinações, com validação fora da janela. A inicialização das estruturas e a compactação ficaram dentro. Fonte e binário têm hashes no ambiente.json; não se preencheram tempos manualmente. Os dados anteriores foram preservados em dados/historico/pre_auditoria/. As medianas novas estão na tabela de resultados do relatório, junto de extremos e quartis.

A auditoria dos .su e da desmontagem confirma o caminho heap_unique (48 B) → sift (32 B), sem recursão e sem chamadas de alocação, mais margem conservadora de 16 B: 96 B. Esse é um limite estático do binário GCC/x86-64, não pico obtido por RSS. O processo de testes inclui dois vetores, histograma e runtime, separados do algoritmo. A prova em outro compilador/ABI ou com interrupções exige nova avaliação.

## Limites da auditoria e pendências

A aprovação do par, a aceitação de C diante das menções a Pascal e o desempenho na máquina da disciplina não são verificáveis com os recursos disponíveis. O domínio, escalas, exatidão, memória extra do build local e execução real foram conferidos. O uso sem comentários no código segue a organização solicitada; as explicações estão nos documentos. Não equivale a confirmação de todos os níveis da rubrica pelo professor.

As referências bibliográficas foram conferidas quanto à identificação presente no trabalho, mas o acesso aos seis endereços (MIT Press, dois DOIs, GCC, POSIX e Linux man-pages) falhou neste ambiente por recusa do túnel HTTP (403 Forbidden). dados/referencias_acesso.json registra a tentativa. A resolução atual dos links e a consulta integral às fontes externas não foram verificadas; a falha de acesso não demonstra inexistência da referência.

Os índices, ponteiros e temporários que o compilador mantém em registradores não alocam RAM adicional. A desmontagem de heap.o não contém registradores vetoriais; mesmo contabilizando conservadoramente todos os 16 registradores gerais de 64 bits como armazenamento adicional, 96+16×8=224 B permanece abaixo de 256 B. Os 96 B apresentados nos resultados são o limite de RAM de pilha com margem, não essa contabilidade ampliada calculada.


# Checklist de atendimento ao enunciado

Atendido: evidência disponível e conferida. Parcial: parte demonstrada, com limitação explícita. Ausente: item exigido sem artefato. Não verificável: depende de informação ou acesso externo. Os estados se referem às evidências desta entrega e não atribuem nota.

| Requisito do PDF | Evidência encontrada | Situação |
|---|---|---|
| §1–2: análise de tempo e espaço de dez estratégias | Dez seções em analise_teorica.md, provas e auditoria individual | Atendido |
| §2: distinguir pilha de heap e outros recursos | Metodologia, .su, desmontagem, modelos e auditoria separam pilha, heap, entrada, processo e disco | Atendido |
| §2: relacionar teoria e experimentos | CSV real, dispersão, duas curvas medidas e oito modelos com hipóteses | Atendido |
| §2/§9: instrumentação em Pascal | Código e evidências em C; §6 permite escolha, objetivos/rubrica citam Pascal | Parcial |
| §3: todos os integrantes conseguem explicar o trabalho | Roteiro e perguntas disponíveis; desempenho oral individual não observado | Não verificável |
| §3/§4.3: aprovação prévia do par | Nenhum comprovante de aprovação fornecido | Não verificável |
| §3: recomendação de C/Python | C para ambas e Python na automação; trata-se de recomendação, não obrigação | Atendido |
| §4.1: inteiros de 16 bits, 0–65535 | uint16_t; geração e testes de extremos e domínio completo | Atendido |
| §4.1: n=1000,100000,10000000 | 42 rodadas medidas e testes nas três escalas; 7 rodadas por algoritmo/n | Atendido |
| §4.1: Embarca com ≤256 B extras para todo n | Caminho estático do build local: 48+32+16=96 B, sem heap ou recursão; independente de n | Atendido |
| §4.1/§8: Datacenter com n=10⁷ em <2 s na referência | Medições locais abaixo de 2 s; máquina da disciplina indisponível | Parcial |
| §4.1: exatidão | Invariantes e 3502 casos por algoritmo confrontados com histograma independente | Atendido |
| §4.1/§6: falso positivo ≤1% para solução probabilística | Não se aplica às duas soluções exatas; Bloom é apenas análise | Atendido |
| §4.2/§4.3: melhor, médio, pior e hipóteses | Deduções individuais; média não definida sem distribuição; O separado de Θ | Atendido |
| §4.2/§4.3: adequação de cada estratégia aos dois clientes | Análise e auditoria com memória e tempo prático/formal separados | Atendido |
| §4.3: exatamente duas estratégias implementadas | heap.c e bitmap.c; histograma exclusivo de testes; outras oito só modeladas | Atendido |
| §4.3: justificar as duas escolhas | Comparação com força bruta, hash, árvore, Bloom e variantes de ordenação | Atendido |
| §4.3: oito extrapolações no mesmo gráfico das medidas | tempo.png/PDF: dez legendas; painel completo mantém expoentes astronômicos | Atendido |
| §5: quatro rejeições quantitativas | Exemplos no relatório e calculos_quantitativos.csv nas três escalas | Atendido |
| §5: cenários pequenos/especiais e restrições violadas | Análise distingue entrada ordenada, iguais, n pequeno e ausência de teto formal de disco/tempo Embarca | Atendido |
| §6: linguagem à escolha | Implementações em C; confirmação da divergência com Pascal depende do professor | Parcial |
| §6: demonstração dos dois algoritmos nas três escalas | make bench executa seis combinações; main imprime segundos e RSS; coletor exibe medianas e grava memória do algoritmo | Atendido |
| §6/§8: vazio e sem duplicatas sem erro | NULL/0, n=0 nos testes, unitário, 65536 valores distintos crescentes/decrescentes | Atendido |
| §7: estrutura src, docs, dados e relatorio.pdf | Arquivos presentes e validados | Atendido |
| §7: ZIP ou Git | Ambos produzidos; manifesto SHA-256 confere o ZIP | Atendido |
| §8: pequenos n≤10 com e sem duplicatas | Sete exemplos manuais e grade exaustiva 0–7, com validação independente | Atendido |
| §8: memória instrumentada por n | Frames static GCC usados para limite válido para todos os n, mais observação de RSS por rodada | Atendido |
| §8: coerência gráfica | CSVs, quartis, manifesto gráfico, tabelas e fontes do PDF conferidos; inspeção visual | Atendido |
| §9: relatório/recomendação | PDF e fonte editável, recomendação por cliente e limitações explícitas | Atendido |
| §10: decisões documentadas e dúvidas levadas ao professor | Decisões documentadas; consulta ao professor não comprovada | Parcial |
| Reprodutibilidade complementar | Makefile, dependências, README, logs e hashes da coleta | Atendido |

## Conferência dos seis critérios da rubrica

| Critério | Peso | Evidência e limitação | Situação |
|---|---|---|---|
| Análise das dez estratégias | 25% | Deduções, casos, hipóteses, recursos e comparação dos clientes | Atendido |
| Justificativa do par | 10% | Decisões técnicas fundamentadas; aprovação externa não demonstrada | Parcial |
| Implementação e instrumentação em Pascal | 20% | Duas soluções em C compiladas/testadas, .su e desmontagem; linguagem depende de confirmação, código sem comentários conforme solicitação | Parcial |
| Dados e coerência teoria/prática | 20% | Medições reais e modelos explícitos; máquina da referência não acessível | Parcial |
| Estratégias exageradas e extrapolação | 15% | Contas das quatro, modelos das oito e cenários especiais | Atendido |
| Relatório, recomendação e comunicação | 10% | PDF, fontes, apresentação e recomendações; defesa oral não avaliada | Parcial |

Pesos somam 100%. Nenhum artefato obrigatório de entrega foi identificado como ausente após as correções. Isso não elimina as pendências externas nem garante nota, aprovação de linguagem ou cumprimento do prazo na máquina da disciplina.


# Roteiro de apresentação e defesa oral

Apresentação de 8 a 10 minutos. Integrantes: Henry Rodrigues, Rafael Maluf e Matheus.

- Minuto 0–1: explicar o problema, D=65536 e a diferença entre 256 B extras e 2 s no hardware da disciplina. Declarar o caráter provisório de linguagem/par.
- Minutos 1–3: mostrar contrato e invariantes. Heap ordena e compacta; bitmap testa e marca um bit, mantendo primeiras ocorrências. Ambos retornam prefixo de u elementos.
- Minutos 3–4: abrir dados/memoria.txt e evidências GCC. Explicar 48+32+16=96 B, heap dinâmico zero e por que RSS é outro recurso.
- Minutos 4–6: mostrar medianas/dispersões e gráfico de tempo. Identificar duas medições e oito previsões. Explicar o painel de expoentes grandes sem ler seu eixo como segundos.
- Minutos 6–8: escolher um cálculo de cada estratégia exagerada; apontar as correções respeitosas do enunciado.
- Minutos 8–10: recomendar por cliente, executar make test se houver tempo e declarar as pendências externas.

## Perguntas prováveis

**Por que o bitmap não serve à Embarca se é O(1)?** Constante em n pode ser grande: só os bits usam 8192 B, contra 256 B permitidos.

**Por que não Quick Sort?** A versão recursiva usual usa pilha dependente de n. Não demonstramos um limite de 256 B para ela. Heap iterativo fornece um caminho de chamadas fixo com evidência no build.

**Como provam que nenhum único sumiu?** O oráculo de testes conta todos os valores de entrada, exige u igual ao número de distintos e confere cada saída uma única vez; também valida a ordem contratada. Ele não é uma terceira implementação entregue ao cliente.

**Como compactar sem apagar o futuro?** O índice de saída nunca ultrapassa o índice já lido. No heap, o vetor está ordenado antes da compactação; no bitmap, o valor atual é lido antes da escrita.

**Os 96 B são universais?** Não. São os frames static deste GCC e flags, com margem conservadora. Recompilar para outra ABI exige auditar de novo; interrupções e infraestrutura são reservas separadas.

**O bitmap passou em menos de 2 s?** Localmente sim, conforme CSV. O requisito da máquina da disciplina permanece pendente.

**Por que n=100000 não pode ser todo distinto?** Há apenas 65536 valores possíveis. Pelo princípio das gavetas, n>D implica repetição.

**Bloom a 1% perde só 1% dos dados necessariamente?** Não. A taxa é de falso positivo por consulta inédita sob hipóteses de hash/ocupação; não é uma garantia determinística de erro total nem de saída inteira correta. Um falso positivo pode descartar um valor novo.

**Por que o Bloom é maior que o bitmap?** Ele é útil para universos enormes/esparsos. Para este domínio pequeno e totalmente conhecido, guardar um bit por valor custa menos que um filtro dimensionado para 65536 distintos a 1%.

**A codificação unária é exponencial?** Em relação aos bits b de um valor, pode ser Θ(2ᵇ). Em relação a n com b=16 fixo, o volume é no máximo 65536n bytes neste formato. Serializar não deduplica: ainda é preciso comparar registros.

**O power set exige guardar todos os subconjuntos?** Não. Enumerar em streaming usa pilha linear; materializar todos os elementos custa Θ(n2ⁿ). As duas variantes foram distinguidas.

**Bogosort sempre leva n! tentativas?** Não. Com repetições o esperado é n!/∏cⱼ!; já ordenado termina na checagem inicial. Com todos iguais, uma checagem basta.

**De onde vieram os segundos das oito curvas?** São modelos declarados, com 1 ns por operação nominal, multiplicadores e I/O idealizado. Não foram medidos e não oferecem garantia de prazo.

**Por que C se a rubrica fala Pascal?** A seção 6 permite linguagem à escolha; adotamos C com base nessa seção, documentamos a inconsistência e precisamos confirmar com o professor.
