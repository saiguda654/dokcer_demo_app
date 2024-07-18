from flask import Flask, jsonify, request
app = Flask(__name__)
products = {
    1: {"name": "Laptop", "price": 1200},
    2: {"name": "Phone", "price": 800},
    3: {"name": "Tablet", "price": 300},
}
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product)
    return "Product not found", 404

@app.route('/product', methods=['POST'])
def add_product():
    new_product = request.json
    product_id = len(products) + 1
    products[product_id] = new_product
    return jsonify(new_product), 201
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
