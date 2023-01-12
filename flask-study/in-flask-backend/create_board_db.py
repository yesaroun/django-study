from flask import Flask
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


@app.route("/generate_test")
def testGenerate():
    name_list = []
    reserve_date_list = []
    room_num_list = []

    for i in range(20):
        # 이름
        last_name = ["kim", "park", "lee", "hwang", "choi"]
        middle_name = ["bo", "in", 'ji', 'mo', 'yun', 'ha', 'joo', 'tae', 'byung', 'young']
        name = choice(last_name) + "-" + choice(middle_name) + choice(middle_name)

        # 예약 날짜
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

        # roomnum
        room_num_str = str(randint(1000, 9999))

        name_list.append(name)
        reserve_date_list.append(result_date)
        room_num_list.append(room_num_str)




    # db코드
    conn = mySQL.connect()
    cursor = conn.cursor()

    for i in range(20):
        cursor.execute(
            f"""
            insert into test(name, reservedate, roomnum)
            values ('{name_list[i]}', '{reserve_date_list[i]}', '{room_num_list[i]}');
            """
        )
        conn.commit()

    cursor.close()
    conn.close()
    return jsonify({'result': 'success'})

if __name__ == "__main__":
    app.run()
