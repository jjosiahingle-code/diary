# Importing
from flask import Flask, render_template, request, redirect, session
# Connecting the database library
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Setting the secret key for the session
app.secret_key = 'my_top_secret_123'
# Establishing SQLite connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creating a DB
db = SQLAlchemy(app)
# Creating a table

class Card(db.Model):
    # Establishing entry fields
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Title
    title = db.Column(db.String(100), nullable=False)
    # Subtitle
    subtitle = db.Column(db.String(300), nullable=False)
    # Text
    text = db.Column(db.Text, nullable=False)
    # The card owner's email
    user_email = db.Column(db.String(100), nullable=False)

    # Outputting object and its ID
    def __repr__(self):
        return f'<Card {self.id}>'
    

# Assignment #1. Create the User table
class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


# Launching content page
@app.route('/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']
            
        # Assignment #4. Implement user verification
        users_db = User.query.all()
        for user in users_db:
            if form_login == user.email and form_password == user.password:
                session['user_email'] = user.email
                return redirect('/index')
        error = 'Incorrect login or password'
        return render_template('login.html', error=error)
        
        
    else:
        return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Assignment #3. Implement user recording
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


# Launching content page
@app.route('/index')
def index():
    # Assignment #4. Make sure user only sees their own cards
    email = session.get('user_email')
    cards = Card.query.filter_by(user_email=email).all()
    return render_template('index.html', cards=cards)

# Launching the card page
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Launching the card creation page
@app.route('/create')
def create():
    return render_template('create_card.html')

# The card form
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Assignment #4. Make card creation happen on behalf of the user
        email = session['user_email']
        card = Card(title=title, subtitle=subtitle, text=text, user_email=email)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.run(debug=True)
