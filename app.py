from flask import Flask, request, jsonify

app = Flask(__name__)
items = {1: {"id": 1, "name": "test"}}
next_id = 2

@app.route("/items", methods=["GET"])
def list_items():
    return jsonify(list(items.values()))

@app.route("/items", methods=["POST"])
def create_item():
    global next_id
    data = request.get_json() or {}
    item = {"id": next_id, "name": data.get("name", "")}
    items[next_id] = item
    next_id += 1
    return jsonify(item), 201

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    if item_id not in items:
        return jsonify({"error": "not found"}), 404
    return jsonify(items[item_id])

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    if item_id not in items:
        return jsonify({"error": "not found"}), 404
    data = request.get_json() or {}
    items[item_id]["name"] = data.get("name", items[item_id]["name"])
    return jsonify(items[item_id])

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id in items:
        del items[item_id]
        return "", 204
    return jsonify({"error": "not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)