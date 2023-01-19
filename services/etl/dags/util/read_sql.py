import sqlparse

def read_sql(filename):
    with open(file=filename, mode="r") as sql_file:
        sql_text = sql_file.read()
        sql_stmts = sqlparse.split(sql_text)

    return sql_stmts