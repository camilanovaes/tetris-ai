import random, time, pygame, sys
from pygame.locals import *
import tetris as t
import algoritmoGenetico as ag

size = [640, 480]
screen = pygame.display.set_mode((size[0], size[1]))

#add individuo,
def jogar(individuo, multVel, scoreMax = 20000, jogoRapido = False):

    t.FPS = int(multVel)
    t.main()

    board = t.getBlankBoard()
    lastFallTime = time.time()
    score = 0
    
    level, fallFreq = t.calculateLevelAndFallFreq(score)

    fallingPiece = t.getNewPiece()
    nextPiece = t.getNewPiece()
    individuo.calcularMelhorJogada(board, fallingPiece)
    
    pecasJogadas = 0
    linhasDestruidas = [0,0,0,0] #combos
    
    vivo = True
    ganhou = False

    
    while vivo: #game loop
        #process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print ("Game exited by user")
                exit()
                
        if fallingPiece == None:
            # nenhuma peca caindo, gera uma nova peca
            fallingPiece = nextPiece
            nextPiece = t.getNewPiece()

            #decide a melhor jogada baseado no que acha (pesos)
            individuo.calcularMelhorJogada(board, fallingPiece, jogoRapido)

            pecasJogadas +=1
            score += 1

            lastFallTime = time.time() # reseta lastFallTime

            if not t.isValidPosition(board, fallingPiece):
                #nao existe possiçao que caiba na tela
                vivo = False


        if jogoRapido or time.time() - lastFallTime > fallFreq:

            if not t.isValidPosition(board, fallingPiece, adjY=1):
                # A peca caiu, adiciona ela para o tabuleiro
                t.addToBoard(board, fallingPiece)
                numLines = t.removeCompleteLines(board)
                if(numLines == 1):
                    score += 40
                    linhasDestruidas[0] += 1
                elif (numLines == 2):
                    score += 120
                    linhasDestruidas[1] += 1
                elif (numLines == 3):
                    score += 300
                    linhasDestruidas[2] += 1
                elif (numLines == 4):
                    score += 1200
                    linhasDestruidas[3] += 1

                fallingPiece = None
            else:
                # A peca ainda esta caindo, move ela para baixo
                fallingPiece['y'] += 1
                lastFallTime = time.time()


        if not jogoRapido:
            desenharNaTela(board,score,level,nextPiece, fallingPiece)

        #condiçao de parada
        if score > scoreMax:
            vivo = False
            ganhou = True

    # retorna [numero de pecas, linhas destruidas(combos de 1,2,3,4), score normal de tetris, ganhou]
    gameState = [pecasJogadas, linhasDestruidas ,score, ganhou]
    return(gameState)




def desenharNaTela(board,score,level,nextPiece,fallingPiece):
    t.DISPLAYSURF.fill(t.BGCOLOR)
    t.drawBoard(board)
    t.drawStatus(score, level)
    t.drawNextPiece(nextPiece)
    if fallingPiece != None:
        t.drawPiece(fallingPiece)

    pygame.display.update()

    t.FPSCLOCK.tick(t.FPS)


if __name__ == '__main__':
    numPesos = 7
    pesos0 = numPesos*[0]
    for k2 in range (0,numPesos):
        pesos0[k2] = 2*random.random()-1
    pesos0= [-0.97, 5.47, -13.74, -0.73,  7.99, -0.86, -0.72]
    indiv = ag.Individuo(pesos0)
	
    print(jogar(indiv,300,scoreMax = 200000))
    
