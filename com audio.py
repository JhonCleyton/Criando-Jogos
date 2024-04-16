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
            print(f"{self.nome} usou uma poção de cura.")
        else:
            print("Você não tem poções de cura suficientes.")

    def usar_pocao_ataque(self):
        if self.inventario["poção_ataque"] > 0:
            self.dano_base += 5
            self.inventario["poção_ataque"] -= 1
            print(f"{self.nome} usou uma poção de ataque.")
        else:
            print("Você não tem poções de ataque suficientes.")

    def equipar_armadura(self):
        if self.inventario["armadura"] > 0:
            self.defesa_base += 5
            self.inventario["armadura"] -= 1
            print(f"{self.nome} equipou uma armadura.")
        else:
            print("Você não tem armaduras suficientes.")

    def equipar_arma(self):
        if self.inventario["arma"] > 0:
            self.dano_base += 10
            self.inventario["arma"] -= 1
            print(f"{self.nome} equipou uma arma.")
        else:
            print("Você não tem armas suficientes.")

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

# Criando uma instância do jogador
jogador = Jogador("Herói", "Guerreiro")

# Loop principal do jogo
executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
    
    # Movimentação do jogador
    teclas = pygame.key.get_pressed()
    mover_jogador(teclas)
    
    # Verifica se houve colisão entre o jogador e algum personagem
    for personagem in personagens:
        if colisao(pygame.Rect(posicao_jogador[0], posicao_jogador[1], largura_jogador, altura_jogador), personagem):
            inimigo = Inimigo("Inimigo", 50, 8)  # Criando um inimigo
            batalha(jogador, inimigo)  # Inicia a batalha
    
    # Desenha os elementos na tela
    desenhar()



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
            print(f"{self.nome} usou uma poção de cura.")
        else:
            print("Você não tem poções de cura suficientes.")

    def usar_pocao_ataque(self):
        if self.inventario["poção_ataque"] > 0:
            self.dano_base += 5
            self.inventario["poção_ataque"] -= 1
            print(f"{self.nome} usou uma poção de ataque.")
        else:
            print("Você não tem poções de ataque suficientes.")

    def equipar_armadura(self):
        if self.inventario["armadura"] > 0:
            self.defesa_base += 5
            self.inventario["armadura"] -= 1
            print(f"{self.nome} equipou uma armadura.")
        else:
            print("Você não tem armaduras suficientes.")

    def equipar_arma(self):
        if self.inventario["arma"] > 0:
            self.dano_base += 10
            self.inventario["arma"] -= 1
            print(f"{self.nome} equipou uma arma.")
        else:
            print("Você não tem armas suficientes.")

    def esta_vivo(self):
        return self.vida_atual > 0

    def abrir_inventario(self):
        print("Inventário:")
        for item, quantidade in self.inventario.items():
            print(f"- {quantidade}x {item}")
        print(f"- Ouro: {self.ouro}")

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

class Chefe(Inimigo):
    def __init__(self, nome, vida, dano, nivel):
        super().__init__(nome, vida, dano)
        self.nivel = nivel

class Lobo(Inimigo):
    def __init__(self):
        super().__init__("Lobo", 30, 8)

class Orc(Inimigo):
    def __init__(self):
        super().__init__("Orc", 40, 10)

class Esqueleto(Inimigo):
    def __init__(self):
        super().__init__("Esqueleto", 25, 6)

class AranhaGigante(Inimigo):
    def __init__(self):
        super().__init__("Aranha Gigante", 35, 12)

class ElementalFogo(Inimigo):
    def __init__(self):
        super().__init__("Elemental de Fogo", 50, 15)

class ChefeCaverna(Chefe):
    def __init__(self):
        super().__init__("Dragão da Caverna", 150, 20, 3)

class Piranha(Inimigo):
    def __init__(self):
        super().__init__("Piranha", 20, 8)

class Crocodilo(Inimigo):
    def __init__(self):
        super().__init__("Crocodilo", 45, 12)

