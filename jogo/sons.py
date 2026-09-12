"""
Sistema de áudio centralizado do jogo.

Carrega os efeitos sonoros uma única vez na inicialização e disponibiliza
funções simples para reproduzi-los durante a partida. O volume de cada som
é configurado aqui, facilitando ajustes posteriores.
"""
import os

import pygame

_CAMINHO_AUDIO = os.path.join(os.path.dirname(__file__), "..", "audio")

# nome -> (subpasta, arquivo, volume, intervalo_minimo_ms)
_CONFIG = {
    # Jogador
    "tiro_jogador_a": ("jogador", "laser1.ogg", 0.40, 90),
    "tiro_jogador_b": ("jogador", "laser2.ogg", 0.40, 90),
    "dano_jogador": ("impactos", "impactPunch_heavy_000.ogg", 0.70, 250),
    "vida_critica": ("interface", "error_007.ogg", 0.45, 0),
    "escudo_bloqueia": ("impactos", "impactPlate_heavy_004.ogg", 0.70, 200),
    "escudo_expirado": ("alertas", "escudo_expirado.wav", 0.40, 0),
    # Inimigos
    "spawn_inimigo": ("alertas", "spawn_inimigo.wav", 0.25, 250),
    "tiro_guarda": ("inimigos", "laser3.ogg", 0.35, 250),
    "tiro_helicoptero": ("inimigos", "laser4.ogg", 0.50, 250),
    "tiro_viatura": ("inimigos", "laser5.ogg", 0.45, 120),
    "tiro_guarda_pesado": ("inimigos", "laser9.ogg", 0.55, 600),
    "tiro_boss": ("inimigos", "laser9.ogg", 0.60, 400),
    # Impactos de acerto
    "impacto_guarda": ("impactos", "impactMetal_light_000.ogg", 0.45, 80),
    "impacto_helicoptero": ("impactos", "impactMetal_medium_003.ogg", 0.50, 80),
    "impacto_viatura": ("impactos", "impactMetal_medium_003.ogg", 0.50, 80),
    "impacto_guarda_pesado": ("impactos", "impactMetal_heavy_004.ogg", 0.60, 80),
    "impacto_mega": ("impactos", "impactPlate_heavy_001.ogg", 0.65, 100),
    "boss_dano": ("impactos", "impactPlate_heavy_002.ogg", 0.80, 120),
    # Explosões
    "explosao_missil": ("explosoes", "impactMining_002.ogg", 0.60, 0),
    "explosao_missil_aguda": ("explosoes", "zapTwoTone2.ogg", 0.30, 0),
    "explosao_bomba": ("explosoes", "impactMining_001.ogg", 0.75, 0),
    "explosao_grande": ("explosoes", "spaceTrash2.ogg", 0.80, 0),
    "inimigo_destruido": ("explosoes", "zapTwoTone.ogg", 0.60, 90),
    "boss_destruido": ("explosoes", "spaceTrash4.ogg", 0.85, 0),
    "boss_destruido_sino": ("explosoes", "impactBell_heavy_001.ogg", 0.70, 0),
    # Vitória (sino triunfal reutilizado ao entrar na tela de vitória)
    "vitoria": ("explosoes", "impactBell_heavy_001.ogg", 0.75, 0),
    # Power-ups
    "powerup_turbo": ("powerups", "powerUp3.ogg", 0.50, 0),
    "powerup_tiro_duplo": ("powerups", "powerUp1.ogg", 0.50, 0),
    "powerup_escudo": ("powerups", "powerUp2.ogg", 0.50, 0),
    "powerup_mega_tiro": ("powerups", "powerUp4.ogg", 0.50, 0),
    "powerup_coracao": ("powerups", "powerUp11.ogg", 0.55, 0),
    "powerup_estrela": ("powerups", "pepSound1.ogg", 0.50, 0),
    # Progresso (novos sons sintetizados via ferramentas/gerar_sons.py)
    "level_up": ("alertas", "level_up.wav", 0.55, 0),
    # Boss
    "boss_entrada": ("alertas", "lowDown.ogg", 0.70, 0),
    "boss_fase2": ("explosoes", "spaceTrash2.ogg", 0.75, 0),
    # Interface / menu (inclui o menu de pausa)
    "menu_hover": ("interface", "select_001.ogg", 0.25, 150),
    "menu_confirmar": ("interface", "confirmation_001.ogg", 0.50, 0),
    "menu_voltar": ("interface", "back_003.ogg", 0.40, 0),
    "game_over": ("interface", "bong_001.ogg", 0.60, 0),
    "nova_partida": ("alertas", "threeTone1.ogg", 0.40, 0),
    "pausar": ("interface", "switch_001.ogg", 0.45, 0),
}

