from flask import Flask, request

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    notification = request.json
    # Simulate sending a notification (e.g., email, SMS)
    print(f"Notification: {notification['message']}")
    return "Notification sent", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
