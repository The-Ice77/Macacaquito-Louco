"""
Ponto de entrada do jogo: verifica dependências, cria a tela e inicia o jogo.
"""
import sys
import subprocess


def _em_ambiente_virtual():
    return sys.prefix != sys.base_prefix


def _mostrar_instrucoes_linux():
    print()
    print("=" * 62)
    print("  COMO INSTALAR O PYGAME-CE NO LINUX")
    print("=" * 62)
    print("A forma mais simples é usar um ambiente virtual (venv):")
    print("    python3 -m venv .venv")
    print("    .venv/bin/pip install -r requirements.txt")
    print("    .venv/bin/python main.py")
    print()
    print("Se o pip precisar compilar do codigo-fonte (erros de SDL2),")
    print("instale antes as dependencias de desenvolvimento:")
    print()
    print("  Debian/Ubuntu:")
    print("    sudo apt install python3-dev libsdl2-dev libsdl2-image-dev \\")
    print("        libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev \\")
    print("        libfreetype-dev")
    print()
    print("  Fedora:")
    print("    sudo dnf install python3-devel SDL2-devel SDL2_image-devel \\")
    print("        SDL2_mixer-devel SDL2_ttf-devel portmidi-devel freetype-devel")
    print()
    print("  Arch Linux:")
    print("    sudo pacman -S python python-pip sdl2 sdl2_image sdl2_mixer sdl2_ttf")
    print()
    print("Depois execute o jogo com o Python do venv:")
    print("    .venv/bin/python main.py")
    print("=" * 62)


def _mostrar_instrucoes():
    if sys.platform.startswith("linux"):
        _mostrar_instrucoes_linux()
        return
    print()
    print("Crie um ambiente virtual e instale as dependencias:")
    print("    python -m venv .venv")
    print("    .venv/bin/pip install -r requirements.txt")
    print("    .venv/bin/python main.py")


def verificar_dependencias():
    try:
        import pygame
        return True
    except ImportError:
        pass

    print("Pygame nao encontrado. Verificando o ambiente...")

    if not _em_ambiente_virtual():
        print("Você está usando o Python do sistema, onde o pip costuma")
        print("ser bloqueado em distribuições Linux modernas (PEP 668).")
        print("O recomendado é rodar pelo venv do projeto:")
        print("    .venv/bin/python main.py")
        print()

    print("Instalando as dependencias no ambiente atual:", sys.prefix)
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
    except subprocess.CalledProcessError:
        print()
        print("Nao foi possivel instalar as dependencias automaticamente.")
        _mostrar_instrucoes()
        return False

    print("Dependencias instaladas com sucesso!")
    print("Reiniciando o jogo...")
    subprocess.Popen([sys.executable] + sys.argv)
    sys.exit()


def main():
    if not verificar_dependencias():
        sys.exit(1)

    import pygame
    from jogo.settings import LARGURA, ALTURA, NOME_JOGO
    from jogo.telas.aplicacao import Jogo

    try:
        pygame.init()
        tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(NOME_JOGO)
    except Exception as e:
        print(f"Erro ao iniciar o jogo: {e}")
        pygame.quit()
        return

    jogo = Jogo(tela)
    jogo.executar()

    pygame.quit()


if __name__ == "__main__":
    main()