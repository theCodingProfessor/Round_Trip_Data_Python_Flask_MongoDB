from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

# MongoDB Connection settings
client = MongoClient('mongodb://localhost:27017/')
db = client['with_flask']
collection = db['for_text']

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/results')
def result():
    function_data = db.for_text.find()
    return render_template('results.html', page_data=function_data)


@app.route('/success', methods=['GET'])
def get_success():
    return render_template('success.html')


@app.route('/success', methods=['POST'])
def post_success():
    # data = dict()
    user_name = request.form['user_name']
    pass_phrase = request.form['pass_phrase']
    user_role = request.form['read_write']
    data = {
        'user_name': user_name,
        'pass_phrase': pass_phrase,
        'user_role': user_role,
        }
    # Insert data into MongoDB collection
    collection.insert_one(data)
    # Redirect or render a response
    return render_template('success.html', user=user_name, password=pass_phrase, role=user_role)


@app.route('/form')
def web_form():
    return render_template('web_form.html')


@app.route('/delete/<string:id>')
def delete(document_id):
    # Delete document from MongoDB collection
    db.for_text.delete_one({'_id': ObjectId(document_id)})
    return redirect(url_for('get_success'))


if __name__ == '__main__':
    app.run()
