#!/usr/bin/env python3
# coding=utf-8
from flask import Flask, request
import MySQLdb

app = Flask(__name__)

# 數據庫連接信息
DB_HOST = "127.0.0.1"
DB_USER = "hj"
DB_PASSWORD = "test1234"
DB_NAME = "testdb"

# 首頁
@app.route('/')
def index():
    student_form = """
    <h2>查詢學生信息</h2>
    <form method="post" action="/query_student" >
        輸入學號:<input name="student_id">
        <input type="submit" value="查詢">
    </form>
    """
    course_form = """
    <h2>查詢課程信息</h2>
    <form method="post" action="/query_course" >
        輸入系所名稱:<input name="department">
        <input type="submit" value="查詢">
    </form>
    """
    enroll_form = """
    <h2>學生選課</h2>
    <form method="post" action="/enroll_course" >
        輸入學生ID:<input name="student_id">
        輸入課程ID:<input name="course_id">
        <input type="submit" value="選課">
    </form>
    """
    withdraw_form = """
    <h2>學生退課</h2>
    <form method="post" action="/withdraw_course" >
        輸入學生ID:<input name="student_id">
        輸入課程ID:<input name="course_id">
        <input type="submit" value="退課">
    </form>
    """

    schedule = """
    <h2>查詢學生課表</h2>
    <form method="post" action="/student_schedule" >
        輸入學號:<input name="student_id">
        <input type="submit" value="查詢">
    </form>
    """
    
    return student_form + course_form + enroll_form + withdraw_form + schedule

# 查詢學生信息
@app.route('/query_student', methods=['POST'])
def query_student():
    # 獲取輸入的學生ID
    student_id = request.form.get("student_id")

    # 自動選課，預選必修課程
    auto_select_required_courses(student_id)

    # 建立資料庫連線
    conn = MySQLdb.connect(host=DB_HOST,
                           user=DB_USER,
                           passwd=DB_PASSWORD,
                           db=DB_NAME)

    # 查詢學生資訊
    query = "SELECT * FROM Student WHERE Student_ID = '{}';".format(student_id)
    cursor = conn.cursor()
    cursor.execute(query)

    # 生成學生資訊表格
    results = """
    <h2>學生資訊</h2>
    <p><a href="/">返回首頁</a></p>
    <table border="1">
        <tr>
            <th>學生ID</th>
            <th>科系</th>
            <th>年級</th>
            <th>班級</th>
            <th>已選學分</th>
        </tr>
    """

    student = cursor.fetchone()
    if student:
        results += "<tr>"
        results += "<td>{}</td>".format(student[0])  # Student_ID
        results += "<td>{}</td>".format(student[1])  # Department
        results += "<td>{}</td>".format(student[2])  # Grade
        results += "<td>{}</td>".format(student[3])  # class
        results += "<td>{}</td>".format(student[4])  # Credit_Selected
        results += "</tr>"
    else:
        results += "<tr><td colspan='5'>找不到該學生</td></tr>"

    results += "</table>"
    return results

# 查詢課程信息
@app.route('/query_course', methods=['POST'])
def query_course():
    department = request.form.get("department")

    conn = MySQLdb.connect(host=DB_HOST,
                           user=DB_USER,
                           passwd=DB_PASSWORD,
                           db=DB_NAME)

    query = "SELECT * FROM Course WHERE Department = '{}';".format(department)

    cursor = conn.cursor()
    cursor.execute(query)

    results = """
    <h2>課程信息查詢結果</h2>
    <p><a href="/">返回首頁</a></p>
    <table border="1">
        <tr>
            <th>課程ID</th>
            <th>課程名稱</th>
            <th>科系</th>
            <th>開課年級</th>
            <th>學分</th>
            <th>上課時間</th>
            <th>下課時間</th>
            <th>最大學生數</th>
            <th>已選學生數</th>
        </tr>
    """

    for row in cursor.fetchall():
        results += "<tr>"
        results += "<td>{}</td>".format(row[0])  # Course_ID
        results += "<td>{}</td>".format(row[1])  # Course_Name
        results += "<td>{}</td>".format(row[2])  # Department
        results += "<td>{}</td>".format(row[9])  # Grade
        results += "<td>{}</td>".format(row[3])  # Credit
        results += "<td>{}</td>".format(row[4])  # Timebegin
        results += "<td>{}</td>".format(row[5])  # Timeend
        results += "<td>{}</td>".format(row[6])  # Max_Capacity
        results += "<td>{}</td>".format(row[7])  # Enrolled_Students
        results += "<td>{}</td>".format(row[8])  # Mandatory
        results += "</tr>"

    results += "</table>"
    return results

