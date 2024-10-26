import sys
import os
from flask import Flask, request, redirect, url_for, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Append the current directory to the system path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create a single instance of SQLAlchemy
db = SQLAlchemy()

app = Flask(__name__)  # Change 'name' to '__name__'

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gossip.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db instance with the app
db.init_app(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # Change 'repr' to '__repr__'
        return f'<Comment {self.id}: {self.content}>'

@app.route('/')
def index():
    comments = Comment.query.order_by(Comment.date_posted.desc()).all()
    return render_template('index.html', comments=comments)

# Route to handle new comment submissions
@app.route('/submit', methods=['POST'])
def submit_comment():
    content = request.form.get('content')
    
    if content:
        new_comment = Comment(content=content)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))

# Create the database tables (Run this part once to initialize the database)
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':  # Change 'name' to '__name__'
    app.run(debug=True)
