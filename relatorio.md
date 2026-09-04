# Relatório de Implementações - Macacuquito Louco

## Data: 03/09/2026

---

## Etapas Concluídas

### 1. Tela Inicial (Menu)
**Arquivo:** `menu.py`

- Título "MACACUQUITO LOUCO" com efeito de sombra
- Partículas animadas no fundo (80 pontos flutuantes)
- Instruções de controles (WASD + ESPAÇO)
- Texto "Pressione ENTER para jogar" com efeito de blink
- Opção "ESC para sair"

### 2. Tela de Game Over
**Arquivo:** `game_over.py`

- Título "GAME OVER" com efeito de sombra
- Exibição da pontuação final
- Opção "ENTER - Reiniciar" com blink
- Opção "ESC - Sair"
- Mensagem "Obrigado por jogar!"
- Partículas animadas no fundo (tema vermelho)

### 3. Sistema de Estados do Jogo
**Arquivo:** `jogo/aplicacao.py`

Três estados implementados:
- `menu` → Tela inicial
- `jogando` → Gameplay principal
- `game_over` → Tela de fim de jogo

Fluxo: MENU → JOGANDO → GAME_OVER → (reiniciar ou sair)

### 4. Dificuldade Progressiva
**Arquivo:** `jogo/aplicacao.py`

- Spawn intervalo diminui 2 unidades a cada 100 pontos
- Inimigos aparecem mais rápido conforme a pontuação aumenta
- Limite mínimo de 15 para o spawn intervalo

### 5. Tratamento de Erros
**Arquivo:** `main.py`, `jogo/aplicacao.py`

Proteções implementadas:
- Inicialização do pygame
- Criação da tela
- Criação de tiros
- Criação de inimigos
- Eventos de teclado

### 6. Sistema de Dependências
**Arquivo:** `requirements.txt` (novo)

```
pygame-ce>=2.5.0
```

### 7. Auto-instalação de Dependências
**Arquivo:** `main.py`

- Verifica se pygame está instalado
- Instala automaticamente via pip se necessário
- Reinicia o jogo após instalação

### 8. Cores para Menus
**Arquivo:** `jogo/settings.py`

Constantes adicionadas:
- `COR_MENU_FUNDO` (10, 10, 30)
- `COR_MENU_TITULO` (0, 255, 255) - ciano neon
- `COR_MENU_TEXTO` (255, 255, 255) - branco
- `COR_MENU_DESTAQUE` (255, 255, 0) - amarelo
- `COR_MENU_SOMBRA` (0, 100, 100) - ciano escuro

---

## Etapa 9: Reorganização da Estrutura

Todos os módulos do jogo foram organizados em um pacote `jogo/`, separando responsabilidades:

### Estrutura Antiga (tudo na raiz)

```
main.py, settings.py, entidade.py, jogador.py,
robo.py, tiro.py, menu.py, game_over.py
```

### Estrutura Nova (pacote jogo/)

```
main.py                # Fino: verifica dependências e inicia o jogo
jogo/
  __init__.py         # Marca como pacote Python
  settings.py         # Configurações e constantes
  entidade.py         # Classe base Entidade (sprite)
  jogador.py          # Classe Jogador
  tiro.py             # Classe Tiro
  robo.py             # Classes de inimigos (Robo, RoboZigueZague)
  menu.py             # Tela inicial
  game_over.py        # Tela de game over
  aplicacao.py        # Classe Jogo: game loop, estados e reset
```

### Responsabilidades separadas

| Arquivo | Responsabilidade |
|---------|-----------------|
| `main.py` | Entrada, auto-instalação de dependências, inicialização da tela |
| `jogo/aplicacao.py` | Game loop, sistema de estados, lógica de jogo, reset |
| demais módulos | Cada entidade/classe com sua própria responsabilidade |

### Melhorias
- `main.py` ficou enxuto (antes concentrava toda a lógica)
- Lógica de reset extraída para o método `Jogo.iniciar_nova_partida()`
- Imports relativos dentro do pacote (`from .settings import ...`)
- Removido tracking indevido de `__pycache__` do Git

---

## Arquivos do Projeto

| Arquivo | Descrição |
|---------|-----------|
| `main.py` | Ponto de entrada, dependências, inicialização |
| `jogo/__init__.py` | Marca o pacote `jogo` |
| `jogo/settings.py` | Configurações e constantes |
| `jogo/entidade.py` | Classe base para sprites |
| `jogo/jogador.py` | Classe do jogador |
| `jogo/robo.py` | Classes de inimigos |
| `jogo/tiro.py` | Classe dos projéteis |
| `jogo/menu.py` | Tela inicial |
| `jogo/game_over.py` | Tela de game over |
| `jogo/aplicacao.py` | Classe Jogo: game loop e estados |
| `requirements.txt` | Dependências |
| `relatorio.md` | Este relatório |

---

## Controles

| Tecla | Ação |
|-------|------|
| W | Mover para cima |
| A | Mover para esquerda |
| S | Mover para baixo |
| D | Mover para direita |
| ESPAÇO | Atirar |
| ENTER | Iniciar / Reiniciar |
| ESC | Sair |

---

## Etapa 10: Novos Inimigos (Etapa A - forças policiais)

Identidade visual cômica/cartunesca inspirada en perseguição aérea, sem copiar
assets. Protagonista: macaco em avião de bananas.

### Arquivos modificados/criados

