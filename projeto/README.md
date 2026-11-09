# PjBL — Deduplicação de leituras de sensores

**Integrantes:** Henry Rodrigues, Rafael Maluf e Matheus.

Projeto acadêmico funcional com exatamente duas estratégias de deduplicação em C: Heap Sort iterativo in-place para Embarca e bitmap de 65536 bits para Datacenter. Python é usado só para experimentos, gráficos e documentos. Texto em português brasileiro.

**Pendências externas:** aprovação do par e de C (o PDF permite escolha mas menciona Pascal na rubrica); teste na máquina de referência. O relatório apresenta somente medições locais.

## Prioridade da apresentação: lógica matemática

Comece por docs/fundamentacao_matematica.md: especificação formal, invariantes, somatórios, contagem de permutações, materialização de subconjuntos, tráfego unário e dimensionamento probabilístico do Bloom. O capítulo abre o relatório. docs/analise_teorica.md desenvolve as dez estratégias. Os códigos são a validação prática de duas escolhas.

Para conferir as contas independentemente: `python3 scripts/validar_matematica.py`.

## Começar

Linux x86-64, GCC, make, binutils, Python 3 com os pacotes de requirements.txt. Não precisa instalar pacotes Python para compilar/testar C. O alvo sanitize requer runtime ASan/UBSan do GCC.

```sh
cd projeto
make
make test
make sanitize
make bench
make docs
```

Para instalar dependências Python, se necessário, use um ambiente virtual gravável e `python3 -m pip install -r requirements.txt`. As versões registradas são as usadas nesta entrega. PDF é gerado por ReportLab, sem LaTeX ou Pandoc. A fonte DejaVu Sans deve existir em `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` (pacote fonts-dejavu-core em distribuições Debian/Ubuntu). Matplotlib é configurado para usar cache em /tmp no alvo docs.

## Execução direta das três escalas

```sh
./build/benchmark heap 1000 7
./build/benchmark heap 100000 7
./build/benchmark heap 10000000 7
./build/benchmark bitmap 1000 7
./build/benchmark bitmap 100000 7
./build/benchmark bitmap 10000000 7
```

Cada comando imprime CSV de sete rodadas medidas depois de um aquecimento; geração, cópia, validação e impressão ficam fora da janela. `make bench` executa os seis comandos, imprime resumos e grava dados/resultados_empiricos.csv (42 medições), resumo.csv, ambiente.json, memoria.txt e desmontagem.txt. As medições existentes serão substituídas por dados reais da nova máquina. Use outra cópia do projeto para preservar a execução entregue. `make docs` regenera previsões, gráficos, docs/resultados.md, docs/relatorio.md e relatorio.pdf a partir desses CSV, sem executar novos benchmarks.

Para preservar evidências brutas de uma nova execução:

```sh
mkdir -p dados/evidencias
cp build/heap.su build/bitmap.su dados/evidencias/
make test > dados/testes.txt 2>&1
make sanitize > dados/sanitizers.txt 2>&1
```

Os frames e ausência de símbolos externos são verificados por scripts/experimentos.py. O script interrompe com erro se o heap iterativo superar 256 B no build. Esses checks não demonstram o limite numa ABI diferente; as flags -mno-red-zone e a evidência atual são x86-64/GCC. Tempos de sanitizer não são benchmarks.

## Contratos

`size_t heap_unique(uint16_t *a, size_t n)` e `size_t bitmap_unique(uint16_t *a, size_t n)` modificam o vetor e retornam u. Somente a[0..u) é saída válida. Para n=0 aceita-se NULL. Heap retorna crescente; bitmap mantém primeiras ocorrências. A cauda é indefinida como saída. Ambos são exatos. Não há alocação dinâmica nas funções; o bitmap automático usa 8192 B só em bits. Vetores e histogramas usados por main/tests são infraestrutura.

## Arquivos

- src/: heap.c, bitmap.c, dedup.h e main.c (demonstração/benchmark).
- tests/: testes e histograma de referência exclusivo para validação.
- dados/: medições reais, resumo, ambiente, evidências de memória, logs e previsões identificadas.
- graficos/: tempo e memória, PNG e PDF.
- docs/analise_teorica.md: dez estratégias, deduções e quatro exemplos quantitativos.
- docs/metodologia.md, modelos.md e discussao.md: métodos e limites da comparação.
- docs/checklist.md: requisitos e revisão pelos pesos da rubrica.
- docs/apresentacao.md: roteiro e perguntas para defesa oral.
- docs/relatorio.md: fonte editável completa, regenerada por scripts/documentos.py.
- relatorio.pdf: relatório final independente do código.
- scripts/: coleta, geração documental, verificação e empacotamento.

A fonte principal do relatório é montada pelos Markdown individuais e dados reais; edite esses arquivos para preservar alterações ao regenerar. As curvas das oito alternativas são modelos hipotéticos e nunca são misturadas ao CSV empírico. Gráficos usam logaritmos para mostrar inclusive tempos astronômicos. Explicação dos eixos e dos custos em docs/modelos.md.

## Verificação e empacotamento

```sh
python3 scripts/verificar.py
python3 scripts/empacotar.py
```

O ZIP é criado no diretório pai, com raiz projeto/. Inclui fontes, documentos e evidências; exclui executáveis, build, caches e arquivos temporários. Para recompilar basta `make`. Para entender decisões e resultados, comece por relatorio.pdf e docs/apresentacao.md. A execução acadêmica na máquina de referência deve repetir as medições e atualizar o relatório.
