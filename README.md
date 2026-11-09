# PjBL — Deduplicação de leituras de sensores

**Integrantes:** Henry Rodrigues, Rafael Maluf e Matheus.

Todos os programas estão em **Python**. A pasta `projeto/` contém somente a entrega: duas estratégias, testes, automação, medições, gráficos separados, análise e relatório PDF. O material para estudar e preparar a apresentação está em **Estudos/**.

```sh
python3 projeto/src/main.py heap 3 1 3 0 65535
python3 projeto/src/main.py bitmap 3 1 3 0 65535
python3 projeto/tests/test.py
python3 -m pip install -r projeto/requirements.txt
python3 projeto/scripts/experimentos.py
MPLCONFIGDIR=/tmp/pjbl-mpl python3 projeto/scripts/documentos.py
```

Os experimentos executam n=1000,100000,10000000 com um aquecimento e três repetições de tempo por algoritmo. Depois executam uma rodada completa de memória para cada uma das seis combinações. O rastreamento pode demorar bastante no maior tamanho: a rodada de memória do heap com dez milhões de leituras levou cerca de 15 minutos nesta coleta. Essa duração não é usada como tempo de desempenho. Geração, cópia e validação ficam fora da janela da função. Nova coleta substitui os dados correntes.

Para medir só memória e preservar as medições de tempo existentes:

```sh
python3 projeto/scripts/experimentos.py --somente-memoria
MPLCONFIGDIR=/tmp/pjbl-mpl python3 projeto/scripts/documentos.py
```

As medições de memória estão em [memoria.json](projeto/dados/memoria.json), separadas do ambiente e das rodadas de tempo. São amostras completas das três escalas, não uma certificação de pior caso ou de RAM total do interpretador.

[Relatório](projeto/relatorio.pdf) · [Análise teórica](projeto/docs/analise_teorica.md) · [Roteiro explicado](Estudos/apresentacao.md) · [Contas passo a passo](Estudos/Matematica.md) · [Guia de estudo e checklist](Estudos/Checklist.md)

**Limitações:** Heap Sort em CPython não atende aos 256 B da Embarca: a amostra de n=1000 teve 380 B de alocações rastreadas. Separadamente, o layout instalado dos frames simultâneos de heap_unique e sift tem capacidade calculada de 312 B, antes dos objetos referenciados. Esses valores são evidências distintas e não devem ser somados como uma medição única. A equipe optou por manter todos os códigos em Python; não se declara a implementação certificada para Embarca. O par e a linguagem precisam ser confirmados com o professor diante das menções a Pascal. Resultados locais não certificam os 2 s na máquina da disciplina. O relatório distingue o que foi efetivamente medido das hipóteses dos modelos.

A entrada das funções é `array('H')`, com 2 B por elemento na máquina avaliada, e é modificada. O retorno u indica o prefixo válido a[0:u]; heap entrega ordem crescente, bitmap mantém primeiras ocorrências. Para vetor vazio, u=0. Apenas os testes usam conjunto e ordenação nativa como referência.

Os seis gráficos PNG são arquivos individuais de alta resolução. Não há executáveis, arquivos C, histórico de medições antigas ou ZIP duplicado nesta entrega. Para compactar só a entrega: `python3 -m zipfile -c entrega.zip projeto` (remova caches `__pycache__` antes, caso existam).
