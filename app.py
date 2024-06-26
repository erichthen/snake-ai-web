import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from agent import Agent, train
from game import SnakeGameAI
from matplotlib import pyplot as plt
import io
import base64

app = Flask(__name__)
socketio = SocketIO(app)

plot_scores = []
plot_mean_scores = []
total_score = 0
record = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    agent = Agent()
    game = SnakeGameAI()
    socketio.start_background_task(train, agent, game, plot_scores, plot_mean_scores, total_score, record, socketio)
    return jsonify({'status': 'Training started'})

def plot_to_base64():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(plot_scores, label='Score', color='blue', linestyle='-', marker='o')
    ax.plot(plot_mean_scores, label='Mean Score', color='red', linestyle='--', marker='x')
    ax.set_title('Training Progress')
    ax.set_xlabel('Number of Games')
    ax.set_ylabel('Score')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper left')
    buf = io.BytesIO()  # Saving to an in-memory buffer rather than saving to a file
    fig.savefig(buf, format='png')
    buf.seek(0)  # Move buffer position to the beginning
    # Read contents of buffer and encode in base64
    # Doing this to embed binary data of image into HTML and JSON
    # Base64 returns bytes, so decode to convert to string
    return base64.b64encode(buf.getvalue()).decode('utf-8')

if __name__ == '__main__':
    socketio.run(app, debug=True)