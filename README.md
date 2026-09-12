🧩 Maze Solver — BFS, DFS e A*

Comparação prática entre três algoritmos clássicos de busca em grafos/espaço de estado — Busca em Largura (BFS), Busca em Profundidade (DFS) e A* (A-estrela) — aplicados à resolução de labirintos representados como uma grade de células livres e obstáculos.
Projeto desenvolvido em Python + Pygame para a disciplina de Inteligência Artificial (Universidade Federal da Grande Dourados — UFGD).

🎯 Objetivo

Implementar e comparar os três algoritmos de busca em termos de:
- Tamanho do caminho encontrado entre a célula de origem e a célula de destino;
- Número de células expandidas durante a busca;
- Tempo de execução.

🧠 Algoritmos implementados
  
- Busca em Largura (BFS): Explora o labirinto "em camadas", processando primeiro as células descobertas há mais tempo (estrutura FIFO, via collections.deque). Como todas as arestas têm o mesmo custo, garante encontrar o caminho mais curto em número de células.

- Busca em Profundidade (DFS): Avança por um caminho até não poder mais progredir, retrocedendo (backtracking) para explorar outro ramo (estrutura LIFO, pilha). Não garante o caminho mais curto, mas costuma expandir menos células.

- A* (A-estrela): Combina o custo já percorrido g(n) com uma estimativa heurística do custo restante h(n) (distância de Manhattan até o objetivo), expandindo sempre a célula de menor f(n) = g(n) + h(n). Usa uma fila de prioridade (heapq) e relaxamento de custo para garantir o caminho ótimo com menos expansões do que a busca cega.

Veja como usar a interface:

1. Escolha o algoritmo desejado na caixa de seleção (BFS, DFS ou A*);
2. Clique em Executar para rodar a busca sobre o labirinto atual, com animação;
3. Clique em Novo Labirinto para gerar um novo tabuleiro aleatório;
4. Acompanhe no rodapé o tamanho do caminho, o número de células expandidas e o tempo de execução.
Legenda de cores:
🟩 Início · 🟪 Objetivo · ⬛ Parede · 🟦 Explorado · 🟨 Caminho final

🛠️ Tecnologias
Python 3.
Pygame — renderização gráfica e interação.
Estruturas de dados: deque (fila), lista (pilha) e heapq (fila de prioridade).

📄 Licença
Este projeto é de uso acadêmico e está disponível livremente para fins de estudo e referência.
