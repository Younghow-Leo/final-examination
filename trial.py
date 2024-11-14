import pymysql

# 数据库连接配置
db_config = {
    'host': 'mysql.sqlpub.com',
    'user': 'younghowleo',
    'password': '9ZzxzHCtZKSJhYh8',
    'db': 'mysqlexamination',
    'port': 3306,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def test_db_connection():
    try:
        # 建立数据库连接
        connection = pymysql.connect(**db_config)
        print("数据库连接成功！")
        
        # 创建游标对象
        with connection.cursor() as cursor:
            # 执行一个简单的查询
            cursor.execute("SELECT DATABASE();")
            result = cursor.fetchone()
            print("当前数据库:", result['DATABASE()'])
        
        # 关闭连接
        connection.close()
    except Exception as e:
        print("数据库连接失败:", str(e))

if __name__ == '__main__':
    test_db_connection()