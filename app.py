from flask import Flask,render_template,request,jsonify
# import subprocess
import bot as bot

app = Flask(__name__)

@app.route("/",methods=['GET'])
def root():
    # return "hello world"
    return render_template('index.html')

@app.route("/bot",methods=['POST'])
def calc():
    data_obtained = request.json
    result = bot.process_input(data_obtained)
    return jsonify(result)

# @app.route("/run_script",methods=['POST'])
# def run_script():
#     # Get user input from the request
#     data = request.get_json()
#     user_input = data['input']

#     # Run the Python script and capture the output
#     result = subprocess.run(['python', 'bot.py',str(data)], text=True, capture_output=True)
#     output = result.stdout.strip()

#     return jsonify({'output':output})

if (__name__) == "__main__":
    app.run(debug=True)