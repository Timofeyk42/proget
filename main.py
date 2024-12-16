from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello_get():
    name = request.args.get('name', 'world')
    return f"Hello, {name}!"

@app.route('/hello', methods=['POST'])
def hello_post():
    data = request.get_json()
    return jsonify(message=f"Hello, {data['name']}!")

if __name__ == '__main__':
    app.run(port=8000)