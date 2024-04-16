import random

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
        self.experiencia = 0
        self.proximo_nivel = 100

    def ganhar_experiencia(self, pontos):
        self.experiencia += pontos
        print(f"Você ganhou {pontos} pontos de experiência!")
        if self.experiencia >= self.proximo_nivel:
            self.nivel += 1
            self.proximo_nivel *= 2
            self.vida_maxima += 20
            self.vida_atual = self.vida_maxima
            print(f"Parabéns, você avançou para o nível {self.nivel}!")
            print(f"Sua vida máxima aumentou para {self.vida_maxima}.")

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
                self.ganhar_experiencia(inimigo.experiencia)
                return True

            inimigo_dano = inimigo.atacar()
            self.receber_dano(inimigo_dano)
            print(f"{inimigo.nome} ataca {self.nome} causando {inimigo_dano} de dano.")
            if not self.esta_vivo():
                print(f"{self.nome} foi derrotado!")
                return False

class Inimigo:
    def __init__(self, nome, vida, dano, experiencia):
        self.nome = nome
        self.vida = vida
        self.dano = dano
        self.experiencia = experiencia

    def atacar(self):
        return random.randint(self.dano // 2, self.dano)

    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0

    def esta_vivo(self):
        return self.vida > 0

class Chefe(Inimigo):
    def __init__(self, nome, vida, dano, experiencia):
        super().__init__(nome, vida, dano, experiencia)

class Lobo(Inimigo):
    def __init__(self):
        super().__init__("Lobo", 30, 8, 20)

class Orc(Inimigo):
    def __init__(self):
        super().__init__("Orc", 40, 10, 30)

class Esqueleto(Inimigo):
    def __init__(self):
        super().__init__("Esqueleto", 25, 6, 15)

class AranhaGigante(Inimigo):
    def __init__(self):
        super().__init__("Aranha Gigante", 35, 12, 25)

class ElementalFogo(Inimigo):
    def __init__(self):
        super().__init__("Elemental de Fogo", 50, 15, 40)

class Piranha(Inimigo):
    def __init__(self):
        super().__init__("Piranha", 20, 8, 10)

class Crocodilo(Inimigo):
    def __init__(self):
        super().__init__("Crocodilo", 45, 12, 35)

class Naga(Inimigo):
    def __init__(self):
        super().__init__("Naga", 60, 18, 50)

class Escorpiao(Inimigo):
    def __init__(self):
        super().__init__("Escorpião", 35, 12, 30)

class ChefeCaverna(Chefe):
    def __init__(self):
        super().__init__("Guerreiro da Caverna", 80, 20, 100)

class ChefePantano(Chefe):
    def __init__(self):
        super().__init__("Senhor do Pântano", 100, 25, 150)

class ChefeDeserto(Chefe):
    def __init__(self):
        super().__init__("Rei do Deserto", 120, 30, 200)

class DicaNPC:
    def __init__(self, nome, frase_inicial, dica):
        self.nome = nome
        self.frase_inicial = frase_inicial
        self.dica = dica

    def interagir(self):
        print(f"{self.nome}: {self.frase_inicial}")
        print(f"{self.nome}: Dica: {self.dica}")

class MissaoNPC:
    def __init__(self, nome, frase_inicial, recompensa):
        self.nome = nome
        self.frase_inicial = frase_inicial
        self.recompensa = recompensa
        self.completa = False

    def interagir(self):
        print(f"{self.nome}: {self.frase_inicial}")
        if not self.completa:
            print("Missão: Encontre o animal de estimação do NPC.")
        else:
            print(f"Missão: Obrigado por encontrar meu animal! Aqui está sua recompensa: {self.recompensa}")

class MissaoCaverna(MissaoNPC):
    def verificar_missao(self):
        if not self.completa:
            print("Missão: Derrote o chefe da caverna.")
        else:
            print("Missão: Missão da caverna completa.")

    def completar_missao(self):
        self.completa = True

class MissaoPantano(MissaoNPC):
    def verificar_progresso(self):
        if not self.completa:
            print("Missão: Derrote o chefe do pântano.")
        else:
            print("Missão: Missão do pântano completa.")

    def completar_missao(self):
        self.completa = True

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
    print(f"Bem-vindo, {jogador.nome} o {jogador.classe}!")
    print("Sua aventura começa agora...")
    caverna = MissaoCaverna("Mago sábio", "Olá, jovem aventureiro!", "100 moedas de ouro")
    pantano = MissaoPantano("Druida", "Saudações, viajante!", "200 moedas de ouro")
    while True:
        inimigo = random.choice([Lobo(), Orc(), Esqueleto(), AranhaGigante(), ElementalFogo(), Piranha(), Crocodilo(), Naga(), Escorpiao()])
        resultado = jogador.batalha(inimigo)
        if not resultado:
            print("Fim de jogo! Você foi derrotado...")
            break
        if jogador.nivel == 5 and not caverna.completa:
            caverna.interagir()
            caverna.verificar_missao()
            escolha = input("Deseja completar a missão? (sim/não): ")
            if escolha.lower() == "sim":
                caverna.completar_missao()
                print("Missão completa!")
                jogador.ouro += 100
                print(f"Você recebeu 100 moedas de ouro como recompensa!")
            else:
                print("Missão não completa!")
        if jogador.nivel == 10 and not pantano.completa:
            pantano.interagir()
            pantano.verificar_progresso()
            escolha = input("Deseja completar a missão? (sim/não): ")
            if escolha.lower() == "sim":
                pantano.completar_missao()
                print("Missão completa!")
                jogador.ouro += 200
                print(f"Você recebeu 200 moedas de ouro como recompensa!")
            else:
                print("Missão não completa!")
        if not jogador.esta_vivo():
            print("Fim de jogo! Você foi derrotado...")
            break
        if jogador.nivel == 15:
            print("Parabéns! Você venceu todos os desafios e completou o jogo!")
            break

jogar_jogo()
