import os
import test_run_system_from_input_file
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/run-sample-data")
def run_sample_data():
    test_run_system_from_input_file.main()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)), debug=True)
