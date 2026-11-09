# Checklist da entrega: C e Python

## Como estudar

1. Ler [Matematica.md](Matematica.md) para refazer as contas. As seções 16 e 17 explicam a pilha e o código C para quem conhece Python.
2. Ensaiar [apresentacao.md](apresentacao.md), acompanhando as duas estratégias na entrada [3,1,3,0,65535].
3. Conferir os métodos usados para cada cliente: limite estático GCC para o núcleo C e pico rastreado para o bitmap Python. Não misturar nenhum deles com RSS.

O projeto contém exatamente duas estratégias de deduplicação. A ponte heap.py não é uma terceira solução; só chama heap.c compartilhando o vetor da infraestrutura.

## Atendimento ao enunciado

| Requisito | Evidência e situação |
|---|---|
| Dez análises e quatro cálculos de inviabilidade | Presentes na análise teórica e relatório |
| Duas implementações | Heap Sort/compactação em src/heap.c e bitmap em src/bitmap.py |
| Corretude, vazio e extremos | Testes Python com referência independente; 3294 casos C nativos, NULL/0, resposta conhecida e sentinelas |
| Ordenados, inversos, iguais e aleatórios | Teste C nas três escalas, domínio completo e enumeração pequena |
| n=1000,100000,10000000 | Novas rodadas híbridas reais, com validação após cada execução |
| Memória Embarca ≤256 B extras | Atendido na compilação local: quadros de pilha GCC 48+32=80 B, mais margem de 16 B, total 96 B; sem memória dinâmica, recursão ou cópia |
| Evidência de memória por tamanho | Três execuções C com o mesmo limite estático válido para todo n; três execuções completas Python com tracemalloc |
| Separar recursos | Pilha/heap C, alocações rastreadas Python, entrada e RSS explicitados separadamente |
| Tempo isolado de preparação/validação | perf_counter_ns; preparação de ponteiro fora; custo da chamada ctypes incluído no tempo C |
| Aquecimento, repetições e dispersão | Um aquecimento e três tempos por combinação; mediana, mínimo e máximo |
| Oito extrapolações | Modelos nominais identificados nos gráficos; não são medições das oito alternativas |
| Datacenter em <2 s na referência | Resultado local abaixo de 2 s; referência da disciplina ainda pendente |
| Linguagem e aprovação do par | C/Python são recomendados no PDF, que também cita Pascal; confirmação dessa divergência e aprovação do par ainda pendentes |
| Relatório, fontes e instruções | PDF, Markdown, scripts e README presentes |
| Código C utilizável sem Python | Teste nativo ligado ao mesmo heap.o; a ponte Python é infraestrutura do computador |

## Resposta à revisão recebida

A crítica ao orçamento físico era correta. A solução atual mudou o núcleo embarcado para C e refez a coleta, em vez de apenas registrar a falha. A comprovação vale para a compilação com GCC para x86-64 registrada em memoria.json; não equivale a teste de uma placa desconhecida. Outro compilador ou ABI exige refazer a análise de pilha.

O prazo de dois segundos pertence a Datacenter. A mediana do Heap Sort C acima de dois segundos é relatada, mas não viola uma exigência temporal inexistente para Embarca. A escolha C é sustentada pela RAM. O bitmap Python atende à mediana local de tempo; a validação formal continua dependente da máquina da disciplina.

## Antes da apresentação

- Compilar com `python3 projeto/scripts/compilar.py --sanitizers`.
- Executar `./projeto/build/test_nativo` para mostrar o teste C sem interpretador.
- Executar os exemplos pequenos e abrir os seis gráficos individuais.
- Mostrar 48+32+16=96 B e explicar por que isso não é soma incompleta de sizeof nem pico de tracemalloc.
- Mostrar os dados atuais de C/Python, sem usar os antigos tempos de Heap Sort Python.
- Explicar que as linguagens diferentes influenciam a comparação de tempos; a razão medida não isola o algoritmo.
- Conferir o prefixo válido a[0:u], as pendências do professor e o escopo local da evidência.
