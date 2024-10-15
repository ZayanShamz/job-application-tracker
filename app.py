from flask import Flask, request, render_template, url_for, redirect, session
from db_setup import init_db
import sqlite3

app = Flask(__name__)

app.secret_key = 'magni_sit_nobis_aspernatur'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM login WHERE username=? AND password=?', (username, password))
        res = cursor.fetchone()
        print(res)
        if res:
            session['username'] = res[1]
            session['login_id'] = res[0]
            conn.close()
            return redirect(url_for('home'))
        else:
            conn.close()
            return "<script>alert('Invalid Credentials');window.location='/'</script>"

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO login (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()
        conn.close()
        return "<script>alert('Registration Succesful');window.location='/'</script>"
    
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    user = session['username']
    lid = session['login_id']
    print('Welcome', user)
    if request.method == 'POST':
        company_name = request.form['company']
        job_title = request.form['jobTitle']
        job_description = request.form['description']
        job_requirements = request.form['requirement']
        platform = request.form['platform']
        date = request.form['date']
        print(f'company : {company_name}\n job_title: {job_title}\n job_description: {job_description}\n  job requirments: {job_requirements}\n platform: {platform}\n date: {date}')
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO jobs (login_id, company_name, job_title, job_description, job_requirements, platform, status, date) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (lid, company_name, job_title, job_description, job_requirements, platform, 'Applied', date))
        

        conn.commit()
        conn.close()
        return "<script>alert('Application Added');window.location='/home'</script>"
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs WHERE login_id=?', (lid,))
    jobs = cursor.fetchall()
    print(jobs)
    conn.close()
    return render_template('home.html', user=user, jobs=jobs)


@app.route('/dashboard/<aid>', methods=['GET', 'POST'])
def dashboard(aid):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs WHERE id=?', (aid,))
    job = cursor.fetchone()
    print(job)
    conn.close()
    
    return render_template('dashboard.html', job=job)

@app.route('/edit/<aid>', methods=['GET', 'POST'])
def edit(aid):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs WHERE id=?', (aid,))
    job = cursor.fetchone()

    if request.method == 'POST':
        company_name = request.form['company']
        job_title = request.form['jobTitle']
        job_description = request.form['description']
        job_requirements = request.form['requirement']
        platform = request.form['platform']
        status = request.form['status']
        follow_up = request.form['follow-up']
        date = request.form['date']
       
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE jobs SET company_name=?, job_title=?, job_description=?, job_requirements=?, 
                       platform=?, status=?, follow_up=?, date=? WHERE id=?''', 
                       (company_name, job_title, job_description, job_requirements, platform, status, follow_up, date, aid))
        conn.commit()
        conn.close()
        return f"<script>alert('Edited');window.location='/dashboard/{aid}';</script>"
    
    return render_template('edit.html', job=job)


@app.route('/delete/<aid>')
def delete(aid):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM jobs WHERE id=?', (aid,))
    conn.commit()
    conn.close()
    return f"<script>alert('Deleted');window.location='/home';</script>"

@app.route('/logout')
def logout():
    session.clear() 
    print("Logout Successfull")
    return redirect(url_for('login')) 

if __name__ == '__main__':
    init_db()  
    app.run(debug=True, port=5005)