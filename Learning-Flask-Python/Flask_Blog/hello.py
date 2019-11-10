from flask import Flask, render_template

app = Flask(__name__) # to look for templates and other resources

post = [
        {
            'author':'Manoj K R',
            'title' : 'Blog post 1 ',
            'content' : 'first post content',
            'data_posted' : 'July 30th 2019'
        }
    ]
@app.route('/')
@app.route('/home') # URL/ROUTE/TO/RESOURCE.
def home():
    return render_template('home.html',posts=post)

@app.route("/about")
def aboutUs():
    return render_template('about.html',title="About Us")
