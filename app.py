from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 数据库配置
db_config = {
    'user': 'admin',
    'password': 'dora_llm@123',
    'host': '127.0.0.1',
    'database': 'user_db',
    'port': 3306,
    'raise_on_warnings': False
}

# 处理根路径 / 的路由，渲染 index.html
@app.route('/')
def index():
    return render_template('index.html')

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        passwd = request.form.get('passwd')

        conn = mysql.connector.connect(**db_config)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE phone = %s AND passwd = %s", (phone, passwd))
        user = c.fetchone()
        c.close()
        conn.close()

        if user:
            session['phone'] = phone
            return redirect('/account')
        elif check_user_exists(phone):
            return "账户或密码错误", 401
        else:
            return redirect('/register')
    return render_template('login.html')

# 注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form.get('phone')
        passwd = request.form.get('passwd')

        if check_user_exists(phone):
            # 用户已存在直接跳转到登录页面
            return redirect('/login')
        else:
            conn = mysql.connector.connect(**db_config)
            c = conn.cursor()
            c.execute("INSERT INTO users (phone, passwd) VALUES (%s, %s)", (phone, passwd))
            conn.commit()
            c.close()
            conn.close()
            return redirect('/login')
    return render_template('register.html')

# 账户页面
@app.route('/account')
def account():
    if 'phone' in session:
        phone = session['phone']
        return render_template('account.html', phone=phone)
    else:
        return redirect('/')

# 退出登录
@app.route('/logout')
def logout():
    session.pop('phone', None)
    return redirect('/')

# 检查用户是否存在
def check_user_exists(phone):
    conn = mysql.connector.connect(**db_config)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE phone = %s", (phone,))
    user = c.fetchone()
    c.close()
    conn.close()
    return user is not None

if __name__ == '__main__':
    app.run(debug=True)
