"""
Classe Jogo: controla o game loop principal e os estados.
"""
import random
import pygame

from .settings import (
    LARGURA, ALTURA, FPS, COR_FUNDO, COR_TEXTO,
    PONTOS_DESBLOQUEIA_GUARDAPESADO, PONTOS_DESBLOQUEIA_CHEFE,
)
from .jogador import Jogador
from .tiro import Tiro
from .inimigo import (
    Guarda, HelicopteroPolicial, ViaturaRapida,
    GuardaPesado, ChefeFinal,
)
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
        self.tiros_inimigos = pygame.sprite.Group()

        self.jogador = self.criar_jogador()
        self.todos_sprites.add(self.jogador)

        self.pontos = 0
        self.spawn_timer = 0
        self.spawn_intervalo = 40
        self.chefe = None
        self.proximo_chefe = PONTOS_DESBLOQUEIA_CHEFE
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
        self.tiros_inimigos.empty()
        self.jogador = self.criar_jogador()
        self.todos_sprites.add(self.jogador)
        self.chefe = None
        self.proximo_chefe = PONTOS_DESBLOQUEIA_CHEFE
        self.game_over = None

    @staticmethod
    def sorteia_posicao_topo(offset=40):
        return random.randint(offset, LARGURA - offset), -40

    def escolher_inimigo(self):
        """Sorteia o tipo de inimigo usando pesos conforme a pontuação."""
        opcoes = [("guarda", 5), ("viatura", 2)]
        if self.pontos >= 100:
            opcoes.append(("helicoptero", 2))
        if self.pontos >= PONTOS_DESBLOQUEIA_GUARDAPESADO:
            opcoes.append(("guarda_pesado", 1))

        tipos = [nome for nome, _ in opcoes]
        pesos = [peso for _, peso in opcoes]
        return random.choices(tipos, weights=pesos, k=1)[0]

    def criar_inimigo(self):
        tipo = self.escolher_inimigo()

        if tipo == "viatura":
            direcao = random.choice([-1, 1])
            x = -40 if direcao == 1 else LARGURA + 40
            inimigo = ViaturaRapida(
                x, random.randint(40, ALTURA // 2), direcao
            )
        elif tipo == "helicoptero":
            x, y = self.sorteia_posicao_topo(60)
            inimigo = HelicopteroPolicial(x, y, self.jogador)
        elif tipo == "guarda_pesado":
            inimigo = GuardaPesado(
                random.randint(40, LARGURA - 40), -40, self.jogador
            )
        else:
            inimigo = Guarda(random.randint(40, LARGURA - 40), -40,
                             self.jogador)

        inimigo.tiros_inimigos = self.tiros_inimigos
        self.todos_sprites.add(inimigo)
        self.inimigos.add(inimigo)

    def tratar_chefe(self):
        """Invoca/reinicia o chefe conforme a pontuação."""
        if self.chefe is None and self.pontos >= self.proximo_chefe:
            chefe = ChefeFinal(random.randint(100, LARGURA - 100),
                               self.jogador)
            chefe.tiros_inimigos = self.tiros_inimigos
            chefe.grupo_inimigos = self.inimigos
            self.todos_sprites.add(chefe)
            self.inimigos.add(chefe)
            self.chefe = chefe
        elif self.chefe is not None and not self.chefe.alive():
            self.proximo_chefe = self.pontos + PONTOS_DESBLOQUEIA_CHEFE // 2
            self.chefe = None

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
                                self.jogador.rect.y,
                                direcao=1
                            )
                            self.todos_sprites.add(tiro)
                            self.tiros.add(tiro)
                        except Exception:
                            pass

    def _deduzir_vida(self):
        """Reduz a vida do jogador (danos acumulados) e checa game over."""
        dano = 0
        if pygame.sprite.spritecollide(self.jogador, self.tiros_inimigos, True):
            dano += 1
        if pygame.sprite.spritecollide(self.jogador, self.inimigos, True):
            dano += 1

        if dano > 0:
            self.jogador.vida -= dano
            if self.jogador.vida <= 0:
                self.estado = "game_over"
                self.game_over = GameOver(self.pontos)

    def processar_jogada(self):
        self.spawn_timer += 1
        if self.spawn_timer > self.spawn_intervalo:
            try:
                self.criar_inimigo()
            except Exception as e:
                print(f"Erro ao criar inimigo: {e}")
            self.spawn_timer = 0

        acertos = pygame.sprite.groupcollide(
            self.inimigos, self.tiros, False, True
        )
        for inimigo, tiros in acertos.items():
            for tiro in tiros:
                inimigo.tomar_dano(tiro.velocidade)
            if not inimigo.alive():
                self.pontos += getattr(inimigo, "pontos", 1)

        if self.pontos > 0 and self.pontos % 100 == 0:
            if self.spawn_intervalo > 15:
                self.spawn_intervalo -= 2

        self.tratar_chefe()
        self._deduzir_vida()

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
