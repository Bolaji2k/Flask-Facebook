from flask import render_template




def create_view(app):

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login')
    def login():
        return render_template('check.html')
