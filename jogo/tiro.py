"""
Classe do Tiro disparado pelo jogador.
"""
#e
from .entidade import Entidade
from .settings import COR_TIRO


class Tiro(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.image.fill(COR_TIRO)

    def update(self):
        self.rect.y -= self.velocidade
        if self.rect.y < 0:
            self.kill()