| Arquivo | Alteração |
|---------|-----------|
| `jogo/robo.py` | **Removido** (renomeado para `inimigo.py`) |
| `jogo/inimigo.py` | **Novo** - classes de inimigos |
| `jogo/tiro.py` | Parametrizado com direção (jogador sobe, inimigo desce) |
| `jogo/jogador.py` | Visual do avião de bananas |
| `jogo/settings.py` | Cores e balanceamento dos inimigos |
| `jogo/aplicacao.py` | Sistema de spawn por peso + projéteis inimigos |
| `jogo/game_over.py` | Cor COR_ROBO renomeada para COR_GAME_OVER |

### `jogo/inimigo.py` - classe abstrata `Inimigo`
- Base abstrata (`ABC`) com `vida`, `pontos`, `cor`, `tomar_dano(dano)`,
  `saiu_da_tela()` e métodos abstratos `_movimentar()` e `_desenhar()`.
- Métodos abstratos garantem que cada inimigo implemente movimento e visual.

### Inimigos da Etapa A

| Classe | Papel | Movimento | Vida/Pontos | Dispara |
|--------|-------|-----------|-------------|---------|
| `Guarda` | básico | desce com leve zigue-zague | 1 / 10 | não |
| `HelicopteroPolicial` | intermediário | segue X do jogador + desce | 3 / 25 | sim |
| `ViaturaRapida` | veloz | entra pela lateral, atravessa | 1 / 15 | não |

### Sistema de spawn por peso (`aplicacao.py`)
- `escolher_inimigo()` sorteia o tipo por pesos conforme a pontuação:
  - `Guarda` (peso 5) + `Viatura` (peso 2) desde o início
  - `Helicoptero` (peso 2) desbloqueado a partir de 100 pontos
- `criar_inimigo()` posiciona cada tipo (viatura entra pelas laterais).
- Pontuação agora usa `inimigo.pontos` (antes sempre +1).

### Projéteis inimigos
- Novo group `tiros_inimigos` no `aplicacao.py`.
- Helicóptero dispara projéteis que descem e colidem com o jogador.
- `Tiro.__init__(x, y, direcao=1)` - `direcao=-1` para inimigos.

### Tratamento de erros
- `criar_inimigo` envolvido em try/except com mensagem clara.
- `criar_tiro_inimigo` retorna `None` em caso de erro (evita crash).

---

## Etapa 10.1: Ajustes pós-Etapa A

- **Guarda** agora se move em direção ao jogador (segue o X do jogador
  enquanto desce), em vez de apenas zigue-zague aleatório.
- **Correção de game over**: o jogador morre exatamente quando a vida chega
  a `0` (antes podia continuar até `-3`). Danos de projéteis inimigos e
  colisões agora são contabilizados juntos no método `_deduzir_vida()`, que
  checa `vida <= 0` imediatamente.

---

## Etapa 10.2: Etapa B — GuardaPesado e ChefeFinal

### GuardaPesado (`jogo/inimigo.py`)
- Novo inimigo raro, lento e resistente (vida 8).
- Aparece a partir de 1200 pontos com peso baixo (1) no spawn.
- Segue o jogador horizontalmente enquanto desce.
- Dispara projéteis **fortes** (vermelhos) em intervalos longos.
- Cores e constantes em `settings.py` (`COR_GUARDAPESADO`,
  `VIDA_GUARDAPESADO`, etc.).

### ChefeFinal (`jogo/inimigo.py`)
- Chefe ruivo/viajero, fica no topo e se move de um lado ao outro.
- Vida 40, vale 200 pontos.
- **Fase 1**: barragem de 2 projéteis normais.
- **Fase 2** (vida ≤ metade): muda para vermelho intenso, fica mais
  rápido, dispara barragem de 3 projéteis fortes e **chama Guardas**
  periodicamente.
- Invocação por pontuação: surge a partir de 2000 pontos
  (`PONTOS_DESBLOQUEIA_CHEFE`); quando derrotado, reaparece após mais
  1000 pontos.

### Tiro (`jogo/tiro.py`)
- `Tiro` agora aceita `cor` opcional para projéteis fortes (padrão
  preservado).

### Integração (`jogo/aplicacao.py`)
- `escolher_inimigo` inclui `guarda_pesado` após 1200 pontos.
- `criar_inimigo` cria `GuardaPesado`.
- Novo método `tratar_chefe()` controla invocação/reinvocação do chefe.
- `iniciar_nova_partida` reseta o chefe e o próximo limiar.

---

## Etapa 10.3: Ajustes de balanceamento e disparo

- **Correção de colisão**: antes, `groupcollide(..., True, True)` matava
  qualquer inimigo com 1 tiro, ignorando a vida. Agora cada tiro aplica
  `tomar_dano(tiro.velocidade)` e o inimigo só morre quando a vida chega a
  `0`. Isso faz a vida dos inimigos (heli, guarda pesado, chefe) contar de
  verdade.
- **Chefe mais resistente**: vida aumentada de 40 para 80 (8 tiros para
  derrotar, em vez de 1).
- **Guarda agora dispara**: projéteis simples em intervalos regulares.
- **Helicóptero e GuardaPesado já disparavam**; confirmado em loop real.
- Todos os inimigos recebem `tiros_inimigos` na criação (`criar_inimigo`).

---

## Etapa 11+ (Próximos Passos)

- [x] Diferentes tipos de inimigos (básicos da Etapa A)
- [x] GuardaPesado (inimigo raro e resistente)
- [x] ChefeFinal (com fases e chamada de inimigos)
- [ ] Power-ups
- [ ] Sons e música
- [ ] Melhorias visuais com sprites
- [ ] Sistema de ondas

---

## Notas Técnicas

- Pygame Community Edition (pygame-ce) 2.5.7
- Python 3.14.7
- Sistema de estados simples (sem máquinas de estados complexas)
- Tratamento de erros para evitar crashes
- Reset completo ao reiniciar o jogo
