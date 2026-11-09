# Extrapolações: hipóteses, unidades e limites

As oito estratégias não foram programadas nem cronometradas. Seus pontos são previsões ilustrativas, não afirmações de que executariam nesses tempos. Para tempo, usa-se custo nominal c=10⁻⁹ s por operação abstrata; não há calibração independente dessas operações. Um hash ou nó de árvore é modelado com 5 operações e Bloom com 7 hashes de custo c, escolha didática otimista. Não se derivou c de Big-O nem se ajustaram as curvas para garantir uma classificação. Multiplicar essas constantes por 0,1 ou 10 desloca os log₁₀ dos tempos em -1 ou +1, sem remover a explosão combinatória. Tráfego unário supõe 10⁹ B/s. Cache, branches, largura de banda e latência estão ausentes desses modelos; a incerteza é grande e não é expressa como erro estatístico.

Nas curvas força bruta/hash/árvore/Bloom, u(n)=D[1-(1-1/D)ⁿ], esperança sob amostragem uniforme independente. O gerador real é determinístico e só aproxima essa hipótese. Os u reais são registrados, não substituídos pela esperança. Para Bogosort, as multiplicidades são balanceadas: q=floor(n/D), r=n mod D, com D-r contagens q e r contagens q+1. Quando n≤D, isso é uma entrada distinta (pior cenário de multiplicidades), diferente da distribuição empírica; não se pretende que todas as curvas sejam o tempo da mesma instância. Usar n! em n>D seria incorreto. O modelo de subconjuntos materializa todos os elementos para tempo e memória, com fator n em ambas as curvas. A variante de streaming é discutida separadamente na análise.

Modelos de tempo em segundos:

- Força bruta: c n max(1,u/2), busca média no prefixo de únicos.
- Hash: 5cn, esperança com boa dispersão; não descreve colisões adversas.
- Árvore: 5cn log₂(u+1), limite de buscas em árvore balanceada.
- Bloom: 7cn + 78586c, limpeza conservadora por byte do filtro máximo mais hashes.
- Bogosort: cn n!/[(q!)^(D-r)((q+1)!)^r], checagem/embaralhamento nominal de cn.
- Subconjuntos: n2ⁿc, custo nominal proporcional aos elementos materializados (um fator constante 2 é absorvido por c).
- Unário: [32768,5×n×(n+1)/2]/10⁹, gravar e varrer em média metade do arquivo por consulta; sem seeks e com comprimentos médios uniformes.
- Matriz: cn², uma operação nominal por célula; não inclui alocação.

RAM extra hipotética em bytes (não medidas): força bruta/Bogosort/unário 128 B de trabalho nominal; hash 16u+128; árvore 32u+128; Bloom ceil[-7u/ln(1-0,01^(1/7))/8]+128, com k=7 e correção discreta para a meta de 1%; subconjuntos n2ⁿ (elementos uint16_t, sem descritores, além da pilha Θ(n)); matriz ceil(n²/8)+128, empacotada. Para subconjuntos, o volume materializado domina a pilha nas escalas dos gráficos; não se deve interpretar isso como memória obrigatória de streaming. Unário usa disco separado n×32768,5 B esperado. Os 128 B são hipótese ilustrativa de escalares e buffer, não garantia de ABI. Comparações no relatório consideram também matrizes em bytes.

A fonte scripts/documentos.py usa lgamma para fatoriais e expoentes em log₁₀ para 2ⁿ. dados/previsoes_log10.csv contém as oito curvas sem overflow e com unidade explícita. Em graficos/tempo.png, o painel esquerdo mostra segundos em escala log de 10⁻⁸ a 10⁶; as curvas fora dessa janela são continuadas integralmente no painel direito. O painel direito mostra o número log₁₀(segundos) sobre eixo symlog: valor 6 representa um milhão de segundos, valor 3000000 representa 10 elevado a três milhões de segundos, não três milhões de segundos. Essa segunda transformação permite ver simultaneamente números negativos (tempos <1 s), valores próximos de zero e expoentes enormes. Nenhuma curva inviável é removida.

As duas linhas sólidas com pontos são medianas medidas; barras no painel prático são mínimo/máximo. As outras oito linhas são modelos. graficos/memoria.png usa o mesmo tratamento de expoentes para RAM e outro painel em bytes para disco, entrada e RSS. O frame GCC mais a margem é constante para os dois algoritmos, e não uma medição dinâmica de pico a cada n. Sobreposições em curvas de RAM constante são esperadas; legenda e CSV permitem identificá-las.
