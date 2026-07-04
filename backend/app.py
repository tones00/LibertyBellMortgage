from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/apply', methods = ['POST'])
def apply(): 
    data = request.get_json()

    #print to terminal to see what arrives
    print("New application recieved: ")
    print(data)

    return jsonify({'status' : 'recieved'})

if __name__ == '__main__':
    app.run(debug=True)


    