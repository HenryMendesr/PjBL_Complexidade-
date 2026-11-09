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
