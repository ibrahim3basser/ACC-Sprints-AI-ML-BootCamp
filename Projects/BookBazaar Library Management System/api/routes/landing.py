from flask import Blueprint 
landing = Blueprint('landing', __name__)

@landing.route('/', methods=['GET'])
def home():

    return """
    <html>
        <head>
            <title>BookBazzar</title>
        </head>
        <body style="text-align: center; margin-top: 100px;">
            <h1>Hello from BookBazzar!</h1>
            <p>That's our relational data schema (SQLite3):</p>
            <img src="/static/SC1.png" style="max-width: 65%; height: auto;" alt="Screenshot of the schema">
        </body>
    </html>
    """,200
