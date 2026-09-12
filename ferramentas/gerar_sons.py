"""
Gera efeitos sonoros sintetizados (WAV) para o jogo.

Usa apenas a biblioteca padrão do Python (wave, math, struct), sem
dependências externas. Os arquivos são criados dentro da pasta audio/
e consumidos pelo sistema de sons do jogo (jogo/sons.py).

Executar com:

    python ferramentas/gerar_sons.py
"""
import math
import os
import struct
import wave

RATE = 22050
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "audio")


def pacote(amostra):
    """Converte uma amostra float (-1..1) em 2 bytes (int16, little endian)."""
    return struct.pack("<h", max(-32767, min(32767, int(amostra * 32767))))


def salvar_wav(caminho, frames):
    with wave.open(caminho, "w") as arquivo:
        arquivo.setnchannels(1)
        arquivo.setsampwidth(2)
        arquivo.setframerate(RATE)
        arquivo.writeframes(b"".join(frames))


def nota(frequencia, duracao, volume=0.4, forma="quadrada"):
    """Gera os frames de uma nota com ataque curto e decaimento natural."""
    total = int(RATE * duracao)
    if forma == "quadrada":
        def onda(t):
            return math.copysign(1.0, math.sin(2 * math.pi * frequencia * t))
    else:
        def onda(t):
            return math.sin(2 * math.pi * frequencia * t)
    frames = []
    for i in range(total):
        t = i / RATE
        progresso = i / total
        envelope = min(1.0, i / (RATE * 0.01)) * (1 - progresso) ** 1.6
        frames.append(pacote(onda(t) * volume * envelope))
    return frames


def deslize(inicial, final, duracao, volume=0.3, forma="quadrada"):
    """Gera um tom que desliza de 'inicial' até 'final' (Hz)."""
    total = int(RATE * duracao)
    if forma == "quadrada":
        def onda(t, f):
            return math.copysign(1.0, math.sin(2 * math.pi * f * t))
    else:
        def onda(t, f):
            return math.sin(2 * math.pi * f * t)
    frames = []
    for i in range(total):
        t = i / RATE
        progresso = i / total
        f = inicial * (final / inicial) ** progresso
        envelope = min(1.0, i / (RATE * 0.005)) * (1 - progresso) ** 1.2
        frames.append(pacote(onda(t, f) * volume * envelope))
    return frames


def gerar_level_up(caminho):
    """Arpejo ascendente alegre (C-E-G-C), usado aos marcos de 100 pontos."""
    arpejo = [523.25, 659.25, 783.99, 1046.50]
    frames = []
    for f in arpejo:
        frames += nota(f, 0.16, volume=0.35)
    frames += nota(1046.50, 0.30, volume=0.42)
    salvar_wav(caminho, frames)
    print(f"gerado: {caminho}")


def gerar_spawn_inimigo(caminho):
    """Pop curto descendente, avisa que um inimigo surgiu no topo."""
    frames = deslize(700, 150, 0.22, volume=0.28)
    salvar_wav(caminho, frames)
    print(f"gerado: {caminho}")


def gerar_escudo_expirado(caminho):
    """Dois tons suaves descendentes, avisa que o escudo terminou."""
    frames = nota(392.0, 0.16, volume=0.30, forma="sine")
    frames += nota(311.13, 0.26, volume=0.30, forma="sine")
    salvar_wav(caminho, frames)
    print(f"gerado: {caminho}")


def main():
    alertas = os.path.join(AUDIO_DIR, "alertas")
    os.makedirs(alertas, exist_ok=True)
    gerar_level_up(os.path.join(alertas, "level_up.wav"))
    gerar_spawn_inimigo(os.path.join(alertas, "spawn_inimigo.wav"))
    gerar_escudo_expirado(os.path.join(alertas, "escudo_expirado.wav"))


if __name__ == "__main__":
    main()