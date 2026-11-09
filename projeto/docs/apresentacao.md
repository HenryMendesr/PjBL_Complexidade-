# Roteiro de apresentação e defesa oral

Apresentação sugerida de 8 a 10 minutos; adaptar ao tempo concedido, sem atribuir papéis a integrantes que não foram informados.

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

**Por que C se a rubrica fala Pascal?** A seção 6 permite linguagem à escolha; adotamos C conforme o pedido, documentamos a inconsistência e precisamos confirmar com o professor.
