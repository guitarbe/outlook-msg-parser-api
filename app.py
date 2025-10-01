from flask import Flask, request, jsonify, abort
import extract_msg
import tempfile
import os

app = Flask(__name__)

@app.route('/parse-msg', methods=['POST'])
def parse_msg():
    if 'file' not in request.files:
        abort(400, "Missing file")
    file = request.files['file']
    if not file.filename.lower().endswith('.msg'):
        abort(400, "File must be .msg")

    with tempfile.NamedTemporaryFile(delete=False, suffix='.msg') as tmp:
        file.save(tmp)
        tmp_path = tmp.name

    try:
        msg = extract_msg.Message(tmp_path)
        msg_info = {
            "subject": msg.subject or "",
            "date": msg.date or "",
            "from": msg.sender or "",
            "to": msg.to or "",
            "body": msg.body or "",
            "attachments": [
                {
                    "filename": att.longFilename or att.shortFilename or "",
                    "data": ""  # 實際附件如需回傳可 base64 編碼/存外部服務
                }
                for att in msg.attachments
            ]
        }
        return jsonify(msg_info)
    finally:
        os.remove(tmp_path)

# Force a new build on Zeabur
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000)
