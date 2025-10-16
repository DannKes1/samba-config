# API de Autenticação com JWT e Refresh Tokens

Este é um guia completo para configurar, executar e testar uma API Node.js de autenticação que utiliza **JSON Web Tokens (JWT)** com um fluxo de **Refresh Tokens** para gerenciamento de sessão.

## Índice

- [Parte 1: Configuração do Ambiente](#parte-1-configuração-do-ambiente)
  - [Pré-requisitos](#pré-requisitos)
  - [Passo a Passo da Configuração](#passo-a-passo-da-configuração)
- [Parte 2: Execução do Servidor](#parte-2-execução-do-servidor)
- [Parte 3: Teste Completo da API](#parte-3-teste-completo-da-api)

---

## Parte 1: Configuração do Ambiente

Nesta seção, prepararemos todo o necessário para executar a aplicação.

### Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados:

*   **Node.js**: Versão LTS recomendada. O `npm` (Node Package Manager) é incluído na instalação.
*   **Visual Studio Code**: Um editor de código-fonte.
*   **Extensão Postman para VS Code**: Instalada a partir do marketplace de extensões do VS Code para testar os endpoints da API.

### Passo a Passo da Configuração

#### 1. Crie a Pasta do Projeto

Crie uma nova pasta em seu computador (ex: `minha-api-auth`). Abra essa pasta no VS Code (`Arquivo > Abrir Pasta...`).

#### 2. Crie os Arquivos

Na raiz do seu projeto, crie dois arquivos:

*   `server.js`
*   `.env`

#### 3. Adicione os Códigos

*   No arquivo `server.js`, cole o código completo da API.
*   No arquivo `.env`, cole a linha abaixo. Este arquivo guarda sua chave secreta de forma segura.

```plaintext
SECRET_KEY='minha-chave-super-secreta-12345-nao-compartilhe'
```

> **Nota**: Você pode trocar o valor da chave por qualquer frase longa que desejar.

#### 4. Instale as Dependências

1.  Abra o terminal integrado do VS Code (`Ctrl + '`).
2.  Execute o comando abaixo para instalar as bibliotecas necessárias (`express`, `jsonwebtoken`, `dotenv` e `body-parser`):

```bash
npm install express jsonwebtoken dotenv body-parser
```

Após a instalação, uma pasta `node_modules` e um arquivo `package.json` serão criados no seu projeto.

Seu ambiente está pronto!

## Parte 2: Execução do Servidor

Com o ambiente configurado, vamos iniciar a API.

1.  Certifique-se de que o terminal do VS Code está aberto na pasta do projeto.
2.  Execute o seguinte comando:

```bash
node server.js
```

Você deverá ver a seguinte mensagem no terminal, confirmando que o servidor está no ar:

```
Servidor rodando na porta 3000
```

> **Importante**: Deixe este terminal rodando durante toda a fase de testes. Se você o fechar, o servidor será desligado.

## Parte 3: Teste Completo da API (Usando a Extensão Postman)

Vamos simular as requisições de um cliente para validar todas as funcionalidades da API.

### Teste 1: Login como Admin

**Objetivo**: Obter os tokens de acesso.

| Configuração | Detalhes |
| :--- | :--- |
| **Método** | `POST` |
| **URL** | `http://localhost:3000/login` |
| **Body** | JSON |

**Corpo da requisição**:

```json
{
  "username": "admin",
  "password": "adminpass"
}
```

**Resultado**: Você receberá os tokens `accessToken` e `refreshToken`. **Copie ambos para usar nos próximos testes.**

### Teste 2: Acessar Rota de Admin

**Objetivo**: Validar o `accessToken` e a permissão de *role*.

| Configuração | Detalhes |
| :--- | :--- |
| **Método** | `GET` |
| **URL** | `http://localhost:3000/usuarios` |
| **Auth** | Bearer Token |
| **Token** | Cole o `accessToken` que você copiou. |

**Resultado**: Você receberá a lista de usuários, provando que o middleware e a verificação de *role* funcionam.

### Teste 3: Renovar Tokens

**Objetivo**: Usar o `refreshToken` para obter um novo `accessToken`.

| Configuração | Detalhes |
| :--- | :--- |
| **Método** | `POST` |
| **URL** | `http://localhost:3000/refresh` |
| **Body** | JSON |

**Corpo da requisição** (use o `refreshToken` do Teste 1):

```json
{
  "refreshToken": "SEU_REFRESH_TOKEN_AQUI"
}
```

**Resultado**: Você receberá um novo `accessToken` e um novo `refreshToken`. **Guarde este novo `refreshToken`.**

### Teste 4: Fazer Logout

**Objetivo**: Invalidar a sessão, revogando o `refreshToken`.

| Configuração | Detalhes |
| :--- | :--- |
| **Método** | `POST` |
| **URL** | `http://localhost:3000/logout` |
| **Body** | JSON |

**Corpo da requisição** (use o **NOVO** `refreshToken` do Teste 3):

```json
{
  "refreshToken": "SEU_NOVO_REFRESH_TOKEN_AQUI"
}
```

**Resultado**: Mensagem de "Sessão revogada com sucesso".

### Teste 5: Validar o Logout

**Objetivo**: Provar que o token revogado não pode mais ser usado.

1.  Volte para a aba da requisição do **Teste 3** (`/refresh`). O `refreshToken` no corpo já é o que foi invalidado no passo anterior.
2.  Clique em **Send** novamente.

**Resultado**: Você receberá um erro `403 Forbidden` com a mensagem `"Refresh Token inválido"`, confirmando que o logout funcionou perfeitamente.
