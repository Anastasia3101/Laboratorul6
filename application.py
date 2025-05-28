from flask import Flask, request, render_template_string
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('POSTGRES_DB', 'messages_db')
DB_USER = os.environ.get('POSTGRES_USER', 'user')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'password')

HTML = '''
    <h1>Mesaje</h1>
    <form method="POST">
        <input name="message" placeholder="Lab 6 Anastasia" required>
        <input type="submit">
    </form>
    <ul>
        {% for msg in messages %}
            <li>{{ msg[1] }}</li>
        {% endfor %}
    </ul>
'''

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        message = request.form['message']
        cur.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
        conn.commit()
    cur.execute("SELECT * FROM messages")
    messages = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string(HTML, messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
