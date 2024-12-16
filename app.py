from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Исправлено name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель Event для хранения данных о мероприятиях
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    classrooms = db.Column(db.String(500), nullable=False)  # Список кабинетов
    points = db.Column(db.String(500), nullable=False)  # Баллы для классов

@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{'id': e.id, 'name': e.name, 'classrooms': e.classrooms, 'points': e.points} for e in events])

# Добавление нового мероприятия
@app.route('/event', methods=['POST'])
def add_event():
    data = request.json
    new_event = Event(name=data['name'], classrooms=data['classrooms'], points=data['points'])
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Event created!'}), 201

if __name__ == '__main__':  # Исправлено name
    app.run(debug=True)