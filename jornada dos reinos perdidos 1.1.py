import random

class Jogador:
    def __init__(self, nome, classe):
        self.nome = nome
        self.classe = classe
        self.nivel = 1
        self.experiencia = 0
        self.vida_maxima = 100
        self.vida_atual = self.vida_maxima
        self.dano_base = 10
        self.defesa = 5
        self.inventario = {"poção_curar": 3, "poção_ataque": 1, "armadura": 0, "arma": 0}
        self.ouro = 0

    def atacar(self):
        return random.randint(self.dano_base // 2, self.dano_base)

    def receber_dano(self, dano):
        dano -= self.defesa
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
            self.dano_base *= 1.5
            self.inventario["poção_ataque"] -= 1
            print(f"{self.nome} usou uma poção de ataque.")
        else:
            print("Você não tem poções de ataque suficientes.")

    def equipar_armadura(self):
        if self.inventario["armadura"] > 0:
            self.defesa += 5
            self.inventario["armadura"] -= 1
            print(f"{self.nome} equipou uma armadura.")
        else:
            print("Você não tem armaduras suficientes.")

    def equipar_arma(self):
        if self.inventario["arma"] > 0:
            self.dano_base += 5
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

    def mercado(self):
        print("Bem-vindo ao mercado!")
        print("O que você gostaria de comprar?")
        while True:
            print("1. Poção de cura - 10 de ouro")
            print("2. Poção de ataque - 15 de ouro")
            print("3. Sair")
            escolha = input("Escolha uma opção: ")
            if escolha == "1":
                if self.ouro >= 10:
                    self.ouro -= 10
                    self.inventario["poção_curar"] += 1
                    print("Você comprou uma poção de cura.")
                else:
                    print("Você não tem ouro suficiente para comprar uma poção de cura.")
            elif escolha == "2":
                if self.ouro >= 15:
                    self.ouro -= 15
                    self.inventario["poção_ataque"] += 1
                    print("Você comprou uma poção de ataque.")
                else:
                    print("Você não tem ouro suficiente para comprar uma poção de ataque.")
            elif escolha == "3":
                print("Obrigado por sua visita!")
                break
            else:
                print("Escolha inválida. Tente novamente.")

    def batalha(self, inimigo):
        print(f"{self.nome} enfrenta {inimigo.nome}!")
        while self.esta_vivo() and inimigo.esta_vivo():
            print(f"{self.nome} (Vida: {self.vida_atual}) vs {inimigo.nome} (Vida: {inimigo.vida})")
            escolha = input("O que você deseja fazer? (atacar/usar poção/equipar armadura/equipar arma/fugir): ")
            if escolha.lower() == "atacar":
                jogador_dano = self.atacar()
                inimigo.receber_dano(jogador_dano)
                print(f"{self.nome} ataca {inimigo.nome} causando {jogador_dano} de dano.")
            elif escolha.lower() == "usar poção":
                self.usar_pocao_curar()
            elif escolha.lower() == "usar poção de ataque":
                self.usar_pocao_ataque()
            elif escolha.lower() == "equipar armadura":
                self.equipar_armadura()
            elif escolha.lower() == "equipar arma":
                self.equipar_arma()
            elif escolha.lower() == "fugir":
                print("Você fugiu da batalha!")
                return False
            elif escolha.lower() == "abrir inventário":
                self.abrir_inventario()
            else:
                print("Escolha inválida. Tente novamente.")
                continue

            if not inimigo.esta_vivo():
                print(f"{inimigo.nome} foi derrotado!")
                return True

            inimigo_dano = inimigo.atacar()
            self.receber_dano(inimigo_dano)
            print(f"{inimigo.nome} ataca {self.nome} causando {inimigo_dano} de dano.")
            if not self.esta_vivo():
                print(f"{self.nome} foi derrotado!")
                return False


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
        super().__init__("Lobo", 30, 10)

class Orc(Inimigo):
    def __init__(self):
        super().__init__("Orc", 40, 15)

class Esqueleto(Inimigo):
    def __init__(self):
        super().__init__("Esqueleto", 25, 8)

class AranhaGigante(Inimigo):
    def __init__(self):
        super().__init__("Aranha Gigante", 35, 12)

class Piranha(Inimigo):
    def __init__(self):
        super().__init__("Piranha", 20, 10)

class Crocodilo(Inimigo):
    def __init__(self):
        super().__init__("Crocodilo", 45, 20)

class ElementalFogo(Inimigo):
    def __init__(self):
        super().__init__("Elemental de Fogo", 50, 25)

class Escorpiao(Inimigo):
    def __init__(self):
        super().__init__("Escorpião", 30, 18)

class Naga(Inimigo):
    def __init__(self):
        super().__init__("Naga", 60, 30)

class NPC:
    def __init__(self, nome, frase_inicial):
        self.nome = nome
        self.frase_inicial = frase_inicial

    def interagir(self):
        print(f"{self.nome}: {self.frase_inicial}")

class Objeto:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def pegar(self):
        print(f"Você pegou o objeto: {self.nome}")

    def usar(self):
        print(f"Você usou o objeto: {self.nome}")

class PoçãoCura(Objeto):
    def __init__(self):
        super().__init__("Poção de Cura", "Recupera 20 pontos de vida")

    def usar(self, jogador):
        jogador.vida_atual += 20
        if jogador.vida_atual > jogador.vida_maxima:
            jogador.vida_atual = jogador.vida_maxima
        print("Você usou uma Poção de Cura e recuperou 20 pontos de vida.")

class PoçãoAtaque(Objeto):
    def __init__(self):
        super().__init__("Poção de Ataque", "Aumenta o dano do próximo ataque em 50%")

    def usar(self, jogador):
        jogador.dano_base *= 1.5
        print("Você usou uma Poção de Ataque. Seu próximo ataque causará mais dano.")

class Armadura(Objeto):
    def __init__(self):
        super().__init__("Armadura", "Aumenta a defesa em 5 pontos")

    def usar(self, jogador):
        jogador.defesa += 5
        print("Você equipou uma Armadura. Sua defesa aumentou.")

class Arma(Objeto):
    def __init__(self):
        super().__init__("Arma", "Aumenta o dano base em 5 pontos")

    def usar(self, jogador):
        jogador.dano_base += 5
        print("Você equipou uma Arma. Seu dano base aumentou.")

class Tesouro(Objeto):
    def __init__(self):
        super().__init__("Tesouro", "Um baú cheio de riquezas")

    def pegar(self, jogador):
        jogador.ouro += 50
        print("Você encontrou um tesouro! Ganhou 50 peças de ouro.")

def explorar_mapa(jogador):
    derrotou_chefe = False
    while not derrotou_chefe:
        terrenos = ["floresta", "montanha", "rio", "caverna", "pântano", "deserto"]
        terreno_atual = random.choice(terrenos)
        print(f"Explorando {terreno_atual}...")
        if terreno_atual == "floresta":
            inimigo = random.choice([Lobo(), Esqueleto(), AranhaGigante()])
            if random.random() < 0.2:
                npc = NPC("Lenhador", "Olá, viajante! Tome cuidado com os lobos por aqui.")
                npc.interagir()
        elif terreno_atual == "montanha":
            inimigo = random.choice([Orc(), Esqueleto(), AranhaGigante()])
            if random.random() < 0.2:
                npc = NPC("Alpinista", "Ei! Você está escalando a montanha também?")
                npc.interagir()
        elif terreno_atual == "rio":
            inimigo = random.choice([Piranha(), Crocodilo(), Esqueleto()])
            if random.random() < 0.2:
                npc = NPC("Pescador", "Cuidado com os crocodilos! Eles são perigosos.")
                npc.interagir()
        elif terreno_atual == "caverna":
            inimigo = random.choice([ElementalFogo(), Escorpiao(), Naga()])
            derrotou_chefe = batalha_chefe(jogador)
            if not jogador.esta_vivo():
                break
        elif terreno_atual == "pântano":
            inimigo = random.choice([ElementalFogo(), Naga(), Orc()])
            derrotou_chefe = batalha_chefe(jogador)
            if not jogador.esta_vivo():
                break
        elif terreno_atual == "deserto":
            inimigo = random.choice([Orc(), Escorpiao(), Crocodilo()])
            derrotou_chefe = batalha_chefe(jogador)
            if not jogador.esta_vivo():
                break

        if batalha(jogador, inimigo):
            jogador.ouro += 10
            print(f"Você ganhou 10 peças de ouro pela vitória!")
            jogador.experiencia += 30
            print(f"Você ganhou 30 pontos de experiência!")
            if jogador.experiencia >= 120:
                jogador.experiencia -= 120
                jogador.vida_maxima += 10
                jogador.vida_atual += 10
                print("Você ganhou 10 pontos de vida!")

        escolha = input("Deseja continuar explorando? (s/n): ")
        if escolha.lower() != "s":
            break

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
        elif escolha.lower() == "usar poção de ataque":
            jogador.usar_pocao_ataque()
        elif escolha.lower() == "equipar armadura":
            jogador.equipar_armadura()
        elif escolha.lower() == "equipar arma":
            jogador.equipar_arma()
        elif escolha.lower() == "fugir":
            print("Você fugiu da batalha!")
            return False
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

def batalha_chefe(jogador):
    chefe = Chefe("Dragão", 100, 30, 5)
    print(f"{jogador.nome} enfrenta o chefe final: {chefe.nome}!")
    while jogador.esta_vivo() and chefe.esta_vivo():
        print(f"{jogador.nome} (Vida: {jogador.vida_atual}) vs {chefe.nome} (Vida: {chefe.vida})")
        escolha = input("O que você deseja fazer? (atacar/usar poção/equipar armadura/equipar arma/fugir): ")
        if escolha.lower() == "atacar":
            jogador_dano = jogador.atacar()
            chefe.receber_dano(jogador_dano)
            print(f"{jogador.nome} ataca {chefe.nome} causando {jogador_dano} de dano.")
        elif escolha.lower() == "usar poção":
            jogador.usar_pocao_curar()
        elif escolha.lower() == "usar poção de ataque":
            jogador.usar_pocao_ataque()
        elif escolha.lower() == "equipar armadura":
            jogador.equipar_armadura()
        elif escolha.lower() == "equipar arma":
            jogador.equipar_arma()
        elif escolha.lower() == "fugir":
            print("Você não pode fugir do chefe final!")
            continue
        elif escolha.lower() == "abrir inventário":
            jogador.abrir_inventario()
        else:
            print("Escolha inválida. Tente novamente.")
            continue

        if not chefe.esta_vivo():
            print(f"{chefe.nome} foi derrotado!")
            return True

        chefe_dano = chefe.atacar()
        jogador.receber_dano(chefe_dano)
        print(f"{chefe.nome} ataca {jogador.nome} causando {chefe_dano} de dano.")
        if not jogador.esta_vivo():
            print(f"{jogador.nome} foi derrotado pelo chefe final!")
            return False

jogador = Jogador("Herói", "Guerreiro")
print("Bem-vindo ao jogo de aventura!")
print("Você acorda em uma terra desconhecida...")
print("Você se encontra diante de um caminho, o que deseja fazer?")
while True:
    print("1. Explorar o mapa")
    print("2. Abrir inventário")
    print("3. Ir ao mercado")
    print("4. Sair do jogo")
    escolha = input("Escolha uma opção: ")
    if escolha == "1":
        explorar_mapa(jogador)
    elif escolha == "2":
        jogador.abrir_inventario()
    elif escolha == "3":
        jogador.mercado()
    elif escolha == "4":
        print("Obrigado por jogar!")
        break
    else:
        print("Escolha inválida. Tente novamente.")

def tutorial():
    print("Bem-vindo ao jogo!")
    print("Antes de começar, aqui estão os controles disponíveis:")
    print("- 'atacar': Ataca o inimigo atual.")
    print("- 'usar poção': Usa uma poção de cura para recuperar vida.")
    print("- 'equipar armadura': Equipa uma armadura para aumentar a defesa.")
    print("- 'equipar arma': Equipa uma arma para aumentar o dano.")
    print("- 'fugir': Foge da batalha atual.")
    print("- 'abrir inventário': Abre o inventário do jogador.")
    print("Agora você está pronto para começar sua aventura!")

def exibir_tutorial():
    tutorial()

def jogar_jogo():
    exibir_tutorial()
    nome = input("Digite o nome do seu herói: ")
    classe = input("Escolha a classe do seu herói (Guerreiro/Mago/Arqueiro): ")
    jogador = Jogador(nome, classe)

    while jogador.esta_vivo():
        explorar_mapa(jogador)
        if not jogador.esta_vivo():
            print("Game Over!")
            break

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
                jogador.batalha(inimigo)
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
                jogador.mercado()
            elif evento == 2:
                print("Você encontrou um mercador que vende armaduras!")
                jogador.inventario["armadura"] += 1
            elif evento == 3:
                print("Você encontrou um NPC com uma missão secundária!")
                npc_dica = DicaNPC("NPC de Dicas", "Eu conheço este lugar muito bem. Posso te dar uma dica útil.", "Tenha cuidado com as criaturas daqui.")
                npc_missao = MissaoNPC("NPC de Missão", "Meu animal de estimação fugiu para a floresta. Você poderia encontrá-lo?", "Uma poção de cura")
                npc_dica.interagir()
                npc_missao.interagir()
                resposta = input("Aceitar a missão? (sim/não): ")
                if resposta.lower() == "sim":
                    jogador.inventario["poção_curar"] += 1
            else:
                print("Você encontrou um ferreiro que vende armas!")
                jogador.inventario["arma"] += 1
        elif terreno_atual == "caverna":
            print("Você entrou em uma caverna escura!")
            inimigo = Orc()
            jogador.batalha(inimigo)
            if not jogador.esta_vivo():
                break
            else:
                print("Você encontrou um NPC com uma missão!")
                npc_dica = DicaNPC("NPC de Dicas", "Cuidado, um poderoso chefe está adormecido nas profundezas da caverna.", "Use uma poção de ataque para aumentar seu dano.")
                npc_missao = MissaoCaverna("NPC de Missão", "Derrote o chefe da caverna e será recompensado.", "Uma armadura")
                npc_dica.interagir()
                npc_missao.interagir()
                resposta = input("Aceitar a missão? (sim/não): ")
                if resposta.lower() == "sim":
                    inimigo_chefe = ChefeCaverna()
                    jogador.batalha(inimigo_chefe)
                    if jogador.esta_vivo():
                        npc_missao.completar_missao()
                        jogador.inventario["armadura"] += 1
                        print("Missão da caverna completa!")
        elif terreno_atual == "pantano":
            print("Você está navegando por um pântano lamacento!")
            inimigo = Piranha()
            jogador.batalha(inimigo)
            if not jogador.esta_vivo():
                break
            else:
                print("Você encontrou um NPC com uma missão!")
                npc_dica = DicaNPC("NPC de Dicas", "Cuidado, o chefe do pântano é muito perigoso.", "Prepare-se com poções antes de enfrentá-lo.")
                npc_missao = MissaoPantano("NPC de Missão", "Derrote o chefe do pântano e será recompensado.", "Uma arma")
                npc_dica.interagir()
                npc_missao.interagir()
                resposta = input("Aceitar a missão? (sim/não): ")
                if resposta.lower() == "sim":
                    inimigo_chefe = ChefePantano()
                    jogador.batalha(inimigo_chefe)
                    if jogador.esta_vivo():
                        npc_missao.completar_missao()
                        jogador.inventario["arma"] += 1
                        print("Missão do pântano completa!")
        elif terreno_atual == "deserto":
            print("Você está atravessando um deserto escaldante!")
            inimigo = Escorpiao()
            jogador.batalha(inimigo)
            if not jogador.esta_vivo():
                break
            else:
                print("Você encontrou um NPC com uma missão!")
                npc_dica = DicaNPC("NPC de Dicas", "Cuidado, o chefe do deserto é muito astuto.", "Aproveite as poções de cura para se manter saudável.")
                npc_missao = MissaoNPC("NPC de Missão", "Derrote o chefe do deserto e será recompensado.", "Uma poção de ataque")
                npc_dica.interagir()
                npc_missao.interagir()
                resposta = input("Aceitar a missão? (sim/não): ")
                if resposta.lower() == "sim":
                    inimigo_chefe = ChefeDeserto()
                    jogador.batalha(inimigo_chefe)
                    if jogador.esta_vivo():
                        npc_missao.completar_missao()
                        jogador.inventario["poção_ataque"] += 1
                        print("Missão do deserto completa!")
                        derrotou_chefe = True

jogar_jogo()