import textwrap

def mostrar_menu():
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))

def realizar_deposito(saldo_atual, valor_deposito, extrato_atual):
    if valor_deposito > 0:
        saldo_atual += valor_deposito
        extrato_atual += f"Depósito:\tR$ {valor_deposito:.2f}\n"
        print("\n=== Depósito efetuado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! Valor inválido. @@@")
    return saldo_atual, extrato_atual

def realizar_saque(saldo_atual, valor_saque, extrato_atual, limite_saque, numero_saques, max_saques):
    saldo_insuficiente = valor_saque > saldo_atual
    limite_excedido = valor_saque > limite_saque
    saques_excedidos = numero_saques >= max_saques

    if saldo_insuficiente:
        print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
    elif limite_excedido:
        print("\n@@@ Operação falhou! Limite de saque excedido. @@@")
    elif saques_excedidos:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor_saque > 0:
        saldo_atual -= valor_saque
        extrato_atual += f"Saque:\t\tR$ {valor_saque:.2f}\n"
        numero_saques += 1
        print("\n=== Saque efetuado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! Valor inválido. @@@")
    return saldo_atual, extrato_atual

def mostrar_extrato(saldo_atual, extrato_atual):
    print("\n================ EXTRATO ================")
    print("Sem movimentações." if not extrato_atual else extrato_atual)
    print(f"\nSaldo:\t\tR$ {saldo_atual:.2f}")
    print("==========================================")

def adicionar_usuario(lista_usuarios):
    cpf = input("Informe o CPF (apenas números): ")
    usuario_existente = encontrar_usuario(cpf, lista_usuarios)
    if usuario_existente:
        print("\n@@@ CPF já cadastrado! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ")

    novo_usuario = {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}
    lista_usuarios.append(novo_usuario)
    print("=== Usuário adicionado com sucesso! ===")

def encontrar_usuario(cpf, lista_usuarios):
    for usuario in lista_usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def criar_nova_conta(numero_agencia, numero_conta, lista_usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = encontrar_usuario(cpf, lista_usuarios)
    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": numero_agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\n@@@ Usuário não encontrado. Criação de conta cancelada! @@@")

def listar_todas_contas(lista_contas):
    for conta in lista_contas:
        detalhes_conta = f"""\
            Agência:\t{conta['agencia']}
            Conta:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(detalhes_conta))

def sistema_bancario():
    MAX_SAQUES = 3
    AGENCIA_PADRAO = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = mostrar_menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = realizar_deposito(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = realizar_saque(saldo, valor, extrato, limite, numero_saques, MAX_SAQUES)

        elif opcao == "e":
            mostrar_extrato(saldo, extrato)

        elif opcao == "nu":
            adicionar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            nova_conta = criar_nova_conta(AGENCIA_PADRAO, numero_conta, usuarios)
            if nova_conta:
                contas.append(nova_conta)

        elif opcao == "lc":
            listar_todas_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Opção inválida, tente novamente.")

sistema_bancario()
