"""
Configurações e constantes globais do jogo.
"""
LARGURA = 1280
ALTURA = 720
FPS = 60

NOME_JOGO = "OPERAÇÃO BANANA"

# Fator visual de escala das entidades (desenho e hitbox proporcionais).
# A arte base é desenhada em uma grade pequena e ampliada suavemente,
# preservando os detalhes. 2.2 = 120% maiores que o padrão antigo (x1.0).
FATOR_ESCALA_JOGADOR = 2.2
FATOR_ESCALA_INIMIGO = 2.0

# Escala de power-ups e projéteis (mantém a proporção com as naves maiores).
FATOR_ESCALA_POWERUP = 1.7
FATOR_ESCALA_PROJETIL = 1.8
FATOR_ESCALA_EXPLOSAO = 1.3          # explosões são visuais dos projéteis

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

# ============================================================
# Balanceamento dos inimigos
# ============================================================
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
# Limiares de pontuação (rebalanceáveis):
# o intervalo de spawn é o tempo entre aparições (em frames, 60 = 1s):
# quanto MAIOR o valor, MAIS lento é o surgimento de inimigos.
SPAWN_INTERVALO_INICIAL = 110
SPAWN_INTERVALO_MINIMO = 30
PONTOS_DESBLOQUEIA_HELICOPTERO = 300
# o guarda pesado aparece um pouco antes do chefe para aquecer a reta final
PONTOS_DESBLOQUEIA_GUARDAPESADO = 350
# o chefe surge com 500 pontos; derrotá-lo encerra o jogo com vitória
PONTOS_DESBLOQUEIA_CHEFE = 500

# Duração (em frames) da transição após derrotar o chefe,
# durante a qual a explosão final é exibida antes da tela de vitória.
VITORIA_TRANSICAO = 55

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
LINHA_EXPLOSAO_BOMBA = 620

# Cores para menus
COR_MENU_FUNDO = (10, 10, 30)
COR_MENU_TITULO = (0, 255, 255)
COR_MENU_TEXTO = (255, 255, 255)
COR_MENU_DESTAQUE = (255, 255, 0)
COR_MENU_SOMBRA = (0, 100, 100)
COR_GAME_OVER = (255, 0, 0)

# ============================================================
# Estilo dos botões e temas (arcade, tema bananas/avião)
# ============================================================
# Bananas (identidade do jogo)
COR_BANANA = (250, 225, 70)
COR_BANANA_PONTA = (130, 96, 30)
COR_BANANA_POLPA = (252, 236, 132)   # polpa clara da banana descascada
COR_BANANA_NOVA = (255, 200, 40)     # banana dourada dos power-ups

# ============================================================
# Menu: selva tropical (folhas, cipós, madeira)
# ============================================================
COR_SELVA_FUNDO = (20, 48, 30)          # fundo escuro da selva
COR_FOLHA = (94, 178, 84)               # folha verde-clara
COR_FOLHA_MEDIA = (64, 138, 66)         # folha média
COR_FOLHA_ESCURA = (44, 100, 50)        # folha escura (profundidade)
COR_CIPO = (116, 84, 48)                # cipó/madeira
COR_MADEIRA = (124, 86, 50)             # placa de madeira
COR_MADEIRA_CLARA = (156, 108, 62)      # brilho da madeira
COR_MADEIRA_BORDA = (84, 56, 32)        # borda escura do botão
COR_MADEIRA_VEIO = (100, 66, 40)        # veios da madeira
COR_MADEIRA_TEXTO = (255, 244, 200)     # texto creme
COR_FLOR = (255, 110, 150)              # flores tropicais
COR_FRUTA = (255, 70, 90)               # frutinhas decorativas

# ============================================================
# Background da gameplay: cidade (Nova York) vista de cima
# Paleta escura e dessaturada: deve ser camada secundária,
# sem competir com jogador, inimigos, projéteis e power-ups.
# ============================================================
COR_CIDADE_FUNDO = (24, 28, 32)         # vazio entre quarteirões
COR_RUA = (38, 43, 48)                  # ruas horizontais
COR_AVENIDA = (33, 38, 42)              # avenidas verticais
COR_FAIXA_RUA = (88, 82, 66)            # faixa tracejada (amarela apagada)
COR_ZEBRA = (98, 102, 108)              # faixa de pedestres (apagada)
COR_PREDIO_1 = (52, 56, 60)
COR_PREDIO_2 = (48, 55, 60)
COR_PREDIO_3 = (56, 54, 50)
COR_PREDIO_4 = (46, 55, 52)
COR_PREDIO_BORDA = (64, 68, 72)
COR_PARQUE = (52, 66, 46)
COR_PARQUE_BORDA = (44, 54, 38)
COR_ARVORE = (46, 58, 42)
COR_ESTACIONAMENTO = (52, 56, 60)
COR_PISCINA = (56, 62, 66)              # (sem uso no cenário atual)
COR_TELHADO_DETALHE = (58, 60, 60)      # (sem uso no cenário atual)
COR_CARRO = [(62, 64, 66), (72, 74, 76), (66, 66, 68)]

# ============================================================
# Power-ups
# ============================================================
# Durações em frames (FPS = 60 -> 60 frames = 1 segundo)
POWERUP_FREQ = 400                 # intervalo base entre spawns (~6,7s)
POWERUP_FREQ_VARIACAO = 100        # variação aleatória do intervalo
POWERUP_MAX_NA_TELA = 3            # limite de power-ups simultâneos
POWERUP_VELOCIDADE = 2             # queda dos power-ups

POWERUP_DURACAO_TURBO = 300        # 5s (velocidade)
POWERUP_DURACAO_TIRO_DUPLO = 420   # 7s (tiro duplo)
POWERUP_DURACAO_ESCUDO = 300       # 5s (escudo)
POWERUP_DURACAO_MEGA_TIRO = 360    # 6s (mega tiro)
POWERUP_MULT_TURBO = 1.5           # multiplicador de velocidade do turbo
MEGA_TIRO_DANO = 3                 # dano de cada tiro no modo mega
POWERUP_BONUS_PONTOS = 50          # pontos da Banana Estrela
COR_TIRO_MEGA = (255, 90, 30)
TIRO_MEGA_TAMANHO = 20
COR_ESCUDO = (255, 220, 60)        # anel visual do escudo

# Cores e símbolos dos power-ups
COR_POWERUP_TURBO = (255, 215, 0)
COR_POWERUP_DOURADO = (255, 200, 40)
COR_POWERUP_CASCA = (170, 140, 60)
COR_POWERUP_EXPLOSIVA = (255, 140, 0)
COR_POWERUP_CORACAO = (255, 80, 120)
COR_POWERUP_ESTRELA = (255, 255, 100)
COR_POWERUP_SIMBOLO = (30, 30, 30)

# Frutas dos power-ups (família de frutas: cada efeito vira uma fruta)
COR_MORANGO = (232, 60, 74)         # turbo (velocidade)
COR_MORANGO_ESC = (150, 30, 44)
COR_ABACAXI = (255, 168, 50)        # mega tiro (explosivo)
COR_ABACAXI_ESC = (184, 102, 28)
COR_MELANCIA_CASCA = (82, 152, 68)  # escudo (fruta protetora)
COR_MELANCIA_CASCA_ESC = (46, 98, 54)
COR_MELANCIA_POLPA = (240, 84, 94)
COR_MACA = (222, 54, 78)            # coração de vida
COR_MACA_ESC = (140, 26, 46)
COR_FRUTA_SEMENTE = (118, 72, 34)
