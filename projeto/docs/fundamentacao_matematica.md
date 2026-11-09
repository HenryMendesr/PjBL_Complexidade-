# Fundamentação matemática e revisão das deduções

Este capítulo organiza a defesa do trabalho: primeiro o que precisa ser provado, depois quanto custa. Resultados empíricos complementam a análise; eles não substituem uma prova, e uma função assintótica não determina segundos.

## 1. Especificação como propriedade matemática

Para o vetor original A=(a₀,…,aₙ₋₁), defina S(A)={aᵢ : 0≤i<n}. A saída é um prefixo B de comprimento u. Exigimos simultaneamente: (i) todo elemento de B pertence a S(A); (ii) cada elemento de S(A) aparece em B; (iii) os elementos de B são dois a dois distintos. Essas três propriedades implicam u=|S(A)|. Acertar apenas u não prova corretude: uma saída de tamanho correto pode trocar um valor por outro.

Para n=0, S é vazio e u=0. Para n>0, 1≤u≤min(n,D), D=65536. O princípio das gavetas prova que n>D implica ao menos uma repetição; não prova que todos os D valores ocorreram. No modelo uniforme independente, E[u]=D[1-(1-1/D)ⁿ], mas esse valor é uma esperança, não o u de uma entrada concreta. Prova: o indicador Iₓ de presença de x tem esperança 1-(1-1/D)ⁿ; somar sobre os D valores e usar linearidade da esperança. Independência entre os indicadores não é necessária.

A leitura de n elementos é necessária no pior caso para qualquer algoritmo exato, sem certificação prévia da entrada: se uma posição não for inspecionada, pode-se alterá-la para um valor ausente e mudar a resposta. Portanto há limite inferior Ω(n) no modelo geral de acesso às leituras. Isso situa o bitmap em Θ(n) com domínio fixo, assintoticamente ótimo nesse modelo; não afirma que sua constante seja a melhor em todo hardware.

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

**Subconjuntos.** Cada posição tem duas decisões independentes, logo 2ⁿ folhas e 2ⁿ⁺¹-1 nós na árvore binária completa. Cada posição pertence a exatamente metade dos subconjuntos: Σ(t=0..n)t binom(n,t)=n2ⁿ⁻¹. Com 2 B por elemento, a materialização exige n2ⁿ B só de payload. Assim, materializar e copiar todos os elementos custa Θ(n2ⁿ) tempo e espaço, além de descritores e pilha Θ(n). Somente enumerar em streaming custa Θ(2ⁿ) visitas e pode usar heap zero; não confundir as duas variantes. As curvas desta revisão usam materialização para AMBOS tempo e RAM. Em n=1000, log₁₀(bytes)=304,029995664, e não apenas log₁₀(2¹⁰⁰⁰)=301,029995664.

**Unário.** Seja Lⱼ=xⱼ+1 o tamanho em bytes do registro j, com j=1,…,n. Gravar todos os registros custa S=ΣLⱼ. Consultar todos os registros anteriores para cada posição, sem parar cedo, relê o registro j exatamente n-j vezes. O tráfego idealizado total é V=Σ(n-j+1)Lⱼ. Essa identidade não exige independência. Para comprimentos de mesma esperança μ=32768,5, a linearidade dá E[V]=μn(n+1)/2, e E[S]=μn. A expressão inclui a gravação inicial e todas as releituras, sem contar novamente um registro corrente que já está disponível no vetor. Para n=10⁷: E[V]=1638425163842500000 B, aproximadamente 1,638425164×10¹⁸ B, e E[V]/10⁹≈1,638×10⁹ s a 1 GB/s. Não estão incluídos syscalls, seeks, comparar contadores e outros custos; esse throughput é hipótese otimista. O custo completo de CPU inclui Ω(n) acessos ao vetor e o custo de contar símbolos; no domínio fixo, o modelo de varredura completa tem Θ(n²) tempo de I/O em melhor e pior caso, com constantes dependentes dos comprimentos.

## 6. Probabilidade do Bloom e o significado dos arredondamentos

Com ku marcações uniformes independentes, a probabilidade de um bit particular continuar zero é exatamente (1-1/m)^(ku). Aproximá-la por exp(-ku/m) e supor independência entre os k bits consultados leva a p≈(1-exp(-ku/m))^k. As ocupações dos bits não são rigorosamente independentes; trata-se do modelo clássico aproximado. O modelo de dupla hash, hashes não uniformes e consultas adversariais podem alterar a taxa. Não se apresenta p como limite determinístico garantido.

No ótimo contínuo, k=(m/u)ln2 e m=-u ln p/(ln2)². Porém k é inteiro. Para u=D e p-alvo=0,01, escolher k=7 exige ajustar m≥-7u/ln(1-p^(1/7)). Arredondando para bytes, 78586 B dão p≈0,0099996885 pela aproximação. Usar 78521 B e simplesmente arredondar k para 7 dá p≈0,010039, ligeiramente acima da meta. Essa correção foi aplicada. Como Bloom não foi implementado, não há taxa empírica observada; uma implementação escolhida precisaria medir a taxa e avaliar as hipóteses. Ambas as soluções entregues são exatas.

Uma taxa p por consulta não implica saída inteira correta com probabilidade 1-p: para r consultas inéditas, a desigualdade da união limita a probabilidade de algum falso positivo por min(1,Σpᵢ), quando limites marginais válidos estão disponíveis. Os eventos não precisam ser independentes para essa desigualdade. A taxa admissível do PDF não é necessária às nossas implementações exatas.

## 7. Decisão por restrição e interpretação dos gráficos

Embarca: provar espaço constante não basta; a constante precisa caber em 256 B. Heap Sort tem prova de correção e evidência local de 96 B. Bitmap usa 8192 B de dados, impossíveis sob o teto, mesmo antes dos escalares. Datacenter: bitmap tem tempo linear e domínio conhecido; medições locais apoiam sua recomendação, mas não provam o prazo na máquina externa.

Curvas hipotéticas misturam limites, esperanças e cenários declarados: não são oito benchmarks. As multiplicidades balanceadas de Bogosort são uma escolha pessimista de multiplicidades, não a esperança das entradas uniformes medidas. Tempos nominais a 1 ns/op e I/O a 1 GB/s são condições de modelos; não são constantes inferidas de O. As transformações dos eixos preservam os expoentes astronômicos sem converter previsões em evidência empírica.

As verificações numéricas deste capítulo estão em scripts/validar_matematica.py, com registro em dados/revisao_matematica.txt. Elas conferem identidades e arredondamentos em casos pequenos por contagem independente; não implementam uma terceira solução de deduplicação.
