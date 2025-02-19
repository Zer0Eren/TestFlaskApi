from flask import Flask, request, jsonify

app = Flask(__name__)

# Ürün listesi
malzeme = [
    {"id": 1, "name": "Asus Rog 4070ti", "price": 50000},
    {"id": 2, "name": "i9 13900K", "price": 30000},
    {"id": 3, "name": "Asus Rog Z790-F", "price": 20000}
]

# Tüm ürünleri getirme
@app.route('/malzeme', methods=["GET"])
def get_malzemeler():
    return jsonify(malzeme)

# ID ile ürün getirme
@app.route('/malzeme/<int:malzeme_id>', methods=['GET'])
def get_malzeme(malzeme_id):
    found_malzeme = next((p for p in malzeme if p["id"] == malzeme_id), None)
    if found_malzeme:
        return jsonify(found_malzeme)
    return jsonify({"error": "Ürün Bulunamadı"}), 404

# Yeni ürün ekleme
@app.route('/malzeme', methods=["POST"])
def add_malzeme():
    new_malzeme = request.get_json()
    new_malzeme["id"] = len(malzeme) + 1
    malzeme.append(new_malzeme)
    return jsonify(new_malzeme), 201

# Ürün güncelleme (PUT - Tam Güncelleme)
@app.route('/malzeme/<int:malzeme_id>', methods=["PUT"])
def update_malzeme(malzeme_id):
    found_malzeme = next((p for p in malzeme if p["id"] == malzeme_id), None)
    if found_malzeme:
        data = request.get_json()
        found_malzeme["name"] = data.get("name", found_malzeme["name"])
        found_malzeme["price"] = data.get("price", found_malzeme["price"])
        return jsonify(found_malzeme)
    return jsonify({"message": "Ürün Bulunamadı"}), 404

# **PATCH - Kısmi Güncelleme**
@app.route('/malzeme/<int:malzeme_id>', methods=["PATCH"])
def patch_malzeme(malzeme_id):
    found_malzeme = next((p for p in malzeme if p["id"] == malzeme_id), None)
    if found_malzeme:
        data = request.get_json()
        
        # Eğer "name" veya "price" varsa, güncelle
        if "name" in data:
            found_malzeme["name"] = data["name"]
        if "price" in data:
            found_malzeme["price"] = data["price"]

        return jsonify(found_malzeme)
    
    return jsonify({"message": "Ürün Bulunamadı"}), 404

# Ürün silme
@app.route('/malzeme/<int:malzeme_id>', methods=['DELETE'])
def delete_malzeme(malzeme_id):
    global malzeme
    malzeme = [p for p in malzeme if p["id"] != malzeme_id]
    return jsonify({"message": "Ürün Silindi"}), 200

# API'yi çalıştırma
if __name__ == '__main__':
    app.run(debug=True)