class Naga(Inimigo):
    def __init__(self):
        super().__init__("Naga", 60, 18)

class ChefePantano(Chefe):
    def __init__(self):
        super().__init__("Kraken", 180, 25, 4)

class Escorpiao(Inimigo):
    def __init__(self):
        super().__init__("Escorpião", 35, 10)

class Golem(Inimigo):
    def __init__(self):
        super().__init__("Golem de Areia", 70, 20)

class Fenix(Inimigo):
    def __init__(self):
        super().__init__("Fênix", 55, 15)

class ChefeDeserto(Chefe):
    def __init__(self):
        super().__init__("Djinn", 200, 30, 5)

class NPC:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def interagir(self):
        print(f"{self.nome}: {self.descricao}")

class DicaNPC(NPC):
    def __init__(self, nome, descricao, dica):
        super().__init__(nome, descricao)
        self.dica = dica

    def interagir(self):
        print(f"{self.nome}: {self.descricao}")
        print(f"Dica: {self.dica}")

class MissaoNPC(NPC):
    def __init__(self, nome, descricao, recompensa):
        super().__init__(nome, descricao)
        self.recompensa = recompensa

    def interagir(self):
        print(f"{self.nome}: {self.descricao}")
        aceitar = input("Você aceita a missão? (sim/não): ")
        if aceitar.lower() == "sim":
            print(f"Você aceitou a missão de {self.nome}!")
            # Aqui você pode adicionar a lógica para a missão
        else:
            print(f"Você recusou a missão de {self.nome}.")

class MissaoCaverna:
    def __init__(self):
        self.completada = False

    def completar_missao(self):
        self.completada = True
        print("Você encontrou o animal de estimação perdido do NPC na caverna!")

    def verificar_missao(self):
        if not self.completada:
            print("Você ainda não completou a missão do NPC na caverna. Continue procurando pelo animal perdido!")
        else:
            print("Você já completou a missão do NPC na caverna. Parabéns!")

class MissaoPantano:
    def __init__(self):
        self.encontrado = False

    def encontrar_item(self):
        self.encontrado = True
        print("Você encontrou o item perdido pelo NPC no pantano!")

    def verificar_progresso(self):
        if not self.encontrado:
            print("Você ainda não encontrou o item perdido pelo NPC no pantano. Continue procurando!")
        else:
            print("Você encontrou o item perdido pelo NPC no pantano. Volte para entregá-lo!")

def batalha(jogador, inimigo):
    print(f"{jogador.nome} enfrenta {inimigo.nome}!")
    while jogador.esta_vivo() and inimigo.esta_vivo():
        print(f"{jogador.nome} (Vida: {jogador.vida_atual}) vs {inimigo.nome} (Vida: {inimigo.vida})")
        escolha = input("O que você deseja fazer? (atacar/usar poção/equipar armadura/equipar arma/fugir): ")
        if escolha.lower() == "atacar":
            jogador_dano = jogador.atacar()
            inimigo.receber_dano(jogador_dano)
            print(f"{jogador.nome} ataca {inimigo.nome} causando {jogador_dano} de dano.")
        elif escolha.lower() == "usar poção":
            jogador.usar_pocao_curar()
        elif escolha.lower() == "equipar armadura":
            jogador.equipar_armadura()
        elif escolha.lower() == "equipar arma":
            jogador.equipar_arma()
        elif escolha.lower() == "fugir":
            print("Você fugiu da batalha!")
            return False
        elif escolha.lower() == "interagir":
            print("Você está interagindo com o ambiente.")
            return True
        elif escolha.lower() == "abrir inventário":
            jogador.abrir_inventario()
        else:
            print("Escolha inválida. Tente novamente.")
            continue
        
        if not inimigo.esta_vivo():
            print(f"{inimigo.nome} foi derrotado!")
            return True
        
        inimigo_dano = inimigo.atacar()
        jogador.receber_dano(inimigo_dano)
        print(f"{inimigo.nome} ataca {jogador.nome} causando {inimigo_dano} de dano.")
        if not jogador.esta_vivo():
            print(f"{jogador.nome} foi derrotado!")
            return False

