import sqlparse
from db.db_engine import get_db


def read_sql(filename):
    with open(file=filename, mode="r") as sql_file:
        sql_text = sql_file.read()
        sql_stmts = sqlparse.split(sql_text)

    return sql_stmts


def exec_sql(sql_stmts):
    for stmt in sql_stmts:
        with get_db() as db:
            db.execute(stmt)
            db.commit()
