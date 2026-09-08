"""
Classe Jogo: controla o game loop principal e os estados.
"""
import random
import pygame

from ..settings import (
    LARGURA, ALTURA, FPS, COR_TEXTO, COR_ESCUDO,
    SPAWN_INTERVALO_INICIAL, SPAWN_INTERVALO_MINIMO,
    PONTOS_DESBLOQUEIA_HELICOPTERO, PONTOS_DESBLOQUEIA_GUARDAPESADO,
    PONTOS_DESBLOQUEIA_CHEFE,
    POWERUP_FREQ, POWERUP_FREQ_VARIACAO, POWERUP_MAX_NA_TELA,
    COR_TIRO_MEGA, TIRO_MEGA_TAMANHO, MEGA_TIRO_DANO,
)
from ..entidades.jogador import Jogador
from ..entidades.tiro import TiroJogador
from ..entidades.inimigo import (
    Guarda, HelicopteroPolicial, ViaturaRapida,
    GuardaPesado, ChefeFinal,
)
from ..entidades.powerup import (
    BananaTurbo, BananaDourada, CascaBanana,
    BananaExplosiva, BananaCoracao, BananaEstrela,
)
from ..visual.efeito import (
    criar_fragmentos, criar_flash_impacto, criar_particulas_coleta,
    criar_linha_turbo, criar_explosao_destruicao,
)
from ..visual.bg_fase import BackgroundFase
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
        self.background = BackgroundFase()

        self.todos_sprites = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.tiros = pygame.sprite.Group()
        self.tiros_inimigos = pygame.sprite.Group()
        self.explosoes = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.efeitos_visuais = pygame.sprite.Group()

        self.jogador = self.criar_jogador()
        self.todos_sprites.add(self.jogador)

        self.pontos = 0
        self.spawn_timer = 0
        self.spawn_intervalo = SPAWN_INTERVALO_INICIAL
        self.powerup_timer = 0
        self.powerup_intervalo = POWERUP_FREQ
        self.turbo_frames = 0
        self.chefe = None
        self.proximo_chefe = PONTOS_DESBLOQUEIA_CHEFE
        self.rodando = True

    def criar_jogador(self):
        return Jogador(LARGURA // 2, ALTURA - 60)

    def iniciar_nova_partida(self):
        self.estado = "jogando"
        self.pontos = 0
        self.spawn_timer = 0
        self.spawn_intervalo = SPAWN_INTERVALO_INICIAL
        self.powerup_timer = 0
        self.powerup_intervalo = POWERUP_FREQ
        self.todos_sprites.empty()
        self.inimigos.empty()
        self.tiros.empty()
        self.tiros_inimigos.empty()
        self.explosoes.empty()
        self.powerups.empty()
        self.efeitos_visuais.empty()
        self.jogador = self.criar_jogador()
        self.todos_sprites.add(self.jogador)
        self.chefe = None
        self.proximo_chefe = PONTOS_DESBLOQUEIA_CHEFE
        self.turbo_frames = 0
        self.game_over = None

    @staticmethod
    def sorteia_posicao_topo(offset=40):
        return random.randint(offset, LARGURA - offset), -40

    def escolher_inimigo(self):
        """Sorteia o tipo de inimigo usando pesos conforme a pontuação."""
        opcoes = [("guarda", 5), ("viatura", 2)]
        if self.pontos >= PONTOS_DESBLOQUEIA_HELICOPTERO:
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
        inimigo.explosoes = self.explosoes
        inimigo.todos_sprites = self.todos_sprites
        self.todos_sprites.add(inimigo)
        self.inimigos.add(inimigo)

    @staticmethod
    def _tipo_powerup(jogador):
        """Sorteia um tipo de power-up. Coração só com vida abaixo do máximo."""
        tipos = ["turbo", "dourada", "casca", "explosiva", "estrela"]
        if jogador.vida < jogador.vida_max:
            tipos.append("coracao")
        return random.choice(tipos)

    def introduzir_powerup(self):
        """Cria um power-up no topo da tela."""
        tipo = self._tipo_powerup(self.jogador)
        x = random.randint(30, LARGURA - 30)
        classes = {
            "turbo": BananaTurbo,
            "dourada": BananaDourada,
            "casca": CascaBanana,
            "explosiva": BananaExplosiva,
            "coracao": BananaCoracao,
            "estrela": BananaEstrela,
        }
        powerup = classes[tipo](x, -30)
        self.todos_sprites.add(powerup)
        self.powerups.add(powerup)

    def tratar_chefe(self):
        """Invoca/reinicia o chefe conforme a pontuação."""
        if self.chefe is None and self.pontos >= self.proximo_chefe:
            chefe = ChefeFinal(random.randint(100, LARGURA - 100),
                               self.jogador)
            chefe.tiros_inimigos = self.tiros_inimigos
            chefe.explosoes = self.explosoes
            chefe.todos_sprites = self.todos_sprites
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
                        self.atirar()

    def atirar(self):
        """Dispara banana(s) conforme os efeitos ativos do jogador."""
        jogador = self.jogador
        mega = jogador.timer_mega_tiro > 0
        cor = COR_TIRO_MEGA if mega else None
        tamanho = TIRO_MEGA_TAMANHO if mega else 12
        dano = MEGA_TIRO_DANO if mega else 1

        posicoes = [jogador.rect.centerx]
        if jogador.timer_tiro_duplo > 0:
            posicoes = [jogador.rect.centerx - 12, jogador.rect.centerx + 12]

        for x in posicoes:
            tiro = TiroJogador(x, jogador.rect.y, cor=cor,
                               tamanho=tamanho, dano=dano)
            self.todos_sprites.add(tiro)
            self.tiros.add(tiro)

    def _deduzir_vida(self):
        """Reduz a vida do jogador (danos acumulados) e checa game over."""
        dano = 0

        # Projéteis não explosivos: dano direto ao tocar o jogador.
        for tiro in list(self.tiros_inimigos):
            if tiro.raio_explosao > 0:
                continue
            if pygame.sprite.collide_rect(self.jogador, tiro):
                dano += 1
                tiro.kill()

        # Projéteis explosivos: ao atingir o jogador, explodem (a explosão
        # causa o dano, uma única vez).
        for tiro in list(self.tiros_inimigos):
            if tiro.raio_explosao <= 0:
                continue
            if pygame.sprite.collide_rect(self.jogador, tiro):
                tiro.explodir()

        # Colisão com o corpo dos inimigos.
        atingidos = pygame.sprite.spritecollide(
            self.jogador, self.inimigos, True)
        if atingidos:
            dano += 1
            for inimigo in atingidos:
                criar_explosao_destruicao(
                    inimigo.rect.centerx, inimigo.rect.centery,
                    inimigo.cor, self.todos_sprites, self.efeitos_visuais,
                )

        # Dano de área das explosões (cada explosão danifica uma única vez).
        for explosao in list(self.explosoes):
            dano += explosao.aplicar_dano_se_no_alcance()

        if dano > 0:
            if self.jogador.timer_escudo > 0:
                return  # escudo absorve todo o dano
            self.jogador.vida -= dano
            self.jogador.ativar_tremor(10)
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
            for _tiro in tiros:
                inimigo.tomar_dano(getattr(_tiro, "dano", 1))
            if not inimigo.alive():
                self.pontos += getattr(inimigo, "pontos", 1)
                criar_explosao_destruicao(
                    inimigo.rect.centerx, inimigo.rect.centery,
                    inimigo.cor, self.todos_sprites, self.efeitos_visuais,
                )
            else:
                criar_flash_impacto(
                    inimigo.rect.centerx, inimigo.rect.bottom,
                    self.todos_sprites, self.efeitos_visuais,
                )

        if self.pontos > 0 and self.pontos % 100 == 0:
            if self.spawn_intervalo > SPAWN_INTERVALO_MINIMO:
                self.spawn_intervalo -= 2

        # Linhas de velocidade atrás do jogador enquanto o turbo está ativo
        if self.jogador.timer_turbo > 0:
            if self.turbo_frames % 3 == 0:
                criar_linha_turbo(
                    self.jogador.rect.centerx, self.jogador.rect.bottom,
                    self.todos_sprites, self.efeitos_visuais,
                )
            self.turbo_frames += 1

        # Spawn de power-ups (ocasional, com limite simultâneo na tela)
        self.powerup_timer += 1
        if self.powerup_timer >= self.powerup_intervalo:
            if len(self.powerups) < POWERUP_MAX_NA_TELA:
                self.introduzir_powerup()
            self.powerup_timer = 0
            self.powerup_intervalo = POWERUP_FREQ + random.randint(
                -POWERUP_FREQ_VARIACAO, POWERUP_FREQ_VARIACAO
            )

        # Coleta de power-ups: aplica o efeito e remove o item
        for powerup in pygame.sprite.spritecollide(
                self.jogador, self.powerups, True):
            bonus = powerup.aplicar(self.jogador)
            if bonus:
                self.pontos += bonus
            criar_particulas_coleta(
                self.jogador.rect.centerx, self.jogador.rect.centery,
                (255, 220, 90), self.todos_sprites, self.efeitos_visuais,
            )

        self.tratar_chefe()
        self._deduzir_vida()

        self.todos_sprites.update()

    def desenhar_hud(self):
        texto = self.font.render(
            f"Vida: {self.jogador.vida}  |  Pontos: {self.pontos}",
            True, COR_TEXTO
        )
        self.tela.blit(texto, (10, 10))

        # Indicador dos efeitos temporários ativos
        efeitos = self.jogador.efeitos_ativos()
        if efeitos:
            texto_efeitos = self.font.render(
                "  ".join(efeitos), True, COR_ESCUDO
            )
            self.tela.blit(texto_efeitos, (10, 40))

    def atualizar(self):
        if self.estado == "menu":
            self.menu.atualizar()
            self.menu.desenhar(self.tela)

        elif self.estado == "jogando":
            self.processar_jogada()
            self.background.atualizar(
                self.jogador.velocidade_atual / self.jogador.velocidade_base
            )
            self.background.desenhar(self.tela)
            self.todos_sprites.draw(self.tela)
            # anel visual do escudo ao redor do jogador
            if self.jogador.timer_escudo > 0:
                pygame.draw.circle(
                    self.tela, COR_ESCUDO,
                    self.jogador.rect.center, 28, 3
                )
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
