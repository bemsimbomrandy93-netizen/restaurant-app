from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

@app.route('/order', methods=['POST'])
def order():

    data = request.get_json()
    food = data['food']

    db = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME']
    )

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO orders (food) VALUES (%s)",
        (food,)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": f"Order received for {food}"
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
