from flask import render_template, request, session
from flask import make_response
from flask import url_for, flash
from flask import redirect
from ..models.models import User, Group, db
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
    
    @app.route('/profile/<id>', methods=['GET','POST'])
    def profile(id):
        email = session.get('email', None)
        if email == None:
           return redirect(url_for('login'))
        user = User.query.filter_by(id=id).first()

        if request.method == 'POST':
            form = request.form

            first_name = form['first_name']
            last_name = form['last_name']
            gender = form['gender']
            age = form['age']
            email = form['email'].lower()
            password = form['password'].strip()

            user = User.query.filter_by(email=email).first()
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
            
            return redirect(url_for('index'))
        return render_template('profile.html', user=user)
    
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
    
    @app.route('/removefriend/<user_id>')
    def removefriend(user_id):
        email = session.get('email', None)
        user = User.query.filter_by(email=email).first()
        friend = User.query.filter_by(id=user_id).first()
        if user in friend.sentrequests:
          friend.sentrequests.remove(user)
        if friend in user.requests:
          user.requests.remove(friend)
        user.friends.remove(friend)
        friend.friends.remove(user)
        db.session.commit()
        flash("User has been removed from your friends!")
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
    
    @app.route('/group/<id>', methods=['GET','POST'])
    def group(id):
        email = session.get('email', None)
        if email == None:
           return redirect(url_for('login'))
        user = User.query.filter_by(email=email).first()
        group = Group.query.filter_by(id=id).first()
        suggestions = []
        users = User.query.all()
        for i in users:
            if i not in group.members:
              if i not in group.grouprequests:
                suggestions.append(i)



        if request.method == 'POST':
            form = request.form

            name = form['group_name']
            user = User.query.filter_by(email=email).first()
            
        return render_template('group.html', group=group, user=user, suggestions=suggestions)
    
    @app.route('/groups', methods=['GET','POST'])
    def groups():
        email = session.get('email', None)
        if email == None:
           return redirect(url_for('login'))
        
        if request.method == 'POST':
            form = request.form

            name = form['group_name']
            user = User.query.filter_by(email=email).first()

            new_group = Group(
                name=name, 
                        )
            new_group.admin.append(user)
            new_group.members.append(user)
                
            db.session.add(new_group)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(f"""{str(e)}""")
                return redirect(url_for('groups', page=1))

            flash("your group has been created")
            return redirect(url_for('groups'))
        
        user = User.query.filter_by(email=email).first()
        groups = user.member_of


        return render_template('your-groups.html', groups=groups, user=user)
    
    @app.route('/discovergroups', methods=['GET','POST'])
    def discovergroups():
        email = session.get('email', None)
        if email == None:
           return redirect(url_for('login'))
        
        groups = []
        allgroups = Group.query.all()
        user = User.query.filter_by(email=email).first()
        for i in allgroups:
            if i not in user.member_of:
              if i not in user.grouprequests_of:
                groups.append(i)
        
    
        return render_template('discover_group.html', groups=groups)
    
    @app.route('/joingroup/<id>', methods=['GET','POST'])
    def joingroup(id):
        email = session.get('email', None)
        if email == None:
           return redirect(url_for('login'))
        user = User.query.filter_by(email=email).first()
        group = Group.query.filter_by(id=id).first()
        group.grouprequests.append(user)

        db.session.commit()
        flash("Your join request has been submitted!")
        return redirect(url_for('discovergroups'))
    
    @app.route('/accepttogroup/<group_id>/<user_id>', methods=['GET','POST'])
    def accepttogroup(group_id, user_id):
        email = session.get('email', None)
        if email == None:
           return redirect(url_for('login'))
        user = User.query.filter_by(id=user_id).first()
        group = Group.query.filter_by(id=group_id).first()
        if group:
            if user:
                group.grouprequests.remove(user)
                group.members.append(user)
                db.session.commit()
                flash("New member added!")
                return redirect(url_for('group', id=group_id))
            
        return redirect(url_for('group', id=group_id))
        
    @app.route('/addtogroup/<group_id>/<user_id>', methods=['GET','POST'])
    def addtogroup(group_id, user_id):
        email = session.get('email', None)
        if email == None:
           return redirect(url_for('login'))
        user = User.query.filter_by(id=user_id).first()
        group = Group.query.filter_by(id=group_id).first()
        if group:
            if user:
                if user in group.grouprequests:
                    group.grouprequests.remove(user)
                    group.members.append(user)
                    db.session.commit()
                    flash("New member added!")
                    return redirect(url_for('group', id=group_id))
                else:
                    group.members.append(user)
                    db.session.commit()
                    flash("New member added!")
                    return redirect(url_for('group', id=group_id))
                
        return redirect(url_for('group', id=group_id))
    
    @app.route('/removemember/<group_id>/<user_id>', methods=['GET','POST'])
    def removemember(group_id, user_id):
        email = session.get('email', None)
        if email == None:
           return redirect(url_for('login'))
        user = User.query.filter_by(id=user_id).first()
        group = Group.query.filter_by(id=group_id).first()
        if group:
            if user:
                group.members.remove(user)
                db.session.commit()
                flash("User removed from group!")
                return redirect(url_for('group', id=group_id))
            else:
                flash("user does not exist")
                return redirect(url_for('group', id=group_id))
        return redirect(url_for('group', id=group_id))
        
 
        

    

    
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