# 自動預選符合學生年級的必修課程到學生課程表並更新已選課人數及學分數
def auto_select_required_courses(student_id):
    conn = MySQLdb.connect(host=DB_HOST,
                           user=DB_USER,
                           passwd=DB_PASSWORD,
                           db=DB_NAME)
    cursor = conn.cursor()

    # 獲取學生的系所及年級信息
    student_query = "SELECT Department, Grade FROM Student WHERE Student_ID = '{}';".format(student_id)
    cursor.execute(student_query)
    student_info = cursor.fetchone()
    if not student_info:
        return "學生ID不存在"

    department, grade = student_info

    # 查詢該系所、年級的必修課程
    required_course_query = """
    SELECT Course_ID FROM Course
    WHERE Department = '{}' AND Mandatory = TRUE AND Grade = {};
    """.format(department, grade)

    cursor.execute(required_course_query)
    required_courses = cursor.fetchall()

    # 檢查學生已經選過的課程
    selected_course_query = "SELECT Course_ID FROM Enrollment WHERE Student_ID = '{}';".format(student_id)
    cursor.execute(selected_course_query)
    selected_courses = cursor.fetchall()
    selected_course_ids = [course[0] for course in selected_courses]

    # 將必修課程自動加入學生的課程表中，但需檢查學生是否已經選過這些必修課程
    for course in required_courses:
        course_id = course[0]
        
        # 檢查學生是否已經選過這門必修課程
        if course_id in selected_course_ids:
            continue  # 若已經選過，則跳過不再重複加選

        # 若未選過，則加選該必修課程
        enroll_query = "INSERT INTO Enrollment (Student_ID, Course_ID) VALUES ('{}', '{}');".format(student_id, course_id)
        cursor.execute(enroll_query)

        # 更新課程的已選課人數
        update_course_query = "UPDATE Course SET Enrolled_Students = Enrolled_Students + 1 WHERE Course_ID = '{}';".format(course_id)
        cursor.execute(update_course_query)

        # 獲取課程學分
        credit_query = "SELECT Credit FROM Course WHERE Course_ID = '{}';".format(course_id)
        cursor.execute(credit_query)
        credit = cursor.fetchone()[0]

        # 更新學生已選學分
        update_credit_query = "UPDATE Student SET Credit_Selected = Credit_Selected + {} WHERE Student_ID = '{}';".format(credit, student_id)
        cursor.execute(update_credit_query)

    conn.commit()
    conn.close()

