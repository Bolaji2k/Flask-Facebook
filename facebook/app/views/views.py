from flask import render_template, request, session
from flask import make_response
from flask import url_for, flash
from flask import redirect
from ..models.models import User, db
from werkzeug.security import generate_password_hash



def create_view(app):
    def is_authenticated():
        email = session.get('email', None)
        if email == None:
           return redirect(url_for('login'))

    @app.route('/')
    def index():
        email = session.get('email', None)
        if email == None:
           return redirect(url_for('login'))

        user = User.query.filter_by(email=session['email']).first()
        friends = user.friends

        return render_template('index.html', user=user, friends=friends)
    
    @app.route('/login', methods=['POST', 'GET'])
    def login():
        error = None
        if request.method == 'POST':
            form = request.form
            email = form['email'].lower()
            password = form['password'].strip()
            
            user = User.query.filter_by(email=email).first()

            if user:
                confirmation = user.verify_password(password)

                if confirmation:
                    session['email'] = email

                    return redirect(url_for('index'))
                else:
                    flash('Incorrect password')
            else:
              flash("invalid email")
              error = "invalid"
              return redirect(url_for('login',error=error))


        if request.method == 'GET':
            session['email'] = None

        

        return render_template('login.html')
    
    
    @app.route('/registration', methods=['GET','POST'])
    def registration():
        if request.method == 'POST':
            form = request.form

            first_name = form['first_name']
            last_name = form['last_name']
            gender = form['gender']
            age = form['age']
            email = form['email'].lower()
            password = form['password'].strip()

            user = User.query.filter_by(email=email).first()

            if user:
                return redirect(url_for('login', page=1,error='type2'))
            else:
                new_user = User(
                    first_name=first_name, 
                    last_name=last_name,
                    gender=gender,
                    age=age,
                    email=email,
                            )
                
                new_user.password = password
                
                db.session.add(new_user)
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    flash(f"""{str(e)}""")
                    return redirect(url_for('login', page=1))

                session['email'] = email
                #flash("Welcome your account has been created")
                return redirect(url_for('index'))
        return render_template('login.html')
    
    @app.route('/friends')
    def friends():
        email = session.get('email', None)
        if email == None:
           return redirect(url_for('login'))
        suggestions = []
        users = User.query.all()
        user = User.query.filter_by(email=email).first()
        for i in users:
            if i.email != user.email:
               if i not in user.friends: 
                     if i not in user.requests:
                             if i in user.sentrequests:
                                 pass
                             else:
                               suggestions.append(i)
        requests = user.sentrequests
        friends = user.friends

        return render_template('friends.html', suggestions=suggestions, friends=friends, requests=requests)
    
    @app.route('/addfriend/<user_id>')
    def addfriend(user_id):
        email = session.get('email', None)
        user = User.query.filter_by(email=email).first()
        friend = User.query.filter_by(id=user_id).first()
        friend.sentrequests.append(user)
        user.requests.append(friend)
        db.session.commit()
        flash("Friend request sent!")
        return redirect(url_for('friends'))
    
    @app.route('/acceptfriend/<user_id>')
    def acceptfriend(user_id):
        email = session.get('email', None)
        user = User.query.filter_by(email=email).first()
        friend = User.query.filter_by(id=user_id).first()
        user.sentrequests.remove(friend)
        user.friends.append(friend)
        friend.friends.append(user)
        db.session.commit()
        flash("New friend added")
        return redirect(url_for('friends'))
    
    @app.route('/groups')
    def groups():
        email = session.get('email', None)
        if email == None:
           return redirect(url_for('login'))
        return render_template('your-groups.html')
    
    @app.route('/forgot_password', methods=['GET','POST'])
    def forgot():
        if request.method == 'POST':
            error = None
            form = request.form
            email = form['email'].lower()
            password = form['password'].strip()
            user = User.query.filter_by(email=email).first()
            if user:
              user.password_hash = generate_password_hash(password)
              flash("You have successfully changed your password!")
              flash("You can now login")
              db.session.commit()
            else:
              flash("user does not exist")
              error = "invalid"
              return redirect(url_for('login',error=error,page=2))


        return redirect(url_for('login'))

