import os
import bin.run_system_from_input_file
from flask import Flask

app = Flask(__name__)

@app.route("/")
def ping():
    return "OK"

@app.route("/run-sample-data")
def run_sample_data():
    return bin.run_system_from_input_file.main()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)), debug=True)
