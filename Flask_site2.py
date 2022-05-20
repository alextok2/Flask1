# from nis import cat
from flask import Flask, render_template, url_for, request, redirect, make_response, session, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime
import json
from flask_restful import Api

from data import news_resources 
from data import db_session
from data.users import User
from data.news import News
from data.category import Category
from forms.user import RegisterForm, LoginForm
from forms.news import NewsForm
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
api = Api(app)

api.add_resource(news_resources.NewsListResource, '/api/news')
api.add_resource(news_resources.NewsResource, '/api/news/<int:news_id>')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/')
@app.route('/index1')
def index1():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
    else:
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
            
        elif request.method == 'POST':
            if request.form.get('radio_reset') == "on":
                res.set_cookie("visits_count", "0")
                visits_count = int(request.cookies.get("visits_count", 0))

        # Без js получаться только костыли

    else:
        res = make_response("Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1', max_age=60 * 60 * 24 * 365 * 2)
    return res
   

@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    if visits_count >= 10:
        session.pop('visits_count', None)
    return make_response(f"Вы пришли на эту страницу {visits_count + 1} раз")

@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    db_sess = db_session.create_session()
    categories = [(c.id, c.name) for c in db_sess.query(Category).all()]
    form.category.choices = categories
    if form.validate_on_submit():
        

        category = Category()
        news = News()
        
        category.id = form.category.data

        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        
        news.categories.append(category)
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
    form=form)

# @app.route('/api/news/<int:id>')
# def api_news(id):
#     db_sess = db_session.create_session()
#     news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
#     if news:
#         data = {"title":news.title, "content":news.content, "user_id":news.user_id, "is_private":news.is_private}

#         json_dump = json.dumps(data)
#         return json_dump
#     return "Такой новости нет"

@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    db_sess = db_session.create_session()
    categories = [(c.id, c.name) for c in db_sess.query(Category).all()]
    form.category.choices = categories
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private

        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
        
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data

            new_category_id = form.category.data
            for categ in news.categories: 
                old_category_id = categ.id
                old_category_name = categ.name
            
            category = Category()

            if old_category_id != new_category_id:
                category.id = old_category_id
                category.name = old_category_name
                news.categories.remove(category)
                #news.categories.remove(category) не работает

                category.id = new_category_id
                news.categories.append(category)

            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html', title='Редактирование новости', form=form)

@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')



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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)




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
    #news.categories.remove(category)

    app.run(debug=True, port=8999, host='127.0.0.1') 