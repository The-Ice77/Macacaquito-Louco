"""
Configurações e constantes globais do jogo.
"""
#d
LARGURA = 800
ALTURA = 600
FPS = 60

# Margem de remoção de projéteis fora da tela
MARGEM_SAIDA_PROJETIL = 40

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

# ============================================================
# Projéteis dos inimigos
# ============================================================
# Guarda -> bala simples (pequena, rápida, reta para baixo)
VEL_BALA_TAMANHO = 8
VEL_BALA = 9
COR_BALA = (255, 230, 150)

# Helicóptero -> míssil (médio, mirado, pequena explosão)
VEL_MISSIL_TAMANHO = 14
VEL_MISSIL = 6
COR_MISSIL = (255, 120, 60)
PERSECUCAO_HELICOPTERO = 0.04          # correção leve (não persegue perfeito)
RAIO_EXPLOSAO_MISSIL = 26
COR_EXPLOSAO_MISSIL = (255, 180, 60)

# Aeronave rápida -> rajada de 2-3 balas muito rápidas
VEL_RAJADA_TAMANHO = 7
VEL_RAJADA = 11
COR_RAJADA = (120, 200, 255)
QTD_RAJADA_VIATURA = 3
INTERVALO_RAJADA = 8                   # frames entre projéteis da rajada
FREQ_RAJADA_VIATURA = 50

# Guarda pesado -> bomba explosiva (grande, lenta, grande explosão)
VEL_BOMBA_TAMANHO = 24
VEL_BOMBA = 3
COR_BOMBA = (80, 80, 80)
RAIO_EXPLOSAO_BOMBA = 55
COR_EXPLOSAO_BOMBA = (255, 120, 0)
INTERVALO_BOMBA = 110                  # cadência da bomba

# Boss -> míssil especial (fase 1)
VEL_MISSIL_BOSS_TAMANHO = 16
VEL_MISSIL_BOSS = 6
COR_MISSIL_BOSS = (255, 80, 200)
PERSECUCAO_BOSS = 0.05
RAIO_EXPLOSAO_MISSIL_BOSS = 30
COR_EXPLOSAO_MISSIL_BOSS = (255, 80, 200)
INTERVALO_TIRO_BOSS_FASE1 = 50

# Boss -> leque de 5 projéteis (fase 2)
VEL_LEQUE_TAMANHO = 9
VEL_LEQUE = 8
COR_LEQUE = (255, 220, 60)
QTD_LEQUE_BOSS = 5
INTERVALO_LEQUE_BOSS = 70

# Boss -> bomba especial (fase 2, muito lenta, explosão maior)
VEL_BOMBA_BOSS_TAMANHO = 32
VEL_BOMBA_BOSS = 2
COR_BOMBA_BOSS = (40, 40, 40)
RAIO_EXPLOSAO_BOMBA_BOSS = 80
COR_EXPLOSAO_BOMBA_BOSS = (255, 0, 0)
INTERVALO_BOMBA_BOSS = 160

# A bomba explode ao atingir a base (region where the player navigates)
LINHA_EXPLOSAO_BOMBA = 520

# Cores para menus
COR_MENU_FUNDO = (10, 10, 30)
COR_MENU_TITULO = (0, 255, 255)
COR_MENU_TEXTO = (255, 255, 255)
COR_MENU_DESTAQUE = (255, 255, 0)
COR_MENU_SOMBRA = (0, 100, 100)
COR_GAME_OVER = (255, 0, 0)
