# Relatório de Implementações - Operação Banana

## Data: 03/09/2026

> Última atualização: 11/09/2026

---

## Visão Geral

**Operação Banana** é um jogo 2D arcade em Python + Pygame onde o jogador controla um macaco em avião-banana, enfrentando forças policiais e um Chefe Final. O jogo foi construído incrementalmente ao longo de diversas etapas de implementação.

---

## Etapas Concluídas

### Etapa 1 — Tela Inicial (Menu)
**Arquivo:** `jogo/telas/menu.py`

- Título "OPERAÇÃO BANANA" com efeito de sombra e dupla camada
- Partículas animadas no fundo (80 pontos flutuantes)
- Macaco desenhado com desenho próprio (olhos, orelhas, sorriso)
- Botões em estilo madeira/selva com símbolos (▶, ×)
- Instruções de controles (WASD + ESPAÇO) na parte inferior
- Texto "Pressione ENTER para jogar" com efeito de blink
- Efeito de partículas celebração do macaco

---

### Etapa 2 — Tela de Game Over
**Arquivo:** `jogo/telas/game_over.py`

- Título "GAME OVER" com efeito de sombra
- Exibição da pontuação final
- Botões "REINICIAR" e "SAIR" em estilo madeira/selva (hover com mouse)
- Rodapé com nome do jogo
- Partículas animadas no fundo (tema vermelho)

---

### Etapa 3 — Sistema de Estados do Jogo
**Arquivo:** `jogo/telas/aplicacao.py`

Estados implementados (expansão contínua):

| Estado | Função |
|--------|--------|
| `menu` | Tela inicial (navegável com mouse/teclado) |
| `nickname` | Cadastro de nickname antes de jogar |
| `entrada` | Transição animada "Prepare-se!" |
| `jogando` | Gameplay principal |
| `pausa` | Pausa durante jogo (ESC) |
| `config` | Menu de opções (volume) |
| `morte` | Animação de morte do jogador |
| `game_over` | Tela de derrota |
| `ranking` | Top 10 pontuações locais |
| `vitoria` | Tela de sucesso ao derrotar o Boss |

---

### Etapa 4 — Dificuldade Progressiva
**Arquivo:** `jogo/telas/aplicacao.py`

- Spawn intervalo diminui a cada 100 pontos
- Inimigos aparecem mais rápido conforme a pontuação aumenta
- Limite mínimo de 15 para o spawn intervalo
- Novos tipos de inimigos são desbloqueados conforme a pontuação:
  - Guarda e Viatura: desde o início
  - Helicóptero: a partir de 100 pontos
  - Guarda Pesado: a partir de 350 pontos
  - Chefe Final: a partir de 500 pontos

---

### Etapas 5–7 — Tratamento de erros, dependências e auto-instalação
**Arquivos:** `main.py`, `jogo/telas/aplicacao.py`

- Verificação e instalação automática de dependências (`requirements.txt`)
- Proteções em inicialização do Pygame, criação da tela, inimigos e projéteis
- Reset completo ao reiniciar (`iniciar_nova_partida()`)

---

### Etapa 8 — Reorganização em Subpacotes
**Estrutura:** `jogo/entidades/`, `jogo/telas/`, `jogo/visual/`

Todos os módulos foram organizados em três subpacotes:
- `entidades/` — entidade, jogador, inimigo, tiro, powerup
- `telas/` — aplicacao, menu, game_over e telas extras
- `visual/` — bg_fase, tema, efeito

Imports relativos atualizados; `main.py` importa de `jogo.telas.aplicacao`.

---

### Etapa 9 — Novos Inimigos (Etapa A)
**Arquivo:** `jogo/entidades/inimigo.py`

Classes abstrata `Inimigo` (ABC) e inimigos:

| Classe | Vida | Pontos | Comportamento |
|--------|------|--------|---------------|
| `Guarda` | 1 | 10 | Desce com zigue-zague, segue X do jogador |
| `HelicopteroPolicial` | 3 | 25 | Segue X do jogador, dispara míssil direcionado |
| `ViaturaRapida` | 1 | 15 | Entra pelas laterais, rajada rápida |

**Sistema de spawn por peso:** `escolher_inimigo()` sorteia tipo conforme pontuação.

**Projéteis inimigos:** `Tiro.__init__(x, y, direcao=1)` — `direcao=-1` para inimigos.

---

### Etapa 10 — GuardaPesado e ChefeFinal
**Arquivo:** `jogo/entidades/inimigo.py`

**GuardaPesado** (a partir de 350 pontos):
- Vida 8, ponto 350
- Segue o jogador, dispara bombas explosivas vermelhas
- Destruição com flash verde e fragmentos

