IP = '127.0.0.1'
PORT = 80
SOCKET_TIMEOUT = 100
BASE_URL = './webroot'
DEFAULT_URL = '/index.html'

REDIRECTION_DICTIONARY = {
    '/css/doremon.css': '/css-moved-to-here/css/doremon.css'
}


def __calc_next(params):
    assert {'num'}.issubset(params.keys())
    assert params['num'].isdigit()
    num = int(params['num'])
    return f'{num + 1}'.encode()


def __calc_area(params):
    assert {'height', 'width'}.issubset(params.keys())
    assert params['height'].isdigit()
    assert params['width'].isdigit()
    height = int(params['height'])
    width = int(params['width'])
    res_str = f'{0.5 * height * width}'
    striped_res = res_str.rstrip('0').rstrip('.') if '.' in res_str else res_str
    return striped_res.encode()


ACTIONS = {
    '/calculate-next': __calc_next,
    '/calculate-area': __calc_area
}

RESPONSE_TYPES = {
    'html': 'text/html; charset=utf-8',
    'css': 'text/css; charset=utf-8',
    'js': 'text/javascript',
    'jpg': 'image/jpeg',
    'ico': 'image/x-icon',
    'gif': 'image/gif',
    'txt': 'text/plain'
}

STATUSES = {
    200: 'OK',
    302: 'Found',
    400: 'Bad Request',
    403: 'Forbidden',
    404: 'Not Found',
    500: 'Internal Server Error'
}

VALID_RESOURCES = {
    '/index.html': 'html',
    '/imgs/abstract.jpg': 'jpg',
    '/imgs/favicon.ico': 'ico',
    '/imgs/loading.gif': 'gif',
    '/js/box.js': 'js',
    '/js/jquery.min.js': 'js',
    '/js/submit.js': 'js',
    '/css-moved-to-here/css/doremon.css': 'css'
}
