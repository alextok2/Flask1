from flask import Flask, render_template, url_for, request
import datetime


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
    # user = User()
    # user.name = "Пользователь 5"
    # user.about = "Биография пользователя 5"
    # user.email = "email5@email.ru"
    db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()

    user = db_sess.query(User).filter(User.id>1, User.email.not_ilike("%1%")).first()
    # for user in db_sess.query(User).filter((User.id>1) | (User.email.not_ilike("%1%"))):
    #     print(user.name)

    user.name = "Измененное имя пользоватеся"
    user.created_date = datetime.datetime.now()

    # db_sess.delete(user)
    db_sess.commit()


    # app.run(debug=True, port=8999, host='127.0.0.1') 