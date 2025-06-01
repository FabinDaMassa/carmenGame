import pygame
import networkx as nx
import random

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Dungeon Graph Visualization")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dungeon, self.salas = self.create_dungeon()
        self.pos = nx.spring_layout(self.dungeon, seed=42)
        self._normalize_positions()
        self.player_pos = self.salas[0]  # Define o início como o primeiro nó

    def create_dungeon(self):
        dungeon = nx.Graph()
        salas = [f"Room {i}" for i in range(6)]
        # Garante que todas as salas estejam conectadas em sequência
        for i in range(len(salas) - 1):
            dungeon.add_edge(salas[i], salas[i + 1], weight=random.randint(5, 20))
        # Adiciona arestas extras aleatórias para criar ramificações
        extra_edges = random.randint(2, 4)
        for _ in range(extra_edges):
            a, b = random.sample(salas, 2)
            if not dungeon.has_edge(a, b):
                dungeon.add_edge(a, b, weight=random.randint(5, 20))
        return dungeon, salas

    def _normalize_positions(self):
        # Normaliza as posições para caberem dentro da tela com margens
        margin = 80
        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        for node in self.pos:
            x, y = self.pos[node]
            norm_x = margin + (x - min_x) / (max_x - min_x) * (self.width - 2 * margin)
            norm_y = margin + (y - min_y) / (max_y - min_y) * (self.height - 2 * margin)
            self.pos[node] = (norm_x, norm_y)

    def draw_graph(self):
        self.screen.fill((0, 0, 0))
        # Desenha arestas
        for u, v in self.dungeon.edges():
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            pygame.draw.line(self.screen, (200, 200, 200), (int(x1), int(y1)), (int(x2), int(y2)), 3)
        # Desenha nós
        for node, (x, y) in self.pos.items():
            sx, sy = int(x), int(y)
            color = (0, 255, 0) if node == self.player_pos else (100, 200, 255)
            pygame.draw.circle(self.screen, color, (sx, sy), 30)
            # Nome do nó
            font = pygame.font.SysFont(None, 24)
            text = font.render(node, True, (0, 0, 0))
            text_rect = text.get_rect(center=(sx, sy))
            self.screen.blit(text, text_rect)
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
            self.draw_graph()
            self.clock.tick(60)

    def handle_mouse_click(self, mouse_pos):
        for node, (x, y) in self.pos.items():
            sx, sy = int(x), int(y)
            if (mouse_pos[0] - sx) ** 2 + (mouse_pos[1] - sy) ** 2 < 30 ** 2:
                self.move_player(node)

    def move_player(self, new_pos):
        if new_pos in self.dungeon.neighbors(self.player_pos):
            self.player_pos = new_pos
            print(f"Moved to {self.player_pos}")

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()