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
