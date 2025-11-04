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

## **Como Utilizar**

### **1. Geração de Chaves**
- Endpoint: `/api/generate`
- Método: `GET`
- Retorna:
  - `n`: Modulus (chave pública e privada)
  - `e`: Expoente público (chave pública)
  - `d`: Expoente privado (chave privada)

### **2. Assinatura de Arquivos**
- Endpoint: `/api/sign`
- Método: `POST`
- Parâmetros:
  - Arquivo (`file`): O arquivo a ser assinado.
  - `n`: Modulus (chave pública e privada).
  - `d`: Expoente privado (chave privada).
- Retorna:
  - `hash`: Hash do arquivo.
  - `salt`: Salt utilizado no hash.
  - `signature`: Assinatura gerada.

### **3. Verificação de Assinaturas**
- Endpoint: `/api/verify`
- Método: `POST`
- Parâmetros:
  - Arquivo (`file`): O arquivo cuja assinatura será verificada.
  - `n`: Modulus (chave pública e privada).
  - `e`: Expoente público (chave pública).
  - `signature`: Assinatura a ser validada.
  - `salt`: Salt utilizado no hash.
- Retorna:
  - `valid`: Indica se a assinatura é válida (`true` ou `false`).

---

## **Notas**
- Este projeto é **apenas para fins acadêmicos** e não deve ser utilizado em ambientes de produção.
- O tamanho das chaves RSA e o algoritmo de hash foram simplificados para facilitar o entendimento dos conceitos.