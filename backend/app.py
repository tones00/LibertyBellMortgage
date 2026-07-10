from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "http://127.0.0.1:5500",  # Live Server local
    "http://localhost:5500",   # Live Server alternate
    "https://libertybell-loans.com",  # Production (for when you deploy)
    "https://libertybellmortgage.netlify.app"  # Netlify (update with your actual URL)
])

@app.route('/api/apply', methods = ['POST'])
def apply(): 
    data = request.get_json()

    #print to terminal to see what arrives
    print("New application recieved: ")
    print(data)

    return jsonify({'status' : 'received'})

if __name__ == '__main__':
    app.run(debug=True)


    