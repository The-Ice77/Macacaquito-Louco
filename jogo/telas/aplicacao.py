"""
Classe Jogo: controla o game loop principal e os estados.
"""
import math
import random
import pygame

from ..settings import (
    LARGURA, ALTURA, FPS, NOME_JOGO, VITORIA_TRANSICAO, COR_TEXTO,
    COR_ESCUDO, COR_JOGADOR,
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
from .vitoria import Vitoria
from ..visual.efeito import (
    criar_fragmentos, criar_flash_impacto, criar_flash_forte,
    criar_particulas_coleta, criar_linha_turbo, criar_explosao_destruicao,
    criar_particulas_propulsao,
)
from ..visual.bg_fase import BackgroundFase
from ..sons import (
    inicializar, tocar, tocar_alternado,
    tocar_musica, parar_musica, pausar_musica, retomar_musica,
)
from .menu import Menu
from .game_over import GameOver
from .pausa import Pausa
from .config import Configuracoes
from .nickname import Nickname
from .ranking import Ranking
from ..ranking import adicionar_pontuacao


SOM_POWERUP = {
    "BananaTurbo": "powerup_turbo",
    "BananaDourada": "powerup_tiro_duplo",
    "CascaBanana": "powerup_escudo",
    "BananaExplosiva": "powerup_mega_tiro",
    "BananaCoracao": "powerup_coracao",
    "BananaEstrela": "powerup_estrela",
}

ROTULO_POWERUP = {
    "BananaTurbo": "TURBO!",
    "BananaDourada": "TIRO DUPLO!",
    "CascaBanana": "ESCUDO!",
    "BananaExplosiva": "MEGA TIRO!",
    "BananaCoracao": "+1 VIDA",
    "BananaEstrela": "+50 PONTOS",
}


class Jogo:
    def __init__(self, tela):
        self.tela = tela
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.fonte_banner = pygame.font.SysFont(None, 64)
        self.fonte_boss = pygame.font.SysFont(None, 48)
        inicializar()
        tocar_musica("menu")

        self.estado = "menu"
        self.menu = Menu()
        self.game_over = None
        self.pausa = Pausa()
        self.config = Configuracoes()
        self.nickname = Nickname()
        self.ranking_tela = None
        self.background = BackgroundFase()
        self.nick = "MACACO"

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
        self.chefe = None
        self.proximo_chefe = PONTOS_DESBLOQUEIA_CHEFE
        self.rodando = True
        self._aviso_critico = False
        self._proximo_milestone = 100
        self.tela_pausa = None
        self.morte_timer = 0
        self.morte_duracao = 60
        self.entrada_timer = 0
        self.frame_jogo = 0
        self.aviso_boss = 0
        self.aviso_powerup = ""
        self.aviso_powerup_timer = 0
        self.inimigos_derrotados = 0
        self.chefe_venceu = False
        self.vitoria_timer = 0
        self.vitoria = None

    def criar_jogador(self):
        return Jogador(LARGURA // 2, ALTURA - 60)

    def iniciar_nova_partida(self):
        self.estado = "entrada"
        tocar("nova_partida")
        tocar_musica("fase")
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
        self.jogador.rect.y = ALTURA + 40   # entra vindo de baixo
        self.todos_sprites.add(self.jogador)
        self.chefe = None
        self.proximo_chefe = PONTOS_DESBLOQUEIA_CHEFE
        self.game_over = None
        self._aviso_critico = False
        self._proximo_milestone = 100
        self.tela_pausa = None
        self.entrada_timer = 0
        self.aviso_boss = 0
        self.aviso_powerup = ""
        self.aviso_powerup_timer = 0
        self.inimigos_derrotados = 0
        self.chefe_venceu = False
        self.vitoria_timer = 0
        self.vitoria = None

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
        tocar("spawn_inimigo")

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
        if self.chefe_venceu:
            return
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
            self.aviso_boss = 80
            self.jogador.reagir("surpresa", 70)
            tocar("boss_entrada")
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
                    tocar("menu_confirmar")
                    self.nickname.texto = ""
                    self.nickname.celebrar()
                    self.estado = "nickname"
                elif resultado == "ranking":
                    tocar("pausar")
                    self.ranking_tela = Ranking()
                    self.estado = "ranking"
                elif resultado == "config":
                    tocar("pausar")
                    self.config.retorno = "menu"
                    self.estado = "config"
                elif resultado == "sair":
                    tocar("menu_voltar")
                    self.rodando = False

            elif self.estado == "nickname":
                resultado = self.nickname.tratar_evento(event)
                if resultado == "confirmar":
                    self.nick = self.nickname.texto
                    self.iniciar_nova_partida()
                elif resultado == "voltar":
                    tocar("menu_voltar")
                    self.estado = "menu"

            elif self.estado == "ranking":
                resultado = self.ranking_tela.tratar_evento(event)
                if resultado == "voltar":
                    self.estado = "menu"

            elif self.estado == "config":
                resultado = self.config.tratar_evento(event)
                if resultado == "voltar":
                    tocar("menu_voltar")
                    self.estado = self.config.retorno

            elif self.estado == "game_over":
                resultado = self.game_over.tratar_evento(event)
                if resultado == "reiniciar":
                    tocar("menu_confirmar")
                    self.iniciar_nova_partida()
                elif resultado == "sair":
                    tocar("menu_voltar")
                    self.rodando = False

            elif self.estado == "jogando":
                if event.type == pygame.KEYDOWN and not self.chefe_venceu:
                    if event.key == pygame.K_SPACE:
                        self.atirar()
                    elif event.key == pygame.K_ESCAPE:
                        self.entrar_pausa()

            elif self.estado == "vitoria":
                resultado = self.vitoria.tratar_evento(event)
                if resultado == "reiniciar":
                    tocar("menu_confirmar")
                    self.iniciar_nova_partida()
                elif resultado == "menu":
                    tocar("menu_voltar")
                    tocar_musica("menu")
                    self.estado = "menu"

            elif self.estado == "entrada":
                pass  # entrada ignorada durante a aparição do jogador

            elif self.estado == "morte":
                pass  # entrada ignorada durante a queda do avião

            elif self.estado == "pausa":
                resultado = self.pausa.tratar_evento(event)
                if resultado == "continuar":
                    tocar("pausar")
                    retomar_musica()
                    self.estado = "jogando"
                elif resultado == "reiniciar":
                    tocar("menu_confirmar")
                    self.iniciar_nova_partida()
                elif resultado == "config":
                    tocar("pausar")
                    self.config.retorno = "pausa"
                    self.estado = "config"
                elif resultado == "sair":
                    tocar("menu_voltar")
                    self.rodando = False

    def entrar_pausa(self):
        """Congela a partida atual e abre o menu de pausa."""
        self.tela_pausa = self.tela.copy()
        self.estado = "pausa"
        tocar("pausar")
        pausar_musica()

    def _abrir_vitoria(self):
        """Abre a tela de vitória (som toca uma única vez)."""
        if self.vitoria is None:
            self.vitoria = Vitoria(self.pontos, self.inimigos_derrotados,
                                   self.jogador.vida)
            tocar("vitoria")
        self.estado = "vitoria"

    def _iniciar_morte(self):
        """Começa a queda do avião: impacto, tremor e som de derrota."""
        parar_musica()
        tocar("explosao_grande")          # som do impacto
        self.todos_sprites.remove(self.jogador)
        criar_explosao_destruicao(
            self.jogador.rect.centerx, self.jogador.rect.centery,
            COR_JOGADOR, self.todos_sprites, self.efeitos_visuais,
        )
        self.estado = "morte"
        self.morte_timer = 0
        self.morte_duracao = random.randint(48, 72)  # ~0,8 a 1,2 s
        self.rank_posicao = adicionar_pontuacao(self.nick, self.pontos)
        self.game_over = GameOver(self.pontos, self.nick,
                                  self.rank_posicao)

    def _atualizar_morte(self):
        """Sequência de queda + escurecimento antes do Game Over."""
        self.morte_timer += 1

        # o efeito de derrota entra logo depois do impacto
        if self.morte_timer == 30:
            tocar("game_over")

        # o avião desce acelerando aos poucos, perdendo o controle
        self.jogador.rect.y += int(0.8 + self.morte_timer * 0.05)
        self.jogador.rect.x += random.randint(-1, 1)
        self.background.atualizar(0.5)
        self.efeitos_visuais.update()

        if (self.morte_timer >= self.morte_duracao or
                self.jogador.rect.top >= ALTURA + 40):
            self.estado = "game_over"
            return

        # desenha a cena em uma superfície própria para o tremor de tela
        cena = pygame.Surface((LARGURA, ALTURA))
        self.background.desenhar(cena)
        self.todos_sprites.draw(cena)
        self._desenhar_aviao_morte(cena)

        self.tela.fill(0)
        if self.morte_timer < 12:
            tremor = 1 + (12 - self.morte_timer) // 2
            self.tela.blit(cena, (random.randint(-tremor, tremor),
                                  random.randint(-tremor, tremor)))
        else:
            self.tela.blit(cena, (0, 0))

        # escurecimento gradual da tela
        escuro = pygame.Surface((LARGURA, ALTURA))
        progresso = self.morte_timer / self.morte_duracao
        escuro.set_alpha(int(min(200, 200 * progresso)))
        escuro.fill(0)
        self.tela.blit(escuro, (0, 0))

    def _desenhar_aviao_morte(self, tela):
        """Desenha o avião girando e sumindo enquanto cai."""
        jogador = self.jogador
        angulo = min(self.morte_timer * 2.2, 140)   # gira lentamente
        rot = pygame.transform.rotozoom(jogador.base_image, angulo, 1)
        frame = pygame.Surface((40, 40), pygame.SRCALPHA)
        frame.blit(rot, (20 - rot.get_width() // 2,
                         20 - rot.get_height() // 2))
        progresso = self.morte_timer / self.morte_duracao
        fade = max(0.0, 1.0 - progresso)
        frame.set_alpha(int(255 * fade))
        tela.blit(frame, jogador.rect.topleft)

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
        tocar_alternado("tiro_jogador_a", "tiro_jogador_b")

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
                if isinstance(inimigo, ChefeFinal):
                    tocar("boss_destruido")
                    tocar("boss_destruido_sino")
                else:
                    tocar("inimigo_destruido")
                criar_explosao_destruicao(
                    inimigo.rect.centerx, inimigo.rect.centery,
                    inimigo.cor, self.todos_sprites, self.efeitos_visuais,
                )

        # Dano de área das explosões (cada explosão danifica uma única vez).
        for explosao in list(self.explosoes):
            dano += explosao.aplicar_dano_se_no_alcance()

        if dano > 0:
            if self.jogador.timer_escudo > 0:
                tocar("escudo_bloqueia")  # escudo absorve todo o dano
                return
            tocar("dano_jogador")
            self.jogador.vida -= dano
            self.jogador.ativar_tremor(10)
            self.jogador.reagir("dano", 22)
            if self.jogador.vida <= 1:
                if not self._aviso_critico:
                    tocar("vida_critica")
                    self._aviso_critico = True
            else:
                self._aviso_critico = False
            if self.jogador.vida <= 0:
                self._iniciar_morte()

    def processar_jogada(self):
        self.frame_jogo += 1

        # após derrotar o chefe a partida venceu: continua apenas a
        # animação da explosão final antes da tela de vitória
        if self.chefe_venceu:
            self.vitoria_timer += 1
            self.todos_sprites.update()
            if self.vitoria_timer >= VITORIA_TRANSICAO:
                self._abrir_vitoria()
            return

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
            som_impacto_tocado = False
            for _tiro in tiros:
                inimigo.tomar_dano(getattr(_tiro, "dano", 1))
                if not som_impacto_tocado:
                    if getattr(_tiro, "dano", 1) >= MEGA_TIRO_DANO:
                        tocar("impacto_mega")
                    elif isinstance(inimigo, ChefeFinal):
                        tocar("boss_dano")
                    elif isinstance(inimigo, GuardaPesado):
                        tocar("impacto_guarda_pesado")
                    elif isinstance(inimigo, ViaturaRapida):
                        tocar("impacto_viatura")
                    elif isinstance(inimigo, HelicopteroPolicial):
                        tocar("impacto_helicoptero")
                    else:
                        tocar("impacto_guarda")
                    som_impacto_tocado = True
            if not inimigo.alive():
                self.pontos += getattr(inimigo, "pontos", 1)
                self.inimigos_derrotados += 1
                criar_explosao_destruicao(
                    inimigo.rect.centerx, inimigo.rect.centery,
                    inimigo.cor, self.todos_sprites, self.efeitos_visuais,
                )
                if isinstance(inimigo, ChefeFinal):
                    tocar("boss_destruido")
                    tocar("boss_destruido_sino")
                    self.jogador.reagir("comemorar", 80)
                    # chefe derrotado: missão cumprida, encerra a partida
                    self.chefe_venceu = True
                    self.vitoria_timer = 0
                    self.chefe = None
                else:
                    tocar("inimigo_destruido")
                    self.jogador.reagir("feliz", 14)
            else:
                if isinstance(inimigo, ChefeFinal):
                    criar_flash_forte(
                        inimigo.rect.centerx, inimigo.rect.centery,
                        self.todos_sprites, self.efeitos_visuais,
                    )
                else:
                    criar_flash_impacto(
                        inimigo.rect.centerx, inimigo.rect.bottom,
                        self.todos_sprites, self.efeitos_visuais,
                    )

        # chefe caiu neste frame: a vitória encerra a partida imediatamente,
        # sem dar chance de o jogador morrer no mesmo instante
        if self.chefe_venceu:
            return

        if self.pontos >= self._proximo_milestone:
            tocar("level_up")
            self._proximo_milestone += 100
            if self.spawn_intervalo > SPAWN_INTERVALO_MINIMO:
                self.spawn_intervalo -= 2

        # Rastro de propulsão atrás do avião (turbo gera rastro mais forte)
        if self.jogador.timer_turbo > 0:
            if self.frame_jogo % 2 == 0:
                criar_linha_turbo(
                    self.jogador.rect.centerx, self.jogador.rect.bottom,
                    self.todos_sprites, self.efeitos_visuais,
                )
            if self.frame_jogo % 4 == 0:
                criar_particulas_propulsao(
                    self.jogador.rect.centerx, self.jogador.rect.bottom,
                    self.todos_sprites, self.efeitos_visuais, turbo=True)
        elif self.frame_jogo % 5 == 0:
            criar_particulas_propulsao(
                self.jogador.rect.centerx, self.jogador.rect.bottom,
                self.todos_sprites, self.efeitos_visuais)

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
            nome_som = SOM_POWERUP.get(type(powerup).__name__)
            if nome_som:
                tocar(nome_som)
            criar_particulas_coleta(
                self.jogador.rect.centerx, self.jogador.rect.centery,
                (255, 220, 90), self.todos_sprites, self.efeitos_visuais,
            )
            rotulo = ROTULO_POWERUP.get(type(powerup).__name__, "POWER UP!")
            self.aviso_powerup = rotulo
            self.aviso_powerup_timer = 55
            self.jogador.reagir("feliz", 30)

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

    def _atualizar_entrada(self):
        self.entrada_timer += 1
        # jogador sobe de baixo para a posição de voo
        alvo_y = ALTURA - 60
        if self.jogador.rect.y > alvo_y:
            self.jogador.rect.y = max(alvo_y, self.jogador.rect.y - 7)
        self.jogador.rect.x = LARGURA // 2 - 20
        self.background.atualizar(0.25)
        self.background.desenhar(self.tela)
        self.todos_sprites.draw(self.tela)
        self._desenhar_banner_entrada()
        if self.entrada_timer >= 50:
            self.estado = "jogando"

    def _desenhar_banner_entrada(self):
        t = self.entrada_timer
        qtd = 20
        fim = 38
        if t <= qtd:
            alpha = int(255 * (t / qtd))
        elif t >= fim:
            alpha = max(0, int(255 * (1 - (t - fim) / (50 - fim))))
        else:
            alpha = 255
        if alpha <= 0:
            return
        titulo = self.fonte_banner.render(NOME_JOGO, True, COR_JOGADOR)
        sombra = self.fonte_banner.render(NOME_JOGO, True, (60, 40, 10))
        titulo.set_alpha(alpha)
        sombra.set_alpha(alpha)
        cx = LARGURA // 2
        self.tela.blit(sombra, (cx - titulo.get_width() // 2 + 3, 153))
        self.tela.blit(titulo, (cx - titulo.get_width() // 2, 150))
        sub = self.font.render("Prepare-se!", True, COR_TEXTO)
        sub.set_alpha(alpha)
        self.tela.blit(sub, (cx - sub.get_width() // 2, 220))

    def _desenhar_aviso_boss(self, tela):
        if self.aviso_boss <= 0:
            return
        self.aviso_boss -= 1
        pulsar = int(140 + 115 * (0.5 + 0.5 * math.sin(self.frame_jogo * 0.4)))
        aviso = self.fonte_boss.render("!!! CHEFE !!!", True, (255, 90, 40))
        aviso.set_alpha(min(255, pulsar + 60))
        tela.blit(aviso, (LARGURA // 2 - aviso.get_width() // 2, 120))

    def _desenhar_aviso_powerup(self, tela):
        if self.aviso_powerup_timer > 0:
            self.aviso_powerup_timer -= 1
        if self.aviso_powerup_timer <= 0:
            return
        progresso = self.aviso_powerup_timer / 55
        alpha = int(255 * min(1.0, progresso * 2))
        rotulo = self.fonte_boss.render(self.aviso_powerup, True, COR_ESCUDO)
        rotulo.set_alpha(alpha)
        tela.blit(rotulo, (LARGURA // 2 - rotulo.get_width() // 2, 70))

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
            self._desenhar_aviso_boss(self.tela)
            self._desenhar_aviso_powerup(self.tela)

        elif self.estado == "entrada":
            self._atualizar_entrada()

        elif self.estado == "morte":
            self._atualizar_morte()

        elif self.estado == "game_over":
            self.game_over.atualizar()
            # novo recorde: feedback sonoro pouco depois da tela abrir
            if (self.game_over.timer == 60 and
                    self.game_over.posicao_ranking is not None):
                tocar("level_up")
            # a música de derrota toca uma única vez, ~1,5s depois da tela
            if self.game_over.timer == 90:
                tocar_musica("morte", loop=False)
            self.game_over.desenhar(self.tela)

        elif self.estado == "vitoria":
            self.vitoria.atualizar()
            self.vitoria.desenhar(self.tela)

        elif self.estado == "pausa":
            if self.tela_pausa is not None:
                self.tela.blit(self.tela_pausa, (0, 0))
            self.pausa.atualizar()
            self.pausa.desenhar(self.tela)

        elif self.estado == "config":
            self.config.atualizar()
            self.config.desenhar(self.tela)

        elif self.estado == "nickname":
            self.nickname.atualizar()
            self.nickname.desenhar(self.tela)

        elif self.estado == "ranking":
            self.ranking_tela.atualizar()
            self.ranking_tela.desenhar(self.tela)

    def executar(self):
        while self.rodando:
            self.clock.tick(FPS)
            self.tratar_eventos()
            self.atualizar()
            pygame.display.flip()
