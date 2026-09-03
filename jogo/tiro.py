"""
Classe do Tiro disparado pelo jogador (banana) e pelos inimigos.
"""
from .entidade import Entidade
from .settings import COR_BANANA, COR_PROJETIL_INIMIGO


class Tiro(Entidade):
    def __init__(self, x, y, direcao=1, cor=None):
        super().__init__(x, y, 10)
        self.direcao = direcao
        if cor is not None:
            self.image.fill(cor)
        elif direcao == 1:
            self.image.fill(COR_BANANA)
        else:
            self.image.fill(COR_PROJETIL_INIMIGO)

    def update(self):
        self.rect.y -= self.velocidade * self.direcao
        if self.rect.y < 0 or self.rect.y > 800:
            self.kill()
