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
