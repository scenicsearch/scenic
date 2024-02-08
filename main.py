import subprocess as sp
import os, flask, random, sqlite3, datetime

keywords = {"darkish": "https://darkish.drexperiment.repl.co/", 
            "youtube": "https://m.youtube.com/",
            "yt": "https://m.youtube.com/",
            "replit": "https://replit.com/", 
            "dfm": "https://www.drfrostmaths.com/login.php",
            "duolingo": "https://www.duolingo.com/", 
            "loe": "https://www.languagesonline-extra.org.uk/login/index.php", 
            "collins": "https://connect.collins.co.uk/school/THEROYAL1/Student/", 
            "zzi.sh": "https://app.quizalize.com/student/code", 
            "ar+tests": "https://ukhosted2.renlearn.co.uk/1893459/Public/RPM/Login/Login.aspx?srcID=s", 
            "kerboodle": "https://www.kerboodle.com/users/login"}
engines = {"google": "https://www.google.com/search?q=", "yahoo": "https://uk.search.yahoo.com/search?p=", "ecosia": "https://www.ecosia.org/search?q=", "bing": "https://www.bing.com/search?q=", "duck+duck+go": "https://duckduckgo.com/?q=", "ask.com": "https://www.ask.com/web?q=", "aol": "https://search.aol.com/aol/search?q=", "you.com": "https://you.com/search?fromSearchBar=true&q="}

app = flask.Flask(__name__)
app.secret_key = os.environ["key"]

@app.route('/')
def index():
  return flask.render_template("index.html")

@app.route('/about')
def about():
  return flask.render_template("about.html")

@app.errorhandler(404)
def page_not_found(e):
  path = flask.request.path
  if path != "/404":
    with open("./404errors.csv", "a") as f:
      f.write(f'{datetime.datetime.now()} - {path} \n')
    return flask.redirect("https://685ee897-88fc-427c-9478-e84b75c634f6-00-2aa6o6h46iw9h.picard.replit.dev/404", code=308)
  return flask.render_template("404.html")

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
  if flask.request.method == 'POST':
    username = flask.request.form['username']
    password = flask.request.form['password']
    salt = random.randint(1000, 9999)
    password = hash(f"{password}{salt}")
    conn = sqlite3.connect('account.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    engine TEXT NOT NULL,
                    searches INTEGER
                  )''')
    c.execute('SELECT * FROM accounts WHERE username = ?', (username,))
    if c.fetchone():
      error = "Username already exists. Please choose a different username."
      return flask.render_template('create.html', error=error)
    c.execute('INSERT INTO accounts (username, password, salt, engine, searches) VALUES (?, ?, ?, ?, ?)', (username, password, salt, "Google", 0))
    conn.commit()
    conn.close()
    return flask.redirect('/login')
  else:
    return flask.render_template('create.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
  if flask.request.method == 'POST':
    username = flask.request.form['username']
    password = flask.request.form['password']
    conn = sqlite3.connect('account.db')
    c = conn.cursor()
    c.execute('SELECT * FROM accounts WHERE username = ?', (username,))
    account = c.fetchone()
    conn.close()
    if account:
      if int(hash(f"{password}{account[3]}")) == int(account[2]):
        flask.session['account'] = account[1:6]
        return flask.redirect('/profile')
    else:
      error = "Invalid username or password."
      return flask.render_template('login.html', error=error)
  return flask.render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
  if 'account' not in flask.session:
    return flask.render_template('notsignedin.html')
  account = list(flask.session['account'])
  if flask.request.method == 'POST':
    new_engine = flask.request.form['engine']
    conn = sqlite3.connect('account.db')
    c = conn.cursor()
    c.execute('UPDATE accounts SET engine = ? WHERE username = ?', (new_engine, account[0]))
    conn.commit()
    conn.close()
    account = [account[0], account[1], account[2], new_engine, account[4]]
    flask.session["account"] = account
  chosen = ["", "", "", "", "", "", "", ""]
  if account[3] == "Google":
    chosen[0] = "selected"
  if account[3] == "Ecosia":
    chosen[1] = "selected"
  if account[3] == "Duck+duck+go":
    chosen[2] = "selected"
  if account[3] == "You.com":
    chosen[3] = "selected"
  if account[3] == "Ask.com":
    chosen[4] = "selected"
  if account[3] == "AOL":
    chosen[5] = "selected"
  if account[3] == "Yahoo":
    chosen[6] = "selected"
  if account[3] == "Bing":
    chosen[7] = "selected"
  return flask.render_template('profile.html', account=account, chosen=chosen)
  
@app.route('/logout')
def logout():
  flask.session.pop('account', None)
  return flask.render_template('notsignedin.html')

@app.route('/tos')
def tos():
  return flask.render_template('tos.html')

@app.route("/search/<terms>")
def search(terms):
  with open("./searches.csv", "a") as f:
    f.write(f'{datetime.datetime.now()} - {terms} \n')
  if 'account' in flask.session:
    account = list(flask.session['account'])
    conn = sqlite3.connect('account.db')
    c = conn.cursor()
    c.execute('UPDATE accounts SET searches = ? WHERE id = ?', (account[4]+1, account[0]))
    conn.commit()
    conn.close()
    account = [account[0], account[1], account[2], account[3], account[4]+1]
    flask.session['account'] = account
    if keywords.get(terms.lower()) is None:
      return flask.redirect(engines[account[3].lower()] + terms, code=308)
  if keywords.get(terms.lower()) is None:
    return flask.redirect(engines["google"] + terms, code=308)
  else:
    return flask.redirect(keywords[terms.lower()], code=308)


@app.route('/robots.txt')
def robots_txt():
    robots = "User-agent: *\nDisallow: /"
    return Response(robots, mimetype='text/plain')

app.run(host='0.0.0.0', port='8080')
