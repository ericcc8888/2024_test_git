from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)  #製作出一個由Flask類別生成的物件(object)

@app.route("/")

@app.route("/aas")  #裝飾器:根部路要做啥事
def hello_world():
    items = ['Apple', 'Banana', 'Orange', 'Mango']
    return render_template("hello.html", name = items)

#command_line下: flask --app flask_linebot.py run

@app.route("/tell_me_a_joke")  #裝飾器:根部路要做啥事
def tell_me_a_joke():
    return "<p>hhahaha</p>"

@app.route("/eat/<string:what_fruit>")
def eat_apple(what_fruit):
    return redirect(url_for('say_apple_is_gone' , fruit = what_fruit)) # url_for(route_function_name)

@app.route("/<string:fruit>")
def say_apple_is_gone(fruit):
    return "<h1> " +fruit+ " is gone.</h1>"

if __name__ == '__main__':
    app.run(debug=True)