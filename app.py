from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)

# Initialize database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Class for schema
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(800), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Main function
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Create database tables
with app.app_context():
    db.create_all()
    print("Database tables created.")

# Home Page
@app.route('/', methods=['GET', 'POST'])
def Maintodopage():
    # Check for "submit button with post-method"
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        # Create a new Todo object and add it to the database session
        new_todo = Todo(title=title, desc=desc)
        db.session.add(new_todo)
        db.session.commit()
        print('Post request received. Todo added to the database.')

    allTodo = Todo.query.all()
    # Render templates and attach with return statements
    return render_template('index.html', allTodo=allTodo)

# CRUD OPERATIONS FOR DATABASE
# Folder 1 of todo app
@app.route('/show')
def showtodo():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'This is main todo page'

# Folder 2 of todo app
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo_to_update = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        todo_to_update.title = request.form['title']
        todo_to_update.desc = request.form['desc']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', todo=todo_to_update)

# Folder 3 of todo app
@app.route('/delete/<int:sno>')
def delete(sno):
    todo_to_delete = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo_to_delete)
    db.session.commit()
    # Return to main page
    return redirect("/")

# Run app here
if __name__ == "__main__":
    app.run(debug=True, port=8000)
