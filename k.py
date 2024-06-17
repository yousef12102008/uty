import telebot
import re
import os

# التوكن الخاص بالبوت من @BotFather
API_KEY = '6848019028:AAGDVZ4MIlMKOL0pRjtjMOadz4qkf9cqarU'  # استبدل YOUR_API_KEY بالتوكن الفعلي

bot = telebot.TeleBot(API_KEY)

# تعريف التعبير النمطي لاستخراج الفيزات مع التاريخ وCVV
pattern = r'\b(\d{16}\|\d{2}\|\d{4}\|\d{3})\b'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! أرسل لي ملفًا نصيًا لاستخراج معلومات الفيزات (الرقم، التاريخ، وCVV).")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        # تنزيل الملف
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # محاولة فك ترميز الملف باستخدام ترميزات مختلفة
        content = None
        for encoding in ['utf-8', 'latin1', 'windows-1252']:
            try:
                content = downloaded_file.decode(encoding)
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            bot.reply_to(message, "لم أتمكن من فك ترميز الملف. تأكد من أن الملف يحتوي على نصوص قابلة للقراءة.")
            return

        # استخراج معلومات الفيزات
        matches = re.findall(pattern, content)

        if matches:
            # كتابة معلومات الفيزات المستخرجة إلى ملف جديد
            output_file_path = 'yousef.txt'
            with open(output_file_path, 'w') as file:
                for match in matches:
                    file.write(match + '\n')

            # إرسال الملف إلى المستخدم
            with open(output_file_path, 'rb') as file:
                bot.send_document(message.chat.id, file)

            os.remove(output_file_path)  # حذف الملف المؤقت بعد الإرسال
            bot.reply_to(message, f"تم استخراج {len(matches)} فيزا.")
        else:
            bot.reply_to(message, "لم يتم العثور على فيزات في الملف المرسل.")
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء معالجة الملف: {e}")

# تشغيل البوت
bot.polling()
