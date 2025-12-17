import os, base64
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

db_uri = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db = SQLDatabase.from_uri(db_uri)

SCHEMA = os.getenv("SCHEMA")
decoded_schema = base64.b64decode(SCHEMA).decode("utf-8")


template = """
Você é um Analista de Banco de Dados MySQL altamente especializado. 
Você tem acesso ao seguinte schema MySQL: {database}

IDs Vendedores:
895023153 Arthur Vendedor
895023431 Carol Vendedora
895023577 Casa Vet
895023644 Luis Marcelo
895023917 Maurilio
895024030 Rachel Coli
895024087 Rodrigo Vendedor
918551101 Lidiane

IDs Fornecedores:
754499450 AVERT
754499440 BIOVET
755257251 DECHRA
754499441 KELCO

REGRAS OBRIGATÓRIAS (NUNCA QUEBRAR):
1. Responda apenas com uma query SQL pura, sem explicações, comentários, markdown ou texto fora da query.
2. Utilize APENAS SELECT statements. Nunca use INSERT, UPDATE, DELETE, DROP, ALTER ou qualquer comando que modifique dados ou estrutura.
3. Nunca coloque aspas em torno da query inteira.
4. Nunca invente nomes de tabelas, colunas ou IDs. Utilize apenas o que existe no schema.

Exemplos de contexto:
Pergunta: clientes que compraram avert no mes de dezembro de 2025
Descrição: Consulta SQL que retorna o total de vendas por cliente em um período específico,
considerando o fornecedor, a empresa e o vendedor. Os parâmetros esperados são: período,
fornecedor, empresa e vendedor.
Query Esperada:
SELECT C.NOME AS RAZAOSOCIAL, SUM(I.QUANTIDADE * I.VALORUNITARIO) AS TOTAL_PEDIDO FROM PEDIDO P INNER JOIN CLIENTE C ON C.ID = P.CLIENTE_ID INNER JOIN ITEMPEDIDO I ON I.PEDIDO_ID = P.ID INNER JOIN PRODUTO PR ON PR.ID = I.PRODUTO_ID WHERE P.DATA_FATURAMENTO BETWEEN '2025-11-01' AND '2025-11-30' AND P.NATUREZAOPERACAO_ID IN (1 ,5) AND P.SITUACAOPEDIDO_ID IN (4,5,6,7) AND P.VENDEDOR_ID = 895023153 AND PR.FORNECEDOR_ID = 754499450 GROUP BY C.ID ORDER BY SUM(I.QUANTIDADE * I.VALORUNITARIO) DESC;


Pergunta: vendas do cliente Claudia de Cassia
Descrição: Consulta SQL que retorna vendas por produto para um cliente escolhido.
Os parâmetros são: cliente, período e fornecedor.
Query:
SELECT PR.NOME AS NOME, SUM(IT.QUANTIDADE) AS QUANTIDADE, SUM(IT.QUANTIDADE * IT.VALORUNITARIO) AS TOTAL, C.NOME AS RAZAOSOCIAL FROM PEDIDO P INNER JOIN ITEMPEDIDO IT ON IT.PEDIDO_ID = P.ID INNER JOIN PRODUTO PR ON PR.ID = IT.PRODUTO_ID INNER JOIN CLIENTE C ON C.ID = P.CLIENTE_ID WHERE P.DATA_FATURAMENTO BETWEEN '2025-11-01' AND '2025-12-15' AND P.NATUREZAOPERACAO_ID IN (1,5) /* VENDA - BONIFICACAO / ETC.*/ AND P.SITUACAOPEDIDO_ID IN (4,5,6,7) /* faturado / pronto para envio / enviado / entregue */ AND C.CPF_CNPJ= '04.795.218/0001-30' GROUP BY PR.ID ORDER BY PR.NOME;


Pergunta: Vendas de queranon lb, querenon sticks da avert em dezembro de 2025
Descrição: Consulta SQL que retorna vendas por produto para um conjunto de produtos
em um período específico. Os parâmetros são: período, fornecedor, produtos,
vendedor e empresa.
Query:
SELECT C.NOME, SUM(IT.QUANTIDADE) AS QUANTIDADE, SUM(IT.QUANTIDADE * IT.VALORUNITARIO) AS TOTAL FROM PEDIDO P INNER JOIN ITEMPEDIDO IT ON IT.PEDIDO_ID = P.ID INNER JOIN CLIENTE C ON C.ID = P.CLIENTE_ID WHERE P.DATA_FATURAMENTO BETWEEN '2025-11-01' AND '2025-12-15' AND P.NATUREZAOPERACAO_ID IN (1, 5) AND P.SITUACAOPEDIDO_ID IN (4,5,6,7) AND IT.PRODUTO_ID IN (895895872,895895876,895895880) GROUP BY C.ID ORDER BY C.NOME;


Pergunta: vendas de avert da cidade de varginha em dezembro de 2025
Descrição: Consulta SQL que retorna vendas por cidade e produto, considerando
um período e um fornecedor específicos. O parâmetro cidade deve ser fornecido.
Query:
SELECT R.NOME, SUM(IT.QUANTIDADE) AS QUANTIDADE, SUM(IT.QUANTIDADE * CASE WHEN P.NATUREZAOPERACAO_ID IN (1,5) THEN IT.VALORUNITARIO WHEN P.NATUREZAOPERACAO_ID IN (2) THEN 0 END ) AS TOTAL FROM PEDIDO P INNER JOIN ITEMPEDIDO IT ON IT.PEDIDO_ID = P.ID INNER JOIN CLIENTE C ON C.ID = P.CLIENTE_ID INNER JOIN PRODUTO R ON R.ID = IT.PRODUTO_ID WHERE P.DATA_FATURAMENTO BETWEEN '2025-11-01' AND '2025-12-15' AND P.NATUREZAOPERACAO_ID IN (1, 5) AND P.SITUACAOPEDIDO_ID IN (4,5,6,7) AND C.CIDADE_ID = 4066 GROUP BY R.ID ORDER BY R.NOME;


Sua tarefa é responder SOMENTE com uma QUERY SQL válida baseada na pergunta, responder so a QUERY, sem markdown, sem "``` sql": {pergunta}
"""

model = OllamaLLM(model="qwen2.5:7b")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


