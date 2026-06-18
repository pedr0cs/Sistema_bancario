#  Sistema Bancário Otimizado 
Desafio do bootcamp de Python da DIO. Esse projeto consiste em um sistema bancário simples.

# Tecnologias e Conceitos Aplicados
* Python
* Programação Orientada a Objetos (POO)
* Herança (ContaCorrente herda de Conta, PessoaFisica herda de Cliente)
* Classes Abstratas / Interfaces (ABC) — Transacao como contrato para Deposito e Saque
* Encapsulamento (atributos protegidos com @property)
* Polimorfismo (ContaCorrente sobrescreve o método sacar())
* Métodos de Classe (Conta.nova_conta() como factory method)

# Operações Financeiras
* Depósito: Uma Classe (Deposito) que credita o valor na conta e se registra no Histórico.
* Saque: Uma classe (Saque) que faz a validação de limite por saque (R$ 500,00) e limite diário (3 saques) agora é responsabilidade da própria ContaCorrente.
* Extrato: Exibe o Histórico de transações da conta selecionada e o saldo atual.
* Cadastrar Usuário (Cliente): Cria um objeto PessoaFisica e armazena em uma lista de clientes. Não é permitido duplicar CPFs.
* Criar Conta Corrente: Usa o método de classe nova_conta() para vincular uma ContaCorrente (Agência fixa "0001", número sequencial) a um cliente já cadastrado.
* Listar Contas: Exibe todas as contas correntes cadastradas e seus respectivos titulares.
* Selecionar Conta: Como essa atualizacao fez com que o sistema suporte mais contas, é necessário escolher qual conta operar antes de acessar depósito/saque/extrato.


#Como Executar o Projeto

1. Certifique-se de ter o Python instalado.
2. Clone este repositório:
```bash
   git clone [https://github.com/pedr0cs/Sistema_bancario.git](https://github.com/pedr0cs/Sistema_bancario.git)
