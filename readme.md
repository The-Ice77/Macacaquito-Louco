# 🍌 Operação Banana

Um mini-game 2D de ação desenvolvido em **Python + Pygame**, inspirado em perseguições caóticas e aventuras de desenhos animados.

Você controla um macaco pilotando um **avião em formato de banana**, enfrentando diferentes tipos de inimigos enquanto tenta sobreviver até o confronto final e resgatar a banana!

> 🚨 **Projeto acadêmico desenvolvido para fins educacionais.**

---

## 🎮 Sobre o jogo

Em **Operação Banana**, o jogador controla um macaco que está fugindo de forças policiais enquanto pilota seu inusitado avião-banana.

Durante a partida, diferentes tipos de inimigos aparecem na tela, cada um possuindo comportamentos e ataques próprios. Bananas especiais também caem do topo da tela, oferecendo vantagens ao serem coletadas.

O objetivo é simples:

**sobreviver, derrotar os inimigos, chegar ao confronto final e completar a Operação Banana.**

O jogo possui uma proposta simples e arcade, com foco em ação rápida, esquiva e diferentes padrões de ataque.

---

## 🕹️ Controles

| Tecla | Ação |
|---|---|
| `W` | Mover para cima |
| `A` | Mover para a esquerda |
| `S` | Mover para baixo |
| `D` | Mover para a direita |
| `SPACE` | Atirar (segurar para rajada) |
| `ESC` | Pausar (durante a partida) |
| `ENTER` | Confirmar / Selecionar |

---

## 📺 Telas do Jogo

| Tela | Descrição |
|---|---|
| **Menu Principal** | Título animado, macaco celebrando, botões selva (JOGAR / SAIR) |
| **Nickname** | Cadastro do nickname (até 8 caracteres) antes de jogar |
| **Entrada** | Transição "Prepare-se!" com nome do jogador antes da partida |
| **Gameplay** | Ação principal: inimigos, power-ups, HUD com vida/pontos |
| **Pausa** | Menu durante jogo (Continuar / Reiniciar / Sair) |
| **Game Over** | Tela de derrota com pontuação e recorde pessoal |
| **Ranking** | Top 10 pontuações locais (nick + score) |
| **Vitória** | Tela de sucesso ao derrotar o Chefe Final (estatísticas e comemoração) |

---

## 👾 Inimigos

Os inimigos possuem características diferentes para evitar que o jogador simplesmente repita a mesma estratégia durante toda a partida.

### 👮 Guarda

O inimigo básico do jogo.

- Baixa resistência
- Movimento oscilante para baixo (zigue-zague suave)
- Segue o jogador horizontalmente
- Dispara projéteis rápidos em intervalos regulares
- Fácil de derrotar

Seu principal objetivo é pressionar o jogador e ocupar espaço na tela.

---

### 🚁 Helicóptero Policial

Um inimigo mais perigoso que utiliza **mísseis**.

- Resistência intermediária
- Movimento aéreo em espiral
- Míssil direcionado inicialmente ao jogador
- Pequena correção de trajetória
- Explosão com área de dano ao atingir o alvo
- Hélice visual animada durante o voo

O jogador precisa prestar atenção nos mísseis e não apenas no próprio helicóptero.

---

### ✈️ Viatura Rápida

Uma aeronave rápida especializada em ataques velozes.

- Alta velocidade
- Entra pelas laterais da tela
- Dispara rajadas de projéteis muito rápidos
- Baixa resistência (1 vida)

É um inimigo criado para testar o tempo de reação do jogador.

---

### 🛡️ Guarda Pesado

Um inimigo lento, porém extremamente perigoso.

- Alta resistência (8 vidas)
- Segue o jogador horizontalmente enquanto desce
- Dispara bombas explosivas lentas (projéteis grandes)
- Áreas de dano ao impacto
- Destruição com flash e fragmentos verdes

A ideia é fazer o jogador reconhecer imediatamente:

> 💣 "Essa bomba vai explodir. É melhor sair de perto."

---

### 👑 Boss (Chefe Final)

Inimigo mais poderoso do jogo. Surge a partir de **500 pontos** na pontuação.

- Alta resistência (80 vidas)
- Permanece no topo da tela, movendo-se de um lado ao outro
- Tema de selva: aparência de chefe caçador

#### Fase 1 (vida > 50%)
- Dispara barragens de **2 projéteis** direcionados ao jogador

#### Fase 2 (vida ≤ 50%)
- Mudança visual: fica vermelho intenso
- Aumenta velocidade de movimento
- Dispara rajadas em **leque** (3 projéteis)
- Adiciona bombas explosivas
- Maior pressão sobre o jogador

Ao ser derrotado, o jogador entra automaticamente na **tela de Vitória**.

---

## 💥 Sistema de projéteis

Cada inimigo possui ataques com comportamentos diferentes:

| Inimigo | Projétil | Característica |
|---|---|---|
| 👮 Guarda | Bala simples | Rápida e reta, descendo |
| 🚁 Helicóptero | Míssil direcionado | Corrige levemente a trajetória |
| ✈️ Viatura | Rajada rápida | Múltiplos projéteis rápidos |
| 🛡️ Guarda Pesado | Bomba explosiva | Lenta, com área de dano |
| 👑 Boss | Múltiplos | Barragens, leques e bombas |

O jogador também pode atirar com o **Espaço** (bananas), disparando projéteis para cima.

---

## 🍌 Power-ups

