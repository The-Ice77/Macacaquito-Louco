# AGENTS.md — Macacaquito-Louco

## 1. Sobre o projeto

Macacaquito-Louco é um jogo 2D desenvolvido em Python utilizando Pygame.

O projeto tem finalidade educacional/escolar e deve priorizar:
- funcionamento correto;
- código simples e legível;
- facilidade de manutenção;
- boa experiência de jogo;
- escopo adequado ao tamanho do projeto.

O projeto não deve ser transformado em uma arquitetura excessivamente complexa.

---

## 2. Tecnologias

Tecnologia principal:
- Python 3
- Pygame

Não adicionar bibliotecas externas sem autorização explícita do usuário.

Sempre que uma funcionalidade puder ser implementada utilizando Python/Pygame puro, prefira essa abordagem.

---

## 3. Estrutura atual

A estrutura principal do projeto é:

    main.py
        Ponto de entrada: verifica dependências, inicializa a tela e inicia o jogo.

    jogo/
        Pacote com os módulos do jogo.

    jogo/__init__.py
        Marca a pasta como pacote Python.

    jogo/settings.py
        Configurações e constantes globais do jogo.

    jogo/entidade.py
        Classe base Entidade, derivada de pygame.sprite.Sprite.

    jogo/jogador.py
        Classe Jogador e lógica relacionada ao jogador.

    jogo/inimigo.py
        Classes relacionadas aos inimigos (forças policiais).

    jogo/tiro.py
        Classe relacionada aos projéteis.

    jogo/menu.py
        Tela inicial do jogo.

    jogo/game_over.py
        Tela de game over.

    jogo/aplicacao.py
        Classe Jogo: game loop, sistema de estados e lógica da partida.

    requirements.txt
        Dependências do projeto.

    AGENTS.md
        Instruções para agentes de desenvolvimento.

    opencode.json
        Configuração do OpenCode.

Os módulos do jogo ficam dentro do pacote `jogo/` e se importam relativamente
(ex.: `from .settings import LARGURA`).

Outros arquivos podem ser adicionados conforme o projeto evoluir.

Antes de criar novos módulos, verificar se realmente são necessários.

---

## 4. Princípios de desenvolvimento

### Simplicidade

Não criar sistemas complexos quando uma solução simples resolver o problema.

Evitar:
- abstrações desnecessárias;
- padrões de projeto sem necessidade;
- excesso de classes;
- sistemas genéricos que não serão reutilizados;
- dependências externas desnecessárias.

O projeto é um jogo escolar de pequeno porte.

### Legibilidade

O código deve ser fácil de entender por um estudante de programação.

Preferir:

    if jogador.vida <= 0:
        game_over = True

em vez de criar abstrações desnecessárias para operações simples.

Use nomes de variáveis, funções e classes claros.

### Consistência

Respeitar a estrutura e o estilo já existentes antes de criar uma abordagem completamente diferente.

Não reescrever arquivos inteiros sem necessidade.

---

## 5. Regras para alterações

Antes de fazer uma alteração significativa:

1. Entender como o código atual funciona.
2. Identificar quais arquivos realmente precisam ser modificados.
3. Explicar brevemente o que será feito quando a alteração for uma etapa importante.
4. Fazer a menor alteração necessária para atingir o objetivo.
5. Preservar funcionalidades existentes.
6. Verificar se a alteração introduziu erros.

Não modificar arquivos que não estejam relacionados à tarefa.

Não apagar funcionalidades existentes apenas para simplificar a implementação sem autorização.

---

## 6. Escopo do jogo

O jogo atualmente possui:

- jogador controlável (macaco em avião de bananas);
- movimentação WASD;
- disparo com Espaço (bananas);
- inimigos: Guarda, Helicóptero Policial, Viatura Rápida, Guarda Pesado, Chefe Final;
- projéteis (jogador e inimigos);
- colisões;
- sistema de vida;
- pontuação;
- spawn de inimigos por pesos;
- game loop;
- HUD;
- menu inicial;
- tela de Game Over;
- reinício da partida;
- dificuldade progressiva.

Funcionalidades futuras podem incluir:

- power-ups;
- sons;
- música;
- melhorias visuais;
- sprites;
- sistema de ondas;
- outros elementos de gameplay.

Priorizar primeiro funcionalidades que aumentem a jogabilidade e apresentação do projeto.

---

## 7. Gameplay

Ao implementar novas funcionalidades:

- manter os controles existentes, salvo instrução contrária;
- não alterar arbitrariamente a velocidade do jogador;
- não alterar arbitrariamente a quantidade inicial de vida;
- não remover o sistema de pontuação;
- manter o jogo responsivo;
- evitar dificuldade injusta;
- evitar situações em que o jogador fique impossibilitado de jogar;
- garantir que o jogo possa ser reiniciado corretamente após Game Over.

Quando alterar balanceamento, explicar brevemente quais valores foram modificados e por quê.

---

## 8. Pygame

Seguir boas práticas básicas de Pygame.

Sempre que possível:

- utilizar `pygame.sprite.Sprite` para entidades;
- utilizar `pygame.Rect` para posicionamento e colisão;
- utilizar `pygame.sprite.Group` quando grupos de sprites forem úteis;
- manter o controle de FPS;
- evitar criar objetos continuamente sem necessidade;
- remover corretamente sprites que não são mais utilizados;
- evitar bloquear o game loop com operações demoradas.

Não criar loops infinitos adicionais dentro do game loop principal.

---

## 9. Assets

Se forem necessários sprites, sons ou outros assets:

