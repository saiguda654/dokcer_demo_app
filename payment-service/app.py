from flask import Flask, request

app = Flask(__name__)

@app.route('/payment', methods=['POST'])
def process_payment():
    payment = request.json
    # Simulate payment processing
    return "Payment processed successfully", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
