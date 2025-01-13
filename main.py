from flask import Flask, request, jsonify

app = Flask("event")

events_list = []


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():

    # Получаем параметры запроса
    name_ = request.args.get('name_')
    rout_ = request.args.get('rout_')
    quantity_teams = request.args.get('quantity_teams')

    # Преобразуем quantity_teams в целое число
    try:
        quantity_teams = int(quantity_teams)
    except (ValueError, TypeError):
        return jsonify(message="Invalid quantity_teams value"), 400

    # Список для хранения имен команд
    names_teams = []

    # Добавляем команды в список
    for i in range(quantity_teams):
        team_name = [request.args.get(f'name_team_{i + 1}'), 0]  # Извлекаем уникальные имена команд
        if team_name:
            names_teams.append(team_name, [0])
        else:
            return jsonify(message=f"Missing name for team {i + 1}"), 400

    # Возвращаем данные в виде строки или JSON
    return jsonify(name=name_, rout=rout_, quantity_teams=quantity_teams, teams=names_teams)
    event = []
    event.append([name, rout, quantity_teams, names_teams])


@app.route('/teams_result', methods=['GET'])
def teams_result():
    return f"Choose an event"
    chname = request.args.get('chname')


@app.route('/hello', methods=['POST'])
def hello_post(names_teams):
    data = request.get_json()
    return jsonify(message=f"Hello, {data['name']}!")


app.run(port=8000)