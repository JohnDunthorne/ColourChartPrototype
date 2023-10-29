from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class KeyValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(100), nullable=False)

db.create_all()

@app.route('/')
def registry():
    key_values = KeyValue.query.all()
    return render_template('registry.html', key_values=key_values)

@app.route('/register', methods=['POST'])
def register():
    key = request.form['key']
    value = request.form['value']
    if key and value:
        new_key_value = KeyValue(key=key, value=value)
        db.session.add(new_key_value)
        db.session.commit()
    return redirect(url_for('registry'))

@app.route('/deregister/<int:id>')
def deregister(id):
    key_value = KeyValue.query.get(id)
    if key_value:
        db.session.delete(key_value)
        db.session.commit()
    return redirect(url_for('registry'))

if __name__ == '__main__':
    app.run(debug=True)