1. Verificar primeiro se já existe um asset adequado no projeto.
2. Não substituir assets existentes sem necessidade.
3. Não adicionar assets de procedência desconhecida sem autorização.
4. Manter os assets organizados em diretórios apropriados.

Se uma funcionalidade puder funcionar inicialmente com formas simples do Pygame, pode-se utilizar um placeholder.

---

## 10. Dependências

A única dependência principal esperada atualmente é:

    pygame

Se uma nova biblioteca for necessária:

- explicar por que ela é necessária;
- informar qual biblioteca será adicionada;
- aguardar autorização do usuário antes de instalar/adicionar a dependência.

Não executar `pip install` automaticamente para adicionar novas dependências.

Se necessário, atualizar `requirements.txt` após autorização.

---

## 11. Testes

O projeto atualmente pode não possuir testes automatizados.

Para cada alteração importante:

- executar o jogo quando possível;
- verificar se não existem erros de execução;
- verificar a funcionalidade modificada;
- verificar se funcionalidades existentes continuam funcionando.

Para bugs simples, tentar reproduzir o problema antes de corrigi-lo.

Não criar uma grande infraestrutura de testes apenas para funcionalidades pequenas.

---

## 12. Execução

A execução normal do jogo é:

    python main.py

Caso exista um ambiente virtual no projeto, utilizá-lo.

Antes de assumir que uma dependência está faltando, verificar o ambiente atual.

Não alterar configurações globais do sistema para executar o projeto.

---

## 13. Tratamento de erros

Evitar `try/except` excessivos.

Não esconder erros silenciosamente.

Não utilizar:

    except:
        pass

para simplesmente esconder problemas.

Quando um erro puder ser tratado de maneira útil, fornecer uma mensagem clara.

---

## 14. Git

O projeto utiliza Git e GitHub.

O agente pode:

- verificar `git status`;
- verificar `git diff`;
- verificar histórico;
- adicionar arquivos ao commit;
- criar commits quando solicitado ou quando isso fizer parte explicitamente da tarefa.

Antes de criar um commit importante, verificar o diff.

Nunca executar operações destrutivas de Git sem autorização explícita.

Nunca executar automaticamente:

    git reset --hard

    git clean -fd

    git checkout .

    git restore .

ou comandos equivalentes que possam apagar alterações do usuário.

---

## 15. Git Push

O agente NÃO deve executar `git push` automaticamente.

Mesmo que uma tarefa tenha sido concluída e commitada:

- não fazer push sem autorização explícita do usuário;
- não alterar o repositório remoto;
- não fazer force push.

O usuário deve continuar tendo controle sobre o envio das alterações para o GitHub.

---

## 16. Commits

Quando o usuário pedir para criar um commit:

1. Verificar `git status`.
2. Verificar as alterações com `git diff`.
3. Confirmar que as alterações estão relacionadas à tarefa.
4. Criar um commit com uma mensagem clara.

Preferir mensagens como:

    feat: adiciona tela de game over

    feat: adiciona novos inimigos

    fix: corrige colisão entre tiro e robo

    fix: corrige reinício da partida

    refactor: organiza game loop

Evitar mensagens genéricas como:

    update

    mudanças

    coisa nova

---

## 17. Documentação

Documentar somente o que for útil.

Comentários devem explicar:
- lógica não óbvia;
- decisões importantes;
- comportamentos que possam causar confusão.

Não adicionar comentários óbvios como:

    # soma 1
    pontos += 1

Remover comentários claramente abandonados ou sem significado quando estiver trabalhando no trecho correspondente.

Não modificar comentários não relacionados à tarefa sem necessidade.

---

## 18. AGENTS.md

Este arquivo contém as regras permanentes do projeto.

Não apagar este arquivo.

Não substituir suas regras por instruções temporárias de uma tarefa.

Se uma nova regra importante para o desenvolvimento do projeto for descoberta, o usuário pode solicitar que este arquivo seja atualizado.

---

## 19. Segurança

Nunca:

- acessar arquivos pessoais que não sejam necessários para o projeto;
- procurar ou expor senhas;
- procurar tokens, chaves de API ou credenciais;
- modificar arquivos fora do projeto sem necessidade;
- executar comandos destrutivos sem autorização;
- instalar software sem autorização;
- fazer `git push` sem autorização;
- alterar configurações do sistema sem necessidade.

Arquivos `.env`, credenciais e segredos não devem ser lidos ou expostos.

---

## 20. Quando houver dúvida

Se houver várias maneiras razoáveis de implementar algo:

1. escolher a solução mais simples;
2. preservar a arquitetura existente;
3. minimizar alterações;
4. considerar o nível educacional do projeto;
5. perguntar ao usuário quando a decisão puder alterar significativamente o escopo.

Não transformar uma tarefa pequena em uma grande refatoração.

---

## 21. Prioridade das instruções

Ao trabalhar neste projeto, seguir esta prioridade:

1. Instruções explícitas do usuário na conversa atual.
2. Regras deste AGENTS.md.
3. Estrutura e comportamento já existentes do projeto.
4. Boas práticas gerais de Python/Pygame.

Se uma instrução nova do usuário entrar em conflito com este arquivo, seguir a instrução explícita do usuário.

---

## 22. Objetivo final

O objetivo não é criar uma arquitetura perfeita.

O objetivo é entregar um jogo:

- divertido;
- funcional;
- apresentável;
- estável;
- fácil de entender;
- adequado ao projeto escolar;
- possível de manter e expandir.

Priorizar terminar um jogo bom em vez de criar um sistema tecnicamente exagerado.