def explorar_mapa(jogador):
    derrotou_chefe = False
    while not derrotou_chefe:
        terrenos = ["floresta", "montanha", "cidade", "caverna", "pantano", "deserto"]
        terreno_atual = random.choice(terrenos)

        print(f"Explorando {terreno_atual}...")
        if terreno_atual == "floresta":
            evento = random.randint(1, 5)
            if evento == 1:
                print("Você encontrou uma poção de cura!")
                jogador.inventario["poção_curar"] += 1
            elif evento == 2:
                print("Você foi atacado por lobos!")
                inimigo = Lobo()
                batalha(jogador, inimigo)
            elif evento == 3:
                print("Você encontrou uma armadilha!")
                jogador.receber_dano(20)
            else:
                print("Você encontrou um saco de ouro!")
                jogador.ouro += random.randint(5, 20)
        elif terreno_atual == "montanha":
            evento = random.randint(1, 5)
            if evento == 1:
                print("Você encontrou uma poção de ataque!")
                jogador.inventario["poção_ataque"] += 1
            elif evento == 2:
                print("Você encontrou um tesouro escondido!")
                jogador.ouro += random.randint(10, 50)
            elif evento == 3:
                print("Você escorregou em uma encosta íngreme e se machucou!")
                jogador.receber_dano(10)
            else:
                print("Você encontrou uma pepita de ouro!")
                jogador.ouro += random.randint(2, 10)
        elif terreno_atual == "cidade":
            evento = random.randint(1, 5)
            if evento == 1:
                print("Você encontrou um mercador!")
                mercado(jogador)
            elif evento == 2:
                print("Você encontrou um mercador que vende armaduras!")
                jogador.inventario["armadura"] += 1
            elif evento == 3:
                print("Você encontrou um NPC com uma missão secundária!")
                npc_dica = DicaNPC("NPC de Dicas", "Eu conheço este lugar muito bem. Posso te dar uma dica útil.", "Tenha cuidado com as criaturas daqui.")
                npc_missao = MissaoNPC("NPC de Missão", "Oi aventureiro! Preciso de sua ajuda para encontrar meu animal de estimação perdido. Você pode ajudar?", "Recompensa: Poção de cura extra.")
                npc_dica.interagir()
                npc_missao.interagir()
            else:
                print("Você encontrou uma bolsa de ouro perdida!")
                jogador.ouro += random.randint(5, 30)
        elif terreno_atual == "caverna":
            evento = random.randint(1, 5)
            if evento == 1:
                print("Você encontrou uma poção de cura em uma caverna!")
                jogador.inventario["poção_curar"] += 1
            elif evento == 2:
                print("Você foi emboscado por um grupo de esqueletos na caverna!")
                inimigo = Esqueleto()
                batalha(jogador, inimigo)
            elif evento == 3:
                print("Você encontrou um baú de tesouro escondido na caverna!")
                jogador.ouro += random.randint(10, 40)
            else:
                print("Você encontrou um NPC na caverna!")
                npc_missao = MissaoNPC("NPC da Caverna", "Oi aventureiro! Estou procurando pelo meu animal de estimação perdido. Você pode me ajudar?", "Recompensa: Ouro extra.")
                npc_missao.interagir()
        elif terreno_atual == "pantano":
            evento = random.randint(1, 5)
            if evento == 1:
                print("Você encontrou uma poção de cura no pantano!")
                jogador.inventario["poção_curar"] += 1
            elif evento == 2:
                print("Você foi atacado por piranhas no pantano!")
                inimigo = Piranha()
                batalha(jogador, inimigo)
            elif evento == 3:
                print("Você encontrou um objeto perdido no pantano!")
                jogador.inventario["objeto_perdido"] = 1
            else:
                print("Você encontrou um NPC no pantano!")
                npc_missao = MissaoNPC("NPC do Pantano", "Oi aventureiro! Preciso de sua ajuda para encontrar meu objeto perdido. Você pode me ajudar?", "Recompensa: Arma especial.")
                npc_missao.interagir()
        elif terreno_atual == "deserto":
            evento = random.randint(1, 5)
            if evento == 1:
                print("Você encontrou uma poção de ataque no deserto!")
                jogador.inventario["poção_ataque"] += 1
            elif evento == 2:
                print("Você foi atacado por uma tempestade de areia no deserto!")
                jogador.receber_dano(15)
            elif evento == 3:
                print("Você encontrou um oásis escondido no deserto!")
                jogador.vida_atual += 20
                if jogador.vida_atual > jogador.vida_maxima:
                    jogador.vida_atual = jogador.vida_maxima
            else:
                print("Você encontrou um NPC no deserto!")
                npc_missao = MissaoNPC("NPC do Deserto", "Oi aventureiro! Posso te oferecer uma recompensa se você me ajudar a encontrar um tesouro enterrado.", "Recompensa: Armadura especial.")
                npc_missao.interagir()

        if terreno_atual in ["caverna", "pantano", "deserto"]:
            chefe = None
            if terreno_atual == "caverna":
                chefe = ChefeCaverna()
            elif terreno_atual == "pantano":
                chefe = ChefePantano()
            elif terreno_atual == "deserto":
                chefe = ChefeDeserto()
            print(f"Você encontrou o chefe {chefe.nome} na {terreno_atual}!")
            derrotou_chefe = batalha(jogador, chefe)
            if derrotou_chefe:
                print(f"Você derrotou {chefe.nome}!")
                if terreno_atual == "caverna":
                    missao_caverna.completar_missao()
                elif terreno_atual == "pantano":
                    missao_pantano.encontrar_item()
                break

