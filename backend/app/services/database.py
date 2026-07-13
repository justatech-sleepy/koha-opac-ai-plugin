import pymysql

connection = pymysql.connect(
    host="localhost",
    user="koha_library",
    password='0kV*TvGz"D;j}38Z',
    database="koha_library",
    port=3306,
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)


def get_connection():
    return connection
