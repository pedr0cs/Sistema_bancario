import sys
from datetime import date

# mostra emojis no windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")


LIMITE_VALOR_SAQUE = 500.00
LIMITE_SAQUES_DIARIOS = 3
LARGURA_TELA = 60


saldo = 0.0
depositos = []
saques = []
saques_realizados_hoje = 0
data_referencia_saques = None


def formatar_moeda(valor: float) -> str:
    return f"R$ {valor:.2f}"


def limpar_tela() -> None:
    print("\n" * 2)


def exibir_cabecalho(titulo: str) -> None:
    separador = "=" * LARGURA_TELA
    print(f"\n{separador}")
    print(f"{titulo:^{LARGURA_TELA}}")
    print(f"{separador}\n")


def exibir_menu() -> None:
    saques_restantes = LIMITE_SAQUES_DIARIOS - saques_realizados_hoje
    separador = "-" * LARGURA_TELA

    print(f"\n{separador}")
    print(f"{'🏦BANCO DIGITAL':^{LARGURA_TELA}}")
    print(separador)
    print(f"💵  Saldo disponível:      {formatar_moeda(saldo)}")
    print(f"🔄  Saques restantes hoje: {saques_restantes}")
    print(separador)
    print("  [1] 💰  Depositar")
    print("  [2] 💸  Sacar")
    print("  [3] 📋  Extrato")
    print("  [0] 🚪  Sair")
    print(f"{separador}\n")


def ler_opcao_menu() -> str:
    return input("👉  Digite o número da opção desejada: ").strip()


def ler_valor_dinheiro(mensagem: str) -> float | None:
    entrada = input(mensagem).strip()

    if not entrada:
        print("❌  Entrada vazia. Informe um valor numérico válido.")
        return None

    # se a digitar virgula automaticamente vai pra um ponto
    entrada_normalizada = entrada.replace(",", ".")

    try:
        valor = float(entrada_normalizada)
    except ValueError:
        print("❌  Valor inválido. Utilize apenas números (ex.: 100 ou 100,50).")
        return None

    if valor <= 0:
        print("❌  O valor deve ser maior que zero.")
        return None

    return valor


def atualizar_controle_saques_diarios() -> None:
    global saques_realizados_hoje, data_referencia_saques

    hoje = date.today()

    if data_referencia_saques != hoje:
        saques_realizados_hoje = 0
        data_referencia_saques = hoje


def realizar_deposito() -> None:
    global saldo

    limpar_tela()
    exibir_cabecalho("💰  DEPÓSITO")

    valor = ler_valor_dinheiro("💵  Informe o valor do depósito: R$ ")

    if valor is None:
        return

    saldo += valor
    depositos.append(valor)

    print(
        f"""
✅  Depósito realizado com sucesso!
    Valor creditado: {formatar_moeda(valor)}
    Novo saldo:      {formatar_moeda(saldo)}
"""
    )


def realizar_saque() -> None:
    global saldo, saques_realizados_hoje

    limpar_tela()
    exibir_cabecalho("💸  SAQUE")

    atualizar_controle_saques_diarios()

    if saques_realizados_hoje >= LIMITE_SAQUES_DIARIOS:
        print(
            f"""
❌  Limite diário de saques atingido.
    Você já realizou {LIMITE_SAQUES_DIARIOS} saques hoje.
    Tente novamente amanhã.
"""
        )
        return

    valor = ler_valor_dinheiro("💵  Informe o valor do saque: R$ ")

    if valor is None:
        return

    if valor > LIMITE_VALOR_SAQUE:
        print(
            f"""
❌  Valor acima do limite permitido por saque.
    Limite máximo: {formatar_moeda(LIMITE_VALOR_SAQUE)}
"""
        )
        return

    if valor > saldo:
        print(
            f"""
❌  Saldo insuficiente para realizar o saque.
    Saldo disponível: {formatar_moeda(saldo)}
    Valor solicitado: {formatar_moeda(valor)}
"""
        )
        return

    saldo -= valor
    saques.append(valor)
    saques_realizados_hoje += 1

    print(
        f"""
✅  Saque realizado com sucesso!
    Valor debitado:  {formatar_moeda(valor)}
    Saldo restante:  {formatar_moeda(saldo)}
    Saques hoje:     {saques_realizados_hoje}/{LIMITE_SAQUES_DIARIOS}
"""
    )


def exibir_extrato() -> None:
    limpar_tela()
    exibir_cabecalho("📋  EXTRATO BANCÁRIO")

    if not depositos and not saques:
        print("ℹ️   Não foram realizadas movimentações.\n")
        return

    print("📥  Depósitos realizados:")
    if depositos:
        for indice, valor in enumerate(depositos, start=1):
            print(f"    {indice:02d}. + {formatar_moeda(valor)}")
    else:
        print("    Nenhum depósito registrado.")

    print("\n📤  Saques realizados:")
    if saques:
        for indice, valor in enumerate(saques, start=1):
            print(f"    {indice:02d}. - {formatar_moeda(valor)}")
    else:
        print("    Nenhum saque registrado.")

    separador = "-" * LARGURA_TELA
    print(separador)
    print(f"💼   Saldo atual: {formatar_moeda(saldo)}")
    print(f"{separador}\n")


def encerrar_sistema() -> None:
    separador = "=" * LARGURA_TELA
    print(f"\n{separador}")
    print(f"{'👋  Obrigado por utilizar o Sistema Bancário!':^{LARGURA_TELA}}")
    print(f"{'Volte sempre!':^{LARGURA_TELA}}")
    print(f"{separador}\n")


def main() -> None:
    limpar_tela()
    separador = "=" * LARGURA_TELA
    print(f"\n{separador}")
    print(f"{'🏦Bem-vindo ao Banco Yoshi Tardelli🏦':^{LARGURA_TELA}}")
    print(f"{separador}\n")

    while True:
        exibir_menu()
        opcao = ler_opcao_menu()

        if opcao == "1":
            realizar_deposito()
        elif opcao == "2":
            realizar_saque()
        elif opcao == "3":
            exibir_extrato()
        elif opcao == "0":
            encerrar_sistema()
            break
        else:
            print("⚠️   Opção inválida. Escolha uma opção entre 0 e 3.")

        input("\n⏎  Pressione ENTER para continuar...")
        limpar_tela()


if __name__ == "__main__":
    main()