from pywebio.input import input, select, input_group
from pywebio.output import put_text, put_image, put_buttons, put_html, put_table, clear
from pywebio.session import go_app
from pywebio import start_server
import database

# الصفحة الرئيسية
def main():
    clear()
    put_html('<div class="container">')
    put_image('static/images/welcome_image.jpg', width="300")  # تغيير الحجم حسب الحاجة
    put_html('<h1>مرحبًا بكم في نظام تسجيل الغياب</h1>')
    put_html('<p>يرجى تسجيل الدخول للمتابعة</p>')

    # تغيير الطريقة التي تظهر بها الأزرار لتكون أفقية
    put_html('<div class="button-container">')
    login_form = input_group("تسجيل الدخول", [
        input("اسم المستخدم", name="username"),
        input("كلمة السر", name="password", type="password"),
        select("صلاحية المستخدم", ['عضو', 'مدير'], name="role")
    ])

    if database.validate_user(login_form['username'], login_form['password'], login_form['role']):
        if login_form['role'] == 'عضو':
            go_app('member', new_window=False)
        else:
            go_app('admin', new_window=False)
    else:
        put_text("اسم المستخدم أو كلمة السر غير صحيحة")
    
    put_html('</div>')  # إنهاء div.button-container
    put_html('</div>')  # إنهاء div.container

# باقي الكود كما هو...


# صفحة العضو
def member():
    clear()
    put_html('<h1>تسجيل بيانات الغياب</h1>')
    school_code = input("كود المدرسة")
    school_name = database.get_school_name(school_code)
    if school_name:
        put_text(f"اسم المدرسة: {school_name}")
        date = input("التاريخ", type='date')
        grade1 = input("الصف الأول (عدد الطلاب الغائبين)", type='number')
        grade2 = input("الصف الثاني (عدد الطلاب الغائبين)", type='number')
        grade3 = input("الصف الثالث (عدد الطلاب الغائبين)", type='number')
        database.record_absence(school_code, date, grade1, grade2, grade3)
        put_text("تم تسجيل الغياب بنجاح")
    else:
        put_text("كود المدرسة غير صحيح")

# صفحة المدير
def admin():
    clear()
    put_html('<h1>صفحة المدير</h1>')
    put_buttons(['إدارة المستخدمين', 'إدارة المدارس', 'عرض الغياب'], 
                [lambda: go_app('add_user', new_window=False), 
                 lambda: go_app('add_school', new_window=False), 
                 lambda: go_app('view_absences', new_window=False)])

# صفحة إضافة المستخدمين
def add_user():
    clear()
    put_html('<h1>إضافة مستخدم جديد</h1>')
    user_form = input_group("بيانات المستخدم", [
        input("اسم المستخدم", name="username"),
        input("كلمة السر", name="password", type="password"),  # استخدام type="password" لإخفاء كلمة السر
        select("صلاحية المستخدم", ['عضو', 'مدير'], name="role")
    ])
    database.add_user(user_form['username'], user_form['password'], user_form['role'])
    put_text("تم إضافة المستخدم بنجاح")

# صفحة إضافة المدارس
def add_school():
    clear()
    put_html('<h1>إضافة مدرسة جديدة</h1>')
    school_form = input_group("بيانات المدرسة", [
        input("كود المدرسة", name="school_code"),
        input("اسم المدرسة", name="school_name")
    ])
    database.add_school(school_form['school_code'], school_form['school_name'])
    put_text("تم إضافة المدرسة بنجاح")

# صفحة عرض الغياب
def view_absences():
    clear()
    put_html('<h1>عرض الغياب</h1>')
    absences = database.get_all_absences_with_school_names()  # استخدام الدالة المعدلة
    put_table(absences)

if __name__ == '__main__':
    start_server([main, member, admin, add_user, add_school, view_absences], port=8089)
