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


@app.route("/generate_user")
def userGenerate():
    password_list = []
    name_list = []
    gender_list = []
    birthday_list = []
    age_list = []
    company_list = []

    for i in range(10):
        # 비밀번호
        password = str(randrange(1000, 9999, 1))

        # 이름
        last_name = ["kim", "park", "lee", "hwang", "choi"]
        middle_name = ["bo", "in", 'ji', 'mo', 'yun', 'ha', 'joo', 'tae', 'byung', 'young']
        name = choice(last_name) + "-" + choice(middle_name) + choice(middle_name)

        # 성별
        gender = choice(["male", "female"])

        # 생년월일
        birthday = randrange(60000, 999999, 1)

        # 나이
        age = randrange(1, 100, 1)

        # 회사
        company = choice(["samsung", "lg", "hyundai"])

        password_list.append(password)
        name_list.append(name)
        gender_list.append(gender)
        birthday_list.append(birthday)
        age_list.append(age)
        company_list.append(company)

    # db코드
    conn = mySQL.connect()
    cursor = conn.cursor()

    for i in range(10):
        cursor.execute(
            f"""
            insert into user(password, name, gender, birthday, age, company)
            values ('{password_list[i]}', '{name_list[i]}', '{gender_list[i]}', '{birthday_list[i]}', '{age_list[i]}', '{company_list[i]}');
            """
        )
        conn.commit()

    cursor.close()
    conn.close()
    return jsonify({'result': 'success'})

if __name__ == "__main__":
    app.run()
