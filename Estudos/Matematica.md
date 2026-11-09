# Contas e argumentos para estudo

A fundamentação completa das dez estratégias está no relatório e em projeto/docs/analise_teorica.md. Este resumo serve à defesa oral.

- Saída correta exige simultaneamente: todos os valores emitidos pertencem à entrada, todo valor da entrada está representado e não há repetição na saída. Somente acertar a quantidade u não basta.
- E[u]=D[1−(1−1/D)ⁿ] decorre de somar indicadores de presença de cada valor. Não requer independência entre os indicadores.
- A soma de alturas dos nós de um heap é O(n): há no máximo floor(n/2ʰ) nós com altura pelo menos h; somar a série geométrica dá O(n). Extrações podem exigir O(log n) cada.
- Na força bruta, introduzir u únicos custa Σ(j=0..u−1)j. Repetir o último valor do prefixo pode exigir u comparações por leitura restante.
- No Bogosort, contar objetos rotulados dá n! possibilidades; ∏cⱼ! delas resultam na ordem desejada de valores. A razão é a probabilidade de sucesso por tentativa independente.
- Subconjuntos: cada posição participa de 2ⁿ⁻¹ folhas, logo a soma de tamanhos é n2ⁿ⁻¹. Multiplicar por dois bytes por elemento dá n2ⁿ B de payload, não apenas 2ⁿ B.
- Unário: o registro j é escrito uma vez e relido n−j vezes; seu peso no tráfego é n−j+1. Somar pesos dá n(n+1)/2 quando comprimentos têm a mesma média.
- Os índices Python são objetos. Dizer que há um número constante de variáveis não prova que suas alocações e frames caibam em 256 B; com n ilimitado, os índices também precisam de log n bits.
