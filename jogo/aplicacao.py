"""
Classe Jogo: controla o game loop principal e os estados.
"""
import random
import pygame

from .settings import LARGURA, ALTURA, FPS, COR_FUNDO, COR_TEXTO
from .jogador import Jogador
from .tiro import Tiro
from .robo import RoboZigueZague
from .menu import Menu
from .game_over import GameOver


class Jogo:
    def __init__(self, tela):
        self.tela = tela
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)

        self.estado = "menu"
        self.menu = Menu()
        self.game_over = None

        self.todos_sprites = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.tiros = pygame.sprite.Group()

        self.jogador = self.criar_jogador()
        self.todos_sprites.add(self.jogador)

        self.pontos = 0
        self.spawn_timer = 0
        self.spawn_intervalo = 40
        self.rodando = True

    def criar_jogador(self):
        return Jogador(LARGURA // 2, ALTURA - 60)

    def iniciar_nova_partida(self):
        self.estado = "jogando"
        self.pontos = 0
        self.spawn_timer = 0
        self.spawn_intervalo = 40
        self.todos_sprites.empty()
        self.inimigos.empty()
        self.tiros.empty()
        self.jogador = self.criar_jogador()
        self.todos_sprites.add(self.jogador)
        self.game_over = None

    def tratar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False
                continue

            if self.estado == "menu":
                resultado = self.menu.tratar_evento(event)
                if resultado == "iniciar":
                    self.iniciar_nova_partida()
                elif resultado == "sair":
                    self.rodando = False

            elif self.estado == "game_over":
                resultado = self.game_over.tratar_evento(event)
                if resultado == "reiniciar":
                    self.iniciar_nova_partida()
                elif resultado == "sair":
                    self.rodando = False

            elif self.estado == "jogando":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        try:
                            tiro = Tiro(
                                self.jogador.rect.centerx,
                                self.jogador.rect.y
                            )
                            self.todos_sprites.add(tiro)
                            self.tiros.add(tiro)
                        except Exception:
                            pass

    def processar_jogada(self):
        self.spawn_timer += 1
        if self.spawn_timer > self.spawn_intervalo:
            try:
                robo = RoboZigueZague(
                    random.randint(40, LARGURA - 40), -40
                )
                self.todos_sprites.add(robo)
                self.inimigos.add(robo)
            except Exception:
                pass
            self.spawn_timer = 0

        colisao = pygame.sprite.groupcollide(
            self.inimigos, self.tiros, True, True
        )
        self.pontos += len(colisao)

        if self.pontos > 0 and self.pontos % 100 == 0:
            if self.spawn_intervalo > 15:
                self.spawn_intervalo -= 2

        if pygame.sprite.spritecollide(self.jogador, self.inimigos, True):
            self.jogador.vida -= 1
            if self.jogador.vida <= 0:
                self.estado = "game_over"
                self.game_over = GameOver(self.pontos)

        self.todos_sprites.update()

    def desenhar_hud(self):
        texto = self.font.render(
            f"Vida: {self.jogador.vida}  |  Pontos: {self.pontos}",
            True, COR_TEXTO
        )
        self.tela.blit(texto, (10, 10))

    def atualizar(self):
        if self.estado == "menu":
            self.menu.atualizar()
            self.menu.desenhar(self.tela)

        elif self.estado == "jogando":
            self.processar_jogada()
            self.tela.fill(COR_FUNDO)
            self.todos_sprites.draw(self.tela)
            self.desenhar_hud()

        elif self.estado == "game_over":
            self.game_over.atualizar()
            self.game_over.desenhar(self.tela)

    def executar(self):
        while self.rodando:
            self.clock.tick(FPS)
            self.tratar_eventos()
            self.atualizar()
            pygame.display.flip()
