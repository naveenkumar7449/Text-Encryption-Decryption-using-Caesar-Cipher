from flask import Flask, request, jsonify, render_template_string
import webbrowser
import threading

app = Flask(__name__)

def caesar_encrypt(text: str, key: int) -> str:
    key = (key % 26 + 26) % 26
    out = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            base = ord('A')
            out.append(chr((ord(ch) - base + key) % 26 + base))
        elif 'a' <= ch <= 'z':
            base = ord('a')
            out.append(chr((ord(ch) - base + key) % 26 + base))
        else:
            out.append(ch)
    return ''.join(out)

def caesar_decrypt(text: str, key: int) -> str:
    key = (key % 26 + 26) % 26
    return caesar_encrypt(text, -key)

def vigenere_encrypt(text: str, key: str) -> str:
    key_filtered = ''.join([c for c in key.lower() if c.isalpha()])
    if not key_filtered:
        raise ValueError("Vigenere key must contain at least one letter (a-z).")
    out = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(key_filtered[ki % len(key_filtered)]) - ord('a')
            out.append(chr((ord(ch) - base + shift) % 26 + base))
            ki += 1
        else:
            out.append(ch)
    return ''.join(out)

def vigenere_decrypt(text: str, key: str) -> str:
    key_filtered = ''.join([c for c in key.lower() if c.isalpha()])
    if not key_filtered:
        raise ValueError("Vigenere key must contain at least one letter (a-z).")
    out = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(key_filtered[ki % len(key_filtered)]) - ord('a')
            out.append(chr((ord(ch) - base - shift + 26*10) % 26 + base))
            ki += 1
        else:
            out.append(ch)
    return ''.join(out)

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Encryption Tool</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .form-group { margin: 15px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 4px; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>Text Encryption & Decryption Tool</h1>
    <form id="encryptForm">
        <div class="form-group">
            <label>Cipher Type:</label>
            <select id="cipher" onchange="updateKeyField()">
                <option value="caesar">Caesar Cipher</option>
                <option value="vigenere">Vigenère Cipher</option>
            </select>
        </div>
        <div class="form-group">
            <label>Text:</label>
            <textarea id="text" rows="4" placeholder="Enter text to encrypt/decrypt"></textarea>
        </div>
        <div class="form-group">
            <label id="keyLabel">Key (number):</label>
            <input type="number" id="key" placeholder="3">
        </div>
        <div class="form-group">
            <label>Operation:</label>
            <select id="mode">
                <option value="encrypt">Encrypt</option>
                <option value="decrypt">Decrypt</option>
            </select>
        </div>
        <button type="submit">Process</button>
    </form>
    <div id="result" class="result" style="display:none;">
        <h3>Result:</h3>
        <p id="output"></p>
    </div>

    <script>
        function updateKeyField() {
            const cipher = document.getElementById('cipher').value;
            const keyLabel = document.getElementById('keyLabel');
            const keyInput = document.getElementById('key');
            
            if (cipher === 'caesar') {
                keyLabel.textContent = 'Key (number):';
                keyInput.placeholder = '3';
                keyInput.type = 'number';
            } else {
                keyLabel.textContent = 'Key (word):';
                keyInput.placeholder = 'SECRET';
                keyInput.type = 'text';
            }
        }

        document.getElementById('encryptForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const data = {
                cipher: document.getElementById('cipher').value,
                text: document.getElementById('text').value,
                key: document.getElementById('key').value,
                mode: document.getElementById('mode').value
            };
            
            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                const output = document.getElementById('output');
                
                if (result.success) {
                    output.textContent = result.result;
                    output.className = '';
                } else {
                    output.textContent = 'Error: ' + result.error;
                    output.className = 'error';
                }
                
                document.getElementById('result').style.display = 'block';
            } catch (error) {
                document.getElementById('output').textContent = 'Network error: ' + error.message;
                document.getElementById('output').className = 'error';
                document.getElementById('result').style.display = 'block';
            }
        });
    </script>
</body>
</html>
    ''')

@app.route('/api/process', methods=['POST'])
def process():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify(success=False, error="Invalid JSON payload"), 400

    cipher = data.get('cipher')
    mode = data.get('mode')
    text = data.get('text', '')
    key = data.get('key', '')

    try:
        if cipher == 'caesar':
            try:
                k = int(key)
            except Exception:
                return jsonify(success=False, error="Caesar cipher requires numeric key"), 400

            if mode == 'encrypt':
                res = caesar_encrypt(text, k)
            elif mode == 'decrypt':
                res = caesar_decrypt(text, k)
            else:
                return jsonify(success=False, error="Invalid mode"), 400

        elif cipher == 'vigenere':
            if not isinstance(key, str) or not any(ch.isalpha() for ch in key):
                return jsonify(success=False, error="Vigenère key must contain alphabetic characters"), 400

            if mode == 'encrypt':
                res = vigenere_encrypt(text, key)
            elif mode == 'decrypt':
                res = vigenere_decrypt(text, key)
            else:
                return jsonify(success=False, error="Invalid mode"), 400
        else:
            return jsonify(success=False, error="Invalid cipher selection"), 400

        return jsonify(success=True, result=res)

    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

if __name__ == '__main__':
    # Auto-open browser after a short delay
    def open_browser():
        webbrowser.open('http://127.0.0.1:5000')
    
    timer = threading.Timer(1.5, open_browser)
    timer.start()
    
    # Debug mode helps during development
    app.run(host='127.0.0.1', port=5000, debug=True)