from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h2>Run Python Program</h2>
            <button onclick="runScript()">Run Python Script</button>
            <script>
                function runScript() {
                    fetch('/run_script')
                        .then(response => response.text())
                        .then(result => console.log(result));
                }
            </script>
        </body>
    </html>
    '''

@app.route('/run_script')
def run_script():
    result = subprocess.run(['python', 'path/to/your/script.py'], capture_output=True, text=True)
    return result.stdout

if __name__ == '__main__':
    app.run(debug=True)
