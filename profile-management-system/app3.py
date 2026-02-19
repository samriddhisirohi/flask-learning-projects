from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#@app.route('/')
#def home():
 #   return "App2 is running"



# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
#Which database to use and where it is located, Database file in current project folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
#Whether SQLAlchemy tracks object changes internally. 
# Avoids a warning

# Create SQLAlchemy instance
db = SQLAlchemy(app)
#SQLAlchemy is a class provided by Flask-SQLAlchemy
#👉 “Attach SQLAlchemy to my Flask app.”
#👉 “Connect my app with the database configuration.”
#👉 “Prepare database tools (models, tables, queries).”
#So db becomes your database object.

#Because now db gives you:
#db.Model → to create tables
#db.Column → to define columns
#db.Integer, db.String, etc.
#db.session → to insert/update/delete data
#db.create_all() → to create tables

# Define a model for the database
class Profile(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    first_name= db.Column(db.String(100),nullable= False)
    #It does not directly use raw SQL types like VARCHAR.
    #It uses Python types that map automatically to the correct database type.
    last_name= db.Column(db.String(100),nullable= False)
    age= db.Column(db.Integer, nullable= False)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Name : {self.first_name}, Age: {self.age}"



# function to render index page
@app.route('/')
def index():
    profiles = Profile.query.all()
    return render_template('index2.html', profiles=profiles)


#function to render add profile page
@app.route('/add_data')
def add_data():
        return render_template('add_profile.html')
    

@app.route('/add', methods=["POST"])
#➡ Defines a URL endpoint /add that accepts only POST requests.

def profile(): #➡ Function that runs when /add route is triggered.
    first_name = request.form.get("first_name")
    #➡ Retrieves the value of first_name from submitted form data.
    last_name = request.form.get("last_name")
    #➡ Retrieves the value of last_name from submitted form data.
    age = request.form.get("age")
    #➡ Retrieves the value of age from submitted form data.

    if first_name != '' and last_name != '' and age is not None:
        #➡ Checks that all required form fields are filled before saving.
        p = Profile(first_name=first_name, last_name=last_name, age=age)
        #➡ Creates a new Profile object (new database row) with the given data
        db.session.add(p)
        #➡ Adds the new object to the database session (prepares it for insertion).
        db.session.commit()
        #➡ Permanently saves the new record into the database.
        return redirect('/')
    #➡ Redirects the user to the home page after successful insertion.

    else: #➡ Runs if validation fails.
        return redirect('/')
    #➡ Redirects user back to home page if form data is invalid.

@app.route('/delete/<int:id>')
def erase(id):
    p = Profile.query.get_or_404(id)
    #➡ Retrieves the Profile object with the given id or returns 404 if not found.
    db.session.delete(p)
    #➡ Marks the retrieved object for deletion from the database.
    db.session.commit()
    #➡ Permanently deletes the record from the database.
    return redirect('/')
    #➡ Redirects user back to home page after deletion.

# Run the app and create database
if __name__ == '__main__':
    with app.app_context():  # Needed for DB operations to work properly
        db.create_all()      # Creates the database and tables
    app.run(debug=True)