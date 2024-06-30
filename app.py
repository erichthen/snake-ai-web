import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from snake_agent import Agent, train
from snake import SnakeGameAI


app = Flask(__name__)
socketio = SocketIO(app)

plot_scores = []
plot_mean_scores = []
total_score = 0
record = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_snake', methods=['POST'])
def start_snake():
    agent = Agent()
    game = SnakeGameAI()
    socketio.start_background_task(train, agent, game, plot_scores, plot_mean_scores, total_score, record, socketio)
    socketio.emit('start_training')
    return jsonify({'status': 'Training started'})

if __name__ == '__main__':
    socketio.run(app, debug=True)