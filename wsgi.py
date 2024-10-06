from pywebio.platform.flask import webio_view
from pywebio import start_server
from flask import Flask

# Import your main function from your app
from app import main

app = Flask(__name__)

# Add a route for your web app
app.add_url_rule('/', 'webio_view', webio_view(main), methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run()
