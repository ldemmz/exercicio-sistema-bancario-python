import datetime

def exibir_menu():
    menu = """
    -----------------------------------------------------------
                Olá usuário, seja bem-vindo!
    Selecione o número correspondente ao tipo de operação 
                    que deseja realizar.

                [0] - Depositar
                [1] - Sacar
                [2] - Visualizar extrato
                [3] - Cadastrar usuário
                [4] - Abrir uma conta
                [5] - Visualizar contas cadastradas
                [6] - Sair
    -----------------------------------------------------------"""
    return print(menu)

def exibir_mensagem_operacao_selecionada(nome_operacao):
    nome_operacao1 = nome_operacao.upper()
    nome_operacao2 = nome_operacao.lower()
    mensagem = f"""
    -----------------------------------------------------------
        -- VOCÊ SELECIONOU A OPÇÃO DE {nome_operacao1} --

    - Para abordar a operação, digite "voltar".
    - Se deseja prosseguir, informe o valor do {nome_operacao2}.
    -----------------------------------------------------------"""
    return print(mensagem)

def exibir_mensagem_operacao_contas(nome_operacao):
    nome_operacao = nome_operacao.upper()
    mensagem = f"""
    -----------------------------------------------------------
        -- VOCÊ SELECIONOU A OPÇÃO DE {nome_operacao} --

    - Para abordar a operação, digite "voltar".
    - Se deseja prosseguir, informe o seu CPF.
    - É necessário que o CPF siga a seguinte formatação: 00000000000
    -----------------------------------------------------------
          """
    return print(mensagem)

def formatar_valor(valor):
    return f"R$ {valor:.2f}"

def realizar_deposito(saldo, valor_deposito, extrato,/):
    if valor_deposito == "voltar":
        return saldo, extrato

    try:
        valor_deposito = float(valor_deposito)
        if valor_deposito > 0:
            saldo += valor_deposito
            data_transacao = datetime.datetime.now()
            extrato.append((data_transacao, "Depósito", valor_deposito))
            print("Depósito realizado com sucesso.")
            print("Saldo atual:", formatar_valor(saldo))
        else:
            print("Valor inválido. Não é permitido o depósito de valores negativos.")
    except ValueError:
        print("Valor inválido. Por favor, tente novamente.")

    return saldo, extrato

def realizar_saque(*, saldo, valor_saque, extrato, limite, numero_saques, limite_saques):
    if valor_saque == "voltar":
        return

    try:
        valor_saque = float(valor_saque)
        if valor_saque <= 0:
            print("Valor inválido. Não é permitido o saque de valores negativos ou nulos.")
        elif numero_saques > (limite_saques - 1):
            print("Transação cancelada! O limite de saques diário foi atingido.")
        elif valor_saque > saldo:
            print("Saldo insuficiente para completar a transação.")
        elif valor_saque > limite:
            print(f"O limite máximo para saques é de {limite} reais.")
        else:
            saldo -= valor_saque
            numero_saques += 1
            data_transacao = datetime.datetime.now()
            extrato.append((data_transacao, "Saque", valor_saque))
            print("Saque realizado com sucesso.")
            print("Saldo atual:", formatar_valor(saldo))
    except ValueError:
        print("Valor inválido. Por favor, tente novamente.")

    return saldo, extrato, numero_saques

def visualizar_extrato(saldo,/, *, extrato):
    if len(extrato) == 0:
        print('Não foram realizadas movimentações.')
    else:
        print("-" * 60)
        print("Aqui está o histórico de suas últimas transações:\n")
        for i, (data, tipo, valor) in enumerate(extrato, start=1):
            print(f"Transação: {i} - Data: {data.strftime('%d/%m/%Y %H:%M:%S')} - Tipo: {tipo} - Valor: {formatar_valor(valor)}")
        print("\nSaldo atual:", formatar_valor(saldo))

def filtrar_usuarios_cadastrados(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_usuario(usuarios):
    while True:
        cpf = input("Insira o CPF: ").lower()
        if cpf == "voltar":
            return
        
        if cpf.isdigit() and len(cpf) == 11:
            usuario = filtrar_usuarios_cadastrados(cpf, usuarios)
            if usuario:
                print("Este CPF já foi cadastrado anteriormente no sistema e encontra-se indisponível.")
                return
            
            nome = input("Favor informar seu nome completo: ")
            data_nascimento = input("Informe sua data de nascimento (dd/mm/aaaa): ")
            endereco = input("Cadastre seu endereço seguindo a formatação adequada (Logradouro, N° - Bairro - Cidade/Sigla do estado): ")

            usuarios.append({"cpf": cpf, "nome": nome, "data_nascimento": data_nascimento, "endereco": endereco})
            print("-" * 60)
            print("Usuário cadastrado com sucesso!")
            break
        else:
            print("Por favor, informe um CPF válido ou digite 'voltar'.")


def abrir_conta(usuarios, agencia, numero_conta):
    while True:
        cpf = input("Insira o CPF para abrir uma conta (ou 'voltar' para retornar ao menu): ")
        usuario = filtrar_usuarios_cadastrados(cpf, usuarios)

        if cpf.lower() == "voltar":
            return 

        if usuario:
            confirmacao = input(f"\n Você realmente deseja abrir uma conta no CPF {cpf}? Digite 'sim' para confirmar. ")
            if confirmacao.lower() == 'sim':
                print("\nConta aberta com sucesso!")
                return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
            else:
                print("\nAbertura de conta cancelada.")
                return
        else:
            print("\nLamentamos, mas não encontramos nenhum registro de usuário no sistema associado ao CPF informado.")
            print('Por favor, informe um CPF válido ou digite "voltar".\n')


def listar_contas(contas):
    if not contas:
        print("\n\nNão existem contas cadastradas.")
    else:
        print("Lista de contas cadastradas:")
        for conta in contas:
            print(f"Agência: {conta['agencia']} - C/C: {conta['numero_conta']} - Titular: {conta['usuario']['nome']}")

def main():
    AGENCIA = "0001"
    LIMITE_SAQUES = 3
    LIMITE = 5500
    saldo = 0
    numero_saques = 0

    usuarios = []
    contas = []
    extrato = []

    while True:
        exibir_menu()
        opcao_selecionada = input("Insira a opção e confirme: ")

        if opcao_selecionada == "0":
            exibir_mensagem_operacao_selecionada("depósito")
            valor_deposito = input("Insira aqui: ")
            saldo, extrato = realizar_deposito(saldo, valor_deposito, extrato)

        elif opcao_selecionada == "1":
            exibir_mensagem_operacao_selecionada("saque")
            valor_saque = input("Insira aqui: ")
            saldo, extrato, numero_saques = realizar_saque(saldo = saldo, valor_saque = valor_saque, extrato = extrato, limite = LIMITE, numero_saques = numero_saques, limite_saques = LIMITE_SAQUES)

        elif opcao_selecionada == "2":
            visualizar_extrato(saldo, extrato = extrato)

        elif opcao_selecionada == "3":
            exibir_mensagem_operacao_contas("cadastro de usuário")
            criar_usuario(usuarios)

        elif opcao_selecionada == "4":
            exibir_mensagem_operacao_contas("abertura de conta")
            numero_conta = len(contas) + 1
            conta = abrir_conta(usuarios, AGENCIA, numero_conta)

            if conta:
                    contas.append(conta)

        elif opcao_selecionada == "5":
            listar_contas(contas)

        elif opcao_selecionada == "6":
            print("-" * 60)
            print("\nVocê foi desconectado do sistema.\n")
            print("-" * 60)
            break

        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")

main()