**ChefeFinal** (a partir de 500 pontos):
- Vida 80, ponto 500
- Fica no topo da tela, move de um lado ao outro
- **Fase 1:** barragem de 2 projéteis direcionados
- **Fase 2 (vida ≤ 50%):** vermelho intenso, rajadas em leque (3 projéteis), bombas explosivas
- Flash vermelho e fragmentos na mudança de fase
- Ao ser derrotado: **vitória** (não reaparece)

---

### Etapa 11 — Power-ups
**Arquivo:** `jogo/entidades/powerup.py`

Bananas que caem do topo e são coletadas ao tocar o jogador:

| Power-up | Efeito | Duração |
|----------|--------|---------|
| Turbo | Velocidade ×1.5 | 10s |
| Tiro Duplo | Dois projéteis | 12s |
| Casca (Escudo) | Bloqueia 1 dano | Absorção |
| Explosiva (Mega Tiro) | Dano ×3 | 8s |
| Coração | +1 vida | Instantâneo |
| Estrela (Pontos) | +150 pontos | Instantâneo |

Efeitos visuais: anel pulsante, flutuação suave, partículas na coleta.

---

### Etapa 12 — Efeitos Visuais e Tema de Selva
**Arquivos:** `jogo/visual/efeito.py`, `jogo/visual/tema.py`

**Efeitos** (`efeito.py`): partículas de fragmentos, flashes de impacto, explosões com dano de área, partículas de propulsão.

**Tema de selva** (`tema.py`):
- Moldura tropical com folhas, cipós e bananas
- Botões em placas de madeira com símbolos (▶, ×, ←)
- Macaco com olhos, orelhas, sorriso e comemoração
- Banana flutuante com brilho

---

### Etapa 13 — Background da Gameplay (Cidade)
**Arquivo:** `jogo/visual/bg_fase.py`

- Cidade procedural vista de cima, estilo Nova York
- Tile que se repete verticalmente com rolagem contínua
- Desfoque (downscale/upscale) e nuvens para sensação de altitude
- Paleta dessaturada para não competir com inimigos

---

### Etapa 14 — Sistema de Áudio Completo
**Arquivo:** `jogo/sons.py`

- Efeitos sonoros carregados de `audio/` (17 categorias)
- Controle de volume (mestre e efeitos separados)
- Música de fundo por estado (menu, gameplay, game over, vitória)
- `tocar()` seguro sem mixer (checagem `mixer.init()`)
- Sons sintetizados em `audio/alertas/` via `ferramentas/gerar_sons.py`
- Referência completa: `audio/LEIA-ME.md`

---

### Etapa 15 — Telas Extras e Fluxo Completo
**Arquivos:** `nickname.py`, `pausa.py`, `config.py`, `ranking.py` (tela), `ranking.py` (lógica), `vitoria.py`

**Nickname:** entrada de até 8 caracteres, cursor piscando, confirmação com Enter.

**Pausa (ESC):** menu com CONTINUAR / REINICIAR / SAIR, botões madeira/selva.

**Configurações:** barras de volume clicáveis (Volume Geral / Efeitos Sonoros), seletor por teclado.

**Ranking:** top 10 pontuações salvas em `ranking.json`, seleção circular entre REINICIAR e MENU.

**Vitória (OPERAÇÃO CONCLUÍDA!):** tela comemorativa ao derrotar o Chefe Final, com:
- Título com brilho e fade-in
- Subtítulo "A BANANA ESTÁ SALVA!"
- Avião comemorando + hélice animada
- Dois macacos celebrando nas laterais
- Painel de resultados (pontuação, inimigos derrotados, vidas restantes)
- Confetes e bananas caindo nas laterais
- Botões JOGAR NOVAMENTE / MENU PRINCIPAL

---

### Etapa 16 — Polimento Visual Completo
**Arquivos:** `tema.py`, `jogador.py`, `efeito.py`, `inimigo.py`, `powerup.py`, `aplicacao.py`, `game_over.py`

- **Jogador:** desenho propio do avião-banana com hélice animada e chama de propulsão
- **Reações:** jogador reage visualmente ao coletar power-up, levar dano, ficar em escudo
- **Inimigos:** oscilação suave (Guarda), hélice animada (Helicóptero), vibração no ataque, flash/fragmentos na destruição e mudança de fase (Boss)
- **Power-ups:** flutuação suave e anel pulsante
- **Propulsão:** partículas de fumaça atrás do avião durante movimento, turbo com flash e rastro
- **Boss:** entrada animada com timer, blink ao tomar dano (fase 2), flash vermelho na mudança de fase
- **Tela de derrota:** layout uniforme e espaçado, painel de recorde (NEW HIGH SCORE!) ou "TENTE NOVAMENTE!"
- **Menu principal:** título com dupla camada, macaco com "olhar" ao mouse, banana flutuante, partículas celebração
- **Rodapés:** nome do jogo em todas as telas

