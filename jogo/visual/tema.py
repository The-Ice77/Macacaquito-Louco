"""
Tema visual de selva para os menus.

Reúne os desenhos geométricos reutilizados pelo Menu e pelo GameOver:
folhas, cipós, bananas, flores e os botões em formato de placa de madeira.
Tudo é desenhado com formas do Pygame (sem imagens).
"""
import math
import random

import pygame

from ..settings import (
    LARGURA, ALTURA,
    COR_FOLHA, COR_FOLHA_MEDIA, COR_FOLHA_ESCURA, COR_CIPO,
    COR_MADEIRA, COR_MADEIRA_CLARA, COR_MADEIRA_BORDA,
    COR_MADEIRA_VEIO, COR_MADEIRA_TEXTO, COR_FLOR, COR_FRUTA,
    COR_BANANA, COR_BANANA_PONTA, COR_JOGADOR,
)

_cache_folhas = {}


def _escurecer(cor, fator=0.55):
    return tuple(max(0, min(255, int(c * fator))) for c in cor)


def folha_surface(largura, altura, cor):
    """Folha estilizada (elipse alongada com veia central), em cache."""
    chave = (largura, altura, cor)
    if chave in _cache_folhas:
        return _cache_folhas[chave]
    superficie = pygame.Surface((largura, altura), pygame.SRCALPHA)
    escura = _escurecer(cor)
    pontos = [
        (2, altura // 2),
        (largura // 4, 2),
        (largura - 8, 2),
        (largura, altura // 2),
        (largura - 8, altura - 2),
        (largura // 4, altura - 2),
    ]
    pygame.draw.polygon(superficie, cor, pontos)
    pygame.draw.line(superficie, escura, (4, altura // 2),
                     (largura - 8, altura // 2), max(2, altura // 6))
    for fracao in (0.3, 0.55, 0.8):
        xv = int(largura * fracao)
        desvio = max(1, altura // 5)
        pygame.draw.line(superficie, escura, (xv, altura // 2),
                         (xv - desvio, altura // 4), 2)
        pygame.draw.line(superficie, escura, (xv, altura // 2),
                         (xv - desvio, altura * 3 // 4), 2)
    _cache_folhas[chave] = superficie
    return superficie


def banana_surface(tamanho=16, cor=COR_BANANA, ponta=COR_BANANA_PONTA):
    """Banana em formato de meia-lua, em uma superfície própria."""
    largura = tamanho * 2 + 8
    altura = tamanho + 10
    superficie = pygame.Surface((largura, altura), pygame.SRCALPHA)
    rect_arco = pygame.Rect(4, 6, tamanho * 2, tamanho)
    pygame.draw.arc(superficie, cor, rect_arco, 0.1, math.pi - 0.1,
                    max(3, tamanho // 2))
    brilho = _escurecer(cor, 1.2)
    brilho = tuple(min(255, c) for c in brilho)
    pygame.draw.arc(superficie, brilho, rect_arco.inflate(-4, -4),
                    0.3, math.pi - 0.5, max(2, tamanho // 4))
    pygame.draw.circle(superficie, ponta, (4, 6 + tamanho // 2),
                       max(2, tamanho // 5))
    pygame.draw.circle(superficie, ponta, (4 + tamanho * 2, 6 + tamanho // 2),
                       max(2, tamanho // 5))
    return superficie


def cipo(tela, pontos, cor=COR_CIPO, largura=5):
    """Cipó/linha grossa com pontas arredondadas, passando por pontos."""
    if len(pontos) < 2:
        return
    pygame.draw.lines(tela, cor, False, pontos, largura)
    for ponto in pontos:
        pygame.draw.circle(tela, cor,
                           (int(ponto[0]), int(ponto[1])), largura // 2 + 1)


def _layout_selva():
    """Posições fixas do cenário de selva (evita variação a cada frame)."""
    if getattr(_layout_selva, "pronto", False):
        return _layout_selva.lista

    borda_esq = [(10, 120), (6, 260), (8, 420), (12, 560)]
    borda_dir = [(LARGURA - 10, 120), (LARGURA - 6, 260),
                 (LARGURA - 8, 420), (LARGURA - 12, 560)]

    # As folhas soltas ficam nas bordas ou no topo/base, para manter a
    # área central (título e botões) limpa e legível.
    flutuantes = []
    for i in range(10):
        if i % 3 == 0:
            x = random.randint(24, 150)
        elif i % 3 == 1:
            x = random.randint(LARGURA - 150, LARGURA - 24)
        else:
            x = random.randint(60, LARGURA - 60)
        if i % 3 == 2:
            y = random.choice([random.randint(56, 140),
                               random.randint(360, ALTURA - 40)])
        else:
            y = random.randint(120, ALTURA - 40)
        flutuantes.append({
            "x": x,
            "y": y,
            "fase": random.uniform(0, math.tau),
            "tam": random.randint(5, 9),
            "cor": (COR_FOLHA_MEDIA if i % 3 else COR_FOLHA_ESCURA),
        })

    # Pequenas folhinhas que atravessam lentamente a tela (partículas).
    particulas = []
    for i in range(14):
        particulas.append({
            "x": random.uniform(-40, LARGURA + 40),
            "y": random.uniform(60, ALTURA - 40),
            "vx": random.uniform(0.15, 0.5),
            "fase": random.uniform(0, math.tau),
            "tam": random.randint(3, 6),
            "cor": (COR_FOLHA_MEDIA if i % 3 else COR_FOLHA_ESCURA),
        })

    flores = [200, 420, 640, 860, 1080, 1260]

    _layout_selva.lista = {
        "borda_esq": borda_esq,
        "borda_dir": borda_dir,
        "topo": list(range(-20, LARGURA + 50, 44)),
        "base": list(range(-10, LARGURA + 40, 38)),
        "flutuantes": flutuantes,
        "particulas": particulas,
        "flores": flores,
        "bananas_penduradas": [210, 400, 590],
    }
    _layout_selva.pronto = True
    return _layout_selva.lista


def _banana_pendurada(tela, x_haste, y, timer, fase):
    """Banana pendurada que balança suavemente."""
    pygame.draw.line(tela, COR_CIPO, (x_haste, y - 16), (x_haste, y - 2), 3)
    angulo = math.sin(timer * 0.05 + fase) * 14
    banana = pygame.transform.rotozoom(banana_surface(14), angulo, 1)
    tela.blit(banana, (x_haste - banana.get_width() // 2,
                       y - banana.get_height() // 2))


def desenhar_moldura_selva(tela, timer):
    """Compõe a moldura tropical: topo, cantos, cipós, base e folhas soltas."""
    layout = _layout_selva()

    # --- topo: folhas pendendo da parte de cima ---
    for i, x in enumerate(layout["topo"]):
        cor = COR_FOLHA_ESCURA if i % 3 == 0 else COR_FOLHA_MEDIA
        folha = folha_surface(64, 30, cor)
        angulo = 10 + math.sin(timer * 0.03 + i) * 5
        rot = pygame.transform.rotozoom(folha, -angulo, 1)
        tela.blit(rot, (x, 16 - rot.get_height() // 2))

    # --- cantos: três folhas grandes em cada canto ---
    cantos = [
        (34, 40, 0, COR_FOLHA),
        (84, 70, 25, COR_FOLHA_MEDIA),
        (38, 96, -30, COR_FOLHA_ESCURA),
        (LARGURA - 34, 40, 180, COR_FOLHA),
        (LARGURA - 84, 70, 155, COR_FOLHA_MEDIA),
        (LARGURA - 38, 96, 210, COR_FOLHA_ESCURA),
    ]
    for x, y, angulo_base, cor in cantos:
        folha = folha_surface(110, 46, cor)
        angulo = angulo_base + math.sin(timer * 0.04) * 4
        rot = pygame.transform.rotozoom(folha, angulo, 1)
        if x < LARGURA // 2:
            pos = (x - rot.get_width() // 2, y - rot.get_height() // 2)
        else:
            pos = (x - rot.get_width() + rot.get_width() // 2,
                   y - rot.get_height() // 2)
        tela.blit(rot, pos)

    # --- cipós laterais com banana pendurada ---
    cipo(tela, [(14, 90), (8, 300), (16, 520)])
    for y, angulo in [(210, -20), (420, 14)]:
        folha = folha_surface(30, 15, COR_FOLHA)
        rot = pygame.transform.rotozoom(folha, angulo, 1)
        tela.blit(rot, (4, y))
    for i, y in enumerate(layout["bananas_penduradas"]):
        _banana_pendurada(tela, 13, y, timer, i * 1.7)

    cipo(tela, [(LARGURA - 14, 90), (LARGURA - 8, 300), (LARGURA - 16, 520)])
    for y, angulo in [(210, 20), (420, -14)]:
        folha = folha_surface(30, 15, COR_FOLHA)
        rot = pygame.transform.rotozoom(folha, angulo, 1)
        tela.blit(rot, (LARGURA - 4 - rot.get_width(), y))
    for i, y in enumerate(layout["bananas_penduradas"]):
        _banana_pendurada(tela, LARGURA - 13, y, timer, 2.6 + i * 1.7)

    # --- base: vegetação (touceiras) com flores e frutinhas ---
    for i, x in enumerate(layout["base"]):
        cor = COR_FOLHA_ESCURA if i % 2 else COR_FOLHA_MEDIA
        folha = folha_surface(52, 26, cor)
        rot = pygame.transform.rotozoom(folha, 12 - (i % 2) * 24, 1)
        tela.blit(rot, (x, ALTURA - 46 + (i % 2) * 10 -
                        rot.get_height() // 2))
    for i, x in enumerate(layout["flores"]):
        y = ALTURA - 34 + (i % 2) * 8
        pygame.draw.circle(tela, COR_FLOR, (x, y), 6)
        pygame.draw.circle(tela, (255, 210, 120), (x, y), 3)
        pygame.draw.circle(tela, COR_FRUTA, (x + 26, y + 8), 4)

    # --- folhas soltas flutuando (leve balanço) ---
    for folha in layout["flutuantes"]:
        x = folha["x"] + math.sin(timer * 0.04 + folha["fase"]) * 7
        angulo = math.sin(timer * 0.05 + folha["fase"]) * 14
        surf = folha_surface(int(folha["tam"] * 3), folha["tam"],
                             folha["cor"])
        rot = pygame.transform.rotozoom(surf, angulo, 1)
        tela.blit(rot, (int(x) - rot.get_width() // 2,
                        int(folha["y"]) - rot.get_height() // 2))

    # --- folhinhas pequenas atravessando lentamente a tela ---
    alcance = LARGURA + 80
    for folha in layout["particulas"]:
        x = (folha["x"] + timer * folha["vx"]) % alcance - 40
        y = folha["y"] + math.sin(timer * 0.03 + folha["fase"]) * 5
        angulo = math.sin(timer * 0.05 + folha["fase"]) * 24
        surf = folha_surface(int(folha["tam"] * 3), folha["tam"],
                             folha["cor"])
        rot = pygame.transform.rotozoom(surf, angulo, 1)
        tela.blit(rot, (int(x) - rot.get_width() // 2,
                        int(y) - rot.get_height() // 2))


def _pontos_estrela(cx, cy, raio_ext, raio_int):
    """Pontos de uma estrela de 5 pontas (usada como ícone de ranking)."""
    pontos = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = raio_ext if i % 2 == 0 else raio_int
        pontos.append((cx + math.cos(ang) * r, cy + math.sin(ang) * r))
    return pontos


def _desenhar_engrenagem(surf, cx, cy, cor):
    """Peça de engrenagem simples (ícone de opções)."""
    escura = _escurecer(cor, 0.55)
    for i in range(8):
        ang = i * math.pi / 4
        dx, dy = math.cos(ang) * 8, math.sin(ang) * 8
        pygame.draw.rect(surf, cor,
                         (int(cx + dx) - 2, int(cy + dy) - 2, 4, 4))
    pygame.draw.circle(surf, cor, (int(cx), int(cy)), 7)
    pygame.draw.circle(surf, escura, (int(cx), int(cy)), 3)


def desenhar_botao_selva(tela, centro_x, centro_y, largura, altura,
                         texto, fonte, timer, hover, simbolo=None):
    """Botão em placa de madeira com folhas e banana animadas (se hover).

    `simbolo` é um ícone pequeno exibido ao lado do botão no hover:
    "banana", "estrela", "engrenagem" ou "folha".

    Retorna o pygame.Rect lógico (base, sem escala) para colisão do mouse.
    """
    escala = 1.07 if hover else 1.0
    w = int(largura * escala)
    h = int(altura * escala)
    lateral = int(math.sin(timer * 0.1) * 4) if hover else 0

    superficie = pygame.Surface((w + 90, h + 70), pygame.SRCALPHA)
    base = pygame.Rect(45, 32, w, h)

    # sombra e madeira
    pygame.draw.rect(superficie, (58, 36, 20), base.move(5, 7),
                     border_radius=15)
    pygame.draw.rect(superficie, COR_MADEIRA, base, border_radius=15)
    pygame.draw.rect(superficie, COR_MADEIRA_CLARA, base, 2,
                     border_radius=15)
    pygame.draw.rect(superficie, COR_MADEIRA_BORDA, base, 4,
                     border_radius=15)
    # pregos/nós de madeira nos cantos
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        pygame.draw.circle(superficie, COR_MADEIRA_BORDA,
                           (base.centerx + dx * (base.w // 2 - 12),
                            base.centery + dy * (base.h // 2 - 12)), 4)
    # veios da madeira
    for k in range(1, 4):
        yv = base.y + (base.h * k) // 4
        pygame.draw.line(superficie, COR_MADEIRA_VEIO,
                         (base.x + 10, yv), (base.right - 10, yv + 3), 3)

    # folhas laterais balançando
    angulo = math.sin(timer * 0.08) * (16 if hover else 6)
    folha = folha_surface(50, 24, COR_FOLHA)
    f_esq = pygame.transform.rotozoom(folha, -20 - angulo, 1)
    f_dir = pygame.transform.rotozoom(folha, 20 + angulo, 1)
    superficie.blit(f_esq, (base.x - 10 - f_esq.get_width(),
                            base.centery - f_esq.get_height() // 2))
    superficie.blit(f_dir, (base.right + 10,
                            base.centery - f_dir.get_height() // 2))

    # banana girando sobre o botão
    banana = banana_surface(18)
    b_angulo = math.sin(timer * 0.09) * (30 if hover else 8)
    b = pygame.transform.rotozoom(banana, b_angulo, 1.15 if hover else 1.0)
    superficie.blit(b, (base.centerx - b.get_width() // 2,
                        base.y - 8 - b.get_height() + 12))

    # ícone pequeno ao lado do botão durante o hover
    if hover and simbolo is not None:
        icx = base.x - 8
        icy = base.centery + int(math.sin(timer * 0.3) * 3)
        pygame.draw.circle(superficie, (255, 240, 150, 70), (icx - 10, icy), 14)
        if simbolo == "banana":
            icon = banana_surface(11)
            icon = pygame.transform.rotozoom(
                icon, math.sin(timer * 0.2) * 18, 1)
            superficie.blit(icon, (icx - icon.get_width() - 4,
                                   icy - icon.get_height() // 2))
        elif simbolo == "estrela":
            pygame.draw.polygon(
                superficie, (255, 240, 120),
                _pontos_estrela(icx - 12, icy, 9, 5))
        elif simbolo == "engrenagem":
            _desenhar_engrenagem(superficie, icx - 12, icy, (255, 240, 170))
        elif simbolo == "folha":
            folha_icon = pygame.transform.rotozoom(
                folha_surface(26, 13, COR_FOLHA),
                math.sin(timer * 0.2) * 10 + 45, 1)
            superficie.blit(folha_icon,
                            (icx + 10 - folha_icon.get_width(),
                             icy - folha_icon.get_height() // 2))

    # texto (com sombra)
    texto_surf = fonte.render(texto, True, COR_MADEIRA_TEXTO)
    sombra = fonte.render(texto, True, (58, 36, 20))
    tx = base.centerx - texto_surf.get_width() // 2
    ty = base.centery - texto_surf.get_height() // 2
    superficie.blit(sombra, (tx + 2, ty + 2))
    superficie.blit(texto_surf, (tx, ty))

    tela.blit(superficie, (centro_x - superficie.get_width() // 2 + lateral,
                           centro_y - superficie.get_height() // 2 -
                           (3 if hover else 0)))

    rect = pygame.Rect(0, 0, largura, altura)
    rect.center = (centro_x, centro_y)
    return rect


def desenhar_macaco(tela, x, y, timer, olhar_x=None, celebrar=False,
                    cor_pelo=COR_JOGADOR, cor_pele=(255, 220, 180)):
    """Macaco geométrico simples, com pequenas animações de menu.

    `x`, `y` é a base (pés) do macaco. Ele pisca, olha para o `olhar_x`
    (posição do mouse), realiza uma pequena ação periódica e pode celebrar.
    """
    escura = _escurecer(cor_pelo, 0.7)
    boca = (120, 50, 25)

    fase = timer * 0.05
    acao = int(timer // 150) % 4      # 0 normal, 1 coça, 2 olhos vivos, 3 pula

    pulo = -int(math.sin(fase) * 2)
    if celebrar:
        pulo = -int(3 + math.sin(fase * 3) * 2)
    elif acao == 3:
        pulo = -int(math.sin(fase * 2) * 5)
    cy = y + pulo

    # cauda atrás (curva)
    pontos_cauda = [(x - 9, cy - 16), (x - 16, cy - 12),
                    (x - 19, cy - 5), (x - 16, cy + 1)]
    pygame.draw.lines(tela, escura, False, pontos_cauda, 3)
    pygame.draw.circle(tela, escura, (x - 16, cy + 1), 3)

    # pernas
    pygame.draw.ellipse(tela, cor_pelo, (x - 12, cy - 6, 8, 8))
    pygame.draw.ellipse(tela, cor_pelo, (x + 4, cy - 6, 8, 8))

    # corpo (tronco) com barriga clara
    pygame.draw.ellipse(tela, cor_pelo, (x - 11, cy - 30, 22, 30))
    pygame.draw.ellipse(tela, (240, 190, 150), (x - 6, cy - 24, 12, 18))

    # braços conforme a ação
    if celebrar:
        pygame.draw.line(tela, cor_pelo, (x - 8, cy - 26), (x - 16, cy - 40), 4)
        pygame.draw.circle(tela, cor_pelo, (x - 17, cy - 41), 4)
        pygame.draw.line(tela, cor_pelo, (x + 8, cy - 26), (x + 16, cy - 40), 4)
        pygame.draw.circle(tela, cor_pelo, (x + 17, cy - 41), 4)
    elif acao == 1:
        # coçando a cabeça
        pygame.draw.line(tela, cor_pelo, (x - 8, cy - 26), (x - 13, cy - 41), 4)
        pygame.draw.circle(tela, cor_pelo, (x - 14, cy - 42), 4)
        pygame.draw.line(tela, cor_pelo, (x + 8, cy - 26), (x + 10, cy - 12), 4)
        pygame.draw.circle(tela, cor_pelo, (x + 10, cy - 11), 4)
    else:
        pygame.draw.line(tela, cor_pelo, (x - 8, cy - 26), (x - 10, cy - 12), 4)
        pygame.draw.circle(tela, cor_pelo, (x - 10, cy - 11), 4)
        pygame.draw.line(tela, cor_pelo, (x + 8, cy - 26), (x + 10, cy - 12), 4)
        pygame.draw.circle(tela, cor_pelo, (x + 10, cy - 11), 4)

    # cabeça
    hx, hy = x, cy - 41
    pygame.draw.circle(tela, cor_pelo, (hx - 14, hy), 6)
    pygame.draw.circle(tela, cor_pelo, (hx + 14, hy), 6)
    pygame.draw.circle(tela, cor_pele, (hx - 14, hy), 3)
    pygame.draw.circle(tela, cor_pele, (hx + 14, hy), 3)
    pygame.draw.circle(tela, cor_pelo, (hx, hy), 15)
    pygame.draw.ellipse(tela, cor_pele, (hx - 10, hy - 4, 20, 18))

    # olhos (piscam periodicamente) com pupilas que seguem o mouse
    pisca = (timer % 120) < 9
    ox = 0
    if olhar_x is not None:
        ox = max(-4, min(4, (olhar_x - hx) // 16))
    if pisca or acao == 2 and (timer // 20) % 2 == 0:
        for ex in (-6, 6):
            pygame.draw.line(tela, (70, 45, 20),
                             (hx + ex + ox, hy - 2), (hx + ex + ox + 4, hy - 2), 2)
    else:
        for ex in (-6, 6):
            pygame.draw.circle(tela, (255, 255, 255),
                               (int(hx + ex + ox), hy - 2), 3)
            pygame.draw.circle(tela, (45, 30, 20),
                               (int(hx + ex + ox + (1 if ox >= 0 else -1)),
                                hy - 2), 1)

    # boca
    if celebrar:
        pygame.draw.circle(tela, boca, (int(hx), hy + 6), 4)
        pygame.draw.rect(tela, (255, 240, 240), (hx - 3, hy + 4, 6, 4))
    else:
        pygame.draw.arc(tela, boca, (hx - 6, hy + 1, 12, 9),
                        0.2, math.pi - 0.2, 2)

    # banana na mão ao comemorar
    if celebrar:
        tela.blit(banana_surface(8), (hx + 12, hy - 9))