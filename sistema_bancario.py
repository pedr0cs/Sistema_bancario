from datetime import date

LIMITE_VALOR_SAQUE = 500.00
LIMITE_SAQUES_DIARIOS = 3
LARGURA_TELA = 60


def formatar_moeda(valor: float) -> str:
    return f"R$ {valor:.2f}"


def limpar_tela() -> None:
    print("\n" * 2)


def exibir_cabecalho(titulo: str) -> None:
    separador = "=" * LARGURA_TELA
    print(f"\n{separador}")
    print(f"{titulo:^{LARGURA_TELA}}")
    print(f"{separador}\n")


# --- MENUS SEPARADOS ---

def exibir_menu_principal():
    separador = "-" * LARGURA_TELA
    print(f"\n{separador}")
    print(f"{'MENU PRINCIPAL':^{LARGURA_TELA}}")
    print(separador)
    print("  [1]   Criar Usuário")
    print("  [2]   Criar Conta Corrente")
    print("  [3]   Listar Contas")
    print("  [4]   Acessar Operações Bancárias")
    print("  [0]   Sair do Sistema")
    print(f"{separador}\n")


def exibir_menu_operacoes(saldo, saques_realizados_hoje):
    saques_restantes = LIMITE_SAQUES_DIARIOS - saques_realizados_hoje
    separador = "-" * LARGURA_TELA

    print(f"\n{separador}")
    print(f"{'OPERAÇÕES BANCÁRIAS':^{LARGURA_TELA}}")
    print(separador)
    print(f"   Saldo disponível:      {formatar_moeda(saldo)}")
    print(f"   Saques restantes hoje: {saques_restantes}")
    print(separador)
    print("  [1]   Depositar")
    print("  [2]   Sacar")
    print("  [3]   Extrato")
    print("  [0]   Voltar ao Menu Principal")
    print(f"{separador}\n")


def ler_opcao_menu() -> str:
    return input("   Digite o número da opção desejada: ").strip()


def ler_valor_dinheiro(mensagem: str) -> float | None:
    entrada = input(mensagem).strip()

    if not entrada:
        print("   Entrada vazia. Informe um valor numérico válido.")
        return None

    entrada_normalizada = entrada.replace(",", ".")

    try:
        valor = float(entrada_normalizada)
    except ValueError:
        print("   Valor inválido. Utilize apenas números (ex.: 100 ou 100,50).")
        return None

    if valor <= 0:
        print("   O valor deve ser maior que zero.")
        return None

    return valor


def atualizar_controle_saques_diarios(saques_realizados_hoje, data_referencia_saques):
    hoje = date.today()
    if data_referencia_saques != hoje:
        return 0, hoje
    return saques_realizados_hoje, data_referencia_saques


def realizar_deposito(saldo, valor, extrato, /):
    saldo += valor
    extrato.append(f"Depósito: + {formatar_moeda(valor)}")
    print(
        f"""
   Depósito realizado com sucesso!
    Valor creditado: {formatar_moeda(valor)}
    Novo saldo:      {formatar_moeda(saldo)}
"""
    )
    return saldo, extrato


def realizar_saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques >= limite_saques:
        print(
            f"""
   Limite diário de saques atingido.
    Você já realizou {limite_saques} saques hoje.
    Tente novamente amanhã.
"""
        )
        return saldo, extrato, numero_saques

    if valor > limite:
        print(
            f"""
   Valor acima do limite permitido por saque.
    Limite máximo: {formatar_moeda(limite)}
"""
        )
        return saldo, extrato, numero_saques

    if valor > saldo:
        print(
            f"""
   Saldo insuficiente para realizar o saque.
    Saldo disponível: {formatar_moeda(saldo)}
    Valor solicitado: {formatar_moeda(valor)}
"""
        )
        return saldo, extrato, numero_saques

    saldo -= valor
    extrato.append(f"Saque: - {formatar_moeda(valor)}")
    numero_saques += 1

    print(
        f"""
   Saque realizado com sucesso!
    Valor debitado:  {formatar_moeda(valor)}
    Saldo restante:  {formatar_moeda(saldo)}
    Saques hoje:     {numero_saques}/{limite_saques}
"""
    )
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    limpar_tela()
    exibir_cabecalho("   EXTRATO BANCÁRIO")

    if not extrato:
        print("ℹ    Não foram realizadas movimentações.\n")
        return

    for movimentacao in extrato:
        print(f"    {movimentacao}")

    separador = "-" * LARGURA_TELA
    print(separador)
    print(f"   Saldo atual: {formatar_moeda(saldo)}")
    print(f"{separador}\n")


