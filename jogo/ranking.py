"""
Sistema de ranking local (top 10) com armazenamento em ranking.json.

Responsável por carregar, salvar, ordenar e adicionar pontuações.
O arquivo fica na raiz do projeto e sobrevive ao fechamento do jogo.

Cada nickname ocupa apenas uma posição: ao jogar novamente com o mesmo
nome, a pontuação guardada só é substituída quando a nova for maior.
"""
import json
import os

MAX_RANKING = 10

_CAMINHO_RANKING = os.path.join(
    os.path.dirname(__file__), "..", "ranking.json")


def normalizar_nick(nick):
    """Chave de comparação do nickname (ignora espaços e maiúsculas)."""
    return str(nick).strip().upper()


def manter_melhor_por_nick(entradas):
    """Descarta nomes repetidos, mantendo a maior pontuação de cada um."""
    melhores = {}
    for entrada in entradas:
        chave = normalizar_nick(entrada["nick"])
        if chave not in melhores or entrada["score"] > melhores[chave]["score"]:
            melhores[chave] = entrada
    return list(melhores.values())


def carregar_ranking():
    """Retorna a lista ordenada (maior -> menor) com até 10 pontuações.

    Cada nickname aparece uma única vez, com a sua melhor pontuação.
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

    # nomes repetidos viram uma entrada só (a melhor), antes de cortar o top 10
    limpo = manter_melhor_por_nick(limpo)
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
    """Adiciona ou atualiza a pontuação do jogador no ranking.

    Se o nickname já existir, a pontuação guardada só é substituída quando a
    nova for maior (nada é gravado caso contrário). Ordena, mantém no máximo
    10 e retorna a posição (1 a 10) caso a entrada tenha entrado ou
    melhorado no ranking, ou None caso contrário.
    """
    entradas = carregar_ranking()
    nova = {"nick": nick, "score": int(score)}
    chave = normalizar_nick(nick)

    # procura uma entrada do mesmo nickname
    indice = None
    for i, entrada in enumerate(entradas):
        if normalizar_nick(entrada["nick"]) == chave:
            indice = i
            break

    if indice is None:
        entradas.append(nova)          # nickname novo entra no ranking
    elif nova["score"] <= entradas[indice]["score"]:
        return None                     # não superou o próprio recorde
    else:
        entradas[indice] = nova        # substitui a pontuação anterior

    entradas.sort(key=lambda e: e["score"], reverse=True)
    entradas = entradas[:MAX_RANKING]
    salvar_ranking(entradas)

    try:
        posicao = entradas.index(nova) + 1
    except ValueError:
        posicao = None
    return posicao