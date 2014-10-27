from flask import Flask, render_template
from collections import namedtuple

app = Flask(__name__)


# class NavigationItem:
#     def __init__(self, href, caption):
#         self.href = href
#         self.caption = caption

NavigationItem = namedtuple("NavigationItem", ['href', 'caption'])


@app.route('/')
def main_page():
    return render_template('mainpage.html',
                           navigation=[NavigationItem("HREF", "CAPTION")])

if __name__ == '__main__':
    # app.debug = True
    app.run(debug=True)
