from flask import Flask, render_template
import requests
from post import Post

app = Flask(__name__)

response = requests.get("https://api.npoint.io/43644ec4f0013682fc0d")
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


@app.route('/contact')
def get_contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)


