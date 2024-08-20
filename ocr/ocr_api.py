import os
import uuid  # 导入UUID模块
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域访问

UPLOAD_FOLDER = './uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 自动创建目录

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    # 生成UUID并替换文件名
    unique_filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
    print(f"Generated UUID filename: {unique_filename}")  # 打印UUID文件名
    
    # 保存文件
    file.save(os.path.join(UPLOAD_FOLDER, unique_filename))

    # TODO 迅飞星火OCR
    

    
    return jsonify({"message": f"File {unique_filename} uploaded successfully!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
