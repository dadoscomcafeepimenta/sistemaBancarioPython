from abc import ABC
from datetime import datetime


class Cliente:
	def __init__(self, endereco):
		self.endereco = endereco
		self.contas = []

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
	def valor(self):
		pass

	@classmethod
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