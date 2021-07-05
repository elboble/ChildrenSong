from flask import Flask, render_template

from serv.content import content
from serv.get_set_anything import gsa
from serv.users import users
from serv.get_qrcode import qr
from serv.devices import devices
from serv.friend import friends
from serv.ai import t2audio
from serv.chat import chat

from setting import PEM,KEY


app = Flask(__name__, template_folder='templates',static_folder='static',static_url_path='/static')
app.register_blueprint(content)
app.register_blueprint(gsa)
app.register_blueprint(users)
app.register_blueprint(qr)
app.register_blueprint(devices)
app.register_blueprint(friends)
app.register_blueprint(t2audio)
app.register_blueprint(chat)



@app.route("/")
def toy():
    return render_template("toy.html")


if __name__ == '__main__':
    app.run("0.0.0.0", 8900, debug=True,ssl_context=(PEM,KEY))




