# PjBL — Deduplicação de leituras de sensores

**Integrantes:** Henry Rodrigues, Rafael Maluf e Matheus.

- **Embarca:** Heap Sort iterativo e compactação em **C**, sem recursão ou alocação dinâmica. Limite conservador de **96 B extras** no build GCC/x86-64 avaliado, incluindo pilha e margem de chamada.
- **Datacenter:** bitmap em **Python**, com 8192 B de bits mais os objetos do interpretador.

`projeto/` contém a entrega e `Estudos/` contém as explicações, contas e roteiro. Os seis gráficos estão em arquivos individuais.

## Compilar e conferir

Ambiente avaliado: Linux x86-64, GCC, binutils e Python 3. Em Windows, usar um ambiente Linux/WSL com essas ferramentas; a compilação entregue usa `.so` e flags GCC de x86-64. Não é necessário instalar dependências de gráficos para executar os algoritmos e testes.

```sh
python3 projeto/scripts/compilar.py --sanitizers
python3 projeto/tests/test.py
python3 projeto/src/main.py heap 3 1 3 0 65535
python3 projeto/src/main.py bitmap 3 1 3 0 65535
```

O primeiro comando compila a biblioteca e executa os testes C nativos, inclusive o build separado com AddressSanitizer/UndefinedBehaviorSanitizer. Os objetos e executáveis ficam em `projeto/build/`, ignorado no Git. Para executar o teste C sem Python após compilar: `./projeto/build/test_nativo`.

O algoritmo embarcado é apenas [heap.c](projeto/src/heap.c), com a função `size_t heap_unique(uint16_t *a, size_t n)`. Ele pode ser ligado diretamente a um programa C, sem Python. `heap.py` é uma ponte usada só para demonstrações, testes e benchmarks no computador; compartilha o buffer de entrada sem copiar. A memória de ctypes/Python não é apresentada como memória do firmware.

## Reproduzir medições e relatório

```sh
python3 -m pip install -r projeto/requirements.txt
python3 projeto/scripts/experimentos.py
MPLCONFIGDIR=/tmp/pjbl-mpl python3 projeto/scripts/documentos.py
```

São n=1000,100000,10000000, um aquecimento e três rodadas de tempo por algoritmo/tamanho. Os dados são iguais para os dois algoritmos. Geração, cópia, preparação de ponteiro e validação ficam fora do tempo; o C inclui o custo da chamada via ctypes. Nova coleta substitui os dados correntes. O bitmap recebe também uma execução completa de memória rastreada por tamanho; os tempos com rastreamento não substituem os benchmarks.

Para repetir só a verificação de memória, preservando os tempos (as fontes e o binário precisam coincidir com os medidos):

```sh
python3 projeto/scripts/experimentos.py --somente-memoria
MPLCONFIGDIR=/tmp/pjbl-mpl python3 projeto/scripts/documentos.py
```

[memoria.json](projeto/dados/memoria.json) guarda os três registros de limite C e os três picos Python, além do relatório bruto `.su`, desmontagem, flags e hashes. **C:** frames de 48+32=80 B, mais margem de 16 B, total conservador de 96 B; heap dinâmico zero por fonte/objeto auditados. O limite é estático e independe de n; não é obtido por tracemalloc. **Python:** pico de alocações rastreadas, que não é toda a RAM do interpretador. Os métodos são explicitados nas figuras e no relatório.

A prova de memória vale para o objeto GCC/x86-64 registrado, usado tanto pela biblioteca quanto pelos testes C. Outro alvo, compilador ou flags exige nova auditoria. O chamador de testes, as referências de validação e interrupções não pertencem à subárvore do algoritmo; um firmware real deve reservar seus próprios recursos. O enunciado pressupõe o vetor de entrada residente.

## Consultar a entrega

[Relatório](projeto/relatorio.pdf) · [Análise teórica](projeto/docs/analise_teorica.md) · [Roteiro explicado](Estudos/apresentacao.md) · [Contas e introdução ao C](Estudos/Matematica.md) · [Checklist](Estudos/Checklist.md)

As duas funções modificam a entrada e retornam u; só a[0:u] é resposta. Heap C entrega ordem crescente e bitmap Python preserva primeiras ocorrências. A API C aceita NULL quando n=0; na infraestrutura Python, usa-se array('H') vazio. Conjuntos e ordenação nativa aparecem apenas na validação.

**Pendências externas:** aprovação do par, confirmação da interpretação de linguagem diante das menções a Pascal e desempenho na máquina de referência. O limite Embarca foi demonstrado no build local; não foi testada uma placa específica. A mediana do bitmap ficou abaixo de 2 s localmente, mas isso não certifica o hardware da disciplina. O prazo de 2 s pertence à Datacenter, não à Embarca.

Apenas fontes, evidências e documentos necessários ficam no Git; arquivos de compilação e caches ficam fora. Para compactar a entrega, excluir `projeto/build` e `__pycache__` da cópia a ser enviada. O repositório Git também é uma forma de entrega permitida pelo PDF.
