API de Autenticação com JWT e Refresh Tokens
Este é um guia completo para configurar, executar e testar uma API Node.js de autenticação que utiliza JSON Web Tokens (JWT) com um fluxo de Refresh Tokens para gerenciamento de sessão.
Índice

Parte 1: Configuração do Ambiente

Pré-requisitos
Passo a Passo da Configuração


Parte 2: Execução do Servidor
Parte 3: Teste Completo da API

Parte 1: Configuração do Ambiente
Nesta seção, prepararemos todo o necessário para executar a aplicação.
Pré-requisitos
Antes de começar, garanta que você tenha os seguintes softwares instalados:

Node.js: Versão LTS recomendada. O npm (Node Package Manager) é incluído na instalação.
Visual Studio Code: Um editor de código-fonte.
Extensão Postman para VS Code: Instalada a partir do marketplace de extensões do VS Code para testar os endpoints da API.

Passo a Passo da Configuração

Crie a Pasta do Projeto:

Crie uma nova pasta em seu computador (ex: minha-api-auth).
Abra essa pasta no VS Code (Arquivo > Abrir Pasta...).


Crie os Arquivos:

Na raiz do seu projeto, crie dois arquivos:

server.js
.env




Adicione os Códigos:


No arquivo server.js, cole o código completo da API.


No arquivo .env, cole a linha abaixo. Este arquivo guarda sua chave secreta de forma segura.
plaintextSECRET_KEY='minha-chave-super-secreta-12345-nao-compartilhe'
Nota: Você pode trocar o valor da chave por qualquer frase longa que desejar.



Instale as Dependências:


Abra o terminal integrado do VS Code (Ctrl + ').


Execute o comando abaixo para instalar as bibliotecas necessárias (express, jsonwebtoken, dotenv e body-parser):
bashnpm install express jsonwebtoken dotenv body-parser
Após a instalação, uma pasta node_modules e um arquivo package.json serão criados no seu projeto.




Seu ambiente está pronto!
Parte 2: Execução do Servidor
Com o ambiente configurado, vamos iniciar a API.


Certifique-se de que o terminal do VS Code está aberto na pasta do projeto.


Execute o seguinte comando:
bashnode server.js


Você deverá ver a seguinte mensagem no terminal, confirmando que o servidor está no ar:

Servidor rodando na porta 3000

Importante: Deixe este terminal rodando durante toda a fase de testes. Se você o fechar, o servidor será desligado.
Parte 3: Teste Completo da API (Usando a Extensão Postman)
Vamos simular as requisições de um cliente para validar todas as funcionalidades da API.
Teste 1: Login como Admin
Objetivo: Obter os tokens de acesso.
Configuração:

Método: POST
URL: http://localhost:3000/login
Aba Body > Selecionar JSON.

Corpo da requisição:
json{
    "username": "admin",
    "password": "adminpass"
}
Ação: Clique em Send.
Resultado: Você receberá os tokens accessToken e refreshToken. Copie ambos para usar nos próximos testes.
Teste 2: Acessar Rota de Admin
Objetivo: Validar o accessToken e a permissão de role.
Configuração:

Método: GET
URL: http://localhost:3000/usuarios
Aba Auth > Type: Bearer Token.
Token: Cole o accessToken que você copiou.

Ação: Clique em Send.
Resultado: Você receberá a lista de usuários, provando que o middleware e a verificação de role funcionam.
Teste 3: Renovar Tokens
Objetivo: Usar o refreshToken para obter um novo accessToken.
Configuração:

Método: POST
URL: http://localhost:3000/refresh
Aba Body > Selecionar JSON.

Corpo da requisição (use o refreshToken do Teste 1):
json{
    "refreshToken": "SEU_REFRESH_TOKEN_AQUI"
}
Ação: Clique em Send.
Resultado: Você receberá um novo accessToken e um novo refreshToken. Guarde este novo refreshToken.
Teste 4: Fazer Logout
Objetivo: Invalidar a sessão, revogando o refreshToken.
Configuração:

Método: POST
URL: http://localhost:3000/logout
Aba Body > Selecionar JSON.

Corpo da requisição (use o NOVO refreshToken do Teste 3):
json{
    "refreshToken": "SEU_NOVO_REFRESH_TOKEN_AQUI"
}
Ação: Clique em Send.
Resultado: Mensagem de "Sessão revogada com sucesso".
Teste 5: Validar o Logout
Objetivo: Provar que o token revogado não pode mais ser usado.
Configuração:

Volte para a aba da requisição do Teste 3 (/refresh).
O refreshToken no corpo já é o que foi invalidado no passo anterior.

Ação: Clique em Send novamente.
Resultado: Você receberá um erro 403 Forbidden com a mensagem "Refresh Token inválido", confirmando que o logout funcionou perfeitamente.
