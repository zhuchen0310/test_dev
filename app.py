from flask import Flask
import os
from flask import render_template
app = Flask(__name__)

@app.route("/qixian/")
def hello_world():
    return render_template("jingfen.html") 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
