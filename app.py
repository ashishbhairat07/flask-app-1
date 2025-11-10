from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Database connection details (match docker-compose.yaml)
DB_CONFIG = {
    "host": "db",
    "database": "mydb",
    "user": "postgres",
    "password": "postgres"
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

@app.route('/')
def home():
    return "Welcome to Flask + Postgres with Docker Compose!"

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "user";')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route('/add_user', methods=['GET'])
def add_user():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Please provide ?name=XYZ"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO "user" (name) VALUES (%s);', (name,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"User '{name}' added successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
