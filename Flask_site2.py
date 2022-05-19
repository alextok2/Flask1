from flask import Flask, render_template, url_for, request, redirect, make_response
import datetime


from data import db_session
from data.users import User
from data.news import News
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'


@app.route('/login')
@app.route('/index1')
def index1():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index1.html", news=news)


@app.route('/cookie_test', methods=['POST', 'GET'])
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(f'''
                            Вы пришли на эту страницу {visits_count + 1} раз
                            <form method="post" action="/cookie_test">

                                <input type="submit" value="Сбросить" name="submit_button">
                                <input type="radio" checked name="radio_reset" style="display:none;">     
                            </form>
                            ''')

        if request.method == 'GET':
            res.set_cookie("visits_count", str(visits_count + 1), max_age=60 * 60 * 24 * 365 * 2)
            print("Штука")
            
        elif request.method == 'POST':
            if request.form.get('radio_reset') == "on":
                res.set_cookie("visits_count", "0")
                visits_count = int(request.cookies.get("visits_count", 0))


        # db_sess = db_session.create_session()
        # news = db_sess.query(News).filter(News.is_private != True)
        # res = make_response(render_template("index1.html", news=news))
        # res.set_cookie("visits_count", '1', max_age=60 * 60 * 24 * 365 * 2)
        
    else:
        res = make_response("Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1', max_age=60 * 60 * 24 * 365 * 2)
    return res
   

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form, message="Такой пользователь уже есть")


        user = User(
                name=form.name.data,
                email=form.email.data,
                about=form.about.data
                )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')


    return render_template('register.html', title='Регистрация', form=form)


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