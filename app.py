from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from re import compile
from datetime import datetime


app = Flask('million_per_n')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/million_per_n.db'
db = SQLAlchemy(app)

username_regex = compile('[^0-9a-z_]')


class Post(db.Model):
    twitter = db.Column(db.String(32), primary_key=True)
    n = db.Column(db.Integer, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, twitter: str, n: int):
        self.twitter = twitter
        self.n = n

    def __repr__(self):
        return f'{self.twitter}\t{self.n}'


def render_index(**kwargs):
    hums = Post.query.count()
    return render_template('index.html', hums=hums, **kwargs)


def error(msg: str):
    return render_index(text_class='text-danger', text_contents=msg)


def internal_error():
    return render_index(text_class='text-warning', text_contents="サーバ内部で問題が発生しました。")


@app.route('/')
def index():
    # print("ルートポイント")
    return render_index()


@app.route('/posted')
def posted():
    try:
        n = int(request.args.get('n'))
    except Exception as e:
        # print(e)
        return error("自然数は1以上1000000以下で入力してください。")

    try:
        twitter = request.args.get('twitter').strip().lower()

        if not twitter:
            # print("空フォームなど")
            return error("フォームの内容を正しく確認できませんでした。")
    except Exception as e:
        # print(e)
        return internal_error()

    # print(twitter, n)

    re_result = username_regex.search(twitter)

    if re_result:
        # print("Twitter異常")
        return error("Twitter IDに不明な文字が検出されました。")

    if n < 1 or 1000000 < n:
        # print("自然数がダメ")
        return error("自然数は1以上1000000以下で入力してください。")

    success_msg = f"@{twitter}さんの投稿: "

    try:
        # print("クエリ投げるよ")
        post = Post.query.filter_by(twitter=twitter).first()

        if not post:
            # print("レコードなし")
            db.session.add(Post(twitter, n))
            success_msg += f"n={n}を受け付けました。"
        else:
            # print("レコードあり")
            post.n = n
            post.modified_at = datetime.now()
            success_msg += f"n={n}に更新しました。"
        db.session.commit()
        # print(Post.query.filter_by(twitter=twitter).first())
    except Exception as e:
        # print(e)
        return internal_error()

    # print("投稿完了")
    return render_index(text_class='text-success', text_contents=success_msg)


db.create_all()
if __name__ == '__main__':
    app.run()
