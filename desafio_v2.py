from datetime import datetime
import textwrap

def menu():
    menu = """
    ============================================
                 Escolha uma opção:
    ============================================

    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair

    ============================================
    => """

    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, quantidade_transacoes, /):
    if valor > 0:
        saldo += valor
        extrato += f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - Depósito: R${valor:.2f}\n"
        print(f"Depósito realizado com sucesso! Novo saldo: R${saldo:.2f}")
    else:
        print("Valor inválido. Por favor digite um valor maior que zero.")

    quantidade_transacoes += 1

    return saldo, extrato, quantidade_transacoes

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques, quantidade_transacoes):
    if numero_saques >= limite_saques:
        print(f"Quantidade máxima de saques diários excedida! Saques permitidos por dia: {limite_saques}")
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

    quantidade_transacoes += 1

    return saldo, extrato, quantidade_transacoes

def exibir_extrato(saldo, /, *, extrato):
    print("============================================")
    print("                  EXTRATO:")
    print("============================================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("============================================")

def filtrar_usuario(cpf, usuarios):
    usuario_filtrado = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuario_filtrado[0] if usuario_filtrado else None

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")

    print("Informe a seguir os dados do endereço:")
    logradouro = input("Logradouro: ")
    numero = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Sigla do estado: ")
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("Usuário não encontrado! Processo de criação de conta encerrado!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
            """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    AGENCIA = "0001"
    LIMITE_TRANSACOES = 10
    LIMITE_SAQUES = 3

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    quantidade_transacoes = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            if quantidade_transacoes <= LIMITE_TRANSACOES:
                valor = float(input("Digite o valor a ser depositado: ").replace(",", "."))
                saldo, extrato, quantidade_transacoes = depositar(saldo, valor, extrato, quantidade_transacoes)
            else:
                print(f"Limite diário de transações excedido! Quantidade de transações (depósitos e saques) efetuada: {quantidade_transacoes}")

        elif opcao == "s":
            if quantidade_transacoes <= LIMITE_TRANSACOES:
                print("Regras para efetuar o saque:\n")

                print(f"1 - Quantidade máxima de saques diários: {LIMITE_SAQUES}. Quantidade de saques efetuada: {numero_saques}")
                print(f"2 - Valor máximo permitido por saque: R${limite:.2f}")
                print(f"3 - O valor do saque não pode exceder o saldo disponível: R${saldo:.2f}")
                print(f"4 - O valor do saque não pode ser negativo!")
                print(f"5 - Não exceder o limite de {LIMITE_TRANSACOES} transações diárias. Quantidade de transações (depósitos e saques) efetuada: {quantidade_transacoes}\n")

                valor = float(input("Digite o valor a ser sacado: ").replace(",", "."))

                saldo, extrato, quantidade_transacoes = sacar(
                    saldo = saldo,
                    valor = valor,
                    extrato = extrato,
                    limite = limite,
                    numero_saques = numero_saques,
                    limite_saques = LIMITE_SAQUES,
                    quantidade_transacoes = quantidade_transacoes
                )
            else:
                print(f"Limite diário de transações excedido! Quantidade de transações (depósitos e saques) efetuada: {quantidade_transacoes}")

        elif opcao == "e":
            exibir_extrato(saldo, extrato = extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()