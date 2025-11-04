# CryptoSigner

CryptoSigner é um projeto acadêmico que implementa um sistema simplificado de assinatura digital utilizando o algoritmo RSA e um hash personalizado (SHA-64). O objetivo do projeto é demonstrar os conceitos básicos de criptografia assimétrica e assinatura digital, permitindo a geração de chaves, assinatura de arquivos e verificação de assinaturas.

---

## **Funcionalidades**
- **Geração de chaves RSA**: Criação de um par de chaves públicas e privadas.
- **Assinatura de arquivos**: Geração de uma assinatura digital para um arquivo utilizando a chave privada.
- **Verificação de assinaturas**: Validação de uma assinatura digital utilizando a chave pública.
- **Hash simplificado (SHA-64)**: Implementação de um hash básico com suporte a salt.

---

## **Requisitos**
- Python 3.8 ou superior
- Ambiente virtual configurado (recomendado)
- Dependências listadas no arquivo `requirements.txt`

---

## **Instalação**

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/CryptoSigner.git
   cd CryptoSigner
   ```

2. **Crie e ative um ambiente virtual**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

---

## **Execução**

1. **Inicie o servidor**
   ```bash
   python3 src/app.py
   ```

2. **Acesse a interface web**
   Abra o navegador e acesse:
   ```
   http://127.0.0.1:5000/
   ```

---

## Como utilizar (interface web)

A aplicação inclui uma interface web pronta para uso, pensada para o fluxo mais comum. As principais ações podem ser feitas sem tocar diretamente na API:

- Acesse a interface: abra http://127.0.0.1:5000/ no navegador.

- Gerar chaves (UI):
  - Clique em "Gerar chaves" na página "Assinar". O frontend chama `/api/generate` e exibirá `n`, `e` e `d`.
  - As chaves também são salvas no `localStorage` do navegador (campo `rsaKeys`) para uso posterior.
  - Você pode reutilizar as chaves com o botão "Carregar chaves salvas".

- Assinar arquivo (UI):
  - Na página "Assinar", selecione o arquivo a ser assinado e clique em "Assinar".
  - A interface envia o arquivo e os valores `n`/`d` (privada) para `/api/sign`.
  - O backend retorna o `hash`, o `salt` (hex) e a `signature` (inteiro); a UI exibe esses valores.
  - O backend salva um arquivo `.sig` (JSON) na pasta `src/data/`. O frontend não gera mais o `.sig` localmente para evitar duplicação.

- Verificar assinatura (UI):
  - Abra a página "Verificar".
  - Faça upload do arquivo original e também do arquivo `.sig` (campo "Arquivo .sig (JSON)").
  - Clique em "Usar .sig" para preencher automaticamente `signature`, `salt`, `n` e `e` a partir do `.sig` carregado. Você pode usar "Usar chaves salvas" para preencher `n`/`e` a partir do `localStorage` ou preenchê-las manualmente se tiver copiado.
  - Clique em "Verificar" para enviar os dados ao endpoint `/api/verify`.
  - O resultado (válida / inválida) é exibido na tela.

## Como utilizar (API direta)

Se preferir usar a API programaticamente, os endpoints principais são os mesmos usados pela interface:

### 1) Geração de chaves
- Endpoint: `/api/generate`
- Método: `GET`
- Resposta (JSON):
  - `n` (string): modulus
  - `e` (string): expoente público
  - `d` (string): expoente privado

> Observação: as chaves são retornadas como strings para evitar perda de precisão no JavaScript (n pode exceder 2**53).

### 2) Assinatura
- Endpoint: `/api/sign`
- Método: `POST`
- Form fields (multipart/form-data):
  - `file`: arquivo a ser assinado (binário)
  - `n`: modulus (string ou número)
  - `d`: expoente privado (string ou número)
- Resposta (JSON):
  - `filename`: nome do arquivo
  - `hash`: hash em hex
  - `salt`: salt em hex
  - `signature`: assinatura (inteiro em string)

### 3) Verificação
- Endpoint: `/api/verify`
- Método: `POST`
- Form fields (multipart/form-data):
  - `file`: arquivo original (binário)
  - `signature`: assinatura (string ou número)
  - `n`: modulus (string ou número)
  - `e`: expoente público (string ou número)
  - `salt`: salt em hex (string)
- Resposta (JSON):
  - `filename`: nome do arquivo
  - `hash`: hash em hex (recomputado)
  - `signature`: assinatura enviada
  - `valid`: booleano indicando sucesso da verificação

---

Mantenha em mente que este projeto é um exemplo acadêmico. Em um cenário real seria necessário usar bibliotecas e formatos padronizados (ex.: PKCS#1, X.509, OpenSSL) e chaves de tamanho adequado.

---

## **Notas**
- Este projeto é **apenas para fins acadêmicos** e não deve ser utilizado em ambientes de produção.
- O tamanho das chaves RSA e o algoritmo de hash foram simplificados para facilitar o entendimento dos conceitos.