from html import escape


def deliver_file_by_name(file_name):

    result = ""
    try:
        file = open(file_name, 'rb')
        result = file.read()
        file.close()
    except OSError:
        print("file does not exist")

    return result


def make_about_page():
    about_html = b""" <html> error 404. Page About does not exist </html>"""
    file_name = "about.html"

    response_page = deliver_file_by_name(file_name)
    if not response_page:
        response_page = about_html

    return response_page


def make_contact_page():
    contact_html = b""" <html> error 404. Page Contact does not exist </html>"""
    file_name = "contact.html"

    response_page = deliver_file_by_name(file_name)
    if not response_page:
        response_page = contact_html

    return response_page


def make_home_page():
    response_page = b""" <html> Still working on it </html>"""
    return response_page


def parse_environ(environ):
    d = environ['REQUEST_URI']
    page_route = escape(d)
    return page_route


def define_body(page_route):
    if page_route == '/about/':
        response_body = make_about_page()

    elif page_route == '/contact/':
        response_body = make_contact_page()

    else:
        response_body = make_home_page()
    return response_body


def application(environ, start_response):
    page_route = parse_environ(environ)
    response_body = define_body(page_route)

    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'),
                        ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]


