
---

# 🧠 Chat SQL com LLM, Prompt Customizado e Schema Codificado

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge\&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey?style=for-the-badge\&logo=flask)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-green?style=for-the-badge)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge\&logo=mysql)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**IA que entende linguagem natural, gera SQL seguro e executa consultas reais usando LangChain e prompt totalmente controlado.**

[Sobre](#-sobre-o-projeto) • [Arquitetura](#-arquitetura-e-conceitos) • [Funcionalidades](#-funcionalidades) • [Tech Stack](#-tech-stack) • [Instalação](#-instalação) • [Exemplo](#-exemplo-de-uso)

</div>

---

## 🧩 Sobre o Projeto

### O Problema

Usuários de negócio precisam de dados **rápidos e específicos**, mas dependem constantemente do time técnico para escrever queries SQL. Dashboards fixos não resolvem perguntas dinâmicas.

### A Solução

Este projeto implementa um **chat inteligente** que:

* Converte **linguagem natural → SQL**
* Usa **prompt customizado e controlado**
* Executa queries reais no banco
* Retorna dados estruturados em tempo real

Tudo isso garantindo **contexto correto do schema**, **controle da IA** e **prevenção de erros comuns**.

---

## 🧠 Arquitetura e Conceitos

### 🔐 Schema do Banco em Base64

O schema do banco (**CREATE TABLE**) é fornecido ao LLM **codificado em Base64**.

**Por quê?**

* Evita quebra de linhas e erros de parsing
* Garante consistência no prompt
* Facilita versionamento e transporte via `.env`
* Reduz risco de o modelo “inventar” colunas

> O schema é decodificado em runtime e injetado no prompt como contexto fixo.

---

### ✍️ Prompt Customizado (Core do Projeto)

O comportamento do LLM **não é genérico**.

O prompt foi projetado para:

* Restringir a IA **somente ao schema fornecido**
* Impedir `DELETE`, `DROP`, `UPDATE`
* Forçar retorno **apenas em SQL válido**
* Padronizar aliases, filtros e joins

Exemplo de instrução interna:

```text
Você é um assistente especializado em SQL.
Use apenas as tabelas e colunas fornecidas.
Nunca invente campos.
Nunca execute comandos destrutivos.
Retorne apenas a query SQL final.
```

Isso torna o sistema:

* Mais **seguro**
* Mais **previsível**
* Muito mais **confiável para produção**

---

### 🦜🔗 LangChain como Orquestrador

O LangChain é usado para:

* Gerenciar **cadeia de prompts**
* Separar contexto (schema) da pergunta do usuário
* Facilitar troca de modelos (Ollama, OpenAI, etc.)
* Garantir consistência na geração de SQL

O fluxo é:

1. Pergunta do usuário
2. Prompt base + schema decodificado
3. LLM gera SQL
4. SQL é validado
5. Query executada no banco
6. Resultado retornado ao frontend

---

## ✨ Funcionalidades

✔ Conversão de linguagem natural em SQL
✔ Prompt totalmente controlado
✔ Schema fixo e seguro (Base64)
✔ Execução real no banco MySQL
✔ Retorno dos dados + query gerada
✔ Interface web simples e responsiva

---

## 🧪 Tech Stack

| Camada   | Tecnologia         | Função                        |
| -------- | ------------------ | ----------------------------- |
| Backend  | Python + Flask     | API e controle da aplicação   |
| IA       | LangChain + LLM    | Orquestração e geração de SQL |
| Database | MySQL              | Fonte de dados                |
| Frontend | Bootstrap + Jinja2 | Interface web                 |

---

## 🚀 Instalação e Configuração

### Pré-requisitos

* Python 3.8+
* MySQL rodando
* Ollama ou outro LLM compatível

### Passos

1. **Clone o repositório**

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

2. **Instale dependências**

```bash
pip install -r requirements.txt
```

3. **Configure o `.env`**

```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=seu_banco

# Schema do banco codificado em Base64
SCHEMA_BASE64=Q1JFQVRFIFRBQkxFIHZlbmRhcyAoLi4uKTs=
```

> 💡 Dica:
> `cat schema.sql | base64`

4. **Execute**

```bash
python main.py
```

5. **Acesse**

```
http://localhost:5000/chat
```

---

## 🧠 Exemplo de Uso

**Usuário:**

> “Quais foram as vendas do produto AVERT em Varginha?”

**SQL Gerado:**

```sql
SELECT cliente, valor_total
FROM vendas
WHERE produto = 'AVERT'
AND cidade = 'Varginha';
```

**Resultado:**

```json
[
  { "cliente": "Farmácia Central", "valor_total": 1250.00 },
  { "cliente": "Hospital Vida", "valor_total": 3400.50 }
]
```

---

## 📁 Estrutura do Projeto

```bash
.
├── main.py
├── requirements.txt
├── .env
├── web/
│   ├── views.py
│   ├── llm.py        # Prompt + LangChain
│   ├── templates/
│   └── static/
└── README.md
```

---

## 👨‍💻 Autor

**Luiz Caetano**
*Software Developer | Backend | IA aplicada a dados*

🔹 Python • SQL • LangChain • LLMs
🔹 Automação e inteligência aplicada a negócios

[LinkedIn](https://www.linkedin.com/in/luiz-caetano)

---

