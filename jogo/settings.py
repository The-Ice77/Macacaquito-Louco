"""
Configurações e constantes globais do jogo.
"""
#d
LARGURA = 800
ALTURA = 600
FPS = 60

# Cores (R, G, B)
COR_FUNDO = (20, 20, 20)
COR_TEXTO = (255, 255, 255)

# Protagonista (macaco / avião de bananas)
COR_JOGADOR = (139, 69, 19)    # marrom (macaco)
COR_BANANA = (255, 255, 0)     # amarelo (projétil do jogador)

# Forças policiais (inimigos)
COR_GUARDA = (30, 80, 180)            # azul guarda básico
COR_HELICOPTERO = (70, 130, 230)      # azul claro helicóptero
COR_VIATURA = (10, 40, 120)           # azul escuro viatura rápida
COR_GUARDAPESADO = (60, 20, 120)      # roxo escuro guarda pesado
COR_CHEFE = (200, 80, 40)             # ruivo (chefe final)
COR_CHEFE_FASE2 = (220, 30, 30)       # vermelho intenso (fase 2)
COR_PROJETIL_INIMIGO = (255, 165, 0)  # laranja (projéteis inimigos)
COR_PROJETIL_FORTE = (255, 60, 60)    # vermelho (projéteis fortes)

# Balanceamento dos inimigos
VIDA_GUARDA = 1
PONTOS_GUARDA = 10
VELOCIDADE_GUARDA = 3

VIDA_HELICOPTERO = 3
PONTOS_HELICOPTERO = 25
VELOCIDADE_HELICOPTERO = 2

VIDA_VIATURA = 1
PONTOS_VIATURA = 15
VELOCIDADE_VIATURA = 9

VIDA_GUARDAPESADO = 8
PONTOS_GUARDAPESADO = 80
VELOCIDADE_GUARDAPESADO = 1

VIDA_CHEFE = 80
PONTOS_CHEFE = 200
VELOCIDADE_CHEFE = 3
# Limiares de pontuação (rebalanceáveis)
PONTOS_DESBLOQUEIA_GUARDAPESADO = 1200
PONTOS_DESBLOQUEIA_CHEFE = 2000

# Cores para menus
COR_MENU_FUNDO = (10, 10, 30)
COR_MENU_TITULO = (0, 255, 255)
COR_MENU_TEXTO = (255, 255, 255)
COR_MENU_DESTAQUE = (255, 255, 0)
COR_MENU_SOMBRA = (0, 100, 100)
COR_GAME_OVER = (255, 0, 0)
