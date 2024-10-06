import sqlite3

# إنشاء قاعدة البيانات والجداول
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    role TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS schools (
                    school_code TEXT PRIMARY KEY,
                    school_name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS absences (
                    school_code TEXT,
                    date TEXT,
                    grade1 INTEGER,
                    grade2 INTEGER,
                    grade3 INTEGER)''')
    conn.commit()
    conn.close()

# التحقق من صحة المستخدم
def validate_user(username, password, role):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", (username, password, role))
    user = c.fetchone()
    conn.close()
    return user is not None

# إضافة مستخدم جديد
def add_user(username, password, role):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    conn.close()

# إضافة مدرسة جديدة
def add_school(school_code, school_name):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT INTO schools (school_code, school_name) VALUES (?, ?)", (school_code, school_name))
    conn.commit()
    conn.close()

# الحصول على اسم المدرسة
def get_school_name(school_code):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT school_name FROM schools WHERE school_code=?", (school_code,))
    school = c.fetchone()
    conn.close()
    return school[0] if school else None

# تسجيل الغياب
def record_absence(school_code, date, grade1, grade2, grade3):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT INTO absences (school_code, date, grade1, grade2, grade3) VALUES (?, ?, ?, ?, ?)", 
              (school_code, date, grade1, grade2, grade3))
    conn.commit()
    conn.close()

# الحصول على جميع تسجيلات الغياب مع أسماء المدارس
def get_all_absences_with_school_names():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''
        SELECT absences.school_code, schools.school_name, absences.date, absences.grade1, absences.grade2, absences.grade3
        FROM absences
        JOIN schools ON absences.school_code = schools.school_code
    ''')
    absences = c.fetchall()
    conn.close()
    return absences

# تهيئة قاعدة البيانات عند تشغيل البرنامج لأول مرة
init_db()
