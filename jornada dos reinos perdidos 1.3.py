import random

class Jogador:
    def __init__(self, nome, classe):
        self.nome = nome
        self.classe = classe
        self.hp = 100
        self.ataque = 10
        self.defesa = 5
        self.nivel = 1
        self.xp = 0
        self.inventario = {
            "ouro": 50,
            "poção_curar": 2,
            "poção_ataque": 1,
            "armas": [],
            "armadura": 0
        }

    def mostrar_status(self):
        print(f"Nome: {self.nome}")
        print(f"Classe: {self.classe}")
        print(f"Nível: {self.nivel}")
        print(f"HP: {self.hp}")
        print(f"Ataque: {self.ataque}")
        print(f"Defesa: {self.defesa}")
        print(f"XP: {self.xp}")
        print(f"Ouro: {self.inventario['ouro']}")
        print("Inventário:")
        for item, quantidade in self.inventario.items():
            if item != "ouro":
                print(f"- {quantidade}x {item}")

    def atacar(self, inimigo):
        dano = self.ataque + sum(arma.dano_bonus for arma in self.inventario["armas"])
        dano -= inimigo.defesa
        inimigo.hp -= dano
        print(f"Você ataca o {inimigo.nome} causando {dano} de dano.")

    def receber_dano(self, dano):
        armadura_bonus = self.inventario["armadura"] * 2
        dano_recebido = dano - (self.defesa + armadura_bonus)
        if dano_recebido > 0:
            self.hp -= dano_recebido
            print(f"Você recebe {dano_recebido} de dano!")

    def curar(self):
        if self.inventario["poção_curar"] > 0:
            self.hp += 20
            self.inventario["poção_curar"] -= 1
            print("Você se curou com uma poção!")
        else:
            print("Você não tem poções de cura.")

    def usar_pocao_ataque(self):
        if self.inventario["poção_ataque"] > 0:
            self.ataque += 5
            self.inventario["poção_ataque"] -= 1
            print("Você usou uma poção de ataque!")
        else:
            print("Você não tem poções de ataque.")

    def esta_vivo(self):
        return self.hp > 0

    def batalha(self, inimigo):
        print(f"Um {inimigo.nome} apareceu!")
        while self.esta_vivo() and inimigo.esta_vivo():
            self.mostrar_status()
            acao = input("O que você quer fazer? (atacar/usar poção/fugir): ").lower()
            if acao == "atacar":
                self.atacar(inimigo)
            elif acao == "usar poção":
                self.curar()
            elif acao == "fugir":
                if random.random() < 0.5:
                    print("Você conseguiu fugir!")
                    break
                else:
                    print("Você falhou em fugir!")
            else:
                print("Comando inválido!")
            
            if inimigo.esta_vivo():
                inimigo.atacar(self)

        if self.esta_vivo():
            xp_ganho = random.randint(10, 20)
            self.xp += xp_ganho
            print(f"Você derrotou o {inimigo.nome} e ganhou {xp_ganho} de XP!")
            if self.xp >= 120:
                self.nivel += 1
                self.hp = 100
                self.xp = 0
                print("Você subiu de nível!")
        else:
            print("Você foi derrotado!")

class Inimigo:
    def __init__(self, nome, hp, ataque, defesa):
        self.nome = nome
        self.hp = hp
        self.ataque = ataque
        self.defesa = defesa

    def atacar(self, jogador):
        dano = self.ataque
        jogador.receber_dano(dano)
        print(f"O {self.nome} ataca você causando {dano} de dano.")

    def esta_vivo(self):
        return self.hp > 0

class Lobo(Inimigo):
    def __init__(self):
        super().__init__("Lobo", 50, 12, 3)

class Orc(Inimigo):
    def __init__(self):
        super().__init__("Orc", 70, 15, 5)

class Bandido(Inimigo):
    def __init__(self):
        super().__init__("Bandido", 60, 13, 4)

class Naga(Inimigo):
    def __init__(self):
        super().__init__("Naga", 80, 18, 6)

class ChefeCaverna(Inimigo):
    def __init__(self):
        super().__init__("Chefe da Caverna", 150, 20, 8)

class ChefePantano(Inimigo):
    def __init__(self):
        super().__init__("Chefe do Pântano", 200, 25, 10)

class Arma:
    def __init__(self, nome, descricao, dano_bonus, preco):
        self.nome = nome
        self.descricao = descricao
        self.dano_bonus = dano_bonus
        self.preco = preco

    def mostrar_detalhes(self):
        print(f"{self.nome} - Dano Bônus: {self.dano_bonus} - Preço: {self.preco} de ouro")

class Loja:
    def __init__(self):
        self.armas_disponiveis = [
            Arma("Espada de Ferro", "Uma espada afiada feita de ferro.", 10, 30),
            Arma("Machado de Batalha", "Um machado grande e pesado.", 15, 40),
            Arma("Arco Longo", "Um arco longo de madeira de qualidade.", 12, 35)
        ]

    def mostrar_armas_disponiveis(self):
        print("Armas disponíveis:")
        for i, arma in enumerate(self.armas_disponiveis, 1):
            arma.mostrar_detalhes()

    def comprar_arma(self, jogador, escolha):
        try:
            escolha = int(escolha)
            if 1 <= escolha <= len(self.armas_disponiveis):
                arma_escolhida = self.armas_disponiveis[escolha - 1]
                if jogador.inventario["ouro"] >= arma_escolhida.preco:
                    jogador.inventario["armas"].append(arma_escolhida)
                    jogador.inventario["ouro"] -= arma_escolhida.preco
                    print(f"Você comprou a {arma_escolhida.nome}!")
                else:
                    print("Você não tem ouro suficiente!")
            else:
                print("Escolha inválida!")
        except ValueError:
            print("Escolha inválida!")

