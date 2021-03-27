from flask import Flask, render_template, request
import requests
from post import Post
from smtplib import SMTP

RECEIVER_EMAIL = "Your email"
SENDER_EMAIL = "Your email"
PASSWORD = "Your Password"

app = Flask(__name__)

response = requests.get("https://api.npoint.io/28097c873466e87a160b")
all_posts = response.json()
posts_list = []
for post in all_posts:
    new_post = Post(post['title'], post['subtitle'], post['author'], post['date'], post['id'])
    posts_list.append(new_post)


@app.route('/')
def get_home():
    return render_template('index.html', posts=posts_list)


@app.route('/post/<int:number>')
def get_post(number):
    print(number)
    current_post = None
    for select_post in posts_list:
        if number == select_post.id:
            current_post = select_post
    return render_template('post.html', num=number, post=current_post)

@app.route('/about')
def get_about():
    return render_template('about.html')


@app.route('/contact', methods=['POST', 'GET'])
def get_contact():
    heading = "contact me"
    if request.method == 'POST':
        heading = "Message sent successfully"
        data = request.form
        with SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=SENDER_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=SENDER_EMAIL,
                to_addrs=RECEIVER_EMAIL,
                msg=f"Subject:From Blog Website\n\n {data['message']}\n Number={data['phone']}"
            )
        return render_template('contact.html', heading=heading)
    else:
        return render_template('contact.html', heading=heading)


# @app.route("/form-entry", methods=['POST', 'GET'])
# def receive_data():
#     if request.method == 'POST':
#         return '<h1> Message sent Successfully.</h1>'


if __name__ == "__main__":
    app.run(debug=True)


