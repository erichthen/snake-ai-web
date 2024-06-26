import matplotlib.pyplot as plt
import base64
import io

def plot(scores, mean_scores):
    plt.ioff()  # Turn off interactive mode
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(scores, label='Score', color='blue', linestyle='-', marker='o')
    ax.plot(mean_scores, label='Mean Score', color='red', linestyle='--', marker='x')
    ax.set_title('Training Progress')
    ax.set_xlabel('Number of Games')
    ax.set_ylabel('Score')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper left')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)  # Close the plot to prevent it from popping up
    return base64.b64encode(buf.getvalue()).decode('utf-8')


