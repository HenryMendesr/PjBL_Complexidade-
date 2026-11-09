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
