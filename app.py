from flask import Flask, render_template, request, redirect, url_for
import pymysql
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 确保JSON响应中的中文正确显示

def get_db():
    return pymysql.connect(
        host='mysql.sqlpub.com',
        user='younghowleo',
        password='9ZzxzHCtZKSJhYh8',
        db='mysqlexamination',
        port=3306,
        charset='utf8mb4',  # 改为utf8mb4
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                due_date DATE,
                status ENUM('待完成', '已完成', '已取消') DEFAULT '待完成',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    with conn.cursor() as cursor:
        # 修改排序方式：从旧到新(ASC)
        cursor.execute('SELECT * FROM todos ORDER BY created_at ASC')
        todos = cursor.fetchall()
        
        # 统计数据部分保持不变
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = '已完成' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = '待完成' THEN 1 ELSE 0 END) as pending
            FROM todos
        ''')
        stats = cursor.fetchone()
    conn.close()
    return render_template('index.html', todos=todos, stats=stats)

# 修改 add 函数，增加错误处理
@app.route('/add', methods=['POST'])
def add():
    try:
        title = request.form.get('title')
        due_date = request.form.get('due_date')
        
        if not title:
            return redirect(url_for('index'))
            
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO todos (title, due_date) VALUES (%s, %s)',
                (title, due_date)
            )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error adding todo: {e}")
        return redirect(url_for('index'))

@app.route('/update/<int:id>/<status>')
def update(id, status):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute(
            'UPDATE todos SET status = %s WHERE id = %s',
            (status, id)
        )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    if request.method == 'POST':
        title = request.form.get('title')
        due_date = request.form.get('due_date')
        with conn.cursor() as cursor:
            cursor.execute(
                'UPDATE todos SET title = %s, due_date = %s WHERE id = %s',
                (title, due_date, id)
            )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM todos WHERE id = %s', (id,))
        todo = cursor.fetchone()
    conn.close()
    return render_template('edit.html', todo=todo)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM todos WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)