from flask import Flask, request
from flask import jsonify
from flaskext.mysql import MySQL
from random import randint, random, randrange, choice

app = Flask(__name__)

# db 커넥트

# db에 접속
mySQL = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'dbmasteruser'
app.config['MYSQL_DATABASE_PASSWORD'] = '12341234'
app.config['MYSQL_DATABASE_DB'] = 'dbmaster'
app.config[
    'MYSQL_DATABASE_HOST'] = 'ls-adadaac456ea353937ad5567ef96af95696e57f0.cxisoligdeb4.ap-northeast-2.rds.amazonaws.com'
mySQL.init_app(app)


@app.route("/generate_board")
def testGenerate():
    title_list = []
    content_list = []
    like_list = []
    img_list = []
    created_list = []
    user_id_list = []

    for i in range(20):
        title_list.append(f"제목{i}")

        content_str = ["hi", "there", "ok", "bye", "haha"]
        content_list.append(choice(content_str))

        like_list.append(randint(0, 30))
        img_list.append("wwww.img.com/" + str(randint(10, 99)))

        # 생성 날짜
        year_date_str = str(randint(2010, 2023))
        month_date = (randint(1, 12))
        if month_date < 10:
            month_date_str = "0" + str(month_date)
        else:
            month_date_str = month_date
        month_checker = True
        day_date_str = ""
        if int(month_date_str) == 2:
            day_date_str = str(randint(1, 28))
        elif int(month_date_str) <= 7:
            if int(month_date_str) % 2 == 0:
                month_checker = True
            else:
                month_checker = False
        else:
            if int(month_date_str) % 2 == 0:
                month_checker = False
            else:
                month_checker = True

        if month_date_str:
            day_date_str = str(randint(1, 30))
        else:
            day_date_str = str(randint(1, 31))
        # 최종 날짜 데이터
        result_date = f"{year_date_str}-{month_date_str}-{day_date_str}"
        created_list.append(result_date)

        # id 불러오기
        conn = mySQL.connect()
        cursor = conn.cursor()

        cursor.execute(
            f"""
            select count(*) from user;
            """
        )
        result = cursor.fetchone()
        print(result)

        cursor.close()
        conn.close()

        user_id_list.append(randint(1, result[0]))

    # db코드
    conn = mySQL.connect()
    cursor = conn.cursor()

    for i in range(20):
        cursor.execute(
            f"""
                insert into board(title, content, likes, img, created, user_id)
                values ("{title_list[i]}", "{content_list[i]}", {like_list[i]}, "{img_list[i]}", "{created_list[i]}", {user_id_list[i]});
            """
        )
        conn.commit()

    cursor.close()
    conn.close()
    return jsonify({'result': 'success'})

if __name__ == "__main__":
    app.run()
