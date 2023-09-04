import os
import sys
import pygame
import random
import sqlite3

from config import *
from Jogada import *

PRETO = (0,0,0)
AZUL = (100,149,237)
CINZA = (79,79,79)
BRANCO = (255, 255, 255)

# Carrega imagens
cache_imagens = {}
def carrega_imagens(imagem):
    if not imagem in cache_imagens:
        try:
            caminho = os.path.join(os.path.dirname(__file__), imagem)
            cache_imagens[imagem] = pygame.image.load(caminho).convert_alpha()
        except pygame.error:
            print('Não será possivel abrir arquivo de imagem: {0}'.format(imagem))
            sys.exit()
    return cache_imagens[imagem]

# Carrega sons
cache_sons = {}
def carrega_sons(som):
    if not som in cache_sons:
        try:
            caminho = os.path.join(os.path.dirname(__file__), som)
            cache_sons[som] = pygame.mixer.Sound(caminho)
        except pygame.error:
            print('Não será possivel ler arquivo de som: {0}'.format(som))
            sys.exit()
    return cache_sons[som]

class Mini(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        arquivo = os.path.join('imagens', 'mini1.png')
        self.image = carrega_imagens(arquivo)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.set_posicao(0, 0)
        self.set_velocidade(0.3, 0.25)
    
    def set_posicao(self, x, y):
        self.posi = pygame.math.Vector2(x, y)
    
    def set_velocidade(self, vx, vy):
        self.velocidade = pygame.math.Vector2(vx, vy)

    def update(self, delta_time):
        largura, altura = pygame.display.get_surface().get_size()
        self.posi += self.velocidade * delta_time
        self.rect.topleft = self.posi

        if self.rect.right > largura :
            self.velocidade[0] = -abs(self.velocidade[0])
            self.rect.right = largura
        elif self.rect.x < 0:
            self.velocidade[0] = abs(self.velocidade[0])
            self.rect.x = 0
        if self.rect.bottom > altura:
            self.velocidade[1] = -abs(self.velocidade[1])
            self.rect.bottom = altura
        elif self.rect.y < 0:
            self.velocidade[1] = abs(self.velocidade[1])
            self.rect.y = 0

def main():

    pygame.init()

    tela = pygame.display.set_mode((700, 600), pygame.RESIZABLE) # cria superficie para o jogo

    pygame.display.set_caption("Teste ")

    # Sons
    arquivo = os.path.join("sons", "Battleship.ogg")
    caminho = os.path.join(os.path.dirname(__file__), arquivo)
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    arquivo = os.path.join('sons', 'tiro.ogg')
    som_tiro = carrega_sons(arquivo)
    pygame.mixer.music.set_volume(0.1)

    font = pygame.font.Font(pygame.font.get_default_font(), 20) 
    font_pause = pygame.font.Font(pygame.font.get_default_font(), 40)

    sprites = pygame.sprite.Group()

    posi_circulo = [tela.get_width()/2, tela.get_height()/2]
    delta_circulo = {"esquerda":0, "direita":0, "acima":0, "abaixo":0}
    velocidade_circulo = 0.4

    barra_espaco = False
    botao_mouse = False

    clock = pygame.time.Clock() 
    
    pygame.time.set_timer(pygame.USEREVENT, 1000) # A cada 1 segundos aparece

    ultimo = 0  
    placar = 0  
    tamanho_tela = None  
    RODANDO = 0
    PAUSADO = 1
    jogo = RODANDO

    # criar o resultado da jogada, inicialmente com zero
    app.app_context().push()
    resultado = Jogada(score = 0)
    db.session.add(resultado)
    db.session.commit()

    while True:
        delta_time = clock.tick(60) 
        
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.VIDEORESIZE: 
                tamanho_tela = evento.size
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                pygame.quit() 
                sys.exit()    
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    delta_circulo["esquerda"] = 1
                elif evento.key == pygame.K_RIGHT:
                    delta_circulo["direita"] = 1
                elif evento.key == pygame.K_UP:
                    delta_circulo["acima"] = 1
                elif evento.key == pygame.K_DOWN:
                    delta_circulo["abaixo"] = 1
                elif evento.key == pygame.K_SPACE:
                    barra_espaco = True
                elif evento.key == pygame.K_p:
                    if jogo != PAUSADO:
                        pygame.mixer.music.pause()
                        pause = font_pause.render("PAUSE", True, AZUL, PRETO)
                        tela.blit(pause, ((tela.get_width()-pause.get_width())/2, (tela.get_height()-pause.get_height())/2))
                        jogo = PAUSADO
                    else:
                        pygame.mixer.music.unpause()
                        jogo = RODANDO

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT:
                    delta_circulo["esquerda"] = 0
                if evento.key == pygame.K_RIGHT:
                    delta_circulo["direita"] = 0
                elif evento.key == pygame.K_UP:
                    delta_circulo["acima"] = 0
                elif evento.key == pygame.K_DOWN:
                    delta_circulo["abaixo"] = 0
                elif evento.key == pygame.K_SPACE:
                    barra_espaco = False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                botao_mouse = True
            if evento.type == pygame.MOUSEBUTTONUP:
                botao_mouse = False
            if evento.type == pygame.MOUSEMOTION:
                posi_circulo = list(pygame.mouse.get_pos())
            if evento.type == pygame.USEREVENT and jogo != PAUSADO:
                mini = Mini(sprites) 
                mini.set_posicao(random.randint(0, tela.get_width() - mini.image.get_width()),
                                   random.randint(0, tela.get_height() - mini.image.get_height()))
                mini.set_velocidade(random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3))

        if tamanho_tela:
            tela = pygame.display.set_mode(tamanho_tela, pygame.RESIZABLE) 
            tamanho_tela = None
        if jogo == PAUSADO:
            pygame.display.flip()
            continue

        tela.fill(PRETO) 

        sprites.update(delta_time)
        sprites.draw(tela)
        
        posi_circulo[0] += (delta_circulo["direita"] - delta_circulo["esquerda"]) * velocidade_circulo * delta_time
        posi_circulo[1] += (delta_circulo["abaixo"] - delta_circulo["acima"]) * velocidade_circulo * delta_time

        clique = barra_espaco or botao_mouse
        agora = pygame.time.get_ticks()
    
        if clique and (agora - ultimo > 500):
            ultimo = agora
            som_tiro.play()

            pygame.draw.circle(tela, CINZA, posi_circulo, 4) 

            for sprite in sprites:
                if sprite.rect.collidepoint(posi_circulo):
                    ponto_mascara = [int(posi_circulo[0] - sprite.rect.x), int(posi_circulo[1] - sprite.rect.y)]
                    if sprite.mask.get_at(ponto_mascara):
                        sprite.kill()
                        placar += 1
                        resultado.score += 1
                        db.session.commit()

        else:
            pygame.draw.circle(tela, AZUL, posi_circulo, 3) 

        texto = font.render('Placar: {0}'.format(placar), True, BRANCO)
        tela.blit(texto, (10, 0))

        pygame.display.flip() 

if __name__ == "_main_":
    main()

main()