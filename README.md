# ChaosBank
Projeto de I.P. IFPE - Paulista
Autores: Luan Victor
         Matheus de Morais
         
THE CHAOS BANK:

Pensem nele como um simulador de aplicativo de banco, tipo esses que a gente usa no celular, só que feito pra rodar direto no computador.

Feito em python para programar tudo, a interface gráfica foi feita com Tkinter, que já vem com o Python, e para guardar os dados, como saldo e transações, usamos um banco de dados SQLite.  

Então com isso, apresentamos as principais funcionalidades mais importantes que se encontra atualmente em um banco digital. Essas são as funcionalidades de forma resumida:

Login e Segurança: Primeiro de tudo, você pode criar sua conta e fazer o login. Pra garantir a segurança, a senha de vocês não fica salva como texto puro, ela vira um "hash" usando o algoritmo SHA256.

Painel Principal: Depois de logar, você cai numa tela principal que tem os botões pra acessar todas as outras funções do programa.

Ver o extrato: Tem uma tela pra ver o saldo e o extrato completo, com todas as transferências, PIX, pagamentos e empréstimos que você fez, tudo em ordem de data.

PIX: Dá pra mandar dinheiro usando uma chave PIX e também gerenciar suas próprias chaves. Você pode cadastrar seu CPF, e-mail ou gerar chaves aleatórias pra receber dinheiro.

Empréstimos e Cartão Virtual: O sistema permite que você peça um empréstimo (com cálculo de juros) e depois te dá a opção de pagar as parcelas ou quitar a dívida toda. Além disso, dá pra gerar um cartão de crédito virtual, com número, validade e CVV.

Outros Serviços: Pra fechar, colocamos uma função de recarga de celular e, pra cada transação importante, o sistema gera uma janelinha de comprovante na hora.

COMO O CODIGO FOI ORGANIZADO?

Separamos o projeto de forma modular, cada um com sua responsabilidade:

main.py: É o arquivo que se executa pra iniciar o programa. Ele cria a janela principal e controla qual tela vai aparecer.

database.py: Esse aqui é o que irá criar as tabelas do banco de dados ou alteralas. Qualquer uma das funções como "pegar o extrato do usuário" ou "registrar um novo empréstimo", é uma função aqui dentro que faz a consulta ou a alteração no banco de dados SQLite. fizemos a deixar toda a lógica de SQL separada nesse arquivo pra organizar melhor.

utils.py: É a principio "caixa de ferramentas". Colocamos aqui as funções em que tem uso em vários lugares. Por exemplo, a função que transforma  senha em um código seguro (hash), a que envia o e-mail de recuperação de senha, e a que formata o CPF pra não aparecer o número inteiro na tela e tambem a que gera o comprovate.

config.py: Pra não deixar informações sensíveis, como senhas e e-mail, jogadas no meio do código, criamos esse arquivo de configuração. só precisamos mexer aqui pra o sistema funcionar em outro computador.

interface: É a parte visual. Todas as telas (login, extrato, etc.) são definidas aqui como classes separadas. Ele contém todos os botões, campos de texto e a lógica de interação do usuário.

