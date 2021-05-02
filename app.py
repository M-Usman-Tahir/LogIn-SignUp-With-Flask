from flask import Flask, redirect, url_for, render_template, request, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'MyCodedData'

@app.route('/')
def start():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        usr = session['user']
        return redirect(url_for('home', user=usr))
    else:
        if request.method=='POST':
            usr = request.form['usrname']
            pswrd = request.form['pswrd']
            lg_data = pd.read_csv('login_data.csv')
            # try:
            if str(lg_data.iloc[lg_data[lg_data['username']==usr].index.values[0]]['password']) == pswrd:
                session['user'] = usr
                return redirect(url_for('home'))
            else:
                print(type(lg_data.iloc[lg_data[lg_data['username']==usr].index.values[0]]['password']))
                print(type(pswrd))
                return render_template('login.html') 
            # except:
            #     return render_template('login.html') 
        else:
            return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        usr = request.form['usrname']
        fname = request.form['fname']
        sname = request.form['sname']
        mail = request.form['mail']
        pswrd = request.form['pswrd']
        Cpswrd = request.form['Cpswrd']
        if len(pswrd)>7 and pswrd == Cpswrd:
            lg_cre = [[usr, fname, sname, mail, pswrd]]
            lg_data = pd.DataFrame(lg_cre)
            lg_data.to_csv('login_data.csv', mode='a', index=False, header=False)
            if True:
                return redirect(url_for('login'))
        else:
            return render_template('Signup.html')
    else:
        return render_template('Signup.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user' in session:
        usr = session['user']
        return render_template('home.html', user=usr)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)