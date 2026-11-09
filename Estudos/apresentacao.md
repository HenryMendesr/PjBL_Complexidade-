# Roteiro de apresentação

Integrantes: Henry Rodrigues, Rafael Maluf e Matheus.

1. Apresentar n, u e D=65536. Explicar por que n>D obriga repetições.
2. Demonstrar `python3 projeto/src/main.py heap 3 1 3 0 65535` e a mesma entrada com bitmap. Comparar as ordens das saídas.
3. Explicar os invariantes: Heap Sort organiza máximos e compacta blocos; bitmap representa presença e nunca escreve à frente da leitura.
4. Abrir as figuras individuais começando por tempo_medido.png. Diferenciar os pontos reais dos oito modelos tracejados.
5. Mostrar uma conta de cada estratégia exagerada. Explicar por que unário não é exponencial em n neste domínio e por que repetições alteram Bogosort.
6. Apresentar as limitações: os 256 B não estão demonstrados em Python; as taxas são locais e a máquina da disciplina precisa ser testada. Não usar os números anteriores de C.

## Perguntas para a defesa

**O(1) implica 256 B?** Não. Constante em n pode ser grande, e Python possui objetos e estruturas internas. O bitmap já usa 8192 B só em bits.

**Por que migrar para Python?** É a linguagem escolhida pela equipe. Isso facilita entendimento, mas exige declarar honestamente o custo do interpretador e os requisitos não cumpridos.

**O resultado tem o mesmo conjunto?** Os testes usam set e dict apenas como referência independente. As funções de produção não usam essas estruturas.

**Como compactar sem perder leituras futuras?** O índice de escrita está sempre na parte já consumida do vetor.

**O bitmap é recomendado para Datacenter?** Sim pelo domínio e pelo custo linear; a meta formal depende da máquina da disciplina. Consultar a nova tabela de resultados Python.

**O que significa E no gráfico completo?** A quantidade vale 10 elevado a E; não confundir o expoente com segundos.
