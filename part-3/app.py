from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schoolk1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELS
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    students = db.relationship('Student', backref='course', lazy=True)
    teachers = db.relationship('Teacher', backref='course', lazy=True)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    university = db.Column(db.String(150))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

# ROUTES
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)

@app.route('/teachers')
def teachers():
    all_teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=all_teachers)

# ADD COURSE
@app.route('/add-course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        new_course = Course(name=name, description=description)
        db.session.add(new_course)
        db.session.commit()
        flash('Course added!', 'success')
        return redirect(url_for('courses'))
    return render_template('add_course.html')

# EDIT COURSE
@app.route('/edit-course/<int:id>', methods=['GET', 'POST'])
def edit_course(id):
    course = Course.query.get_or_404(id)
    if request.method == 'POST':
        course.name = request.form['name']
        course.description = request.form.get('description', '')
        db.session.commit()
        flash('Course updated!', 'success')
        return redirect(url_for('courses'))
    return render_template('edit_course.html', course=course)

# DELETE COURSE
@app.route('/delete-course/<int:id>')
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted!', 'danger')
    return redirect(url_for('courses'))

# ADD TEACHER
@app.route('/add-teacher', methods=['GET', 'POST'])
def add_teacher():
    courses = Course.query.all()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course_id = int(request.form['course_id'])
        new_teacher = Teacher(name=name, email=email, course_id=course_id, university="XYZ University")
        db.session.add(new_teacher)
        db.session.commit()
        flash('Teacher added!', 'success')
        return redirect(url_for('teachers'))
    return render_template('add_teacher.html', courses=courses)

# EDIT TEACHER
@app.route('/edit-teacher/<int:id>', methods=['GET', 'POST'])
def edit_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    courses = Course.query.all()
    if request.method == 'POST':
        teacher.name = request.form['name']
        teacher.email = request.form['email']
        teacher.course_id = int(request.form['course_id'])
        db.session.commit()
        flash('Teacher updated!', 'success')
        return redirect(url_for('teachers'))
    return render_template('edit_teacher.html', teacher=teacher, courses=courses)

# DELETE TEACHER
@app.route('/delete-teacher/<int:id>')
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    flash('Teacher deleted!', 'danger')
    return redirect(url_for('teachers'))

# ADD STUDENT
@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    courses = Course.query.all()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course_id = int(request.form['course_id'])
        new_student = Student(name=name, email=email, course_id=course_id)
        db.session.add(new_student)
        db.session.commit()
        flash('Student added!', 'success')
        return redirect(url_for('index'))
    return render_template('add_student.html', courses=courses)

# EDIT STUDENT
@app.route('/edit-student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    courses = Course.query.all()
    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.course_id = int(request.form['course_id'])
        db.session.commit()
        flash('Student updated!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_student.html', student=student, courses=courses)

# DELETE STUDENT
@app.route('/delete-student/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted!', 'danger')
    return redirect(url_for('index'))

# INIT DB & SAMPLE DATA
def init_db():
    with app.app_context():
        db.create_all()
        if Course.query.count() == 0:
            sample_courses = [
                Course(name='Python Basics', description='Learn Python programming fundamentals'),
                Course(name='Web Development', description='HTML, CSS, JavaScript and Flask'),
                Course(name='Data Science', description='Data analysis with Python')
            ]
            db.session.add_all(sample_courses)
            db.session.commit()
            print("Sample courses added!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