_SONS = {}            # nome -> (Sound, volume, intervalo_minimo_ms)
_ULTIMA_TOCADA = {}   # nome -> instante (ms) até o qual ignorar nova reprodução
_ALTERNA_PING = False
_INICIALIZADO = False
_VOLUME_MESTRE = 1.0  # volume geral (afeta tudo, inclusive música)
_VOLUME_EFEITOS = 1.0 # volume dos efeitos sonoros

# nome -> (subpasta, arquivo) das músicas de fundo
_MUSICAS = {
    "menu": ("soundtrack", "menu_sound.mp3"),
    "fase": ("soundtrack", "01. Bad Piggies Theme.mp3"),
    "morte": ("soundtrack", "menu_death.mp3"),
}
_MUSICA_ATUAL = None  # música de fundo tocando no momento


def volume_mestre():
    """Volume geral atual, de 0.0 a 1.0."""
    return _VOLUME_MESTRE


def set_volume_mestre(valor):
    """Define o volume geral (0.0 a 1.0)."""
    global _VOLUME_MESTRE
    _VOLUME_MESTRE = max(0.0, min(1.0, valor))
    if _INICIALIZADO and pygame.mixer.get_init():
        pygame.mixer.music.set_volume(_VOLUME_MESTRE)


def volume_efeitos():
    """Volume dos efeitos sonoros atual, de 0.0 a 1.0."""
    return _VOLUME_EFEITOS


def set_volume_efeitos(valor):
    """Define o volume dos efeitos sonoros (0.0 a 1.0)."""
    global _VOLUME_EFEITOS
    _VOLUME_EFEITOS = max(0.0, min(1.0, valor))


def _caminho(pasta, arquivo):
    return os.path.join(_CAMINHO_AUDIO, pasta, arquivo)


def tocar_musica(nome, loop=True):
    """Toca uma música de fundo, conforme a chave em _MUSICAS.

    Com `loop=False`, a música reproduz uma única vez.
    """
    global _MUSICA_ATUAL
    if not _INICIALIZADO or not pygame.mixer.get_init():
        return
    dados = _MUSICAS.get(nome)
    if dados is None:
        return
    if _MUSICA_ATUAL == nome:
        return
    try:
        pygame.mixer.music.load(_caminho(*dados))
    except pygame.error as e:
        print(f"Aviso: nao foi possivel carregar a musica '{dados[1]}': {e}")
        return
    pygame.mixer.music.set_volume(_VOLUME_MESTRE)
    pygame.mixer.music.play(-1 if loop else 0)
    _MUSICA_ATUAL = nome


def parar_musica():
    """Para a música de fundo (se houver)."""
    global _MUSICA_ATUAL
    if _INICIALIZADO and pygame.mixer.get_init():
        pygame.mixer.music.stop()
    _MUSICA_ATUAL = None


def pausar_musica():
    """Pausa a música de fundo."""
    if _INICIALIZADO and pygame.mixer.get_init() and _MUSICA_ATUAL:
        pygame.mixer.music.pause()


def retomar_musica():
    """Retoma a música de fundo que estava pausada."""
    if _INICIALIZADO and pygame.mixer.get_init() and _MUSICA_ATUAL:
        pygame.mixer.music.unpause()


def inicializar():
    """Carrega todos os efeitos sonoros (deve ser chamado uma única vez)."""
    global _INICIALIZADO
    if _INICIALIZADO:
        return
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init()
        except pygame.error:
            print("Aviso: mixer de audio nao disponivel; jogo sem som.")
            _INICIALIZADO = True
            return
    pygame.mixer.set_num_channels(16)
    for nome, (pasta, arquivo, volume, intervalo) in _CONFIG.items():
        try:
            som = pygame.mixer.Sound(_caminho(pasta, arquivo))
        except Exception as e:
            print(f"Aviso: nao foi possivel carregar o som '{arquivo}': {e}")
            continue
        _SONS[nome] = (som, volume, intervalo)
    _INICIALIZADO = True


def tocar(nome):
    """Reproduz um efeito sonoro pelo nome, respeitando o intervalo mínimo."""
    dados = _SONS.get(nome)
    if dados is None:
        return
    som, volume, intervalo = dados
    agora = pygame.time.get_ticks()
    if agora < _ULTIMA_TOCADA.get(nome, 0):
        return
    _ULTIMA_TOCADA[nome] = agora + intervalo
    som.set_volume(volume * _VOLUME_EFEITOS * _VOLUME_MESTRE)
    som.play()


def tocar_alternado(nome_a, nome_b):
    """Alterna entre dois nomes a cada chamada (ex.: dois lasers do jogador)."""
    global _ALTERNA_PING
    _ALTERNA_PING = not _ALTERNA_PING
    tocar(nome_a if _ALTERNA_PING else nome_b)


def ajustar_volume(nome, volume):
    """Muda o volume de um efeito em tempo de execução (0.0 a 1.0)."""
    dados = _SONS.get(nome)
    if dados is None:
        return
    som, _atual, intervalo = dados
    _SONS[nome] = (som, max(0.0, min(1.0, volume)), intervalo)