class InteracaoObjeto:
    def __init__(self, nome, descricao, acao):
        self.nome = nome
        self.descricao = descricao
        self.acao = acao

    def interagir(self):
        print(f"Você encontrou um(a) {self.nome}!")
        print(self.descricao)
        print(self.acao)

class InteracaoNPC:
    def __init__(self, nome, saudacao, oferta):
        self.nome = nome
        self.saudacao = saudacao
        self.oferta = oferta

    def interagir(self):
        print(f"{self.nome}: {self.saudacao}")
        print(self.oferta)

    def completar(self):
        print(f"{self.nome}: Muito bem, você completou minha missão!")

class Mapa:
    def __init__(self):
        self.terrenos = ["floresta", "caverna", "pântano", "deserto", "objeto", "NPC", "loja"]

    def explorar(self):
        terreno_atual = random.choice(self.terrenos)
        print(f"Você está explorando um {terreno_atual}...")
        return terreno_atual

def jogar_jogo():
    nome = input("Qual é o seu nome? ")
    classe = input("Escolha sua classe (Guerreiro/Mago): ")
    jogador = Jogador(nome, classe)

    mapa = Mapa()
    while jogador.esta_vivo():
        terreno_atual = mapa.explorar()
        if terreno_atual == "floresta":
            evento = random.randint(1, 4)
            if evento == 1:
                inimigo = Lobo()
            elif evento == 2:
                inimigo = Orc()
            elif evento == 3:
                inimigo = Bandido()
            else:
                inimigo = Naga()
            jogador.batalha(inimigo)
        elif terreno_atual == "caverna":
            inimigo_chefe = ChefeCaverna()
            print("Você entrou em uma caverna escura!")
            jogador.batalha(inimigo_chefe)
            if jogador.esta_vivo():
                print("Você encontrou uma poção de ataque!")
                jogador.inventario["poção_ataque"] += 1
        elif terreno_atual == "pântano":
            npc_missao = InteracaoNPC("Alquimista", "Olá viajante! Posso te ajudar a derrotar o chefe do pântano.", "Complete minha missão e te recompensarei!")
            npc_missao.interagir()
            resposta = input("Deseja aceitar a missão? (sim/não): ")
            if resposta.lower() == "sim":
                print("Você aceitou a missão do pântano!")
                jogador.batalha(ChefePantano())
                if jogador.esta_vivo():
                    npc_missao.completar()
                    nova_arma = Arma("Cajado de Magia", "Um cajado mágico que aumenta o poder mágico.", 8, 0)
                    jogador.inventario["armas"].append(nova_arma)
                    print("Missão do pântano completa!")
        elif terreno_atual == "deserto":
            print("Você está atravessando um deserto escaldante!")
            evento = random.randint(1, 5)
            if evento == 1:
                print("Você encontrou uma caravana e comprou uma poção de cura!")
                jogador.inventario["poção_curar"] += 1
            elif evento == 2:
                print("Você se perdeu e acabou desidratado!")
                jogador.receber_dano(15)
            elif evento == 3:
                print("Você encontrou um oásis e recuperou sua energia!")
                jogador.curar()
            else:
                print("Você foi atacado por bandidos!")
                inimigo = Bandido()
                jogador.batalha(inimigo)
        elif terreno_atual == "objeto":
            objeto = InteracaoObjeto("Cofre", "Um cofre antigo, pode conter tesouros.", "Ao abrir, pode encontrar ouro ou uma arma.")
            objeto.interagir()
            resposta = input("Deseja abrir o cofre? (sim/não): ")
            if resposta.lower() == "sim":
                evento = random.randint(1, 2)
                if evento == 1:
                    jogador.inventario["ouro"] += random.randint(20, 50)
                    print("Você encontrou ouro dentro do cofre!")
                else:
                    nova_arma = Arma("Adaga Envenenada", "Uma adaga afiada com veneno aplicado.", 12, 0)
                    jogador.inventario["armas"].append(nova_arma)
                    print("Você encontrou uma arma dentro do cofre!")
        elif terreno_atual == "NPC":
            npc = InteracaoNPC("Comerciante", "Bem-vindo, aventureiro! Tenho ótimas ofertas para você.", "Veja o que tenho para vender:")
            npc.interagir()
            resposta = input("Deseja comprar algo? (sim/não): ")
            if resposta.lower() == "sim":
                loja = Loja()
                loja.mostrar_armas_disponiveis()
                escolha = input("Escolha o número da arma que deseja comprar ou 'cancelar' para sair: ")
                if escolha.lower() != "cancelar":
                    loja.comprar_arma(jogador, escolha)
        elif terreno_atual == "loja":
            loja = Loja()
            loja.mostrar_armas_disponiveis()
            escolha = input("Escolha o número da arma que deseja comprar ou 'cancelar' para sair: ")
            if escolha.lower() != "cancelar":
                loja.comprar_arma(jogador, escolha)

def main():
    jogar_jogo()

if __name__ == "__main__":
    main()
