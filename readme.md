# 🍌 Macacaquito-Louco

Um mini-game 2D de ação desenvolvido em **Python + Pygame**, inspirado em perseguições caóticas e aventuras de desenhos animados.

Você controla um macaco pilotando um **avião em formato de banana**, enfrentando diferentes tipos de inimigos enquanto tenta sobreviver até o confronto final.

> 🚨 **Projeto acadêmico desenvolvido para fins educacionais.**

---

## 🎮 Sobre o jogo

Em **Macacaquito-Louco**, o jogador controla um macaco que está fugindo de forças policiais enquanto pilota seu inusitado avião-banana.

Durante a partida, diferentes tipos de inimigos aparecem na tela, cada um possuindo comportamentos e ataques próprios.

O objetivo é simples:

**sobreviver, derrotar os inimigos e chegar ao confronto final.**

O jogo possui uma proposta simples e arcade, com foco em ação rápida, esquiva e diferentes padrões de ataque.

---

## 🕹️ Controles

| Tecla | Ação |
|---|---|
| `W` | Mover para cima |
| `A` | Mover para a esquerda |
| `S` | Mover para baixo |
| `D` | Mover para a direita |
| `SPACE` | Atirar |

---

## 👾 Inimigos

Os inimigos possuem características diferentes para evitar que o jogador simplesmente repita a mesma estratégia durante toda a partida.

### 👮 Guarda

O inimigo básico do jogo.

- Baixa resistência
- Movimento simples
- Dispara projéteis rápidos
- Fácil de derrotar

Seu principal objetivo é pressionar o jogador e ocupar espaço na tela.

---

### 🚁 Helicóptero Policial

Um inimigo mais perigoso que utiliza **mísseis**.

- Resistência intermediária
- Movimento aéreo
- Míssil direcionado inicialmente ao jogador
- Pequena correção de trajetória
- Pequena área de explosão

O jogador precisa prestar atenção nos mísseis e não apenas no próprio helicóptero.

---

### ✈️ Aeronave Policial

Uma aeronave rápida especializada em ataques velozes.

- Alta velocidade
- Movimento rápido pela tela
- Dispara pequenas rajadas
- Projéteis muito rápidos

É um inimigo criado para testar o tempo de reação do jogador.

---

### 🛡️ Guarda Pesado

Um inimigo lento, porém extremamente perigoso.

Seu principal ataque é uma **bomba explosiva**:

- Grande
- Lenta
- Fácil de identificar
- Explode ao atingir o alvo
- Possui uma área de dano

A ideia é fazer o jogador reconhecer imediatamente:

> 💣 "Essa bomba vai explodir. É melhor sair de perto."

---

## 👑 Boss

No final da partida, o jogador enfrenta o **Boss**, um inimigo mais poderoso com diferentes padrões de ataque.

O confronto possui **duas fases**, aumentando a dificuldade durante a batalha.

### Fase 1

O Boss utiliza ataques direcionados ao jogador, incluindo mísseis com leve correção de trajetória.

### Fase 2

O combate se torna mais intenso, adicionando:

- Rajadas em leque
- Ataques com múltiplos projéteis
- Bombas explosivas
- Maior pressão sobre o jogador

O objetivo é fazer com que o jogador observe os padrões dos ataques e encontre oportunidades para atacar.

---

## 💥 Sistema de projéteis

Um dos principais elementos do jogo é a variedade dos projéteis.

Cada inimigo possui ataques com comportamentos diferentes:

| Inimigo | Projétil | Característica |
|---|---|---|
| 👮 Guarda | Bala | Rápida e reta |
| 🚁 Helicóptero | Míssil | Direcionado ao jogador |
| ✈️ Aeronave | Rajada | Vários projéteis rápidos |
| 🛡️ Guarda Pesado | Bomba | Lenta e explosiva |
| 👑 Boss | Míssil / Leque / Bomba | Ataques variados |

Essa diferenciação permite que o jogador identifique visualmente o perigo e reaja de acordo com cada situação.

---

## 🍌 Power-ups

Bananas especiais que caem do topo da tela e podem ser coletadas pelo jogador:

| Power-up | Efeito |
|---|---|
| 🟡 Turbo | Aumenta a velocidade por um tempo |
| 🟡 Dourada | Tiro duplo (dois projéteis) |
| 🛡️ Casca | Escudo que bloqueia dano |
| 💥 Explosiva | Mega tiro (projéteis mais fortes) |
| ❤️ Coração | Recupera 1 vida |
| ⭐ Estrela | Pontos bônus |

---

## ❤️ Sistema de vida

O jogador começa com **5 vidas**.

Os ataques inimigos causam dano ao jogador, tornando necessário:

- Desviar dos projéteis
- Observar os padrões dos inimigos
- Evitar colisões
- Escolher bons momentos para atacar

---

## 🏆 Objetivo

O objetivo principal é:

1. ✈️ Controlar o avião-banana
2. 👾 Derrotar os inimigos
3. 💥 Desviar dos diferentes tipos de projéteis
4. 📈 Acumular pontuação
5. 👑 Enfrentar o Boss
6. 🏆 Sobreviver ao confronto final

---

## 🧱 Estrutura do projeto


Macacaquito-Louco/
│
├── main.py                    # Entrada: dependências, tela e início do jogo
├── requirements.txt           # Dependências (pygame-ce)
├── readme.md
├── relatorio.md               # Relatório de implementações
├── AGENTS.md                  # Instruções para agentes
├── opencode.json
│
└── jogo/
    ├── __init__.py            # Marca o pacote jogo
    ├── settings.py            # Configurações e constantes globais
    │
    ├── entidades/             # Entidades do jogo
    │   ├── entidade.py        # Classe base Entidade (sprite)
    │   ├── jogador.py         # Jogador (macaco no avião de bananas)
    │   ├── inimigo.py         # Forças policiais e chefe final
    │   ├── tiro.py            # Projéteis e explosões
    │   └── powerup.py         # Power-ups colecionáveis
    │
    ├── telas/                 # Game loop e telas
    │   ├── aplicacao.py       # Classe Jogo: loop, estados, partida
    │   ├── menu.py            # Menu inicial
    │   └── game_over.py       # Tela de game over
    │
    └── visual/                # Cenário, tema e efeitos
        ├── bg_fase.py         # Background da gameplay (cidade, nuvens)
        ├── tema.py            # Tema de selva (menus)
        └── efeito.py          # Partículas, flashes e explosões