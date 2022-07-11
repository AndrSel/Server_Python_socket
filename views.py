def home():
    with open('./home.html', 'r') as template:
        return template.read()

def page():
    with open('./page.html', 'r') as template:
        return template.read()