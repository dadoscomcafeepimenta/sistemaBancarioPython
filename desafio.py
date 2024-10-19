from datetime import datetime

menu = """
============================================
             Escolha uma opção:
============================================

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

============================================
=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Digite o valor a ser depositado: ").replace(",", "."))

        if valor > 0:
            saldo += valor
            extrato += f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - Depósito: R${valor:.2f}\n"
            print(f"Depósito realizado com sucesso! Novo saldo: R${saldo:.2f}")

        else:
            print("Valor inválido. Por favor digite um valor maior que zero.")

    elif opcao == "s":

        print("Regras para efetuar o saque:\n")

        print(f"1 - Quantidade máxima de saques diários: {LIMITE_SAQUES}. Quantidade de saques efetuada: {numero_saques}")
        print(f"2 - Valor máximo permitido por saque: R${limite:.2f}")
        print(f"3 - O valor do saque não pode exceder o saldo disponível: R${saldo:.2f}")
        print(f"4 - O valor do saque não pode ser negativo!\n")

        valor = float(input("Digite o valor a ser sacado: ").replace(",", "."))

        if numero_saques >= LIMITE_SAQUES:
            print(f"Quantidade máxima de saques diários excedida! Saques permitidos por dia: {LIMITE_SAQUES}")

        elif valor > limite:
            print(f"Valor máximo por saque excedido! Valor máximo permitido: R${limite:.2f}")

        elif valor > saldo:
            print(f"Você não possui saldo suficiente para essa operação! Saldo disponível: R${saldo:.2f}")

        elif valor > 0:
            saldo -= valor
            extrato += f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - Saque: R${valor:.2f}\n"
            numero_saques += 1
            print(f"Saque realizado com sucesso! Novo saldo: R${saldo:.2f}")

        else:
            print("Não foi possível realizar o saque. O valor informado é inválido.")

    elif opcao == "e":

        print("============================================")
        print("                  EXTRATO:")
        print("============================================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo atual: R$ {saldo:.2f}")
        print("============================================")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")