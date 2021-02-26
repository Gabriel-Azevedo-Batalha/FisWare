# FisWare
## Idéia
   Um jogo que sorteia um minigame, que, se vencido, vai sortear outro incrementando a dificuldade
## Como iniciar
   Para iniciar use: python3 game.py na pasta raiz
## Menu
- Pressione **S** para iniciar o jogo
- Pressione **P** para abrir a aba de prática
    - Selecione usando o número correspondente ao minigame
- Pressione **O** para abrir a aba de opções
    - Altere a dificuldade inicial usando **<** e **>**
    - Ative o mudo usando **M**
- Em qualque aba pressione **B** para voltar
- Ao concluir um minigame pressione enter para sair da tela de resultados
## Minigames
### Pong
- Objetivo: Marcar um ponto
- Derrota: Deixar o adversário marcar um ponto
- Controles: **UP** e **DOWN**
### BallNChain
- Objetivo: Acertar com a bola todos os alvos
- Derrota: Deixar um alvo sair da tela, ser atingido por um alvo ou atingir você mesmo com a bola
- Controles: **UP**, **DOWN**, **LEFT** e **RIGHT**
### Dodge
- Objetivo: Desviar de todos os lasers
- Derrota: Ser atingido
- Controles: **UP**, **DOWN**, **LEFT** e **RIGHT**
### Claw (Em desenvolvimento)
- Objetivo: Mover a bola azul para o alvo
- Derrota: Deixar o tempo acabar
- Controles: **UP**, **DOWN**, **LEFT** e **RIGHT** para se mover e **SPACE** para abrir a garra
- Obs: Segurar **SHIFT** faz o contador de tempo paralizar(Para debugging), não existe incremento de dificuldade