def criar_usuario(usuarios):
    limpar_tela()
    exibir_cabecalho("   CADASTRO DE USUÁRIO")

    cpf = input("   Digite apenas os números do CPF: ").strip()
    cpf_limpo = "".join(caractere for caractere in cpf if caractere.isdigit())

    if not cpf_limpo:
        print("   CPF inválido. Digite apenas números.")
        return

    for usuario in usuarios:
        if usuario["cpf"] == str(cpf_limpo):
            print("   Já existe um usuário cadastrado com esse CPF!")
            return

    nome = input("   Nome completo: ").strip()
    data_nascimento = input("   Data de nascimento (dd/mm/aaaa): ").strip()
    
    print("\n   Informe o endereço:")
    logradouro = input("    Logradouro (Rua/Av): ").strip()
    numero = input("    Número: ").strip()
    bairro = input("    Bairro: ").strip()
    cidade = input("    Cidade: ").strip()
    estado = input("    Sigla do Estado (ex: SP): ").strip()

    endereco_formatado = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"

    usuarios.append({
        "nome": nome,
        "data_de_nascimento": data_nascimento,
        "cpf": str(cpf_limpo),
        "endereco": endereco_formatado
    })

    print(f"\n   Usuário {nome} cadastrado com sucesso!")


def criar_conta_corrente(usuarios, contas, numero_conta):
    limpar_tela()
    exibir_cabecalho("   CRIAR CONTA CORRENTE")

    cpf = input("   Digite o CPF do usuário para a conta (apenas números): ").strip()
    cpf_limpo = "".join(caractere for caractere in cpf if caractere.isdigit())

    usuario_encontrado = None
    for usuario in usuarios:
        if usuario["cpf"] == str(cpf_limpo):
            usuario_encontrado = usuario
            break

    if not usuario_encontrado:
        print("   Usuário não encontrado! Cadastre o usuário primeiro.")
        return None

    agencia = "0001"
    
    contas.append({
        "agencia": agencia,
        "numero_da_conta": numero_conta,
        "usuario": usuario_encontrado
    })

    print(
        f"""
   Conta criada com sucesso!
    Agência: {agencia}
    Conta:   {numero_conta}
    Titular: {usuario_encontrado['nome']}
"""
    )
    return numero_conta + 1


def listar_contas(contas):
    limpar_tela()
    exibir_cabecalho("   CONTAS CADASTRADAS")

    if not contas:
        print("    Nenhuma conta cadastrada no sistema.\n")
        return

    separador = "-" * LARGURA_TELA
    for conta in contas:
        print(f"   Agência: {conta['agencia']} | CC: {conta['numero_da_conta']}")
        print(f"   Titular: {conta['usuario']['nome']} (CPF: {conta['usuario']['cpf']})")
        print(f"{separador}")


def encerrar_sistema() -> None:
    separador = "=" * LARGURA_TELA
    print(f"\n{separador}")
    print(f"{'   Obrigado por utilizar o Sistema Bancário!':^{LARGURA_TELA}}")
    print(f"{'Volte sempre!':^{LARGURA_TELA}}")
    print(f"{separador}\n")


def main() -> None:
    limpar_tela()
    separador = "=" * LARGURA_TELA
    print(f"\n{separador}")
    print(f"{'Bem-vindo ao Banco Yoshi Tardelli':^{LARGURA_TELA}}")
    print(f"{separador}\n")

    saldo = 0.0
    extrato = []
    saques_realizados_hoje = 0
    data_referencia_saques = None
    
    usuarios = []
    contas = []
    proximo_numero_conta = 1

    while True:
        saques_realizados_hoje, data_referencia_saques = atualizar_controle_saques_diarios(
            saques_realizados_hoje, data_referencia_saques
        )
        
        exibir_menu_principal()
        opcao = ler_opcao_menu()

        if opcao == "1":
            criar_usuario(usuarios)

        elif opcao == "2":
            retorno_conta = criar_conta_corrente(usuarios, contas, proximo_numero_conta)
            if retorno_conta is not None:
                proximo_numero_conta = retorno_conta

        elif opcao == "3":
            listar_contas(contas)

        elif opcao == "4":
            while True:
                limpar_tela()
                exibir_menu_operacoes(saldo, saques_realizados_hoje)
                opcao_banco = ler_opcao_menu()

                if opcao_banco == "1":
                    limpar_tela()
                    exibir_cabecalho("   DEPÓSITO")
                    valor = ler_valor_dinheiro("   Informe o valor do depósito: R$ ")
                    if valor is not None:
                        saldo, extrato = realizar_deposito(saldo, valor, extrato)

                elif opcao_banco == "2":
                    limpar_tela()
                    exibir_cabecalho("   SAQUE")
                    valor = ler_valor_dinheiro("   Informe o valor do saque: R$ ")
                    if valor is not None:
                        saldo, extrato, saques_realizados_hoje = realizar_saque(
                            saldo=saldo,
                            valor=valor,
                            extrato=extrato,
                            limite=LIMITE_VALOR_SAQUE,
                            numero_saques=saques_realizados_hoje,
                            limite_saques=LIMITE_SAQUES_DIARIOS
                        )

                elif opcao_banco == "3":
                    exibir_extrato(saldo, extrato=extrato)

                elif opcao_banco == "0":
                    break
                else:
                    print("    Opção inválida. Escolha entre 0 e 3.")
                
                input("\n   Pressione ENTER para continuar...")

        elif opcao == "0":
            encerrar_sistema()
            break
        else:
            print("    Opção inválida. Escolha uma opção entre 0 e 4.")

        input("\n   Pressione ENTER para continuar...")
        limpar_tela()


if __name__ == "__main__":
    main()
