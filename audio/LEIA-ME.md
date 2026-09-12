# Áudios do Macacaquito-Louco

Documento de referência dos arquivos de áudio da pasta `audio/`,
organizados por **categoria de uso** no jogo.

## Estrutura da pasta

    audio/
    ├── jogador/      disparos do jogador (bananas)
    ├── inimigos/     disparos dos inimigos (policia)
    ├── impactos/     impacto de acerto de tiro no inimigo
    ├── explosoes/    explosoes e destruicao de inimigos/boss
    ├── powerups/     coleta de power-ups
    ├── alertas/      avisos, progresso e eventos importantes
    ├── interface/    cliques e feedbacks de menu/pausa
    └── reservas/     arquivos originais nao utilizados (backup)

Os arquivos `.wav` em `alertas/` são **sintetizados por código** — gerados
por `ferramentas/gerar_sons.py` (Python puro, sem dependências externas).
Para regenerá-los:

    python ferramentas/gerar_sons.py

O sistema de sons está centralizado em `jogo/sons.py` (carrega os efeitos
uma única vez, controla volume e frequência de repetição).

---

## `jogador/` — disparos do jogador

| Arquivo | Uso |
|---|---|
| `laser1.ogg` | Tiro básico do jogador (variante A, alternada) |
| `laser2.ogg` | Tiro básico do jogador (variante B, alternada) |

## `inimigos/` — disparos dos inimigos

| Arquivo | Uso |
|---|---|
| `laser3.ogg` | Bala simples do Guarda |
| `laser4.ogg` | Missil mirado do Helicoptero |
| `laser5.ogg` | Rajada da Viatura Rapida |
| `laser9.ogg` | Bomba do Guarda Pesado e ataques pesados do Boss |

## `impactos/` — impacto de acerto

| Arquivo | Uso |
|---|---|
| `impactMetal_light_000.ogg` | Guarda atingido |
| `impactMetal_medium_003.ogg` | Helicoptero / Viatura atingidos |
| `impactMetal_heavy_004.ogg` | Guarda Pesado atingido |
| `impactPlate_heavy_001.ogg` | Mega tiro atingindo inimigo |
| `impactPlate_heavy_002.ogg` | Boss recebendo dano |
| `impactPlate_heavy_004.ogg` | Escudo absorvendo dano |
| `impactPunch_heavy_000.ogg` | Jogador recebe dano |

## `explosoes/` — explosões e destruição

| Arquivo | Uso |
|---|---|
| `impactMining_002.ogg` | Explosao do missil do Helicoptero |
| `zapTwoTone2.ogg` | Complemento agudo da explosao do missil |
| `impactMining_001.ogg` | Explosao da bomba do Guarda Pesado |
| `spaceTrash2.ogg` | Explosao grande / fase 2 do Boss |
| `zapTwoTone.ogg` | Inimigo destruido |
| `spaceTrash4.ogg` | Boss destruido |
| `impactBell_heavy_001.ogg` | Sino pesado do Boss derrotado |

## `powerups/` — coleta de power-ups

| Arquivo | Uso |
|---|---|
| `powerUp1.ogg` | Banana Dourada (tiro duplo) |
| `powerUp2.ogg` | Casca de Banana (escudo) |
| `powerUp3.ogg` | Banana Turbo |
| `powerUp4.ogg` | Banana Explosiva (mega tiro) |
| `powerUp11.ogg` | Banana Coracao (+ vida) |
| `pepSound1.ogg` | Banana Estrela (pontos) |

## `alertas/` — avisos, progresso e eventos importantes

| Arquivo | Uso |
|---|---|
| `lowDown.ogg` | Entrada do Boss |
| `threeTone1.ogg` | Inicio de nova partida |
| `level_up.wav` *(gerado)* | Marco de 100 pontos (dificuldade aumenta) |
| `spawn_inimigo.wav` *(gerado)* | Um inimigo surgiu na tela |
| `escudo_expirado.wav` *(gerado)* | Escudo do jogador acabou |

## `interface/` — menus e pausa

| Arquivo | Uso |
|---|---|
| `select_001.ogg` | Hover sobre um botao |
| `confirmation_001.ogg` | Confirmar (Jogar / Reiniciar / Continuar) |
| `back_003.ogg` | Voltar / Sair |
| `bong_001.ogg` | Game Over |
| `error_007.ogg` | Vida critica (1 de vida) |
| `switch_001.ogg` | Alternar entre jogar e pausa |

## `reservas/` — originais não utilizados

Arquivos que vieram no pacote original, mas que o jogo ainda não usa.
Podem ser reaproveitados no futuro sem necessidade de reposicionamento.

---

## Sons por evento (resumo)

| Evento | Arquivo |
|---|---|
| Jogador atira | `jogador/laser1.ogg` e `jogador/laser2.ogg` (alternados) |
| Guarda atira | `inimigos/laser3.ogg` |
| Helicoptero atira | `inimigos/laser4.ogg` |
| Viatura atira | `inimigos/laser5.ogg` |
| Guarda Pesado atira | `inimigos/laser9.ogg` |
| Inimigo atacado | `impactos/impactMetal_*` (por tipo) |
| Mega tiro acerta | `impactos/impactPlate_heavy_001.ogg` |
| Boss acertado | `impactos/impactPlate_heavy_002.ogg` |
| Explosao de missil | `explosoes/impactMining_002.ogg` + `zapTwoTone2.ogg` |
| Explosao de bomba | `explosoes/impactMining_001.ogg` |
| Inimigo destruido | `explosoes/zapTwoTone.ogg` |
| Boss destruido | `explosoes/spaceTrash4.ogg` + `impactBell_heavy_001.ogg` |
| Jogador recebe dano | `impactos/impactPunch_heavy_000.ogg` |
| Escudo bloqueia | `impactos/impactPlate_heavy_004.ogg` |
| Escudo acabou | `alertas/escudo_expirado.wav` |
| Vida critica | `interface/error_007.ogg` |
| Power-up coletado | `powerups/*` (um por tipo) |
| Marca de 100 pontos | `alertas/level_up.wav` |
| Inimigo surgiu | `alertas/spawn_inimigo.wav` |
| Boss entrou | `alertas/lowDown.ogg` |
| Boss mudou de fase | `explosoes/spaceTrash2.ogg` |
| Hover em botao | `interface/select_001.ogg` |
| Confirmar / Reiniciar | `interface/confirmation_001.ogg` |
| Voltar / Sair | `interface/back_003.ogg` |
| Pausar / Continuar | `interface/switch_001.ogg` |
| Game Over | `interface/bong_001.ogg` |
| Nova partida | `alertas/threeTone1.ogg` |