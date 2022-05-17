from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/countdown')
def countdown():
    countdown_list = ["%d" %i for i in range(10, 0, -1)]
    countdown_list.append("Пуск!")
    return '</br>'.join(countdown_list)

@app.route('/image')
def image():
    return f'''<img src="{url_for('static', filename='Patriot.png')}")
        alt="Здесь должна быть картинка, но ее нет">

        <img src="{url_for('static', filename='мем.png')}")
        alt="Здесь должна быть картинка, но ее нет">

        <img src="/static/Patriot.png"
         alt="здесь должна была быть картинка, но не нашлась">



        '''
        # 1. Какая функция понадобилась вам для размещения картинки?
        # Ответ: url_for()

        # 2. Добавьте еще одну картинку на вашу страницу. Но назовите файл русскими буквами. Посмотрите код 
        # страницы в браузере, что происходит с названием картинки, заданным русскими буквами? Почему?
        # Ответ:<img src="/static/%D0%BC%D0%B5%D0%BC.png") alt="Здесь должна быть картинка, но ее нет">

        # 3.Можно написать и вот так:
        # return '''<img src="/static/img/riana.jpg" alt="здесь должна была быть картинка, но не нашлась">'''
        # Однако этот вариант кода хуже с точки зрения дальнейшего сопровождения. Почему?
        # Ответ: Во-первых, URL могут измениться, и тогда нам придется везде их менять, а если где-то забудем,
        #  то это негативно скажется на отображении страниц сайта. Или же, URL могут генерироваться динамически
        #  и тогда мы в принципе не сможем их явно прописать. Наконец, один и тот же шаблон для разных приложений, 
        # возможно, должен подставлять разный URL, например, для подключения внешних CSS или JS файлов. 


@app.route('/sample_page')
def return_sample_page():
    return """<!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/main.css') }}" />    
    </head>
    <body>
        <h1> Hello </h1>
    </body>
    </html>"""
    # Не работает подключение css, но код правильный

@app.route('/bootstrap_sample')
def bootstrap():
    return render_template('bootstrap_sample.html')
    # Не подключается css, но js подключился

@app.route('/two_params/<username>/<int:number>')
@app.route('/greeting/<username>')
def greeting(username, number=0):
 return f'''<!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initialscale=1,
        shrink-to-fit=no">
        <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
        crossorigin="anonymous">
        
    </head>
    <body>
        <div>Это первый параметр и его тип: {str(type(username))[1:-1]}</div>
        <div>Это второй параметр и его тип: {str(type(number))[1:-1]}</div>
        
    </body>
    </html>
    '''

@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return render_template('form_sample.html')
    elif request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        print(request.form['class'])
        print(request.form['file'])
        print(request.form['about'])
        print(request.form.get('accept'))
        print(request.form['sex'])
        return "Форма отправлена"

enctype="multipart/form-data"
@app.route('/sample_file_upload', methods=['POST', 'GET'])
def sample_file_upload():
    if request.method == 'GET':
        return render_template('sample_file_upload.html')
    elif request.method == 'POST':
        f = request.files['file']
        f1 = request.files['file1']
        print(f.read()[0], f1.read()[0])
        return "Форма отправлена"


if __name__ == '__main__':
    app.run(debug=True, port=8999, host='127.0.0.1')