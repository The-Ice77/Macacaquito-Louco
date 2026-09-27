# Relatório de Implementações - Operação Banana

## Data: 03/09/2026

> Última atualização: 12/09/2026

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
- Instruções de controles (WASD/setas + ESPAÇO) na parte inferior
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

**Ranking:** top 10 pontuações salvas em `ranking.json`, seleção circular entre REINICIAR e MENU. Cada nickname ocupa uma única posição (ver Etapa 21).

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

### Etapa 18 — Redesenho Visual das Entidades (Sprites Geométricas)
**Arquivos:** `jogo/entidades/*`, `jogo/visual/efeito.py`, `jogo/visual/tema.py`

Todos os elementos passaram a ser desenhados com formas geométricas detalhadas do Pygame (sem imagens externas):

- **Jogador:** avião-banana com hélice animada, chama de propulsão e macaco piloto com reações (normal, feliz, dano, surpresa, comemorar)
- **Inimigos:**
  - Guarda: viatura policial vista de cima (rodas, luzes rotativas, faróis)
  - Helicóptero: rotor superior animado, patins, estabilizadores de cauda
  - Viatura Rápida: aeronave de persecução alongada, rastro de velocidade
  - Guarda Pesado: blindado com esteiras, placas de armadura e canhão com recuo ao disparar
  - Chefe: asas varridas, pods de mísseis, luzes policiais piscando, rachaduras na fase 2
- **Projéteis:** tiro do jogador virou banana descascada; solta a casca atrás como efeito visual
- **Power-ups:** família de frutas (morango=TURBO, abacaxi=MEGA TIRO, melancia=ESCUDO, maçã=+VIDA, banana dourada=TIRO DUPLO, banana premiada=+PONTOS)
- **Efeitos:** cascas de banana girando, impacto da banana, rastro de propulsão, partículas de coleta

---

### Etapa 19 — Aumento de Resolução e Escala das Entidades
**Arquivos:** `jogo/settings.py`, `jogo/entidades/*`, `jogo/telas/*`, `jogo/visual/*`

- **Resolução** aumentada de `800x600` (4:3) para `1280x720` (16:9)
- **Fatores de escala** (a arte base é desenhada em grade pequena e ampliada com `smoothscale`, preservando os detalhes):

| Elemento | Fator | Tamanho na tela |
|----------|-------|-----------------|
| Jogador | 2.2 | 40 → 88 px |
| Inimigos | 2.0 | 40–70 → 80–140 px |
| Power-ups | 1.7 | 30 → 51 px |
| Projéteis | 1.8 | 12–32 → 21–58 px |
| Explosões | 1.3 | só visual |

- **Explosão:** separou o raio de dano (`raio_dano`, gameplay) do raio visual (`raio_max`)
- **Layout de todas as telas** (menu, game over, pausa, opções, vitória, nickname, ranking), HUD, banner de entrada e o fundo da fase (avenidas em `[220, 640, 1060]`) reposicionados para 1280x720
- `LINHA_EXPLOSAO_BOMBA` ajustada de `520` para `620`
- Fonte/Velocidades de jogo mantidas (balanceamento inalterado)

---

### Etapa 20 — Ritmo do Jogo (multiplicador global de velocidade)
**Arquivos:** `jogo/settings.py`, `jogo/entidades/*`, `jogo/visual/bg_fase.py`, `jogo/telas/aplicacao.py`

Na etapa anterior a resolução foi aumentada, mas as velocidades ficaram
intactas. Como elas são medidas em **pixels por frame**, o mesmo valor
passou a percorrer uma tela 1,2x (vertical) a 1,6x (horizontal) maior, e o
jogo ficou com aparência de lentidão (relatado por quem jogou).

- **`FATOR_VELOCIDADE = 1.5`** em `settings.py`: multiplicador global aplicado
  a todas as velocidades, com as entidades agora grandes o bastante para que
  o ritmo visual volte ao da resolução anterior

| Velocidade | Antes (px/frame) | Agora (px/frame) |
|------------|------------------|------------------|
| Jogador | 5 | 7,5 (turbo: 11,25) |
| Banana do jogador | 10 | 15 |
| Guarda | 3 | 4,5 |
| Helicóptero | 2 | 3 |
| Viatura rápida | 9 | 13,5 |
| Guarda pesado | 1 | 1,5 |
| Chefe (fase 1 / fase 2) | 3 / 5 | 4,5 / 7,5 |
| Bala do guarda | 9 | 13,5 |
| Míssil do helicóptero / chefe | 6 | 9 |
| Rajada da viatura | 11 | 16,5 |
| Bomba (guarda pesado / chefe) | 3 / 2 | 4,5 / 3 |
| Leque do chefe | 8 | 12 |
| Queda dos power-ups | 2 | 3 |
| Rolagem do cenário | 1,6 | 2,4 |

- Também acompanhados: entrada do jogador na tela, entrada dramática do chefe,
  perseguição lateral dos inimigos, descida da viatura rápida e o aumento de
  velocidade do chefe na fase 2
- **Tempos de travessia de tela** ficaram iguais ou melhores que os da versão
  `800x600` (ex.: guarda 200 → 160 frames, viatura 89 → 95 frames,
  bala do guarda 27 → 27 frames)
- **Cadências não foram alteradas** (intervalos de spawn e de tiro), para não
  aumentar a densidade de inimigos junto com a velocidade

---

### Etapa 21 — Ranking: uma posição por nickname
**Arquivos:** `jogo/ranking.py`

