import os
import secrets
from flask import Flask, render_template, request, redirect, url_for
from models import db, Todo
from forms import TodoForm
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max size

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TodoForm()
    if form.validate_on_submit():
        image_filename = None
        if form.image.data:
            image_file = form.image.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(image_file.filename)
            image_filename = random_hex + f_ext
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)

        new_todo = Todo(title=form.title.data, image_file=image_filename)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('index'))

    todos = Todo.query.order_by(Todo.date_created.desc()).all()
    return render_template('index.html', form=form, todos=todos)

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    if todo.image_file:
        try:
             os.remove(os.path.join(app.config['UPLOAD_FOLDER'], todo.image_file))
        except:
             pass 
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
