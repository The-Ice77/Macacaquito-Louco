"""
Ponto de entrada do jogo: verifica dependências, cria a tela e inicia o jogo.
"""
import sys
import subprocess


def verificar_dependencias():
    try:
        import pygame
        return True
    except ImportError:
        print("Pygame nao encontrado. Instalando...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("Dependencias instaladas com sucesso!")
            subprocess.Popen([sys.executable] + sys.argv)
            sys.exit()
        except Exception as e:
            print(f"Erro ao instalar dependencias: {e}")
            print("Execute manualmente: pip install -r requirements.txt")
            return False


def main():
    if not verificar_dependencias():
        sys.exit(1)

    import pygame
    from jogo.settings import LARGURA, ALTURA
    from jogo.aplicacao import Jogo

    try:
        pygame.init()
        tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Macacuquito Louco")
    except Exception as e:
        print(f"Erro ao iniciar o jogo: {e}")
        pygame.quit()
        return

    jogo = Jogo(tela)
    jogo.executar()

    pygame.quit()


if __name__ == "__main__":
    main()
