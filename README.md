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

Os experimentos executam n=1000,100000,10000000 com um aquecimento e três repetições por algoritmo. Heap Sort em Python pode demorar vários minutos no maior tamanho. A geração, cópia e validação ficam fora do tempo. Nova coleta substitui os dados correntes; os resultados presentes são reais desta versão Python.

[Relatório](projeto/relatorio.pdf) · [Análise teórica](projeto/docs/analise_teorica.md) · [Roteiro](Estudos/apresentacao.md)

**Limitações:** a amostra de Heap Sort em CPython apresentou 380 B de alocações rastreadas, acima dos 256 B da Embarca; essa restrição não foi atendida no ensaio. O par e a linguagem precisam ser confirmados com o professor diante das menções a Pascal. Resultados locais não certificam os 2 s na máquina da disciplina. O relatório distingue o que foi efetivamente medido das hipóteses dos modelos.

A entrada das funções é `array('H')`, com 2 B por elemento na máquina avaliada, e é modificada. O retorno u indica o prefixo válido a[0:u]; heap entrega ordem crescente, bitmap mantém primeiras ocorrências. Para vetor vazio, u=0. Apenas os testes usam conjunto e ordenação nativa como referência.

Os cinco gráficos PNG são arquivos individuais de alta resolução. Não há executáveis, arquivos C, histórico de medições antigas ou ZIP duplicado nesta entrega. Para compactar só a entrega: `python3 -m zipfile -c entrega.zip projeto` (remova caches `__pycache__` antes, caso existam).
