from flask import Flask, render_template, url_for, request

from data import db_session
from data.users import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')




if __name__ == '__main__':

    db_session.global_init("db/blogs.sqlite")
    user = User()
    user.name = "Пользователь 1"
    user.about = "биография пользователя 1"
    user.email
    # app.run(debug=True, port=8999, host='127.0.0.1') 