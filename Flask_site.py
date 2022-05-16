from flask import Flask, render_template, url_for

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
        '''

if __name__ == '__main__':
    app.run(port=8999, host='127.0.0.1')