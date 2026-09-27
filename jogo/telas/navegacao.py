"""
Navegacao: seleção de itens de menu pelo teclado (setas ou WASD).

Todas as telas de menu do jogo guardam os botões que desenharam em
`self.botoes`, no formato (rect, acao), e já acendiam o destaque quando o
mouse passava por cima. Esta classe guarda qual ação está selecionada e
traduz as teclas em movimento e confirmação, para que teclado e mouse nunca
fiquem dessincronizados.

Uso numa tela:
  1. herdar de Navegacao;
  2. chamar `self._iniciar_navegacao(acao_inicial)` no __init__;
  3. no _botao, somar o selecionado ao hover: `hover or acao == self.acao_selecionada`;
  4. depois de montar os botões, chamar `self._sincronizar_mouse(mouse)`;
  5. no tratar_evento, chamar `self._navegar_teclado(event)`.
"""
import pygame

from ..sons import tocar

# nos menus as setas e o WASD fazem o mesmo papel
TECLA_CIMA = (pygame.K_UP, pygame.K_w)
TECLA_BAIXO = (pygame.K_DOWN, pygame.K_s)
TECLA_CONFIRMAR = (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE)


class Navegacao:
    def _iniciar_navegacao(self, acao_inicial):
        self.acao_selecionada = acao_inicial
        self.mouse_anterior = None

    def _esta_selecionado(self, acao):
        return acao == self.acao_selecionada

    def _acao_selecionada(self):
        """Ação a executar na confirmação (None se ainda não há botões)."""
        if not self.botoes:
            return None
        return self.acao_selecionada

    def _mover_selecao(self, delta):
        """Move o destaque uma posição, dando a volta na lista de botões."""
        acoes = [acao for rect, acao in self.botoes]
        if not acoes:
            return
        if self.acao_selecionada in acoes:
            posicao = acoes.index(self.acao_selecionada)
        else:
            posicao = 0
        self.acao_selecionada = acoes[(posicao + delta) % len(acoes)]
        tocar("menu_hover")

    def _sincronizar_mouse(self, mouse):
        """O mouse só assume a seleção quando ele realmente se move.

        Sem essa checagem, um mouse parado em cima de um botão desfaria a
        navegação feita pelo teclado no frame seguinte.
        """
        if mouse == self.mouse_anterior:
            return
        self.mouse_anterior = mouse
        for i, (rect, acao) in enumerate(self.botoes):
            if rect.collidepoint(mouse) and not self._esta_selecionado(acao):
                self.acao_selecionada = acao
                return

    def _navegar_teclado(self, event):
        """Devolve a ação confirmada, ou None se não for tecla de navegação."""
        if event.type != pygame.KEYDOWN:
            return None
        if event.key in TECLA_CIMA:
            self._mover_selecao(-1)
        elif event.key in TECLA_BAIXO:
            self._mover_selecao(1)
        elif event.key in TECLA_CONFIRMAR:
            return self._acao_selecionada()
        return None
