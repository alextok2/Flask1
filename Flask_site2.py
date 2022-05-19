from flask import Flask, render_template, url_for, request
import datetime


from data import db_session
from data.users import User
from data.news import News


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/index1')
def index1():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index1.html", news=news)


if __name__ == '__main__':
    db_session.global_init("db/blogs.sqlite")
    # user = User()
    # user.name = "Пользователь 5"
    # user.about = "Биография пользователя 5"
    # user.email = "email5@email.ru"
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()

    # user = db_sess.query(User).filter(User.id==1).first()#, User.email.not_ilike("%1%")).first()
    # for user in db_sess.query(User).filter((User.id>1) | (User.email.not_ilike("%1%"))):
    #     print(user.name)

    # user.name = "Измененное имя пользоватеся"
    # user.created_date = datetime.datetime.now()

    # db_sess.delete(user)


    # news = News(title="Первая новость", content="Уже вторая запись", user=user, is_private=False)
    # db_sess.add(news)

    # news = News(title="Личная запись", content="Эта запись личная", is_private=True)
    # user.news.append(news)
    # db_sess.commit()

    # for news in user.news:
    #     print(news)

    app.run(debug=True, port=8999, host='127.0.0.1') 