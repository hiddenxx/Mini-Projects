## **Learning Flask**
---

> ### Initializing Flask app

Once you start a flask app , you need to export the environment variable FLASK_APP  
export FLASK_APP=<name>.py  
flask run  

Once the flask app is running , you can access the app in "localhost:5000" or "127.0.0.1:5000".
* Always run **FLASK APP** in **DEBUG** mode when developing so that the changes you do on the code will be reflected in the application - export FLASK_DEBUG=1  
* If you want to run the FLASK_APP from inside the editor , then do a ifmain() to specify the main function and app.run(debug=True) from there.

---
> ### Adding routes to Flask application

In order to add more routes to a function , you can specify more decorators to handle more routes.  
Meaning if you want "/" and "/home" to return you the template home page , then you can add both routes as decorators to the home-page function.

> ### Using templates

Create a folder called templates to store all the html templates which you want to send to the application.  
Import render_template from flask which handles rendering the template as string and sends it to the function to be displayed.
render_template("<HTML-PAGE-FILENAME>")

> ### Sending Args to template

In order to dynamically create content in the HTML template , we will be sending arguments using render_template.  
Templating Engine that Flask uses is called " Jinja2 ". It allows us to write code in our templates.  
When we send api calls to the database , we can use those data to be presented in the web page using the code which we can write in the code block of the web page.  

Eg :

A code block is repr'd by {% (function) %} (CODE HERE) {% end(function) %}

> ### Template Inheirtance

If there a template which is common over all the web pages , put them into layout.html and inherit them while writing other functions.  
You can use {%block (NAME-OF-BLOCK) %}{% endblock (NAME-OF-BLOCK)%} to insert something unique to that particular page.  
In order to use the block of (NAME-OF-BLOCK), you have extend the layout.html in the other templates for the page.

Eg :

    {% extends "layout.html" %} # Inheirtance to get that layout.
    {% block (NAME-OF-BLOCK) %}
    **SOME-CODE-HERE**
    {% endblock (NAME-OF-BLOCK) %}

Lets see why this is powerful :
* You can use bootstrap to style and create templates.
  * You can make different (div class='container' )(/div) to hold the content blocks.
