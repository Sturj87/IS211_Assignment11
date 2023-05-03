from flask import Flask, render_template, request, redirect
import re
import pickle
import os

app=Flask(__name__)

to_do_items = []

added = False
@app.route('/')
def index():
    global added
    global to_do_items
    if os.path.exists('to_do_data.pkl') and added == False:
        with open('to_do_data.pkl', 'rb') as file:
            to_do_items.extend(pickle.load(file))
            added = True
    error = request.args.get('error')
    return render_template("index.html", items=to_do_items, error=error)

@app.route('/save', methods=['POST'])
def save():
    file = open("to_do_data.pkl", "wb")
    pickle.dump(to_do_items, file)
    return redirect('/')
@app.route('/submit', methods=['POST'])
def submit():
    # retrieve the data from the submitted form
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']


    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        error_msg = 'Invalid email address'
        return redirect(f'/?error={error_msg}')

    elif not priority in ('Low', 'Medium', 'High'):
        error_msg = 'Invalid Priority Level'
        return redirect(f'/?error={error_msg}')

    # append the new to-do item to the global list
    to_do_items.append((task, email, priority))

    # redirect back to the index page
    return redirect('/')

# @app.route('/delete/<int:item_index>', methods=['POST'])
# def delete(item_index):
#     global to_do_items
#     if item_index >= 0 and item_index < len(to_do_items):
#         to_do_items.pop(item_index)
#     return redirect('/')

@app.route('/clear', methods=['POST'])
def clear():
    to_do_items.clear()
    return redirect('/')



if __name__=='__main__':
    app.run()