Bananas especiais que caem do topo da tela e podem ser coletadas pelo jogador:

| Power-up | Efeito | Duração |
|---|---|---|
| 🟡 Turbo | Aumenta a velocidade de movimento | 10s |
| 🟡 Tiro Duplo | Dispara dois projéteis simultâneos | 12s |
| 🛡️ Casca | Escudo que bloqueia um dano | Até absorver |
| 💥 Explosiva | Mega tiro (dano aumentado ×3) | 8s |
| ❤️ Coração | Recupera 1 vida | Instantâneo |
| ⭐ Estrela | Pontos bônus (+150) | Instantâneo |

Power-ups incluem efeitos visuais: anel pulsante, flutuação suave e partículas de coleta.

---

## ❤️ Sistema de vida

O jogador começa com **5 vidas**.

Os ataques inimigos causam dano ao jogador, tornando necessário:

- Desviar dos projéteis
- Observar os padrões dos inimigos
- Evitar colisões diretas
- Escolher bons momentos para atacar

**Avviso de vida:** quando a vida chega a 1, um avviso sonoro é emitido.

---

## 🔊 Sons e Música

O jogo possui um sistema de áudio completo centralizado em `jogo/sons.py`, com efeitos sonoros separados por categoria:

| Categoria | Uso |
|---|---|
| `jogador/` | Disparos do avião-banana |
| `inimigos/` | Disparos dos inimigos (por tipo) |
| `impactos/` | Acertos em inimigos e no jogador |
| `explosoes/` | Destruição de inimigos e do Boss |
| `powerups/` | Coleta de cada tipo de banana |
| `alertas/` | Entrada do Boss, início de partida, poderes |
| `interface/` | Botões, pausa, game over, confirmações |
| `soundtrack/` | Trilha sonora de fundo |

Controles de volume (geral e efeitos) estão disponíveis no menu **OPÇÕES**.

---

## 🏆 Objetivo

O objetivo principal é:

1. ✈️ Controlar o avião-banana
2. 👾 Derrotar os inimigos
3. 💥 Desviar dos diferentes tipos de projéteis
4. 📈 Acumular pontuação
5. 🛡️ Sobreviver ao Guarda Pesado
6. 👑 Enfrentar e derrotar o Boss
7. 🎉 Completar a **Operação Banana** (tela de Vitória)

---

## 🧱 Estrutura do projeto

```
Macacaquito-Louco/
│
├── main.py                      # Entrada: dependências, tela e início do jogo
├── requirements.txt             # Dependências (pygame-ce)
├── readme.md                    # Este arquivo
├── relatorio.md                 # Relatório de implementações
├── AGENTS.md                    # Instruções para agentes
├── opencode.json                # Configuração do OpenCode
│
├── audio/                       # Assets de som organizados por uso
│   ├── jogador/
│   ├── inimigos/
│   ├── impactos/
│   ├── explosoes/
│   ├── powerups/
│   ├── alertas/
│   ├── interface/
│   ├── soundtrack/
│   └── LEIA-ME.md               # Referência de todos os sons
│
├── ferramentas/                 # Scripts auxiliares
│   └── gerar_sons.py            # Gera efeitos sintetizados (alertas/)
│
└── jogo/
    ├── __init__.py              # Marca o pacote jogo
    ├── settings.py              # Configurações e constantes globais
    ├── sons.py                  # Sistema de áudio centralizado
    ├── ranking.py               # Sistema de ranking local (top 10)
    │
    ├── entidades/               # Entidades do jogo
    │   ├── entidade.py          # Classe base Entidade (sprite)
    │   ├── jogador.py           # Jogador (macaco no avião de bananas)
    │   ├── inimigo.py           # Guarda, Helicoptero, Viatura, GuardaPesado, ChefeFinal
    │   ├── tiro.py              # Projéteis e explosões
    │   └── powerup.py           # Power-ups colecionáveis
    │
    ├── telas/                   # Game loop e telas
    │   ├── aplicacao.py         # Classe Jogo: loop, estados e lógica da partida
    │   ├── menu.py              # Menu inicial (tema selva)
    │   ├── nickname.py          # Entrada de nickname
    │   ├── pausa.py             # Menu de pausa durante a partida
    │   ├── config.py            # Menu de configurações (volume)
    │   ├── game_over.py         # Tela de game over
    │   ├── ranking.py           # Tela do ranking local
    │   └── vitoria.py           # Tela de vitória
    │
    └── visual/                  # Elementos visuais reutilizados
        ├── bg_fase.py           # Background da gameplay (cidade)
        ├── tema.py              # Tema de selva (moldura, botões, macaco)
        └── efeito.py            # Partículas, flashes e explosões
```

---

## 🚀 Como executar

```bash
# Instalar dependências (opcional, instala automaticamente)
pip install -r requirements.txt

# Executar o jogo
python main.py
```

---

## 🛠️ Tecnologias

- **Python 3**
- **Pygame Community Edition (pygame-ce) 2.5.8**
- Assets de áudio: arquivos `.ogg` e `.wav`
- Geração procedural de sons via `ferramentas/gerar_sons.py`

---

## 📝 Notas

- **Projeto acadêmico** — não utiliza assets gráficos externos (sprites são formas geométricas do Pygame).
- **Sons sintetizados** em `audio/alertas/` são gerados por código Python puro.
- **Ranking local** salva as top 10 pontuações em `ranking.json` (na raiz do projeto).
