from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Use environment variable for database URL, with a fallback for local development
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///causal_inference.db')
db = SQLAlchemy(app)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'tags': self.tags.split(',') if self.tags else []
        }

@app.route('/api/topics', methods=['GET', 'POST'])
def handle_topics():
    if request.method == 'POST':
        data = request.json
        new_topic = Topic(
            title=data['title'],
            content=data['content'],
            tags=','.join(data['tags'])
        )
        db.session.add(new_topic)
        db.session.commit()
        return jsonify(new_topic.to_dict()), 201
    else:
        topics = Topic.query.all()
        return jsonify([topic.to_dict() for topic in topics])

@app.route('/api/topics/<int:topic_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    
    if request.method == 'GET':
        return jsonify(topic.to_dict())
    
    elif request.method == 'PUT':
        data = request.json
        topic.title = data['title']
        topic.content = data['content']
        topic.tags = ','.join(data['tags'])
        db.session.commit()
        return jsonify(topic.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(topic)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)