# 學生選課
@app.route('/enroll_course', methods=['POST'])
def enroll_course():
    student_id = request.form.get("student_id")
    course_id = request.form.get("course_id")

    conn = MySQLdb.connect(host=DB_HOST,
                           user=DB_USER,
                           passwd=DB_PASSWORD,
                           db=DB_NAME)
    
    
    student_query = "SELECT * FROM Student WHERE Student_ID = '{}';".format(student_id)
    course_query = "SELECT * FROM Course WHERE Course_ID = '{}';".format(course_id)

    cursor = conn.cursor()

    cursor.execute(student_query)
    student = cursor.fetchone()
    if not student:
        return """
        <p>學生ID不存在，請重新輸入</p>
        <p><a href="/">返回首頁</a></p>
        """

    cursor.execute(course_query)
    course = cursor.fetchone()
    if not course:
        return """
        <p>課程ID不存在，請重新輸入</p>
        <p><a href="/">返回首頁</a></p>
        """

    department_query = "SELECT Department FROM Student WHERE Student_ID = '{}';".format(student_id)
    cursor.execute(department_query)
    student_department = cursor.fetchone()[0]

    course_department_query = "SELECT Department FROM Course WHERE Course_ID = '{}';".format(course_id)
    cursor.execute(course_department_query)
    course_department = cursor.fetchone()[0]

    if student_department != course_department:
        return """
        <p>學生所屬科系與課程不符</p>
        <p><a href="/">返回首頁</a></p>
        """

    capacity_query = "SELECT Enrolled_Students, Max_Capacity FROM Course WHERE Course_ID = '{}';".format(course_id)
    cursor.execute(capacity_query)
    enrolled_students, max_capacity = cursor.fetchone()

    if enrolled_students >= max_capacity:
        return """
        <p>課程已滿員</p>
        <p><a href="/">返回首頁</a></p>
        """

    enrollment_query = "SELECT * FROM Enrollment WHERE Student_ID = '{}' AND Course_ID = '{}';".format(student_id, course_id)
    cursor.execute(enrollment_query)
    if cursor.fetchone():
        return """
        <p>學生已選過該課程</p>
        <p><a href="/">返回首頁</a></p>
        """
    
    # 檢查學生年級是否低於課程開設年級
    if student[2] < course[9]:
        return """
        <p>您的年級不符合該課程的開設年級要求！</p>
        <p><a href="/">返回首頁</a></p>
        """

    total_credit_query = "SELECT Credit_Selected FROM Student WHERE Student_ID = '{}';".format(student_id)
    cursor.execute(total_credit_query)
    total_credit = cursor.fetchone()[0]

    if total_credit + course[3] > 30:
        return """
        <p>學生選課總學分已超過30學分限制</p>
        <p><a href="/">返回首頁</a></p>
        """

    # 檢查衝堂
    time_conflict_query = """
    SELECT * FROM Enrollment e
    JOIN Course c ON e.Course_ID = c.Course_ID
    WHERE e.Student_ID = '{}' AND (c.Timebegin BETWEEN '{}' AND '{}' OR c.Timeend BETWEEN '{}' AND '{}');
    """.format(student_id, course[4], course[5], course[4], course[5])

    cursor.execute(time_conflict_query)
    conflicting_courses = cursor.fetchall()

    if conflicting_courses:
        conflict_info = "<br>".join(["課程名稱：{}，上課時間：{}-{}".format(c[1], c[4], c[5]) for c in conflicting_courses])
        return """
        <p>加選失敗，與以下課程衝堂：<br>{}</p>
        <p><a href="/">返回首頁</a></p>
        """.format(conflict_info)

    update_query = "UPDATE Course SET Enrolled_Students = Enrolled_Students + 1 WHERE Course_ID = '{}';".format(course_id)
    cursor.execute(update_query)
    
    # 更新學生已選學分
    update_credit_query = "UPDATE Student SET Credit_Selected = Credit_Selected + {} WHERE Student_ID = '{}';".format(course[3], student_id)
    cursor.execute(update_credit_query)

    enroll_query = "INSERT INTO Enrollment (Student_ID, Course_ID) VALUES ('{}', '{}');".format(student_id, course_id)
    cursor.execute(enroll_query)

    conn.commit()
    conn.close()

    return """
    <p>選課成功</p>
    <p><a href="/">返回首頁</a></p>
    """

# 退選課程
@app.route('/withdraw_course', methods=['POST'])
def drop_course():
    # 取得輸入的學生ID和課程ID
    student_id = request.form.get("student_id")
    course_id = request.form.get("course_id")

    # 建立資料庫連線
    conn = MySQLdb.connect(host=DB_HOST,
                           user=DB_USER,
                           passwd=DB_PASSWORD,
                           db=DB_NAME)

    # 先確認該學生和課程是否存在
    student_query = "SELECT * FROM Student WHERE Student_ID = '{}';".format(student_id)
    course_query = "SELECT * FROM Course WHERE Course_ID = '{}';".format(course_id)

    cursor = conn.cursor()

    # 查詢學生是否存在
    cursor.execute(student_query)
    student = cursor.fetchone()
    if not student:
        return """
        <p>學生ID不存在！</p>
        <p><a href="/">返回主頁</a></p>
        """

    # 查詢課程是否存在
    cursor.execute(course_query)
    course = cursor.fetchone()
    if not course:
        return """
        <p>課程ID不存在！</p>
        <p><a href="/">返回主頁</a></p>
        """

    # 確認學生已選擇該課程
    enrollment_query = "SELECT * FROM Enrollment WHERE Student_ID = '{}' AND Course_ID = '{}';".format(student_id, course_id)
    cursor.execute(enrollment_query)
    if not cursor.fetchone():
        return """
        <p>學生未選擇該課程！</p>
        <p><a href="/">返回主頁</a></p>
        """

    # 檢查課程是否為必修
    if course[-1]:  # 最後一個欄位是 Mandatory
        # 提出警告，因為該課程為必修
        return """
        <p>警告：您正試圖退選一門必修課程！</p>
        <p>確定要退選嗎？</p>
        <form action="/confirm_withdraw" method="post">
            <input type="hidden" name="student_id" value="{}">
            <input type="hidden" name="course_id" value="{}">
            <input type="hidden" name="confirm" value="true"> <!-- 確定退選按鈕 -->
            <input type="submit" value="確定退選">
        </form>
        <p><a href="/">取消</a></p>
        """.format(student_id, course_id)
    else:
        # 若不是必修課程，則允許退選
        # 更新課程的已選學生人數
        update_course_query = "UPDATE Course SET Enrolled_Students = Enrolled_Students - 1 WHERE Course_ID = '{}';".format(course_id)
        cursor.execute(update_course_query)

        # 更新學生已選學分
        update_credit_query = "UPDATE Student SET Credit_Selected = Credit_Selected - {} WHERE Student_ID = '{}';".format(course[3], student_id)
        cursor.execute(update_credit_query)

        # 從 Enrollment 表中刪除選課紀錄
        drop_query = "DELETE FROM Enrollment WHERE Student_ID = '{}' AND Course_ID = '{}';".format(student_id, course_id)
        cursor.execute(drop_query)

        conn.commit()
        conn.close()

        return """
        <p>退選成功！</p>
        <p><a href="/">返回主頁</a></p>
        """

