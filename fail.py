from flask import Flask, render_template,request
app = Flask(__name__)
@app.route("/")
def failed():
     return "sorry you are not krish"
if __name__ == "__main__":
    app.run(host='192.168.1.15' , port= 80, debug= True)
