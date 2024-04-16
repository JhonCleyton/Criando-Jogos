import random

def jogar_jogo():
    numero_secreto = random.randint(1, 100)
    tentativas = 0
    max_tentativas = 10

    print("Bem-vindo ao jogo de adivinhação!")
    print("Tente adivinhar o número secreto entre 1 e 100.")

    while tentativas < max_tentativas:
        tentativa = int(input("Digite um número: "))
        tentativas += 1

        if tentativa < numero_secreto:
            print("Tente um número maior.")
        elif tentativa > numero_secreto:
            print("Tente um número menor.")
        else:
            print(f"Parabéns! Você acertou o número secreto ({numero_secreto}) em {tentativas} tentativas!")
            break
    else:
        print(f"Você excedeu o número máximo de tentativas. O número secreto era {numero_secreto}.")

    jogar_novamente = input("Deseja jogar novamente? (s/n): ")
    if jogar_novamente.lower() == 's':
        jogar_jogo()
    else:
        print("Obrigado por jogar!")

if __name__ == "__main__":
    jogar_jogo()