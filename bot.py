from pyrogram import Client, filters
import sqlite3

# إعداد البوت
API_ID = "26080422"  # احصل عليه من my.telegram.org
API_HASH = "461f2bad51bbfcd2d51b65457f5a5fa5"
BOT_TOKEN = "7468110835:AAGEYk0q2ILHLrHNGUJtUY8avyJbrYoiyww"
AUTHORIZED_USERS = [6540710973] 
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# إنشاء قاعدة البيانات
conn = sqlite3.connect("responses.db", check_same_thread=False)
cursor = conn.cursor()

# # إنشاء جدول لتخزين الردود والملفات
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS responses (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     code TEXT UNIQUE NOT NULL,
#     response TEXT NOT NULL,
#     file_path TEXT
# )
# """)
# conn.commit()

# وظيفة لإضافة البيانات إلى قاعدة البيانات
def add_response(code, response, file_path=None):
    try:
        cursor.execute("INSERT INTO responses (code, response, file_path) VALUES (?, ?, ?)", (code, response, file_path))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"الرقم {code} موجود بالفعل.")

# التعامل مع الأمر /start
@app.on_message(filters.command("start"))
def start(client, message):
    if len(message.command) > 1:
        code = message.command[1]  # الرقم المرسل مع الرابط

        # البحث عن الرد ومسار الملف في قاعدة البيانات
        cursor.execute("SELECT response, file_path FROM responses WHERE code = ?", (code,))
        result = cursor.fetchone()

        if result:
            response, file_path = result

            # إرسال الرد النصي مع الملف إذا كان موجودًا
            if file_path:
                message.reply_document(document=file_path, caption=response)
            else:
                message.reply_text(response)
        else:
            message.reply_text("عذرًا، الرقم غير موجود في النظام. 😕")
    else:
        message.reply_text("مرحبًا! يرجى استخدام رابط يحتوي على بيانات 😊")

add_response("66523254", "شهادة (عدنان محمد) موثقة!", "files/CERTIFICATE_Black.png")

# تشغيل البوت
app.run()