# 確定退選的路由
@app.route('/confirm_withdraw', methods=['POST'])
def confirm_withdraw():
    student_id = request.form.get("student_id")
    course_id = request.form.get("course_id")

    # 確認退選
    if request.form.get("confirm") == "true":
        conn = MySQLdb.connect(host=DB_HOST,
                               user=DB_USER,
                               passwd=DB_PASSWORD,
                               db=DB_NAME)

        cursor = conn.cursor()

        # 更新課程的已選學生人數
        update_course_query = "UPDATE Course SET Enrolled_Students = Enrolled_Students - 1 WHERE Course_ID = '{}';".format(course_id)
        cursor.execute(update_course_query)

        # 更新學生已選學分
        course_query = "SELECT Credit FROM Course WHERE Course_ID = '{}';".format(course_id)
        cursor.execute(course_query)
        credit = cursor.fetchone()[0]

        update_credit_query = "UPDATE Student SET Credit_Selected = Credit_Selected - {} WHERE Student_ID = '{}';".format(credit, student_id)
        cursor.execute(update_credit_query)

        # 從 Enrollment 表中刪除選課紀錄
        drop_query = "DELETE FROM Enrollment WHERE Student_ID = '{}' AND Course_ID = '{}';".format(student_id, course_id)
        cursor.execute(drop_query)

        conn.commit()
        conn.close()

        return """
        <p>退選成功！</p>
        <p><a href="/">返回主頁</a></p>
        """
    else:
        return """
        <p>您已取消退選！</p>
        <p><a href="/">返回主頁</a></p>
        """

# 列出學生的課程表
@app.route('/student_schedule', methods=['POST'])
def student_schedule():
    # 取得輸入的學生ID
    student_id = request.form.get("student_id")

    # 建立資料庫連線
    conn = MySQLdb.connect(host=DB_HOST,
                           user=DB_USER,
                           passwd=DB_PASSWORD,
                           db=DB_NAME)
    
    

    cursor = conn.cursor()

    
    # 查詢學生所選的課程及相關資訊並按照上課時間排序
    schedule_query = """
    SELECT c.Course_ID, c.Course_Name, c.Department, c.Credit, c.Timebegin, c.Timeend
    FROM Enrollment e
    JOIN Course c ON e.Course_ID = c.Course_ID
    WHERE e.Student_ID = '{}'
    ORDER BY c.Timebegin;
    """.format(student_id)

    cursor.execute(schedule_query)
    schedule = cursor.fetchall()

    conn.close()

    # 根據查詢結果生成課程表
    schedule_table = "<h2>學生課程表</h2>"
    schedule_table += "<table border='1'><tr><th>課程ID</th><th>課程名稱</th><th>科系</th><th>學分</th><th>上課時間</th></tr>"
    for course in schedule:
        course_id, course_name, department, credit, time_begin, time_end = course
        schedule_table += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{} - {}</td></tr>".format(course_id, course_name, department, credit, time_begin, time_end)
    schedule_table += "</table>"

    return schedule_table

if __name__ == "__main__":
    app.run(debug=True)