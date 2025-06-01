class Dungeon:
    def __init__(self):
        self.graph = nx.Graph()
        self.rooms = []
        self.start = None
        self.end = None

    def create_dungeon(self, num_rooms):
        self.rooms = [f"Room {i}" for i in range(num_rooms)]
        for i in range(num_rooms - 1):
            self.graph.add_edge(self.rooms[i], self.rooms[i + 1], weight=random.randint(1, 10))

        for _ in range(num_rooms // 2):
            a, b = random.sample(self.rooms, 2)
            if not self.graph.has_edge(a, b):
                self.graph.add_edge(a, b, weight=random.randint(1, 10))

        self.start = self.rooms[0]
        self.end = self.rooms[-1]

    def visualize_dungeon(self, screen):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_color='black')
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.axis('off')
        plt.savefig('dungeon_graph.png')
        img = pygame.image.load('dungeon_graph.png')
        screen.blit(img, (0, 0))
        pygame.display.flip()

    def get_neighbors(self, room):
        return list(self.graph.neighbors(room))