from textwrap import indent

from IPython import embed

import sqlparse

from pyhive import presto  # or import hive
from pyhive import hive # or import hive


def presto_execute_fetchall(server, sql):
    cursor = presto.connect(server).cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result


def get_presto_select():
    result = presto_execute_fetchall(
        'localhost',
        'select * from minio.default.customer_text limit 5')
    return result


def get_presto_create():
    result = presto_execute_fetchall(
        'localhost',
        'show create table minio.default.customer_text')
    return result[0][0]


def get_hive():
    cursor = hive.connect('localhost').cursor()
    cursor.execute('SELECT * FROM customer_text limit 5')
    result = cursor.fetchall()
    cursor.close()
    return result


def create_hive_text_table():
    cursor = hive.connect('localhost').cursor()
    sql = '''
    create external table customer_text2(id string, fname string, lname string)
        ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
        STORED as TEXTFILE location 's3a://customer-data-text2/'
    '''
    cursor.execute(sql)
    cursor.close()
    return result


def create_hive_parq_table():
    cursor = hive.connect('localhost').cursor()
    sql = '''
    create external table customer_parq(id string, fname string, lname string)
        STORED AS PARQUET location 's3a://customer-data-parq/'
    '''
    cursor.execute(sql)
    sql = 'insert into customer_parq select * from customer_text'
    cursor.execute(sql)
    sql = 'insert into customer_parq select * from customer_text2'
    cursor.execute(sql)
    cursor.close()


def print_parsed_sql(parsed):
    tokens = parsed[0].tokens
    for token in tokens:
        if token.is_keyword:
            print('keyword: {}'.format(str(token).strip()))
        else:
            print(indent(str(token).strip(), '\t'))


def main():
    # print(get_presto_select())
    presto_create_stmt = get_presto_create()
    print(presto_create_stmt)
    parsed = sqlparse.parse(presto_create_stmt)
    print_parsed_sql(parsed)
    # print(get_hive())
    # create_hive_text_table()
    # create_hive_parq_table()
    pass


if __name__ == '__main__':
    main()
