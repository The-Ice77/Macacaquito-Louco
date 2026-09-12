# Como Funciona o Código — Operação Banana

Este documento explica o código do jogo, organizado pelas pastas, e por
função/classe. É um guia de leitura: siga a ordem dos tópicos para entender
o jogo do ponto de entrada até o game loop.

---

## Sumário

1. [Arquitetura geral](#1-arquitetura-geral)
2. [main.py — ponto de entrada](#2-mainpy--ponto-de-entrada)
3. [jogo/settings.py — configurações](#3-jogosettingspy--configurações)
4. [jogo/sons.py — áudio](#4-jogosonspy--áudio)
5. [jogo/ranking.py — ranking local](#5-jogorankingpy--ranking-local)
6. [jogo/entidades/ — entidades do jogo](#6-jogoentidades--entidades-do-jogo)
7. [jogo/telas/ — telas e game loop](#7-jogotelas--telas-e-game-loop)
8. [jogo/visual/ — elementos visuais reutilizados](#8-jogovisual--elementos-visuais-reutilizados)
9. [Fluxo do jogo (game loop e estados)](#9-fluxo-do-jogo-game-loop-e-estados)

---

## 1. Arquitetura geral

O jogo roda em **Python + Pygame** e usa:

- **Sprites** (`pygame.sprite.Sprite`) para todas as entidades (jogador,
  inimigos, tiros, power-ups, explosões, efeitos).
- **Grupos de sprites** (`pygame.sprite.Group`) para desenho e colisão em
  massa.
- Um **sistema de estados simples** na classe `Jogo` (menu, nickname,
  entrada, jogando, pausa, config, morte, game_over, ranking, vitoria).

Os módulos ficam no pacote `jogo/` e usam imports relativos, por exemplo:

```python
from ..settings import LARGURA, ALTURA
```

A interação entre as partes:

```
main.py  →  jogo.telas.aplicacao.Jogo  (game loop)
                ├── jogo/settings.py   (configurações)
                ├── jogo/sons.py       (áudio)
                ├── jogo/ranking.py    (ranking local)
                ├── jogo/entidades/    (jogador, inimigos, tiros, power-ups)
                ├── jogo/telas/        (menu, pausa, game over, etc.)
                └── jogo/visual/       (fundo da fase, tema, efeitos)
```

---

## 2. main.py — ponto de entrada

O arquivo mais simples: verifica as dependências, cria a tela e inicia o jogo.

### Funções

- `_em_ambiente_virtual()` — True se o Python atual é de um venv
  (`sys.prefix != sys.base_prefix`). Usado para dar instruções corretas de
  instalação.
- `_mostrar_instrucoes_linux()` / `_mostrar_instrucoes()` — imprime como
  instalar o pygame no Linux (e demais sistemas).
- `verificar_dependencias()` — tenta `import pygame`. Se falhar, tenta
  instalar com `pip install -r requirements.txt` automaticamente e reinicia
  o jogo. Se ainda assim falhar, mostra as instruções.
- `main()` — inicia o pygame, cria a tela em `(LARGURA, ALTURA)`, define o
  título e cria `Jogo(tela)`. Em seguida chama `jogo.executar()`, que roda o
  game loop até o jogador sair. Ao final, `pygame.quit()`.

---

## 3. jogo/settings.py — configurações

Apenas constantes globais. Não tem funções, mas concentra todo o
**balanceamento** do jogo em um só lugar:

- **Tela:** `LARGURA = 1280`, `ALTURA = 720`, `FPS = 60`.
- **Escala visual:** `FATOR_ESCALA_JOGADOR = 2.2`, `FATOR_ESCALA_INIMIGO = 2.0`,
  `FATOR_ESCALA_POWERUP = 1.7`, `FATOR_ESCALA_PROJETIL = 1.8`,
  `FATOR_ESCALA_EXPLOSAO = 1.3`. A arte é desenhada pequena e ampliada com
  suavização (detalhes preservados).
- **Cores:** do jogador (marrom), banana (amarelo), forças policiais, cidade
  e selva dos menus.
- **Inimigos:** vida, pontos e velocidade de cada um; limiares de desbloqueio
  (`PONTOS_DESBLOQUEIA_HELICOPTERO = 300`,
  `PONTOS_DESBLOQUEIA_GUARDAPESADO = 350`,
  `PONTOS_DESBLOQUEIA_CHEFE = 500`).
- **Projéteis dos inimigos:** velocidade, cor, raio de explosão e cadência
  (balas do guarda, míssil do helicóptero, rajada da viatura, bomba do guarda
  pesado, e os padrões do chefe — fase 1 e fase 2).
- **Power-ups:** frequência de spawn, duração de cada efeito em frames
  (60 frames = 1 segundo) e multiplicadores (`POWERUP_MULT_TURBO = 1.5`,
  `MEGA_TIRO_DANO = 3`).
- **Cores dos menus e cidades.**

> Sempre que for ajustar dificuldade, comece por aqui.

---

## 4. jogo/sons.py — áudio

Sistema de áudio **centralizado**: carrega todos os efeitos uma única vez e
expõe funções simples para tocar.

### Configuração interna

- `_CONFIG` — dicionário "nome do som" → `(pasta, arquivo, volume,
  intervalo_mínimo_ms)`. O intervalo evita que um som se repita rápido demais.
- `_SONS` — sons carregados em memória.
- `_VOLUME_MESTRE` e `_VOLUME_EFEITOS` — volumes controlados nas opções.
- `_MUSICAS` — músicas de fundo por estado (menu, fase e morte).

### Funções principais

- `inicializar()` — inicia o mixer (se disponível), configura 16 canais e
  carrega todos os sons de `audio/`. Se o mixer falhar, o jogo segue sem som
  (sem quebrar).
- `tocar(nome)` — toca um efeito respeitando o intervalo mínimo e aplicando
  os volumes.
- `tocar_alternado(a, b)` — alterna entre dois sons a cada chamada (usado
  para os dois lasers do jogador).
- `tocar_musica(nome, loop=True)` / `parar_musica()` /
  `pausar_musica()` / `retomar_musica()` — controle da trilha sonora.
- `volume_mestre()` / `set_volume_mestre(valor)` e
  `volume_efeitos()` / `set_volume_efeitos(valor)` — leitura/escrita dos
  volumes (0.0 a 1.0), usadas pela tela de opções.
- `ajustar_volume(nome, volume)` — muda o volume de um efeito em execução.

---

## 5. jogo/ranking.py — ranking local

Salva o top 10 de pontuações em `ranking.json` (na raiz do projeto).

- `carregar_ranking()` — lê o arquivo, ignora entradas inválidas, ordena do
  maior para o menor e devolve até 10 itens. Arquivo ausente/corrompido
  retorna lista vazia.
- `salvar_ranking(entradas)` — ordena, limita a 10 e grava em JSON.
- `adicionar_pontuacao(nick, score)` — insere uma pontuação, ordena e salva.
  Retorna a **posição** (1 a 10) se entrou no ranking, ou `None`.

---

## 6. jogo/entidades/ — entidades do jogo

### 6.1 `entidade.py` — base comum

Funções auxiliares:

- `escalar(superficie, fator)` — amplia uma superfície mantendo a proporção
  com `pygame.transform.smoothscale` (preserva os detalhes).
- `redimensionar(superficie, largura, altura)` — redimensiona para um
  tamanho exato.

Classe `Entidade(pygame.sprite.Sprite)`:

- `__init__(x, y, velocidade)` — cria a superfície `image`, o `rect`
  centralizado e o timer de tremor.
- `mover(dx, dy)` — desloca o `rect`.
- `ativar_tremor(frames)` / `_aplicar_tremor()` — o sprite "treme" ao levar
  dano (ciclo simétrico para não deslocar a posição permanentemente).

### 6.2 `jogador.py` — o protagonista (macaco no avião-banana)

Funções de desenho (módulo):

- `_desenhar_aviao(superficie, reacao)` — desenha o avião-banana com o macaco
  piloto. A `reacao` muda a expressão: `normal`, `feliz`, `dano`, `surpresa`,
  `comemorar`.
- `_desenhar_helice(superficie, angulo)` — hélice girando no nariz.
- `_desenhar_chama(superficie, timer)` — chama de propulsão que tremula.

Classe `Jogador(Entidade)`:

- `__init__(x, y)` — desenha o avião em 40x40 e amplia com
  `FATOR_ESCALA_JOGADOR`. Inicializa vida (5), velocidades e os timers dos
  efeitos temporários (turbo, tiro duplo, mega tiro, escudo).
- `reagir(nome, frames)` — dispara uma reação visual curta.
- `ativar_turbo/s` / `ativar_tiro_duplo` / `ativar_mega_tiro` /
  `ativar_escudo` — ligam os efeitos por um tempo (em frames).
- `escudo_ativo()` — True enquanto o escudo durar.
- `recuperar_vida()` — +1 vida se houver espaço (retorna bool).
- `efeitos_ativos()` — lista os efeitos atuais para o HUD (TURBO, 2X, MEGA,
  ESCUDO).
- `_atualizar_visual(direcao_x, movendo)` — inclina, balança e anima o avião
  (só visual, não mexe na hitbox).
- `update()` — decrementa os timers dos efeitos, lê as teclas (WASD), move o
  jogador, limita à tela e atualiza o visual.

### 6.3 `inimigo.py` — forças policiais

Funções auxiliares: `_escurecer(cor, fator)`, `_aclarar(cor, fator)` e
`sombra_oval(...)` para criar contornos e sombras.

Classe abstrata `Inimigo(Entidade)` (ABC):

- `__init__` — cria a superfície base, chama `_desenhar()`, amplia com
  `FATOR_ESCALA_INIMIGO` e prepara inclinação visual (tilt).
- `tomar_dano(dano)` — reduz vida e treme; morre (kill) se vida ≤ 0.
- `saiu_da_tela()` — remove o inimigo se sair da margem.
- `_registrar_tiro(tiro)` — adiciona o tiro aos grupos de colisão/desenho.
- `_atualizar_visual()` — inclina a imagem conforme o movimento horizontal.
- Métodos abstratos/final: `_movimentar()` e `_desenhar()` por tipo; `update()`
  chama movimento + visual + saída de tela.

Inimigos concretos:

| Classe | Movimento | Ataque |
|--------|-----------|--------|
| `Guarda` | desce + zigue-zague + segue o X do jogador | bala simples reta |
| `HelicopteroPolicial` | desce e alinha com o jogador | míssil mirado (homing leve) |
| `ViaturaRapida` | atravessa a tela pelas laterais | rajada de 3 balas rápidas |
| `GuardaPesado` | desce lento com oscilação | bomba explosiva que explode na base |
| `ChefeFinal` | fica no topo, patrulha de lado a lado | fase 1: míssil duplo; fase 2: leque de 5 + bomba + convoca guardas |

Detalhes por classe:

- `Guarda.update()` — além do movimento, espera o `intervalo_tiro` e dispara
  via `atirar()`.
- `HelicopteroPolicial` — rotaciona o rotor (`_desenhar_rotor()`); `atirar()`
  usa `direcao_para()` para mirar o jogador.
- `ViaturaRapida` — dispara uma **rajada** (`_disparar_bala()` + timer) e
  espelha o desenho conforme a direção.
- `GuardaPesado` — `atirar()` ativa tremor e recuo do canhão; a bomba
  `explodir_na_linha`.
- `ChefeFinal` — pontos-chave:
  - entrada dramática (desce de fora da tela, sem atacar, `timer_entrada`);
  - `tomar_dano()` faz piscar branco (`blink_timer`);
  - `entrar_fase2()` quando `vida <= metade_vida`: acelera, atira mais rápido,
    muda a cor e solta explosão visual;
  - padrões de ataque: `_atacar_fase1()` (míssil duplo), `_leque()`,
    `_bomba_especial()` e `chamar_guardas()`.

### 6.4 `tiro.py` — projéteis e explosões

Funções auxiliares:

- `direcao_para(ox, oy, ax, ay)` — vetor unitário de um ponto até outro
  (usado para mirar o jogador).
- `_desenhar_banana(lado, cor)` — banana descascada (polpa clara) com veia e
  sementes, reaproveitando a silhueta do `tema.py`.

Classe `Tiro(Entidade)`:

- `__init__(x, y, vx, vy, ...)` — projétil configurável: `homing` (alvo),
  `velo_perseguicao` (intensidade da correção), `raio_explosao`,
  `explodir_na_linha`.
- `_corrigir_trajetoria()` — homing suave: aproxima o vetor velocidade da
  direção do alvo.
- `saiu_da_tela()` — checa se já passou da margem.
- `criar_explosao(x, y)` — cria a `Explosao` e remove o projétil.
- `explodir()` — somente dispara explosão se houver raio; escolhe o som pelo
  tamanho da explosão.
- `update()` — corrige trajetória, move e explode ao sair da tela ou ao
  atingir `explodir_na_linha`.

Classe `TiroJogador(Tiro)` — a banana descascada do jogador. Sempre reta para
cima, carrega `dano` (1 ou 3 no mega). A imagem é a banana desenhada e
ampliada por `FATOR_ESCALA_PROJETIL`.

Classe `Explosao(Entidade)` — explosão visual com **dano de área aplicado uma
única vez**:

- `raio_dano` (ray de dano, gameplay) separado de `raio_max` (raio visual
  ampliado pelo fator de escala).
- `_raio_atual()` — animação: cresce até 35% da duração e encolhe depois.
- `_desenhar_estado()` — círculo central + círculos satélites + fade.
- `aplicar_dano_se_no_alcance()` — aplica 1 dano ao alvo apenas se dentro de
  `raio_dano`, uma única vez.
- `update()` — avança o timer, redesenha e se remove ao final.

### 6.5 `powerup.py` — power-ups (frutas coletáveis)

Função auxiliar:

- `_pequena_banana(cor, ponta)` — banana-crescente mini usada em dois
  power-ups.

Classe base `PowerUp(Entidade)`:

- `__init__` — desenha em 30x30, guarda `self.icon` (fundo estático) e a
  `fase` para animações.
- `aplicar(jogador)` — aplica o efeito (sobrescrito); retorna pontos bônus
  quando houver.
- `update()` — cai devagar, flutua o ícone, desenha o anel pulsante e amplia o
  quadro completo com `FATOR_ESCALA_POWERUP`. Sai da tela ao ultrapassar
  `ALTURA`.

| Classe | Forma desenhada | Efeito (`aplicar`) |
|--------|-----------------|--------------------|
| `BananaTurbo` | morango | `ativar_turbo` |
| `BananaDourada` | duas bananas | `ativar_tiro_duplo` |
| `CascaBanana` | fatia de melancia | `ativar_escudo` |
| `BananaExplosiva` | abacaxi | `ativar_mega_tiro` |
| `BananaCoracao` | maçã em coração | `recuperar_vida` (+1) |
| `BananaEstrela` | banana dourada | devolve `POWERUP_BONUS_PONTOS` |

Algumas classes sobrescrevem `_efeito_dinamico` para animações próprias
(pulso dourado, carga laranja, cintilação de estrela).

---

## 7. jogo/telas/ — telas e game loop

### 7.1 `aplicacao.py` — o coração do jogo

É a classe `Jogo`, que controla o game loop e os estados.

**Inicialização (`__init__`):**
- cria fontes, telas (Menu, Pausa, Config, Nickname), o fundo e acessa os
  grupos de sprites (`todos_sprites`, `inimigos`, `tiros`, `tiros_inimigos`,
  `explosoes`, `powerups`, `efeitos_visuais`);
- cria o jogador e variáveis da partida (pontos, timers, chefe, etc.).

**Preparação da partida (`iniciar_nova_partida`):**
- zera pontos, timers, grupos e recria o jogador; define estado `entrada`.
- Métodos de criação:
  - `criar_jogador()` — cria o jogador na base da tela.
  - `sorteia_posicao_topo(offset)` — posição aleatória no topo.
  - `escolher_inimigo()` — sorteia o tipo **com pesos** conforme a
    pontuação (guarda, viatura, depois helicóptero e guarda pesado).
  - `criar_inimigo()` — instancia o inimigo sorteadO e o liga aos grupos.
  - `_tipo_powerup(jogador)` — sorteia um power-up; coração só aparece com
    vida baixa.
  - `introduzir_powerup()` — cria o power-up no topo da tela.
  - `tratar_chefe()` — invoca o chefe quando a pontuação atinge o
    `proximo_chefe` e o reposiciona para um próximo chefe se ele morrer.

**Eventos (`tratar_eventos`):**
- distribui `pygame.event` conforme o estado atual. Ex.: espaço para atirar,
  ESC para pausar; na pausa, continuar/reiniciar/opções/sair; no game over,
  reiniciar/sair; na vitória, reiniciar/menu; no menu, iniciar/ranking/
  config/sair.

**Fluxo de gameplay (`processar_jogada`)** — chamado a cada frame em
`jogando`:
1. se o chefe foi derrotado, apenas anima a explosão final e abre a vitória
   após `VITORIA_TRANSICAO`;
2. spawn de inimigos (timer + intervalo);
3. **colisão tiros × inimigos** (`groupcollide`): cada tiro causa `dano`,
   toca o som do impacto, adiciona pontos e contabiliza inimigos derrotados;
   o chefe derrotado dispara a vitória;
4. nível de dificuldade: a cada 100 pontos toca `level_up` e reduz o
   `spawn_intervalo`;
5. rastro de propulsão do avião (mais forte com turbo);
6. spawn/coleta de power-ups (aplica efeito, pontua, partículas, aviso);
7. `tratar_chefe()` e `_deduzir_vida()`;
8. `todos_sprites.update()` (move tudo).

**Dano ao jogador (`_deduzir_vida`):**
- projéteis normais causam dano ao tocar; explosivos explodem ao tocar;
- colisão corpo a corpo com inimigos dá +1 dano; explosões aplicam dano de
  área uma vez;
- o **escudo** bloqueia todo o dano; sem escudo, reduz a vida, treme e
  reage; vida ≤ 0 chama `_iniciar_morte()`.

**Fim de jogo:**
- `_iniciar_morte()` — remove o jogador, explode, salva o ranking
  (`adicionar_pontuacao`), cria `GameOver`.
- `_atualizar_morte()` — sequência de queda + tremor de tela + escurecimento;
  ao final, estado `game_over`.
- `_abrir_vitoria()` — cria a tela `Vitoria` (uma vez) e define o estado.
- `atirar()` — cria `TiroJogador` (mega = dano 3 e cor laranja; tiro duplo =
  2 bananas desalinhadas) e solta a casca atrás.

**Desenho:**
- `desenhar_hud()` — vida, pontos e efeitos ativos.
- `_atualizar_entrada()` / `_desenhar_banner_entrada()` — jogador sobe de
  baixo e o título "OPERAÇÃO BANANA — Prepare-se!" aparece com fade.
- `_desenhar_aviso_boss()` — aviso "!!! CHEFE !!!" pulsante.
- `_desenhar_aviso_powerup()` — rótulo do power-up coletado.

**Game loop (`executar`):**
```python
while self.rodando:
    self.clock.tick(FPS)      # mantém 60 FPS
    self.tratar_eventos()     # entrada
    self.atualizar()          # lógica + desenho por estado
    pygame.display.flip()     # mostra o frame
```

O método `atualizar()` despacha por estado: `menu`, `jogando`, `entrada`,
`morte`, `game_over`, `vitoria`, `pausa`, `config`, `nickname`, `ranking`.

### 7.2 `menu.py` — tela inicial

Classe `Menu`:

- `atualizar()` — incrementa o timer (animações).
- `desenhar(tela)` — desenha o fundo, a moldura de selva e os botões
  JOGAR/RANKING/OPÇOES/SAIR (via `_botao`), a dica de controles, o macaco e o
  título animado (`_desenhar_titulo`, com slide e fade).
- `_botao(...)` — cria o botão de madeira e guarda `(rect, ação)` para o
  clique.
- `tratar_evento(event)` — mouse (clique em botão) ou teclado (ENTER = iniciar,
  ESC = sair). Devolve a ação para o `Jogo` decidir.

### 7.3 `nickname.py` — cadastro do nickname

Classe `Nickname`:

- `atualizar()` — timer + duração da comemoração do macaco.
- `celebrar()` — macaco celebra ao iniciar.
- `desenhar(tela)` — título, campo de texto em madeira, botão CONFIRMAR, dica
  e macaco decorativo.
- `_desenhar_campo(tela)` — campo com cursor piscando e contador `3/8`.
- `_desenhar_confirmar` / `_desenhar_voltar_dica` / `_desenhar_dica` — partes
  visuais.
- `tratar_evento(event)` — aceita até 8 caracteres alfanuméricos (uppercase),
  Backspace apaga; ENTER confirma (bloqueado se vazio), ESC volta.
- `_confirmar()` — valida e devolve `"confirmar"`.

### 7.4 `pausa.py` — menu de pausa

Classe `Pausa`:

- `desenhar(tela)` — escurece a tela congelada (camada SRCALPHA) e desenha os
  botões CONTINUAR / REINICIAR / OPÇOES / SAIR.
- `tratar_evento(event)` — clique ou ESC (continua).

### 7.5 `config.py` — opções (volume)

Classe `Configuracoes`:

- `self.itens` — lista de opções no formato `(rotulo, obter, definir)`.
  Hoje: VOLUME GERAL e EFEITOS SONOROS. Para adicionar uma opção, basta
  incluir um item nesta lista.
- `desenhar(tela)` — moldura de selva, título, itens com barra de volume e
  botão VOLTAR.
- `_desenhar_item` / `_desenhar_barra` — barra estilo trilho de madeira com
  preenchimento banana e knob, clicável.
- `tratar_evento(event)` — mouse no trilho/knob para definir o volume;
  teclado: setas W/S para trocar item, A/D para diminuir/aumentar.
- `_ajustar_por_barra(indice, x_mouse)` — calcula o volume conforme o x do
  clique.
- `_ajustar(indice, delta)` — muda o volume em passos de `_PASSO_VOLUME`.

### 7.6 `game_over.py` — tela de derrota

Classe `GameOver` (recebe `pontos`, `nick`, `posicao_ranking`):

- `desenhar(tela)` — moldura de selva, botões REINICIAR/SAIR (posições fixas,
  layout uniforme), título "GAME OVER" pulsante, nickname e pontuação.
- `_desenhar_pontuacao` — mostra o nick em destaque e o SCORE.
- `_desenhar_record` — painel "NEW HIGH SCORE!" + `POSITION #N` quando o
  jogador entrou no top 10.
- `_desenhar_frase_motivacional` — "TENTE NOVAMENTE!" caso contrário.
- `tratar_evento(event)` — ENTER reinicia, ESC sai.

### 7.7 `ranking.py` (tela)

Classe `Ranking` (recebe opcional `destaque_nick`/`destaque_score`):

- `desenhar(tela)` — título "HIGH SCORES", "TOP 10", lista do ranking e botão
  VOLTAR.
- `_desenhar_lista` / `_desenhar_linha` — linhas posição / nick / pontuação;
  a linha do jogador recém-inserido fica **destacada** com fundo banana e
  "NOVO!".
- `tratar_evento(event)` — clique ou ESC para voltar.

### 7.8 `vitoria.py` — tela de vitória

Classe `Vitoria` (recebe `pontos`, `inimigos_derrotados`, `vidas`):

- `_criar_particulas` / `_criar_bananas` — confetes e bananas caindo nas
  laterais; `_atualizar_particulas` renova quando saem da tela.
- `atualizar()` — timer + partículas.
- `desenhar(tela)` — moldura de selva, partículas, título com **fade-in**
  (`_fade_in`) e brilho, subtítulo "A BANANA ESTÁ SALVA!", avião comemorando
  (reutiliza `_desenhar_aviao`/`_desenhar_helice` do jogador), macacos
  celebrando, painel de resultados (pontuação / inimigos / vidas) e botões
  JOGAR NOVAMENTE / MENU PRINCIPAL.
- `tratar_evento(event)` — ENTER reinicia, ESC volta ao menu.

---

## 8. jogo/visual/ — elementos visuais reutilizados

### 8.1 `bg_fase.py` — fundo da gameplay (cidade)

Gera a cidade proceduralmente (estilo Nova York vista de cima) em um **tile**
que se repete verticalmente.

- `PASSO_V = 150`, `TILE_H` (altura do tile, múltiplo de `PASSO_V` e ≥ 2
  telas), `AVENIDAS = [220, 640, 1060]` e `COLUNAS` (bordas + avenidas).
- `BackgroundFase.__init__` — gera o tile, desfoca (downscale/upscale),
  cria os carros e as nuvens.
- `_desfocar` — desfoque por downscale + upscale (sensação de altitude).
- `_gerar_tile` — ruas horizontais, avenidas verticais, faixas de pedestre e
  quarteirões (prédios, parques e estacionamentos).
- `_faixa_central` — faixa amarela tracejada no centro das vias.
- `_desenhar_quarteiroes` — decide prédio/parque/estacionamento por quarteirão;
  há um parque grande (estilo Central Park) em uma coluna fixa.
- `_edificios` / `_parque` / `_estacionamento` — formas dos quarteirões.
- `_gerar_carros` / `_desenhar_carro` — poucos carros discretos circulando.
- `_gerar_nuvem` / `_criar_nuvem` / `_atualizar_nuvens` — nuvens translúcidas
  com parallax (descem mais devagar que o chão).
- `atualizar(mult)` — rola o cenário (a rolagem acelera com o
  `multiplier` da velocidade do jogador).
- `desenhar(tela)` — desenha o tile em duas posições (loop contínuo), os
  carros e as nuvens por cima.

### 8.2 `tema.py` — tema de selva dos menus

Reúne os desenhos geométricos reutilizados pelos menus.

- `folha_surface(...)` — folha estilizada com cache (`_cache_folhas`).
- `banana_surface(tamanho, cor, ponta)` — banana em meia-lua (usada também
  pelo jogador e pelos tiros).
- `cipo(...)` — linha grossa com pontas redondas.
- `_layout_selva()` — posições fixas do cenário (geradas uma vez).
- `desenhar_moldura_selva(tela, timer)` — compõe toda a moldura: folhas no
  topo, nos cantos, cipós com bananas penduradas, vegetação na base com
  flores e folhas flutuantes.
- `_banana_pendurada` — banana balançando na haste.
- `_pontos_estrela` / `_desenhar_engrenagem` — ícones do ranking e opções.
- `desenhar_botao_selva(...)` — botão em placa de madeira com sombra, pregos,
  veios, folhas laterais, banana girando e ícone ao passar o mouse (hover).
- `desenhar_macaco(...)` — macaco geométrico animado: pisca, olha para o
  mouse, coça, pula e celebra.

### 8.3 `efeito.py` — efeitos visuais (partículas, flashes)

- `EfeitoVisual` — base dos efeitos (timer de duração).
- `Particula` — fragmento com velocidade, gravidade e fade; formatos
  quadrado, círculo ou linha.
- `Flash` — flash circular que cresce e encolhe.
- Funções de criação (todas recebem os grupos para auto-registro):
  - `criar_fragmentos(...)` — estilhaços ao destruir inimigos.
  - `criar_flash_impacto(...)` / `criar_flash_forte(...)` — flashes ao
    acertar (o segundo é maior, usado no chefe).
  - `criar_particulas_propulsao(...)` — fumaça atrás do avião (mais forte
    com turbo).
  - `criar_particulas_coleta(...)` — partículas ao coletar power-up.
  - `criar_linha_turbo(...)` — linha de velocidade do turbo.
  - `criar_explosao_destruicao(...)` — flash + estilhaços da destruição.
  - `CascaProjetil` / `criar_casca_banana(...)` — casca que se solta da
    banana do jogador, gira e some.
  - `criar_impacto_banana(...)` — reação da banana ao acertar (flash +
    pedaços amarelos).

---

## 9. Fluxo do jogo (game loop e estados)

Fluxo principal da partida:

```
main → Jogo.executar()
  │
  ├─ estado "menu" ......... tela inicial (JOGAR / RANKING / OPÇOES / SAIR)
  ├─ estado "nickname" ..... digita o nick → ENTER
  ├─ estado "entrada" ...... "OPERAÇÃO BANANA — Prepare-se!" (50 frames)
  ├─ estado "jogando" ...... processar_jogada() todo frame
  │      ├── spawn de inimigos (dificuldade progressiva)
  │      ├── colisão tiro × inimigo → pontos
  │      ├── spawn/coleta de power-ups
  │      ├── tratar_chefe() → chefe aos 500 pontos
  │      ├── _deduzir_vida() → danos, escudo, morte
  │      └── todos_sprites.update()
  │      ├── ESC → "pausa" (continuar / reiniciar / opções / sair)
  ├─ estado "morte" ......... queda do avião + fade (48–72 frames)
  ├─ estado "game_over" ..... REINICIAR / SAIR
  └─ chefe derrotado → "vitoria" (55 frames de explosão final)
```

Ciclo de cada frame: **`clock.tick(60)`** → **`tratar_eventos()`** →
**`atualizar()`** (por estado) → **`display.flip()`**.

---