import textwrap

class SistemaBancario:
    def __init__(self):
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3
        self.usuarios = []
        self.contas = []
        self.AGENCIA = '0001'

    def menu(self):
        menu = """\n
        ==============================   MENU  ============================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [q]\tSair
        [nu]\tNovo Usuario
        [nc]\tNova Conta
        [lc]\tLista de contas
        ===================================================================
        Comando => """
        return input(textwrap.dedent(menu))
        
    def deposito(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f'Deposito:\tR$ {valor:.2f}\n'
            print('\nDepósito realizado com sucesso!')
        else:
            print('\nOperação falhou! O valor informado é inválido.')
        
    def saque(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.LIMITE_SAQUES

        if excedeu_saldo:
            print('\nOperação falhou! Você não tem saldo suficiente.')
        elif excedeu_limite:
            print('\nOperação falhou! O valor do saque excede o limite máximo de R$ 500.00.')
        elif excedeu_saques:
            print('\nOperação falhou! Número máximo de saques excedido.')
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f'Saque:\t\tR$ {valor:.2f}\n'
            self.numero_saques += 1
            print('Saque realizado com sucesso!')
        else:
            print('\nOperação falhou! O valor informado é inválido.')

    def imprimir_extrato(self):
        print("============================== EXTRATO ==============================")
        print("Não foram realizadas movimentações na conta." if not self.extrato else self.extrato)
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("=====================================================================")

    def criar_usuario(self):
        cpf = input('Informe o CPF (somente números): ')
        usuario = self.filtrar_usuarios(cpf)

        if usuario:
            print('Já existe usuário com esse CPF.')
            return
        
        nome = input('Informe o nome completo: ')
        data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
        endereco = input('Informe o endereço (logradouro, N - bairro - cidade/ sigla estado)')

        self.usuarios.append({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})

        print('Usuário registrado com sucesso!')

    def filtrar_usuarios(self, cpf):
        usuarios_filtrados = [usuario for usuario in self.usuarios if usuario['cpf'] == cpf]
        return usuarios_filtrados[0] if usuarios_filtrados else None

    def criar_conta(self):
        cpf = input('Informe o CPF do usuário: ')
        usuario = self.filtrar_usuarios(cpf)

        if usuario:
            conta_existente = any(conta['usuario']['cpf'] == cpf for conta in self.contas)
            if conta_existente:
                print('Já existe uma conta associada a este CPF.')
            else:
                print('\nConta criada com sucesso!')
                return {'agencia': self.AGENCIA, 'numero_conta': len(self.contas) + 1, 'usuario': usuario}
        else:
            print('\nUsuário não encontrado, processo de criação de conta cancelado.')
        return None

    def listar_contas(self):
        print("==================== Contas Cadastradas ====================")
        for conta in self.contas:
            print(f"Agencia: {conta['agencia']}\nC/C: {conta['numero_conta']}\nTitular: {conta['usuario']['nome']}")
            print("=" * 50)

def main():
    sistema = SistemaBancario()
    
    while True:
        opcao = sistema.menu()

        if opcao == 'd':
            valor = float(input('Informe o valor do depósito: '))
            sistema.deposito(valor)
        elif opcao == 's':
            valor = float(input('Informe o valor do saque: '))
            sistema.saque(valor)
        elif opcao == 'e':
            sistema.imprimir_extrato()
        elif opcao == 'nu':
            sistema.criar_usuario()
        elif opcao == 'nc':
            conta = sistema.criar_conta()
            if conta:
                sistema.contas.append(conta)
        elif opcao == 'lc':
            sistema.listar_contas()
        elif opcao == 'q':
            break
        else:
            print('Opção inválida, por favor selecione novamente uma opção válida.')

if __name__ == '__main__':
    main()