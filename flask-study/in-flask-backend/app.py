from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1>Hello, World</h1>"


@app.route("/about")
def show_about():
    return "<div>This is about page</div>"


@app.route("/project")
def show_project():
    return "<h1>This is project page</h1>"


# 특정 게시물을 보여주는 URL
# @app.route("/feeds/<feed_id>")
# def show_one_feed(feed_id):
#     return f"<h2>Feed Id : {feed_id}<h2>"


@app.route("/myinfo/<username>")
def show_my_info(username):
    return f"<h1>Username is {username}</h1>"


# REST API 만들기
# 서버에서 유저에게 데이터를 보내기 위해 사용
from flask import jsonify
# 유저가 보낸 데이터 request에 담겨서 온다.
from flask import request


# GET -> 피드 조회
# POST -> 피드 생성


@app.route('/api/v1/', methods=['GET'])
def show_all_feeds():
    data = {
        "id": 1,
        "title": "제목",
        "img": "www.image.com/1",
        "like": "100",
        "reviews": [
            {"id": 1, "nickname": "leo", "content": "댓글1"},
            {"id": 2, "nickname": "leo", "content": "댓글2"},
            {"id": 3, "nickname": "leo", "content": "댓글3"},
            {"id": 4, "nickname": "leo", "content": "댓글4"},
        ]
    }
    print(type(data))  # 우리가 서버에서 만든 객체 데이터
    print(type(jsonify(data)))  # 클라이언트에서 이해하는 JSon 데이터
    return jsonify(data)


# 게시글 하나 조회
@app.route('/api/v1/feeds/<int:feed_id>', methods=['GET'])
def show_one_feed(feed_id):
    print(feed_id)
    return jsonify({"result": "success"})


# 게시글 생성
# POST /api/v1/feeds
from flask import request


@app.route('/api/v1/feeds/', methods=['POST'])
def create_one_feed():
    name = request.form['name']
    age = request.form['age']

    print(name, age)
    return jsonify({"result": "success"})


# db 커넥트
from flaskext.mysql import MySQL

# db에 접속
mySQL = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'java006$'
app.config['MYSQL_DATABASE_DB'] = 'ozdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mySQL.init_app(app)


# conn = mySQL.connect()
# cursor = conn.cursor()
# cursor.execute(
#     """
#     #SELECT * FROM ozdb;
#     """)
# # datas = cursor.fetchone()   # django의 get과 비슷
# datas = cursor.fetchall()   # django -> all()
#
# conn.commit()
# cursor.close()
# conn.close()


# 유저 부분
@app.route('/api/v1/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():
    conn = mySQL.connect()
    cursor = conn.cursor()

    if request.method == "GET":  # 유저 조회
        cursor.execute(
            """
            select * from user;
            """
        )
        results = cursor.fetchall()
        # print(data)

        return jsonify({'result': results})
    elif request.method == "POST":  # 유저 생성
        name = request.form['name']
        age = request.form['age']

        cursor.execute(
            f"""
            insert into user(name, age)
            values ('{name}', '{age}');
            """
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'result': 'success'})


if __name__ == "__main__":
    app.run()
