from abc import ABC, abstractmethod
from datetime import datetime, date


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


def exibir_menu_operacoes(conta: "Conta"):
    separador = "-" * LARGURA_TELA

    print(f"\n{separador}")
    print(f"{'OPERAÇÕES BANCÁRIAS':^{LARGURA_TELA}}")
    print(separador)
    print(f"   Conta:  {conta.numero}  |  Titular: {conta.cliente.nome}")
    print(f"   Saldo disponível:      {formatar_moeda(conta.saldo)}")

    if isinstance(conta, ContaCorrente):
        saques_hoje = len(conta.historico.transacoes_do_tipo_hoje("Saque"))
        saques_restantes = conta.limite_saques - saques_hoje
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


def encerrar_sistema() -> None:
    separador = "=" * LARGURA_TELA
    print(f"\n{separador}")
    print(f"{'   Obrigado por utilizar o Sistema Bancário!':^{LARGURA_TELA}}")
    print(f"{'Volte sempre!':^{LARGURA_TELA}}")
    print(f"{separador}\n")



class Transacao(ABC):
    """Interface das transações (UML: Transacao)."""

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta: "Conta") -> bool:
        pass


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: "Conta") -> bool:
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: "Conta") -> bool:
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self) -> list:
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao) -> None:
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

    def transacoes_do_tipo_hoje(self, tipo: str) -> list:
        """Usado para checar o limite diário de saques sem precisar
        guardar um contador/data separados na conta."""
        hoje = date.today()
        return [
            t
            for t in self._transacoes
            if t["tipo"] == tipo
            and datetime.strptime(t["data"], "%d/%m/%Y %H:%M:%S").date() == hoje
        ]



class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta: "Conta", transacao: Transacao) -> bool:
        return transacao.registrar(conta)

    def adicionar_conta(self, conta: "Conta") -> None:
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf




