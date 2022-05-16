from http.server import HTTPServer, CGIHTTPRequestHandler

def simple_web_server():
    server_address = ('', 8888)
    handler = CGIHTTPRequestHandler
    handler.cgi_directories = ['/cgi']
    server = HTTPServer(server_address, handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

    # 1. На каком адресе «поднят» ваш веб-сервер? Какой порт он использует? 
    # Ответ: на localhost'e. Порт 8888.

    # 2. Перейдите по адресу localhost:8000 (или 127.0.0.1:8080). Что происходит? Однозначны ли эти адреса?
    # Ответ: Мы попали на директорий файлов на нашем сервере через клиент(браузер). Да, localhost и 127.0.0.1 одназначны, localhost является виртуальным хостом адреса 127.0.0.1

    # 3. Что такое порт? Для чего он нужен?
    # Ответ: Порт - Просто идентификатор, чтобы определить получателя. Нужен чтобы разделить IP-адрес

    # 4. Какое значение может принимать номер порта?
    # Ответ: любой от 0 до 65535, но лучше от 1024, т.к. это системные порты

    # 5. Какие номера портов чаще всего используются для протокола HTTP? (назовите минимум 3)
    # Ответ: 80, 81, 443 https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BF%D0%BE%D1%80%D1%82%D0%BE%D0%B2_TCP_%D0%B8_UDP

    # 6. Можно ли запустить этот код в облачном сервисе (например, Google Colab). Будет ли он работать
    # точно также, как при запуске на локальном ПК (сервере)?
    # Ответ: Будет, но доступ мы к нему через локалхост не получим

def first_web_page():
    pass
    # 1. Перейдите по адресу localhost:8000/cgi-bin/index.py и посмотрите на результат выполнения вашего
    # скрипта. Что происходит?
    # Ответ: 
    # print("Content-type: text/html; charset=utf-8")
    # print()
    # print("<h1>Hello, world!</h1>")
    # 
    # Через python3 -m http.server --cgi 8000 получилось получить html-страничку

    # 2. А что пишет вам веб-сервер?
    # 127.0.0.1 - - [16/May/2022 20:53:02] "GET / HTTP/1.1" 200 -
    # 127.0.0.1 - - [16/May/2022 20:53:04] "GET /cgi-bin/ HTTP/1.1" 200 -
    # 127.0.0.1 - - [16/May/2022 20:53:05] "GET /cgi-bin/index.py HTTP/1.1" 200 -
list1 = ["%d\n" %i for i in range(10, 0, -1)]
list1.append("Пуск")
print(*list1)
# print(range(10, 0, -1))
