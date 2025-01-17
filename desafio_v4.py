import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
	def __init__(self, endereco):
		self.endereco = endereco
		self.contas = []

	def realizar_transacao(self, conta, transacao):
		transacao.registrar(conta)

	def adicionar_conta(self, conta):
		self.contas.append(conta)

class PessoaFisica(Cliente):
	def __init__(self, endereco, cpf, nome, data_nascimento):
		super().__init__(endereco)
		self.cpf = cpf
		self.nome = nome
		self.data_nascimento = data_nascimento

class Conta:
	def __init__(self, numero, cliente):
		self._saldo = 0
		self._numero = numero
		self._agencia = "0001"
		self._cliente = cliente
		self._historico = Historico()

	@classmethod
	def nova_conta(cls, cliente, numero):
		return cls(numero, cliente)

	@property
	def saldo(self):
		return self._saldo

	@property
	def numero(self):
		return self._numero

	@property
	def agencia(self):
		return self._agencia

	@property
	def cliente(self):
		return self._cliente

	@property
	def historico(self):
		return self._historico

	def sacar(self, valor):
		saldo = self.saldo
		excedeu_saldo = valor > saldo

		if excedeu_saldo:
			print(f"Você não possui saldo suficiente para essa operação! Saldo disponível: R${self._saldo:.2f}")
		elif valor > 0:
			self._saldo -= valor
			print(f"Saque realizado com sucesso! Novo saldo: R${self._saldo:.2f}")
			return True
		else:
			print("Não foi possível realizar o saque. O valor informado é inválido.")

		return False

	def depositar(self, valor):
		if valor > 0:
			self._saldo += valor
			print(f"Depósito realizado com sucesso! Novo saldo: R${self._saldo:.2f}")
			return True
		else:
			print("Valor inválido. Por favor digite um valor maior que zero.")

		return False

class ContaCorrente(Conta):
	def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
		super().__init__(numero, cliente)
		self.limite = limite
		self.limite_saques = limite_saques

	def sacar(self, valor):
		numero_saques = len(
			[transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
		)

		excedeu_limite = valor > self.limite
		excedeu_saques = numero_saques > self.limite_saques

		if excedeu_limite:
			print(f"Valor máximo por saque excedido! Valor máximo permitido: R${self.limite:.2f}")
		elif excedeu_saques:
			print(f"Quantidade máxima de saques diários excedida! Saques permitidos por dia: {self.limite_saques}")
		else:
			return super().sacar(valor)

		return False

	def __str__(self):
		return f"""\
			Agência:\t{self.agencia}
			C/C:\t\t{self.numero}
			Titular:\t{self.cliente.nome}
		"""

class Historico:
	def __init__(self):
		self._transacoes = []

	@property
	def transacoes(self):
		return self._transacoes

	def adicionar_transacao(self, transacao):
		self._transacoes.append(
			{
				"tipo": transacao.__class__.__name__,
				"valor": transacao.valor,
				"data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
			}
		)

class Transacao(ABC):
	@property
	@abstractmethod
	def valor(self):
		pass

	@classmethod
	@abstractmethod
	def registrar(cls, conta):
		pass

class Saque(Transacao):
	def __init__(self, valor):
		self._valor = valor

	@property
	def valor(self):
		return self._valor

	def registrar(self, conta):
		sucesso_transacao = conta.sacar(self.valor)

		if sucesso_transacao:
			conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
	def __init__(self, valor):
		self._valor = valor

	@property
	def valor(self):
		return self._valor

	def registrar(self, conta):
		sucesso_transacao = conta.depositar(self.valor)

		if sucesso_transacao:
			conta.historico.adicionar_transacao(self)

def menu():
	menu_str = """
	============================================
				 Escolha uma opção:
	============================================

	[d]\tDepositar
	[s]\tSacar
	[e]\tExtrato
	[nc]\tNova conta
	[lc]\tListar contas
	[nu]\tNovo cliente
	[q]\tSair

	============================================
	=> """

	return input(textwrap.dedent(menu_str))

def filtrar_cliente(cpf, clientes):
	clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
	return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
	if not cliente.contas:
		print("\nO cliente informado não possui conta!")
		return

	# FIXME: não permite cliente escolher a conta
	return cliente.contas[0]

def executar_transacao(transacao, clientes):
	cpf = input("Informe o CPF do cliente: ")
	cliente = filtrar_cliente(cpf, clientes)

	if not cliente:
		print("\nCliente não encontrado!")
		return

	valor = float(input(f"Informe o valor do {'depósito' if isinstance(transacao, Deposito) else 'saque'}: "))
	transacao = Deposito(valor) if isinstance(transacao, Deposito) else Saque(valor)

	conta = recuperar_conta_cliente(cliente)
	if not conta:
		return

	cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
	cpf = input("Informe o CPF do cliente: ")
	cliente = filtrar_cliente(cpf, clientes)

	if not cliente:
		print("\nCliente não encontrado!")
		return

	conta = recuperar_conta_cliente(cliente)
	if not conta:
		return

	print("============================================")
	print("                  EXTRATO:")
	print("============================================")

	transacoes = conta.historico.transacoes

	extrato = ""
	if not transacoes:
		print("Não foram realizadas movimentações." if not extrato else extrato)
	else:
		for transacao in transacoes:
			extrato += f"\n{transacao['data']} - {transacao['tipo']} - {transacao['valor']:.2f}"

	print(extrato)
	print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
	print("============================================")

def criar_cliente(clientes):
	cpf = input("Informe o CPF (somente números): ")
	cliente = filtrar_cliente(cpf, clientes)

	if cliente:
		print("\nJá existe cliente com esse CPF!")
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

	cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

	clientes.append(cliente)

	print("Cliente criado com sucesso!")

def criar_conta(numero_conta, clientes, contas):
	cpf = input("Informe o CPF (somente números): ")
	cliente = filtrar_cliente(cpf, clientes)

	if not cliente:
		print("\nCliente não encontrado! Processo de criação de conta encerrado!")
		return

	conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
	contas.append(conta)
	cliente.contas.append(conta)

	print("Conta criada com sucesso!")

def listar_contas(contas):
	for conta in contas:
		print("=" * 100)
		print(textwrap.dedent(str(conta)))

def main():
	clientes = []
	contas = []

	while True:
		opcao = menu()

		if opcao == "d":
			executar_transacao(transacao=Deposito(0), clientes=clientes)

		elif opcao == "s":
			executar_transacao(transacao=Saque(0), clientes=clientes)

		elif opcao == "e":
			exibir_extrato(clientes)

		elif opcao == "nu":
			criar_cliente(clientes)

		elif opcao == "nc":
			numero_conta = len(contas) + 1
			criar_conta(numero_conta, clientes, contas)

		elif opcao == "lc":
			listar_contas(contas)

		elif opcao == "q":
			break

		else:
			print("Operação inválida, por favor selecione novamente a operação desejada.")

main()