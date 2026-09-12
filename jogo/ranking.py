"""
Sistema de ranking local (top 10) com armazenamento em ranking.json.

Responsável por carregar, salvar, ordenar e adicionar pontuações.
O arquivo fica na raiz do projeto e sobrevive ao fechamento do jogo.
"""
import json
import os

MAX_RANKING = 10

_CAMINHO_RANKING = os.path.join(
    os.path.dirname(__file__), "..", "ranking.json")


def carregar_ranking():
    """Retorna a lista ordenada (maior -> menor) com até 10 pontuações.

    Arquivo ausente, vazio ou corrompido resulta em ranking vazio.
    """
    try:
        with open(_CAMINHO_RANKING, "r", encoding="utf-8") as arquivo:
            dados = arquivo.read()
        if not dados.strip():
            return []
        bruto = json.loads(dados)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    except OSError as e:
        print(f"Aviso: nao foi possivel ler o ranking: {e}")
        return []

    if not isinstance(bruto, list):
        return []

    limpo = []
    for item in bruto:
        if not isinstance(item, dict):
            continue
        nick = item.get("nick")
        try:
            score = int(item.get("score"))
        except (TypeError, ValueError):
            continue
        if nick is not None and score >= 0:
            limpo.append({"nick": str(nick), "score": score})

    limpo.sort(key=lambda e: e["score"], reverse=True)
    return limpo[:MAX_RANKING]


def salvar_ranking(entradas):
    """Grava a lista de pontuações no arquivo (ordenada, até 10)."""
    entradas = sorted(entradas, key=lambda e: e["score"], reverse=True)
    entradas = entradas[:MAX_RANKING]
    try:
        with open(_CAMINHO_RANKING, "w", encoding="utf-8") as arquivo:
            json.dump(entradas, arquivo, ensure_ascii=False, indent=4)
    except OSError as e:
        print(f"Aviso: nao foi possivel salvar o ranking: {e}")


def adicionar_pontuacao(nick, score):
    """Adiciona uma pontuação ao ranking.

    Ordena, mantém no máximo 10 e retorna a posição (1 a 10) caso tenha
    entrado no ranking, ou None caso contrário.
    """
    nova = {"nick": nick, "score": int(score)}
    entradas = carregar_ranking()
    entradas.append(nova)
    entradas.sort(key=lambda e: e["score"], reverse=True)
    entradas = entradas[:MAX_RANKING]
    salvar_ranking(entradas)

    try:
        posicao = entradas.index(nova) + 1
    except ValueError:
        posicao = None
    return posicao