---

### Etapa 17 — Rebalanceamento Final e Vitória
**Arquivos:** `settings.py`, `aplicacao.py`, `sons.py`, `vitoria.py`

- **Chefe Final:** desbloqueado a partir de **500 pontos** (antes 2000)
- **Guarda Pesado:** desbloqueado a partir de **350 pontos** (antes 1200)
- **Sem reaparecimento do Boss:** ao ser derrotado, jogo encerra com vitória
- **Transição de vitória:** ~55 frames mostrando explosão final antes da tela
- **Contador de inimigos derrotados:** novas estatísticas na tela de vitória
- **Som de vitória:** reutiliza sino pesado existente (`impactBell_heavy_001.ogg`)

---

## Estrutura Final do Projeto

```
Macacaquito-Louco/
│
├── main.py
├── requirements.txt
├── readme.md
├── relatorio.md
├── AGENTS.md
├── opencode.json
├── ranking.json                # Dados do ranking local (top 10)
│
├── audio/
│   ├── jogador/                # Sons do jogador
│   ├── inimigos/               # Sons dos inimigos
│   ├── impactos/               # Sons de impacto
│   ├── explosoes/              # Sons de explosão
│   ├── powerups/               # Sons de power-up
│   ├── alertas/                # Sons de alerta (sintetizados)
│   ├── interface/              # Sons de menu e interface
│   ├── soundtrack/             # Música de fundo
│   └── LEIA-ME.md              # Referência dos sons
│
├── ferramentas/
│   └── gerar_sons.py           # Gera sons sintetizados (.wav)
│
└── jogo/
    ├── __init__.py
    ├── settings.py
    ├── sons.py
    ├── ranking.py              # Lógica do ranking (carregar/salvar)
    │
    ├── entidades/
    │   ├── entidade.py
    │   ├── jogador.py
    │   ├── inimigo.py
    │   ├── tiro.py
    │   └── powerup.py
    │
    ├── telas/
    │   ├── aplicacao.py
    │   ├── menu.py
    │   ├── nickname.py
    │   ├── pausa.py
    │   ├── config.py
    │   ├── game_over.py
    │   ├── ranking.py
    │   └── vitoria.py
    │
    └── visual/
        ├── bg_fase.py
        ├── tema.py
        └── efeito.py
```

---

## Controles

| Tecla | Ação |
|-------|------|
| W / ↑ | Mover para cima |
| A / ← | Mover para esquerda |
| S / ↓ | Mover para baixo |
| D / → | Mover para direita |
| ESPAÇO | Atirar (segurar para rajada) |
| ENTER | Confirmar / Selecionar |
| ESC | Pausar (durante jogo) / Voltar (nos menus) |

---

## Arquivos Novos / Modificados (etapas recentes)

| Arquivo | Descrição |
|---------|-----------|
| `jogo/sons.py` | Sistema de áudio centralizado |
| `jogo/ranking.py` | Lógica do ranking (carregar/salvar/adicionar) |
| `jogo/telas/nickname.py` | Tela de entrada de nickname |
| `jogo/telas/pausa.py` | Menu de pausa |
| `jogo/telas/config.py` | Menu de configurações (volume) |
| `jogo/telas/ranking.py` | Tela do ranking |
| `jogo/telas/vitoria.py` | Tela de vitória |
| `audio/` (pasta inteira) | Assets de som organizados |
| `ferramentas/gerar_sons.py` | Script de geração de sons sintetizados |
| `ranking.json` | Dados persistidos do ranking |

---

## Próximos Passos (pendências)

- [x] Sons e música
- [x] Diferentes tipos de inimigos (básicos)
- [x] GuardaPesado (inimigo raro e resistente)
- [x] ChefeFinal (com fases)
- [x] Power-ups
- [x] Efeitos visuais e tema de selva
- [x] Background da gameplay
- [x] Reorganização em subpacotes
- [x] Telas extras (nickname, pausa, config, ranking, vitória)
- [x] Ranking local
- [x] Polimento visual completo
- [x] Rebalanceamento e fluxo de vitória
- [ ] Melhorias visuais com sprites
- [ ] Sistema de ondas

---

## Notas Técnicas

- Pygame Community Edition (pygame-ce) 2.5.8
- Python 3.14.7
- Sistema de estados simples (sem máquinas de estados complexas)
- Tratamento de erros para evitar crashes
- Reset completo ao reiniciar o jogo
- Ranking persistente em JSON (top 10)
- Áudio centralizado e seguro sem mixer
