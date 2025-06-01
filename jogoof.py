import random
import networkx as nx

import pygame
import math
import sys

class JogoDungeonRPG:
    def __init__(self):
        self.estamina_inicial = 100
        self.poder_inicial = 10
        self.fase_atual = 1
        self.itens = []
        
        # Configurações do Pygame
        pygame.init()
        self.largura = 1000
        self.altura = 700
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Dungeon RPG dos Grafos")
        
        # Cores
        self.cores = {
            'fundo': (20, 20, 40),
            'no_normal': (100, 150, 200),
            'no_atual': (50, 200, 50),
            'no_objetivo': (200, 50, 50),
            'no_visitado': (200, 200, 50),
            'aresta_normal': (150, 150, 150),
            'aresta_percorrida': (255, 165, 0),
            'texto': (255, 255, 255),
            'painel': (40, 40, 60)
        }
        
        # Fontes
        self.fonte_pequena = pygame.font.Font(None, 20)
        self.fonte_media = pygame.font.Font(None, 24)
        self.fonte_grande = pygame.font.Font(None, 32)
        
        self.clock = pygame.time.Clock()
        self.reiniciar_jogo()

    def reiniciar_jogo(self):
        self.estamina = self.estamina_inicial
        self.poder = self.poder_inicial
        self.itens = []
        self.grafo = nx.Graph()
        self.salas = []
        self.inicio = None
        self.fim = None
        self.atual = None
        self.caminho_percorrido = []
        self.visitados = set()
        self.posicoes_nos = {}
        self.raio_no = 30
        self.mensagem = ""
        self.tempo_mensagem = 0

    def rolar_dado(self, lados=20):
        return random.randint(1, lados)

    def gerar_item(self):
        itens_possiveis = [
            ("Espada de Ferro", 3), ("Cajado Místico", 4), ("Machado de Guerra", 5),
            ("Escudo Antigo", 2), ("Amuleto Sagrado", 2), ("Armadura Leve", 1),
            ("Elmo de Bronze", 2), ("Botas Rápidas", 1), ("Capa de Invisibilidade", 3),
            ("Anel de Força", 2), ("Poção de Poder", 2)
        ]
        item, bonus = random.choice(itens_possiveis)

        bonus += self.rolar_dado(4) // 2
        self.poder += bonus
        self.itens.append((item, bonus))

        self.mostrar_mensagem(f"Encontrou '{item}'! Poder +{bonus}")

    def gerar_monstro(self):
        temas = {
            1: ["Esqueleto", "Aranha Gigante", "Xamã das Trevas"],
            2: ["Cobra da Selva", "Tribo Esquecida", "Espírito da Floresta"],
            3: ["Lobo de Gelo", "Golem Congelado", "Feiticeiro Invernal"]
        }
        monstro = random.choice(temas[self.fase_atual])
        dificuldade = random.randint(5, 25)


        
        rolagem = self.rolar_dado() + self.poder


        
        if rolagem >= dificuldade:
            ganho = random.randint(2, 6)

            self.mostrar_mensagem(f"Derrotou {monstro}! Poder +{ganho}")
            self.poder += ganho
            if self.rolar_dado() > 12:
                self.gerar_item()
        else:
            perda = random.randint(5, 15)

            self.mostrar_mensagem(f"{monstro} te feriu! Estamina -{perda}")
            self.estamina -= perda

    def criar_dungeon(self, num_salas):
        self.grafo.clear()

        self.salas = [f"S{i}" for i in range(num_salas)]
        
        # Criar conexões lineares
        for i in range(num_salas - 1):
            peso = random.randint(5, 20)
            self.grafo.add_edge(self.salas[i], self.salas[i + 1], weight=peso)

        # Adicionar conexões extras
        for _ in range(num_salas // 2):
            a, b = random.sample(self.salas, 2)
            if not self.grafo.has_edge(a, b):
                self.grafo.add_edge(a, b, weight=random.randint(5, 20))

        self.inicio = self.salas[0]
        self.fim = self.salas[-1]
        self.atual = self.inicio
        self.caminho_percorrido = []
        self.visitados = {self.atual}
        
        # Calcular posições dos nós
        self.calcular_posicoes_nos()



    def calcular_posicoes_nos(self):
        # Usar layout do networkx e converter para coordenadas da tela
        pos = nx.spring_layout(self.grafo, seed=42)

        
        # Área do grafo (deixando espaço para o painel de informações)
        grafo_largura = self.largura - 250
        grafo_altura = self.altura - 100
        offset_x = 50
        offset_y = 50
        
        self.posicoes_nos = {}
        for no, (x, y) in pos.items():
            # Normalizar coordenadas para a tela
            tela_x = int(offset_x + (x + 1) * grafo_largura / 2)
            tela_y = int(offset_y + (y + 1) * grafo_altura / 2)
            self.posicoes_nos[no] = (tela_x, tela_y)




    def desenhar_grafo(self):
        self.tela.fill(self.cores['fundo'])
        
        # Desenhar arestas
        arestas_percorridas = set(tuple(sorted(par)) for par in self.caminho_percorrido)
        
        for u, v in self.grafo.edges():
            pos_u = self.posicoes_nos[u]
            pos_v = self.posicoes_nos[v]
            
            cor = self.cores['aresta_percorrida'] if tuple(sorted((u, v))) in arestas_percorridas else self.cores['aresta_normal']
            pygame.draw.line(self.tela, cor, pos_u, pos_v, 3)
            
            # Desenhar peso da aresta
            peso = self.grafo[u][v]['weight']
            meio_x = (pos_u[0] + pos_v[0]) // 2
            meio_y = (pos_u[1] + pos_v[1]) // 2
            
            texto_peso = self.fonte_pequena.render(str(peso), True, self.cores['texto'])
            rect_peso = texto_peso.get_rect(center=(meio_x, meio_y))
            pygame.draw.rect(self.tela, self.cores['fundo'], rect_peso.inflate(4, 4))
            self.tela.blit(texto_peso, rect_peso)

        # Desenhar nós
        for no in self.grafo.nodes():
            pos = self.posicoes_nos[no]
            
            # Escolher cor do nó
            if no == self.atual:

                cor = self.cores['no_atual']
            elif no == self.fim:

                cor = self.cores['no_objetivo']
            elif no in self.visitados:

                cor = self.cores['no_visitado']
            else:

                cor = self.cores['no_normal']
            
            pygame.draw.circle(self.tela, cor, pos, self.raio_no)
            pygame.draw.circle(self.tela, self.cores['texto'], pos, self.raio_no, 2)
            
            # Texto do nó
            texto_no = self.fonte_media.render(no, True, self.cores['texto'])
            rect_no = texto_no.get_rect(center=pos)
            self.tela.blit(texto_no, rect_no)









    def desenhar_painel_info(self):
        # Painel de informações
        painel_x = self.largura - 240
        painel_y = 10
        painel_largura = 230
        painel_altura = 200
        
        pygame.draw.rect(self.tela, self.cores['painel'], 
                        (painel_x, painel_y, painel_largura, painel_altura))
        pygame.draw.rect(self.tela, self.cores['texto'], 
                        (painel_x, painel_y, painel_largura, painel_altura), 2)
        
        # Informações do jogador
        info_y = painel_y + 10
        textos = [
            f"Fase: {self.fase_atual}",
            f"Estamina: {self.estamina}",
            f"Poder: {self.poder}",
            f"Atual: {self.atual}",
            f"Objetivo: {self.fim}",
            "",
            "Clique em um nó vizinho",
            "para se mover"
        ]
        
        for texto in textos:
            if texto:
                superficie_texto = self.fonte_pequena.render(texto, True, self.cores['texto'])
                self.tela.blit(superficie_texto, (painel_x + 10, info_y))
            info_y += 20







    def desenhar_mensagem(self):
        if self.tempo_mensagem > 0:
            superficie_msg = self.fonte_media.render(self.mensagem, True, self.cores['texto'])
            rect_msg = superficie_msg.get_rect(center=(self.largura // 2, 30))
            pygame.draw.rect(self.tela, self.cores['painel'], rect_msg.inflate(20, 10))
            self.tela.blit(superficie_msg, rect_msg)
            self.tempo_mensagem -= 1





    def mostrar_mensagem(self, texto):
        self.mensagem = texto
        self.tempo_mensagem = 180  # 3 segundos a 60 FPS


    def obter_no_clicado(self, pos_mouse):
        for no, pos_no in self.posicoes_nos.items():
            distancia = math.sqrt((pos_mouse[0] - pos_no[0])**2 + (pos_mouse[1] - pos_no[1])**2)
            if distancia <= self.raio_no:
                return no
        return None




    def pode_mover_para(self, destino):
        return destino in self.grafo.neighbors(self.atual)

















































    def mover_para(self, destino):
        if not self.pode_mover_para(destino):
            self.mostrar_mensagem("Movimento inválido!")
            return False
            
        custo = self.grafo[self.atual][destino]['weight']
        
        if custo > self.poder:
            self.mostrar_mensagem(f"Poder insuficiente! Necessário: {custo}")
            return False
        
        self.estamina -= custo
        self.caminho_percorrido.append((self.atual, destino))
        self.atual = destino
        self.visitados.add(destino)
        
        # Evento de monstro
        if self.atual != self.fim and self.atual != self.inicio:
            if random.random() < 0.8:
                self.gerar_monstro()
        
        return True

    def gerar_boss(self):
        bosses = {
            1: ("Rei Esqueleto", 25),
            2: ("Guardião da Selva", 30),
            3: ("Senhor do Gelo", 35)
        }
        nome, dificuldade = bosses[self.fase_atual]


        
        rolagem = self.rolar_dado() + self.poder


        
        if rolagem >= dificuldade:

            self.mostrar_mensagem(f"Derrotou {nome}! Fase concluída!")
            return True
        else:

            self.mostrar_mensagem(f"{nome} te derrotou!")
            self.estamina = 0
            return False





    def jogar_fase(self):
        self.criar_dungeon(6)
        self.mostrar_mensagem(f"Fase {self.fase_atual} iniciada!")
        
        rodando = True
        while rodando and self.atual != self.fim and self.estamina > 0:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:  # Clique esquerdo
                        no_clicado = self.obter_no_clicado(evento.pos)
                        if no_clicado and no_clicado != self.atual:
                            self.mover_para(no_clicado)
            
            # Desenhar tudo
            self.desenhar_grafo()
            self.desenhar_painel_info()
            self.desenhar_mensagem()
            
            pygame.display.flip()
            self.clock.tick(60)
            
            # Verificar condições de fim
            if self.estamina <= 0:
                self.mostrar_mensagem("Game Over - Estamina esgotada!")
                pygame.time.wait(2000)
                return False
        
        if self.atual == self.fim:
            if self.gerar_boss():
                self.fase_atual += 1
                return True
            else:
                return False
        
        return self.estamina > 0









    def jogar(self):
        self.mostrar_mensagem("Bem-vindo ao Dungeon RPG dos Grafos!")
        
        rodando = True
        while rodando and self.fase_atual <= 3 and self.estamina > 0:
            resultado = self.jogar_fase()
            if not resultado:
                rodando = False
        
        if self.estamina > 0 and self.fase_atual > 3:
            self.mostrar_mensagem("PARABÉNS! Você completou todas as fases!")
        
        # Tela final
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
            
            self.desenhar_grafo()
            self.desenhar_painel_info()
            self.desenhar_mensagem()
            pygame.display.flip()
            self.clock.tick(60)




if __name__ == "__main__":




    jogo = JogoDungeonRPG()