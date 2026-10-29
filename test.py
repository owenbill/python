import sqlalchemy
from sqlalchemy.sql import text
from sqlalchemy import create_engine

# Define DB Connection 
CONNECTION_STRING = "postgresql+psycopg2://user:xxxx@xx.xx.xx.xx:5432/ragdb"

# 故意留下 SQL injection bug 的查詢
def get_question_history(user_id, rid):
    """
    這個函數包含 SQL injection bug
    """
    engine = create_engine(CONNECTION_STRING)
    
    # ❌ BUG: 直接將使用者輸入參數拼接到 SQL query 中
    # 這是典型的 SQL injection 漏洞
    query_text = text(f"""
        Select question, INSERT_TIME from user_question_history 
        WHERE USER_ID='{user_id}' AND
              RID={rid}
        ORDER BY INSERT_TIME DESC LIMIT 10
    """)
    
    with engine.connect() as con:
        rs = con.execute(query_text)
        
        question_history = []
        for row in rs:
            question_history.append([row[0], row[1]])
            
        return question_history

print(get_question_history('XXXXXX',1))