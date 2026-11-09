## Resultados locais efetivamente medidos

CPU informada ao ambiente: AMD EPYC 9V74 80-Core Processor. Sistema: Linux-6.18.57-x86_64-with-glibc2.41. Compilador: gcc (Debian 14.2.0-19) 14.2.0.

| Algoritmo | n | u | Mediana (s) | Mín–máx (s) | Q1–Q3 (s) | Extra conservador (B) | RSS pico (KiB) |
|---|---|---|---|---|---|---|---|
| heap | 1000 | 996 | 0.000015543 | 0.000014461–0.000045778 | 0.000014943–0.000027561 | 96 | 11904 |
| bitmap | 1000 | 996 | 0.000001002 | 0.000000991–0.000001062 | 0.000000991–0.000001012 | 8224 | 11904 |
| heap | 100000 | 51485 | 0.008639077 | 0.008214097–0.010335410 | 0.008412892–0.009500212 | 96 | 11904 |
| bitmap | 100000 | 51485 | 0.000325342 | 0.000308507–0.001213317 | 0.000309929–0.000426512 | 8224 | 11904 |
| heap | 10000000 | 65536 | 1.623778035 | 1.498388893–1.828633656 | 1.563083458–1.781125109 | 96 | 40192 |
| bitmap | 10000000 | 65536 | 0.006033297 | 0.006005024–0.006242396 | 0.006009632–0.006099775 | 8224 | 40192 |

O RSS é o máximo residente de cada processo Linux, inclui dois vetores, oráculo, runtime e páginas tocadas. Não é memória extra do algoritmo e não deve ser subtraído do vetor para inferir a pilha. A inicialização do bitmap está dentro do cronômetro.
