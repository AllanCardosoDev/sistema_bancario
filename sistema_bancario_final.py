import textwrap
from abc import ABC, abstractmethod
from datetime import date

# ========================= Classe Transacao (Interface) =========================
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

# ========================= Classes de Transações (Depósito e Saque) =========================
class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta.saldo += self.valor
            conta.historico.adicionar_transacao(f"Depósito: R$ {self.valor:.2f}")
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > conta.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif self.valor > conta.limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif conta.numero_saques >= conta.limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif self.valor > 0:
            conta.saldo -= self.valor
            conta.numero_saques += 1
            conta.historico.adicionar_transacao(f"Saque: R$ {self.valor:.2f}")
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

# ========================= Classe Historico =========================
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def exibir(self):
        print("\n================ EXTRATO ================")
        if not self.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in self.transacoes:
                print(transacao)
        print("==========================================")

# ========================= Classe Cliente =========================
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# ========================= Classe PessoaFisica (Herança de Cliente) =========================
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

# ========================= Classe Conta =========================
class Conta:
    def __init__(self, numero, agencia, cliente):
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.saldo = 0.0
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    def nova_conta(cls, cliente, numero):
        return cls(numero=numero, agencia="0001", cliente=cliente)

# ========================= Classe ContaCorrente (Herança de Conta) =========================
class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite=500, limite_saques=3):
        super().__init__(numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        saque = Saque(valor)
        saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        deposito.registrar(self)

# ========================= Classe SistemaBancario =========================
class SistemaBancario:
    def __init__(self):
        self.usuarios = []
        self.contas = []

    def menu(self):
        menu = """\n
        ==============================   MENU  ============================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nu]\tNovo Usuário
        [nc]\tNova Conta
        [lc]\tListar Contas
        [q]\tSair
        ===================================================================
        Comando => """
        return input(textwrap.dedent(menu))

    def criar_usuario(self):
        cpf = input("Informe o CPF (somente números): ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        usuario = PessoaFisica(cpf, nome, data_nascimento, endereco)
        self.usuarios.append(usuario)
        print("\n=== Usuário criado com sucesso! ===")

    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            numero_conta = len(self.contas) + 1
            conta = ContaCorrente(numero_conta, "0001", usuario)
            usuario.adicionar_conta(conta)
            self.contas.append(conta)
            print("\n=== Conta criada com sucesso! ===")
        else:
            print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

    def listar_contas(self):
        for conta in self.contas:
            print(f"\nAgência: {conta.agencia} | C/C: {conta.numero} | Titular: {conta.cliente.nome}")

    def filtrar_usuario(self, cpf):
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

# ========================= Função Principal =========================
def main():
    sistema = SistemaBancario()

    while True:
        opcao = sistema.menu()

        if opcao == "d":
            cpf = input("Informe o CPF do titular: ")
            usuario = sistema.filtrar_usuario(cpf)
            if usuario and usuario.contas:
                conta = usuario.contas[0]
                valor = float(input("Informe o valor do depósito: "))
                conta.depositar(valor)
            else:
                print("\n@@@ Conta não encontrada. @@@")

        elif opcao == "s":
            cpf = input("Informe o CPF do titular: ")
            usuario = sistema.filtrar_usuario(cpf)
            if usuario and usuario.contas:
                conta = usuario.contas[0]
                valor = float(input("Informe o valor do saque: "))
                conta.sacar(valor)
            else:
                print("\n@@@ Conta não encontrada. @@@")

        elif opcao == "e":
            cpf = input("Informe o CPF do titular: ")
            usuario = sistema.filtrar_usuario(cpf)
            if usuario and usuario.contas:
                conta = usuario.contas[0]
                conta.historico.exibir()
            else:
                print("\n@@@ Conta não encontrada. @@@")

        elif opcao == "nu":
            sistema.criar_usuario()

        elif opcao == "nc":
            sistema.criar_conta()

        elif opcao == "lc":
            sistema.listar_contas()

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida. @@@")

if __name__ == "__main__":
    main()
