from functools import wraps
from flask import Flask, flash, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user
import random

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/hospital_db"
db.init_app(app)

app.secret_key = 'kevin_pronoy'

##login
login_manager = LoginManager(app)

# Set the default login view
@login_manager.unauthorized_handler
def unauthorized():
    # Redirect to the appropriate login page based on the user's role
    flash("You need to login first.", "warning")
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Creating db models (tables)

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    def get_id(self):
        return self.user_id

class Patients(db.Model):
    __tablename__ = 'patients'
    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date)

class TriageStaff(db.Model):
    __tablename__ = 'triage_staff'
    staff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    role_desc = db.Column(db.String(50), nullable=False)

class Queue(db.Model):
    __tablename__ = 'queue'
    queue_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    severity = db.Column(db.Integer, nullable=False)
    wait_time = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='waiting')  # New column

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/patient_signup', methods=['GET', 'POST'])
def patient_signup():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        phone_number = request.form['phoneNumber']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        role = 'Patient'
        
        # Check if the user already exists
        existing_user_query = text("SELECT * FROM users WHERE username = :username OR email = :email")
        result = db.session.execute(existing_user_query, {'username': username, 'email': email}).first()

        if result:
            flash('User with that username or email already exists.', 'danger')
            return redirect(url_for('patient_signup'))

        # Insert into Users table
        insert_user_query = text("""
            INSERT INTO users (username, password, email, role) 
            VALUES (:username, :password, :email, :role);
        """)
        
        db.session.execute(insert_user_query, {'username': username, 'password': password, 'email': email, 'role': role})
        db.session.commit()

        # Fetch the newly created user ID again
        new_user_id_result = db.session.execute(existing_user_query, {'username': username, 'email': email}).first()
        new_user_id = new_user_id_result[0]  # Assuming user_id is the first column in the SELECT result

        # Insert into Patients table
        insert_patient_query = text("""
            INSERT INTO patients (user_id, first_name, last_name, phone_number, address) 
            VALUES (:user_id, :first_name, :last_name, :phone_number, :address);
        """)
        
        db.session.execute(insert_patient_query, {
            'user_id': new_user_id, 
            'first_name': first_name, 
            'last_name': last_name, 
            'phone_number': phone_number, 
            'address': address
        })
        db.session.commit()
        
        flash('Patient signup successful!', 'success')
        return redirect(url_for('patient_login'))

    return render_template('patient_signup.html')


@app.route('/staff_signup', methods=['GET', 'POST'])
def staff_signup():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        phone_number = request.form['phoneNumber']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        role = 'Staff'
        
        # Check if the user already exists
        existing_user_query = text("SELECT * FROM users WHERE username = :username OR email = :email")
        result = db.session.execute(existing_user_query, {'username': username, 'email': email}).first()

        if result:
            flash('User with that username or email already exists.', 'danger')
            return redirect(url_for('staff_signup'))

        # Insert into Users table
        insert_user_query = text("""
            INSERT INTO users (username, password, email, role) 
            VALUES (:username, :password, :email, :role);
        """)
        
        db.session.execute(insert_user_query, {'username': username, 'password': password, 'email': email, 'role': role})
        db.session.commit()

        # Fetch the newly created user ID again
        new_user_id_result = db.session.execute(existing_user_query, {'username': username, 'email': email}).first()
        new_user_id = new_user_id_result[0]  # Assuming user_id is the first column in the SELECT result

        # Insert into TriageStaff table
        insert_staff_query = text("""
            INSERT INTO triage_staff (user_id, first_name, last_name, phone_number, address) 
            VALUES (:user_id, :first_name, :last_name, :phone_number, :address);
        """)
        
        db.session.execute(insert_staff_query, {
            'user_id': new_user_id, 
            'first_name': first_name, 
            'last_name': last_name, 
            'phone_number': phone_number, 
            'address': address
        })
        db.session.commit()
        
        flash('Staff signup successful!', 'success')
        return redirect(url_for('staff_login'))

    return render_template('staff_signup.html')


@app.route('/patient_login', methods=['GET', 'POST'])
def patient_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()

        if user and user.password == password and user.role == 'Patient':
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('patient_dashboard'))
        else:
            flash('Invalid credentials or not a patient.', 'danger')

    return render_template('patient_login.html')

@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()

        if user and user.password == password and user.role == 'Staff':
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('staff_dashboard'))
        else:
            flash('Invalid credentials or not a staff member.', 'danger')

    return render_template('staff_login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "success")
    return redirect(url_for('index'))

@app.route("/patient_dashboard", methods=['GET', 'POST'])
@login_required
def patient_dashboard():
    if current_user.role != 'Patient':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        severity = request.form['severity']
        wait_time = random.randint(20, 50)

        insert_queue_query = text("""
            INSERT INTO queue (patient_id, severity, wait_time, status) 
            VALUES (:patient_id, :severity, :wait_time, 'waiting');
        """)
        
        try:
            db.session.execute(insert_queue_query, {
                'patient_id': current_user.user_id,
                'severity': severity,
                'wait_time': wait_time
            })
            db.session.commit()
            
            flash('Queue request submitted successfully!', 'success')
        except Exception as e:
              db.session.rollback()
              flash('An error occurred trying to add queue', 'danger')
              print(e)

    
    # Fetch current patient info
    patient = Patients.query.filter_by(user_id=current_user.user_id).first()
    
    # Fetch queue status
    queue_status = Queue.query.filter_by(patient_id=current_user.user_id).all()

    return render_template('patient_dashboard.html', patient=patient, queue_status=queue_status)


@app.route("/staff_dashboard", methods=['GET', 'POST'])
@login_required
def staff_dashboard():
    if current_user.role != 'Staff':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        queue_id = request.form['queue_id']
        
        update_queue_query = text("""
            UPDATE queue SET status='complete' WHERE queue_id=:queue_id
        """)
        
        try:
            db.session.execute(update_queue_query, {'queue_id': queue_id})
            db.session.commit()
            
            # Reduce wait time of all other waiting patients by 5 minutes
            reduce_wait_time_query = text("""
                UPDATE queue SET wait_time = wait_time - 5 WHERE status = 'waiting'
            """)
            db.session.execute(reduce_wait_time_query)
            db.session.commit()
            
            flash('Patient admitted and wait times updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the queue.', 'danger')
            print(e)

    queues = Queue.query.all()
    for queue in queues:
        print(f'Queue ID: {queue.queue_id}, Status: {queue.status}')  # Debugging print statement

    return render_template('staff_dashboard.html', queues=queues)

if __name__ == '__main__':
    app.run(debug=True)
