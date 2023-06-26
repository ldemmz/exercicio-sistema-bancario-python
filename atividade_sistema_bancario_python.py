"""
================================================================================================
Criado por: Leonardo de Carvalho Pinto Rodrigues

Contato: github.com/ldemmz
        instagram.com/lel_lql
        linkedin.com/in/leonardor99


=======================================

Desafio: Criar um sistema bancário com as operações: sacar, depositar e visualizar extrato.

=======================================

Considerações:

O projeto trabalhará apenas com 1 usuário;
Apresentar mensagem de erro caso o depósito ou saque apresente valor negativo;
Permitir no máximo 3 saques diários;
Limite de valor por saque – R$ 500,00;
Formatação da moeda – R$ XXXX.XX;
Listar todos os depositos e saques realizados na conta e exibir mensagem na ausência de extrato;
Informar saldo atual no extrato.

================================================================================================
"""


import datetime

historico_transacoes = []
saldo = 0
LIMITE_SAQUES = 3
saques_diarios = 0
data_operacao = datetime.datetime.now()

menu = """
-----------------------------------------------------------

            Olá usuário, seja bem-vindo!
  Selecione o número correspondente ao tipo de operação 
                que deseja realizar.

            [0] - Depositar
            [1] - Sacar
            [2] - Visualizar extrato
            [3] - Sair
-----------------------------------------------------------
"""
print(menu)

def formatar_valor(valor):
    return f"R$ {valor:.2f}"
def realizar_deposito():
    global saldo
    print("-" * 60)
    print("""
-- VOCÊ SELECIONOU A OPÇÃO DE DEPÓSITO --

- Para abordar a operação, digite "voltar".
- Se deseja prosseguir, informe o valor do depósito.
""".lstrip())
    print("-" * 60)
    while True:
        valor_deposito = input("Insira aqui: ")
        if valor_deposito == "voltar":
            break
        try:
            valor_deposito = float(valor_deposito)
            if valor_deposito > 0:
                saldo += valor_deposito
                historico_transacoes.append((data_operacao, "Depósito", valor_deposito))
                print("-" * 60)
                print("Depósito realizado com sucesso.")
                print("Saldo atual:", formatar_valor(saldo))
                break
            else:
                print("Valor inválido. Não é permitido o depósito de valores negativos.")
        except ValueError:
            print("Valor inválido. Por favor, tente novamente.")

def realizar_saque():
    global saldo, saques_diarios
    print("-" * 60)
    print("""
-- VOCÊ SELECIONOU A OPÇÃO DE SAQUE --

- Para abordar a operação, digite "voltar".
- Se deseja prosseguir, informe o valor do saque.
""".lstrip())
    print("-" * 60)
    while True:
        valor_saque = input("Insira aqui: ")
        if valor_saque == "voltar":
            break
        try:
            valor_saque = float(valor_saque)
            if valor_saque > 0:
                if valor_saque <= saldo and saques_diarios < LIMITE_SAQUES:
                    saldo -= valor_saque
                    historico_transacoes.append((data_operacao, "Saque", valor_saque))
                    saques_diarios += 1
                    print("Saque realizado com sucesso.")
                    print("Saldo atual:", formatar_valor(saldo))
                    break
                else:
                    print("Saldo insuficiente ou limite diário de saques atingido.")
            else:
                print("Valor inválido. Não é permitido o saque de valores negativos.")
        except ValueError:
            print("Valor inválido. Por favor, tente novamente.")

def visualizar_extrato():
    if len(historico_transacoes) == 0:
        print('Não foram realizadas movimentações.')
    else:
        print("-" * 60)
        print("Aqui está o histórico de suas últimas transações:\n")
        for i, (data, tipo, valor) in enumerate(historico_transacoes, start=1):
            print(f"Transação: {i} - Data: {data.strftime('%d/%m/%Y %H:%M:%S')} - Tipo: {tipo} - Valor: {formatar_valor(valor)}")
        print("\nSaldo atual:", formatar_valor(saldo))

while True:
    opcao_selecionada = input("Insira a opção e confirme: ")

    if opcao_selecionada == "0":
        realizar_deposito()

    elif opcao_selecionada == "1":
        realizar_saque()

    elif opcao_selecionada == "2":
        visualizar_extrato()

    elif opcao_selecionada == "3":
        print("-" * 60)
        print("\n Você foi desconectado do sistema. \n")
        print("-" * 60)
        break

    else:
        print("Opção inválida. Por favor, selecione uma opção válida.")

    print(menu)