def mercado(jogador):
    print("Bem-vindo ao mercado!")
    while True:
        print("O que você deseja comprar?")
        print("1. Poção de cura - 10 de ouro")
        print("2. Poção de ataque - 15 de ouro")
        print("3. Armadura - 50 de ouro")
        print("4. Arma - 100 de ouro")
        print("5. Sair do mercado")
        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            if jogador.ouro >= 10:
                jogador.inventario["poção_curar"] += 1
                jogador.ouro -= 10
                print("Você comprou uma poção de cura.")
            else:
                print("Você não tem ouro suficiente.")
        elif escolha == "2":
            if jogador.ouro >= 15:
                jogador.inventario["poção_ataque"] += 1
                jogador.ouro -= 15
                print("Você comprou uma poção de ataque.")
            else:
                print("Você não tem ouro suficiente.")
        elif escolha == "3":
            if jogador.ouro >= 50:
                jogador.inventario["armadura"] += 1
                jogador.ouro -= 50
                print("Você comprou uma armadura.")
            else:
                print("Você não tem ouro suficiente.")
        elif escolha == "4":
            if jogador.ouro >= 100:
                jogador.inventario["arma"] += 1
                jogador.ouro -= 100
                print("Você comprou uma arma.")
            else:
                print("Você não tem ouro suficiente.")
        elif escolha == "5":
            print("Obrigado pela visita!")
            break
        else:
            print("Escolha inválida. Tente novamente.")

def main():
    nome_jogador = input("Qual é o seu nome? ")
    print(f"Bem-vindo, {nome_jogador}!")

    escolha_classe = input("Escolha sua classe (Guerreiro/Mago/Ladino): ")
    jogador = Jogador(nome_jogador, escolha_classe)

    print(f"Você é um(a) {jogador.classe} de nível {jogador.nivel}!")

    while jogador.esta_vivo():
        print("\nMapa:")
        print("1. Explorar")
        print("2. Abrir inventário")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            explorar_mapa(jogador)
        elif opcao == "2":
            jogador.abrir_inventario()
        elif opcao == "3":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

missao_caverna = MissaoCaverna()
missao_pantano = MissaoPantano()
main()
# Encerra o Pygame
pygame.quit()


# Execução do jogo
if __name__ == "__main__":
    main()
