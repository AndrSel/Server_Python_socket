import socket
import views

URLS = {
    '/home.html': views.home(),
    '/page.html': views.page()
}


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 4000))
    server.listen(10)
    print('Server working ...')
    while True:
        try:
            client, address = server.accept()
        except KeyboardInterrupt:
            print('exit')
            server.close()
        except socket.error:
            print('socket.error')
        else:
            try:
                data = client.recv(1024).decode('utf-8')
                print(data)
                print()
                # print(data.split(' ')[1])
                print()
                # content = 'Hello'.encode('utf-8')
                content = load_pages(data)
                client.send(content)
                client.close()
            except socket.error:
                print('socket.error')


def parse_requset(request):
    '''
    Парсит запрос
    '''
    method = request.split(' ')[0]
    url = request.split(' ')[1]
    return (method, url)


def generate_headers(method, url):
    '''
    Генерирует запрос
    '''
    if not method == 'GET':
        #return ('HTTP/1.1 405 Method not allowed\n\n', 405)
        return ('HTTP/1.1 405 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n', 405)
    if not url in URLS.keys():
        #return ('HTTP/1.1 404 Method not allowed\n\n', 404)
        return ('HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n', 404)

    #return ('HTTP/1.1 200 OK\n\n', 200)
    return ('HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n', 200)


def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Page not found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method</p>'
    return URLS[url]


def load_pages(data):
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    method, url = parse_requset(data)
    headers, code = generate_headers(method, url)

    '''
    try:
        with open(f'.{link}', 'rb') as file:
            otvet = file.read()
        return HDRS.encode('utf-8') + otvet
    except FileNotFoundError:
        return (HDRS_404 + 'Page not found').encode('utf-8')
    '''
    return (headers+ generate_content(code, url)).encode('utf-8')


if __name__ == '__main__':
    start_server()
