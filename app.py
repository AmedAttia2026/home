import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# إعداد Flask ليقرأ ملف HTML من نفس المجلد
app = Flask(__name__, template_folder='.')

# نفس مفتاح قاعدة البيانات الخاص بك
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://admin:admin1312312313@aws.rhgcybe.mongodb.net/?appName=aws")
client = MongoClient(MONGO_URI)
db = client['university_system']
calc_col = db['calculator_projects'] # مجموعة جديدة لحفظ حسابات المساحات

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/load')
def load_project():
    project_key = request.args.get('key')
    if not project_key:
        return jsonify({"status": "error", "message": "No key provided"}), 400
    
    project = calc_col.find_one({"key": project_key}, {"_id": 0})
    return jsonify({"status": "success", "data": project})

@app.route('/api/save', methods=['POST'])
def save_project():
    data = request.json
    project_key = data.get('key')
    project_state = data.get('state')
    
    if not project_key:
        return jsonify({"status": "error", "message": "No key provided"}), 400
    
    # تحديث أو إدخال البيانات الجديدة للمفتاح
    calc_col.update_one(
        {"key": project_key},
        {"$set": {"key": project_key, "state": project_state}},
        upsert=True
    )
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # تشغيل السيرفر على البورت 5000
    app.run(host='0.0.0.0', port=5000, debug=True)