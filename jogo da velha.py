def imprimir_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print("|".join(linha))
        print("-" * 5)

def verificar_vitoria(tabuleiro, jogador):
    # Verificar linhas e colunas
    for i in range(3):
        if tabuleiro[i][0] == tabuleiro[i][1] == tabuleiro[i][2] == jogador or \
           tabuleiro[0][i] == tabuleiro[1][i] == tabuleiro[2][i] == jogador:
            return True

    # Verificar diagonais
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] == jogador or \
       tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] == jogador:
        return True

    return False

def jogar_jogo():
    tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
    jogador_atual = "X"

    print("Bem-vindo ao Jogo da Velha!")
    imprimir_tabuleiro(tabuleiro)

    for rodada in range(9):
        print(f"Rodada {rodada + 1}: Vez do jogador {jogador_atual}")
        linha = int(input("Escolha a linha (0, 1, 2): "))
        coluna = int(input("Escolha a coluna (0, 1, 2): "))

        if tabuleiro[linha][coluna] != " ":
            print("Essa posição já está ocupada. Tente novamente.")
            continue

        tabuleiro[linha][coluna] = jogador_atual
        imprimir_tabuleiro(tabuleiro)

        if verificar_vitoria(tabuleiro, jogador_atual):
            print(f"Parabéns! O jogador {jogador_atual} venceu!")
            break

        jogador_atual = "O" if jogador_atual == "X" else "X"
    else:
        print("Empate!")

    jogar_novamente = input("Deseja jogar novamente? (s/n): ")
    if jogar_novamente.lower() == 's':
        jogar_jogo()
    else:
        print("Obrigado por jogar!")

if __name__ == "__main__":
    jogar_jogo()