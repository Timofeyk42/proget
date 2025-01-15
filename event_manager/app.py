from flask import Flask, render_template, request, jsonify, redirect, url_for, g
from database import get_db, init_db, add_event, get_events, delete_event
import os

print("Current working directory:", os.getcwd())  # Вывод текущей рабочей директории

app = Flask(__name__, template_folder='templates')  # Явно указываем папку с шаблонами

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    events_list = get_events()
    return render_template('index.html', events=events_list)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        name_ = request.form.get('name_')
        rout_ = request.form.get('rout_')
        quantity_teams = request.form.get('quantity_teams')
        
        try:
            quantity_teams = int(quantity_teams)
        except (ValueError, TypeError):
            return render_template('create_event.html', error="Invalid quantity_teams value")

        if not name_ or not rout_:
            return render_template('create_event.html', error="Name and Route are required fields")

        names_teams = []
        for i in range(quantity_teams):
            team_name = request.form.get(f'name_team_{i+1}')
            if not team_name:
                return render_template('create_event.html', error=f"Missing name for team {i+1}")
            names_teams.append([team_name, 0])
        
        event = {
            "name": name_,
            "rout": rout_,
            "quantity_teams": quantity_teams,
            "teams": names_teams
        }
        add_event(name_, rout_, quantity_teams, names_teams)
        return render_template('result.html', event=event)
    
    return render_template('create_event.html')

@app.route('/events')
def events():
    events_list = get_events()
    return jsonify(events_list)

@app.route('/events/view/<int:event_id>')
def view_event(event_id):
    events_list = get_events()
    event = next((e for e in events_list if e['id'] == event_id), None)
    if event:
        return render_template('view_event.html', event=event)
    else:
        return "Event not found", 404

@app.route('/events/delete/<int:event_id>', methods=['POST'])
def delete_event_route(event_id):
    delete_event(event_id)
    return redirect(url_for('index'))

if __name__ == "__main__":
    init_db(app)  # Передаем объект приложения в init_db
    app.run(port=8000)