class Conta:
    def __init__(self, numero: int, cliente: Cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> "Conta":
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("   O valor do saque deve ser maior que zero.")
            return False

        if valor > self._saldo:
            print(
                f"""
   Saldo insuficiente para realizar o saque.
    Saldo disponível: {formatar_moeda(self._saldo)}
    Valor solicitado: {formatar_moeda(valor)}
"""
            )
            return False

        self._saldo -= valor
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("   O valor do depósito deve ser maior que zero.")
            return False

        self._saldo += valor
        return True


class ContaCorrente(Conta):
    def __init__(
        self,
        numero: int,
        cliente: Cliente,
        limite: float = LIMITE_VALOR_SAQUE,
        limite_saques: int = LIMITE_SAQUES_DIARIOS,
    ):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        numero_saques_hoje = len(self.historico.transacoes_do_tipo_hoje("Saque"))

        if numero_saques_hoje >= self.limite_saques:
            print(
                f"""
   Limite diário de saques atingido.
    Você já realizou {self.limite_saques} saques hoje.
    Tente novamente amanhã.
"""
            )
            return False

        if valor > self.limite:
            print(
                f"""
   Valor acima do limite permitido por saque.
    Limite máximo: {formatar_moeda(self.limite)}
"""
            )
            return False

        return super().sacar(valor)



def criar_usuario(clientes: list) -> None:
    limpar_tela()
    exibir_cabecalho("   CADASTRO DE USUÁRIO")

    cpf = input("   Digite apenas os números do CPF: ").strip()
    cpf_limpo = "".join(caractere for caractere in cpf if caractere.isdigit())

    if not cpf_limpo:
        print("   CPF inválido. Digite apenas números.")
        return

    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf_limpo:
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

    cliente = PessoaFisica(
        nome=nome,
        data_nascimento=data_nascimento,
        cpf=cpf_limpo,
        endereco=endereco_formatado,
    )
    clientes.append(cliente)

    print(f"\n   Usuário {nome} cadastrado com sucesso!")


def criar_conta_corrente(clientes: list, contas: list, numero_conta: int):
    limpar_tela()
    exibir_cabecalho("   CRIAR CONTA CORRENTE")

    cpf = input("   Digite o CPF do usuário para a conta (apenas números): ").strip()
    cpf_limpo = "".join(caractere for caractere in cpf if caractere.isdigit())

    cliente_encontrado = None
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf_limpo:
            cliente_encontrado = cliente
            break

    if not cliente_encontrado:
        print("   Usuário não encontrado! Cadastre o usuário primeiro.")
        return None

    conta = ContaCorrente.nova_conta(cliente=cliente_encontrado, numero=numero_conta)
    contas.append(conta)
    cliente_encontrado.adicionar_conta(conta)

    print(
        f"""
   Conta criada com sucesso!
    Agência: {conta.agencia}
    Conta:   {conta.numero}
    Titular: {cliente_encontrado.nome}
"""
    )
    return numero_conta + 1


def listar_contas(contas: list) -> None:
    limpar_tela()
    exibir_cabecalho("   CONTAS CADASTRADAS")

    if not contas:
        print("    Nenhuma conta cadastrada no sistema.\n")
        return

    separador = "-" * LARGURA_TELA
    for conta in contas:
        print(f"   Agência: {conta.agencia} | CC: {conta.numero}")
        print(f"   Titular: {conta.cliente.nome} (CPF: {conta.cliente.cpf})")
        print(separador)


def selecionar_conta(contas: list):
    if not contas:
        print("\n    Nenhuma conta cadastrada. Crie uma conta primeiro (opção 2).\n")
        return None

    limpar_tela()
    exibir_cabecalho("   SELECIONAR CONTA")
    separador = "-" * LARGURA_TELA
    for conta in contas:
        print(f"   Conta: {conta.numero} | Agência: {conta.agencia} | Titular: {conta.cliente.nome}")
    print(separador)

    numero_digitado = input("   Digite o número da conta: ").strip()
    if not numero_digitado.isdigit():
        print("   Número de conta inválido.")
        return None

    numero_digitado = int(numero_digitado)
    for conta in contas:
        if conta.numero == numero_digitado:
            return conta

    print("   Conta não encontrada.")
    return None


def exibir_extrato(conta: "Conta") -> None:
    limpar_tela()
    exibir_cabecalho("   EXTRATO BANCÁRIO")

    transacoes = conta.historico.transacoes

    if not transacoes:
        print("ℹ    Não foram realizadas movimentações.\n")
    else:
        for transacao in transacoes:
            sinal = "+" if transacao["tipo"] == "Deposito" else "-"
            print(
                f"    {transacao['tipo']:<10} {sinal} {formatar_moeda(transacao['valor']):<15} "
                f"({transacao['data']})"
            )

    separador = "-" * LARGURA_TELA
    print(separador)
    print(f"   Saldo atual: {formatar_moeda(conta.saldo)}")
    print(f"{separador}\n")



def main() -> None:
    limpar_tela()
    separador = "=" * LARGURA_TELA
    print(f"\n{separador}")
    print(f"{'Bem-vindo ao Banco Yoshi Tardelli':^{LARGURA_TELA}}")
    print(f"{separador}\n")

    clientes: list[Cliente] = []
    contas: list[Conta] = []
    proximo_numero_conta = 1

    while True:
        exibir_menu_principal()
        opcao = ler_opcao_menu()

        if opcao == "1":
            criar_usuario(clientes)

        elif opcao == "2":
            retorno_conta = criar_conta_corrente(clientes, contas, proximo_numero_conta)
            if retorno_conta is not None:
                proximo_numero_conta = retorno_conta

        elif opcao == "3":
            listar_contas(contas)

        elif opcao == "4":
            conta = selecionar_conta(contas)
            if conta is not None:
                while True:
                    limpar_tela()
                    exibir_menu_operacoes(conta)
                    opcao_banco = ler_opcao_menu()

                    if opcao_banco == "1":
                        limpar_tela()
                        exibir_cabecalho("   DEPÓSITO")
                        valor = ler_valor_dinheiro("   Informe o valor do depósito: R$ ")
                        if valor is not None:
                            transacao = Deposito(valor)
                            sucesso = conta.cliente.realizar_transacao(conta, transacao)
                            if sucesso:
                                print(
                                    f"""
   Depósito realizado com sucesso!
    Valor creditado: {formatar_moeda(valor)}
    Novo saldo:      {formatar_moeda(conta.saldo)}
"""
                                )

                    elif opcao_banco == "2":
                        limpar_tela()
                        exibir_cabecalho("   SAQUE")
                        valor = ler_valor_dinheiro("   Informe o valor do saque: R$ ")
                        if valor is not None:
                            transacao = Saque(valor)
                            sucesso = conta.cliente.realizar_transacao(conta, transacao)
                            if sucesso:
                                mensagem_saques = ""
                                if isinstance(conta, ContaCorrente):
                                    saques_hoje = len(
                                        conta.historico.transacoes_do_tipo_hoje("Saque")
                                    )
                                    mensagem_saques = (
                                        f"    Saques hoje:     {saques_hoje}/{conta.limite_saques}\n"
                                    )
                                print(
                                    f"""
   Saque realizado com sucesso!
    Valor debitado:  {formatar_moeda(valor)}
    Saldo restante:  {formatar_moeda(conta.saldo)}
{mensagem_saques}"""
                                )

                    elif opcao_banco == "3":
                        exibir_extrato(conta)

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