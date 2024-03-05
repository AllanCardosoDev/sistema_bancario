class SistemaBancario:
    def __init__(self):
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Operação falhou! O valor informado é inválido.")

    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.LIMITE_SAQUES

        if excedeu_saldo:
            print(f"Operação falhou! Você não tem saldo suficiente. Saldo atual: R$ {self.saldo:.2f}")
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite máximo de R$ 500.00.")
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque: R$ {valor:.2f}\n"
            self.numero_saques += 1
            print(f"Ainda é possível sacar {self.LIMITE_SAQUES - self.numero_saques} vez(es).\n")
        else:
            print("Operação falhou! O valor informado é inválido.")

    def mostrar_extrato(self):
        print("\n---------------- Extrato ----------------")
        print("Não foram realizados movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("-----------------------------------------\n")


def main():
    sistema = SistemaBancario()
    while True:
        print('-------------------------------------------')
        print('Sistema Bancário Simplificado')
        print('1 - Depositar')
        print('2 - Sacar')
        print('3 - Extrato')
        print('4 - Sair')
        opcao = input('Escolha uma opção: ')
        if opcao == '1':
            valor = float(input('Insira o valor a ser depositado: R$ '))
            sistema.depositar(valor)
        elif opcao == '2':
            valor = float(input('Insira o valor a ser sacado: R$ '))
            sistema.sacar(valor)
        elif opcao == '3':
            sistema.mostrar_extrato()
        elif opcao == '4':
            print('Obrigado por utilizar os nossos serviços.')
            break
        else:
            print('Opção inválida. Por favor, insira uma opção de 1 a 4.\n')


if __name__ == '__main__':
    main()
