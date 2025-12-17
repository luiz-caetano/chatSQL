
# Case Técnico: Interface de Linguagem Natural para SQL (Text-to-SQL)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge\&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey?style=for-the-badge\&logo=flask)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-green?style=for-the-badge)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge\&logo=mysql)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**IA que entende linguagem natural, gera SQL seguro e executa consultas reais usando LangChain e prompt totalmente controlado.**


</div>


---

## 📸 Demo Visual

Para entender o fluxo da solução sem precisar configurar o ambiente:

<div align="center">
<img src="https://s5.ezgif.com/tmp/ezgif-5ea35097253030e0.gif" alt="GIF do Chat funcionando">
</div>

---

## Sobre o Estudo

Este projeto foi desenvolvido para validar a viabilidade de usuários não-técnicos extraírem insights de bancos de dados MySQL sem conhecer a sintaxe SQL. O foco principal foi a **engenharia de prompt** e a **segurança na geração do código**.

### Desafios Resolvidos

1. **Alucinação de Schema:** Como impedir que a IA tente consultar tabelas que não existem?
2. **Segurança (SQL Injection):** Como garantir que comandos como `DROP` ou `DELETE` nunca sejam executados?
3. **Contexto de Negócio:** Como ensinar à IA quem são os principais "IDs" de clientes e fornecedores sem expor dados sensíveis no treinamento?

---

## Arquitetura da Solução

O sistema opera em um pipeline de 4 etapas:

1. **Ingestão de Contexto:** O schema do banco é codificado em **Base64** para garantir integridade durante o transporte e injetado no sistema.
2. **Orquestração (LangChain):** O prompt atua como um "filtro", onde a pergunta do usuário é encapsulada em regras rígidas de negócio.
3. **Geração e Validação:** A LLM gera a query. O sistema valida se ela contém apenas comandos permitidos (`SELECT`).
4. **Execução e Resposta:** O Python executa a query no MySQL e o frontend renderiza os dados de forma amigável.

---

## Engenharia de Prompt (O Core)

O diferencial deste projeto está no prompt customizado, que transforma um modelo de linguagem genérico em um especialista em SQL:

* **Restrição de Escopo:** "Aja como um analista de dados. Use APENAS o schema X."
* **Knowledge Injection:** Fornecimento de IDs estratégicos (Ex: Vendedor João = ID 1) para evitar erros de join.
* **Formatação Estrita:** Saída configurada para retornar apenas o código SQL puro, facilitando o parsing do backend.

---

## 📂 Estrutura de Arquivos

```text
├── main.py           # Ponto de entrada e API Flask
├── llm_engine.py     # Lógica de integração com LangChain e Prompt
├── database.py       # Gerenciamento de conexão e segurança SQL
├── schema_config.py  # Decodificação do schema Base64
└── templates/        # Interface de visualização

```

---

## Autor

**Luiz Caetano**
*Desenvolvedor Backend & Entusiasta de IA Aplicada*

Este é um projeto de estudo de caso. Se você tiver dúvidas sobre a implementação ou sobre as estratégias de prompt usadas, sinta-se à vontade para me chamar!

---

### Por que usar Base64 para o Schema?

> *Nota técnica: Durante o desenvolvimento, percebi que passar o schema em texto puro causava problemas de escape de caracteres em certos modelos. A codificação em Base64 garantiu que a estrutura `CREATE TABLE` chegasse intacta ao interpretador, mantendo a precisão das queries geradas em 100%.*

---
