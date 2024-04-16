import pygame
import random

# Definição das constantes de cor
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()  # Inicialização do mixer para áudio

# Definição da largura e altura da tela
largura_tela = 800
altura_tela = 600

# Definição da largura e altura do jogador
largura_jogador = 50
altura_jogador = 50

# Carregamento da imagem do jogador
imagem_jogador = pygame.Surface((largura_jogador, altura_jogador))
imagem_jogador.fill((0, 255, 0))  # Cor verde para o jogador

# Definição da posição inicial do jogador
posicao_jogador = [largura_tela // 2, altura_tela // 2]

# Definição da velocidade do jogador
velocidade_jogador = 5

# Definição da posição inicial dos personagens
posicoes_personagens = [
    [100, 100],
    [400, 200],
    [600, 400]
]

# Definição da largura e altura dos personagens
largura_personagem = 50
altura_personagem = 50

# Lista de personagens
personagens = [pygame.Rect(x, y, largura_personagem, altura_personagem) for x, y in posicoes_personagens]

# Criação da tela
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Interagindo com Personagens")

# Carregamento do áudio de ataque
ataque_som = pygame.mixer.Sound("ataque.wav")

# Função para desenhar o jogador e os personagens na tela
def desenhar():
    tela.fill(BRANCO)  # Limpa a tela com a cor branca
    # Desenha o jogador
    tela.blit(imagem_jogador, posicao_jogador)
    # Desenha os personagens
    for personagem in personagens:
        pygame.draw.rect(tela, (255, 0, 0), personagem)
    pygame.display.flip()  # Atualiza a tela

# Função para mover o jogador
def mover_jogador(teclas):
    if teclas[pygame.K_LEFT]:
        posicao_jogador[0] -= velocidade_jogador
    if teclas[pygame.K_RIGHT]:
        posicao_jogador[0] += velocidade_jogador
    if teclas[pygame.K_UP]:
        posicao_jogador[1] -= velocidade_jogador
    if teclas[pygame.K_DOWN]:
        posicao_jogador[1] += velocidade_jogador

# Função para detectar colisão entre dois retângulos
def colisao(retangulo1, retangulo2):
    return retangulo1.colliderect(retangulo2)

# Função para realizar uma batalha entre o jogador e um inimigo
def batalha(jogador, inimigo):
    print(f"{jogador.nome} enfrenta {inimigo.nome}!")
    while jogador.esta_vivo() and inimigo.esta_vivo():
        print(f"{jogador.nome} (Vida: {jogador.vida_atual}) vs {inimigo.nome} (Vida: {inimigo.vida})")
        escolha = input("O que você deseja fazer? (atacar/usar poção): ")
        if escolha.lower() == "atacar":
            jogador_dano = jogador.atacar()
            inimigo.receber_dano(jogador_dano)
            print(f"{jogador.nome} ataca {inimigo.nome} causando {jogador_dano} de dano.")
            ataque_som.play()  # Reproduz o som de ataque
        elif escolha.lower() == "usar poção":
            jogador.usar_pocao_curar()
        else:
            print("Escolha inválida. Tente novamente.")
            continue
        
        if not inimigo.esta_vivo():
            print(f"{inimigo.nome} foi derrotado!")
            personagens.remove(inimigo)  # Remove o inimigo da lista de personagens
            return True
        
        inimigo_dano = inimigo.atacar()
        jogador.receber_dano(inimigo_dano)
        print(f"{inimigo.nome} ataca {jogador.nome} causando {inimigo_dano} de dano.")
        if not jogador.esta_vivo():
            print(f"{jogador.nome} foi derrotado!")
            return False

# Classe para representar o jogador
class Jogador:
    def __init__(self, nome, classe):
        self.nome = nome
        self.classe = classe
        self.nivel = 1
        self.vida_maxima = 100
        self.vida_atual = self.vida_maxima
        self.dano_base = 10
        self.defesa_base = 5
        self.inventario = {"poção_curar": 3, "poção_ataque": 1, "armadura": 0, "arma": 0}
        self.ouro = 0

    def atacar(self):
        return random.randint(self.dano_base // 2, self.dano_base)

    def receber_dano(self, dano):
        dano -= self.defesa_base
        if dano < 0:
            dano = 0
        self.vida_atual -= dano
        if self.vida_atual < 0:
            self.vida_atual = 0

    def curar(self):
        cura = random.randint(10, 20)
        self.vida_atual += cura
        if self.vida_atual > self.vida_maxima:
            self.vida_atual = self.vida_maxima

    def usar_pocao_curar(self):
        if self.inventario["poção_curar"] > 0:
            self.curar()
            self.inventario["poção_curar"] -= 1
            print(f"{self.nome} usou uma poção de cura. Vida atual: {self.vida_atual}")
        else:
            print("Você não tem poções de cura.")

    def esta_vivo(self):
        return self.vida_atual > 0

# Classe para representar um inimigo
class Inimigo:
    def __init__(self, nome, vida, dano):
        self.nome = nome
        self.vida = vida
        self.dano = dano

    def atacar(self):
        return random.randint(self.dano // 2, self.dano)

    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0

    def esta_vivo(self):
        return self.vida > 0

# Instanciando o jogador
nome_jogador = input("Digite o nome do jogador: ")
classe_jogador = input("Escolha uma classe para o jogador (guerreiro/mago): ")
jogador = Jogador(nome_jogador, classe_jogador)

# Instanciando os inimigos
inimigo1 = Inimigo("Orc", 50, 15)
inimigo2 = Inimigo("Esqueleto", 30, 10)
inimigo3 = Inimigo("Bruxa", 40, 12)

# Loop principal do jogo
jogo_ativo = True
relogio = pygame.time.Clock()
while jogo_ativo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo_ativo = False

    teclas = pygame.key.get_pressed()
    mover_jogador(teclas)

    # Verifica colisão entre jogador e personagens
    for personagem in personagens:
        if colisao(pygame.Rect(posicao_jogador[0], posicao_jogador[1], largura_jogador, altura_jogador), personagem):
            batalha(jogador, inimigo1)  # Simplesmente usando inimigo1 para testar a batalha
            break

    desenhar()
    relogio.tick(60)

pygame.quit()
