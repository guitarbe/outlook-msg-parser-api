import os
from flask import Flask, request, jsonify, abort
import extract_msg
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "ok", "message": "MSG Parser API is running"})

@app.route('/parse-msg', methods=['POST'])
def parse_msg():
    if 'file' not in request.files:
        abort(400, "Missing file")
    
    file = request.files['file']
    
    if not file.filename:
        abort(400, "No file selected")
    
    if not file.filename.lower().endswith('.msg'):
        abort(400, "File must be .msg")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.msg') as tmp:
        file.save(tmp)
        tmp_path = tmp.name
    
    try:
        msg = extract_msg.Message(tmp_path)
        msg_info = {
            "subject": msg.subject or "無主旨",
            "messageDate": msg.date or "",
            "date": msg.date or "",
            "senderName": msg.sender or "未知寄件者",
            "senderEmail": msg.sender or "",
            "to": msg.to or "",
            "body": msg.body or "",
            "text": msg.body or "",
            "attachments": [
                {
                    "filename": att.longFilename or att.shortFilename or "",
                    "data": ""
                }
                for att in msg.attachments
            ]
        }
        return jsonify(msg_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

# 這裡改用環境變數 PORT
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # 改為 8080 作為預設值
    app.run(host='0.0.0.0', port=port)
```

### 方法 2：新增/修改 Procfile

在專案根目錄新增 `Procfile`：
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
