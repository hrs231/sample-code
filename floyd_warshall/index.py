from flask import Flask
import test_run_system_from_input_file

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/run-sample-data")
def run_sample_data():
    test_run_system_from_input_file.main()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