Antes, cada partida colocava uma linha nova no ranking, então o mesmo jogador
ocupava várias posições (o `ranking.json` local chegou a ter o mesmo nick 6
vezes, sobrando poucas posições para os outros jogadores).

- `adicionar_pontuacao(nick, score)` agora **atualiza** a pontuação do
  nickname em vez de criar uma linha nova
- A pontuação anterior **só é substituída quando a nova for maior**; se o
  jogador não superou o próprio recorde, nada é gravado
- `carregar_ranking()` agrupa as entradas por nickname e mantém a melhor de
  cada um (antes de aplicar o corte do top 10), o que também limpa
  automaticamente os arquivos com nomes repetidos
- `normalizar_nick(nick)` ignora espaços extras e maiúsculas ao comparar os
  nomes, para "macaco" e "MACACO" serem reconhecidos como o mesmo jogador
- `adicionar_pontuacao` devolve `None` quando não superou o próprio recorde:
  a tela de Game Over não anuncia "POSITION #N" nesse caso, mas continua
  avisando quando o jogador entra ou melhora sua posição

---

### Etapa 22 — Movimento com as Setas do Teclado
**Arquivos:** `jogo/entidades/jogador.py`, `jogo/telas/menu.py`

O relatório já documentava `W / ↑`, `A / ←`, `S / ↓` e `D / →`, mas apenas a
tela de configurações aceitava as duas formas — na partida só o WASD
funcionava.

- `Jogador.update()` passou a ler cada direção em dois conjuntos de teclas
  (WASD e setas), usando variáveis `cima`, `baixo`, `esquerda` e `direita`
  para não repetir a checagem no movimento, na inclinação visual e na animação
- Nenhuma outra mudança: a velocidade, a hitbox e a inclinação continuam
  iguais, então as setas são apenas um controle adicional
- Dica da tela inicial ajustada para "W A S D ou SETAS - Mover"

---

### Etapa 23 — Menus navegáveis pelo teclado
**Arquivos:** `jogo/telas/navegacao.py` (novo), `menu.py`, `pausa.py`,
`game_over.py`, `vitoria.py`, `ranking.py`, `config.py`

Só a tela de opções aceitava setas/WASD. Nos outros menus o teclado só
funcionava para ENTER e ESC, então quem não usava mouse dependia de adivinhar
o que cada ENTER faria — e no menu principal, na pausa e na vitória não dava
nem para escolher a opção.

- Novo módulo `navegacao.py` com a classe `Navegacao`, usada por herança pelas
  telas: guarda a ação selecionada, move o destaque em ciclo, confirma com
  ENTER/ESPAÇO e cede o destaque para o mouse
- O botão selecionado **acende igual ao hover do mouse** (escala, folhas
  balançando, banana girando e ícone), reaproveitando o destaque que já
  existia — nenhum visual novo
- **Teclado e mouse não se atropelam:** o mouse só assume a seleção quando
  ele realmente se move, então um mouse parado em cima de um botão não
  desfaz a navegação feita pelas setas
- ENTER agora confirma **o item destacado** em todos os menus. O primeiro item
  é o de sempre (JOGAR, CONTINUAR, REINICIAR), então o comportamento
  anterior continua valendo para quem aperta ENTER sem mexer nas setas
- ESC, BACKSPACE e o mouse continuam com o comportamento de antes
- Tela de opções: a navegação por cima/baixo agora inclui o botão VOLTAR no
  mesmo ciclo (antes ele só era acessível pelo mouse), e as setas laterais
  sobre o VOLTAR não alteram nada
- Dicas de controle nas telas de menu e de pausa

**Correção junto:** em `vitoria.py` e `ranking.py` a lista `self.botoes` não
era limpa a cada quadro, então crescia a cada frame (2 botões por frame na
vitória, 1 no ranking). Além de vazar memória, fazia o teste de mouse varrer
uma lista cada vez maior. Agora é reconstruída por frame.

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
    │   ├── vitoria.py
    │   └── navegacao.py
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
| W / ↑ | Mover para cima (na partida) |
| A / ← | Mover para esquerda (na partida) |
| S / ↓ | Mover para baixo (na partida) |
| D / → | Mover para direita (na partida) |
| ESPAÇO | Atirar (segurar para rajada) |
| ↑ ↓ (ou W / S) | Navegar entre os itens dos menus |
| ← → (ou A / D) | Diminuir / aumentar o volume nas opções |
| ENTER (ou ESPAÇO) | Confirmar o item selecionado |
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
- [x] Ranking com uma posição por nickname
- [x] Controle alternativo com as setas do teclado
- [x] Menus navegáveis pelo teclado
- [x] Polimento visual completo
- [x] Rebalanceamento e fluxo de vitória
- [x] Redesenho visual das entidades (sprites geométricas)
- [x] Aumento de resolução e escala das entidades
- [x] Ajuste do ritmo de velocidade do jogo
- [ ] Sistema de ondas

---

## Notas Técnicas

- Pygame Community Edition (pygame-ce) 2.5.8
- Python 3.14.7
- Resolução 1280x720 (16:9), com entidades ampliadas por fatores de escala
- Velocidades em px/frame multiplicadas por `FATOR_VELOCIDADE`, para compensar o aumento de resolução
- Sistema de estados simples (sem máquinas de estados complexas)
- Tratamento de erros para evitar crashes
- Reset completo ao reiniciar o jogo
- Ranking persistente em JSON (top 10)
- Áudio centralizado e seguro sem mixer
