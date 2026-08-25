"""
Ponto de entrada do jogo: inicializa a tela e roda o loop principal.
"""

import random
import pygame

from settings import LARGURA, ALTURA, FPS, COR_FUNDO, COR_TEXTO
from jogador import Jogador
from tiro import Tiro
from robo import RoboZigueZague


def main():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Robot Defense - Template")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    todos_sprites = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    tiros = pygame.sprite.Group()

    jogador = Jogador(LARGURA // 2, ALTURA - 60)
    todos_sprites.add(jogador)

    pontos = 0
    spawn_timer = 0

    rodando = True
    while rodando:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tiro = Tiro(jogador.rect.centerx, jogador.rect.y)
                    todos_sprites.add(tiro)
                    tiros.add(tiro)

        # timer de entrada dos inimigos
        spawn_timer += 1
        if spawn_timer > 40:
            robo = RoboZigueZague(random.randint(40, LARGURA - 40), -40)
            todos_sprites.add(robo)
            inimigos.add(robo)
            spawn_timer = 0

        # colisão tiro x robô
        colisao = pygame.sprite.groupcollide(inimigos, tiros, True, True)
        pontos += len(colisao)

        # colisão robô x jogador
        if pygame.sprite.spritecollide(jogador, inimigos, True):
            jogador.vida -= 1
            if jogador.vida <= 0:
                print("GAME OVER!")
                rodando = False

        # atualizar
        todos_sprites.update()

        # desenhar
        tela.fill(COR_FUNDO)
        todos_sprites.draw(tela)

        # Painel de pontos e vida
        texto = font.render(f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, COR_TEXTO)
        tela.blit(texto, (10, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
