from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# Retrieving all messages or create a new one.
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.desc()).all()
        return jsonify([message.to_dict() for message in messages])
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'body' not in data or 'username' not in data:
            return jsonify({"error": "Missing data"}), 400

        new_message = Message(body=data['body'], username=data['username'])
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201

# Retrieving, updating, or deleting a specific message.
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)  
    if not message:
        return jsonify({"error": "Message not found"}), 404

    data = request.get_json()
    message.body = data.get('body', message.body)
    db.session.commit()
    return jsonify(message.to_dict())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id) 
    if not message:
        return jsonify({"error": "Message not found"}), 404

    db.session.delete(message)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(port=5555)


