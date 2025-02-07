import os
import socket
from flask import Flask, render_template, request, redirect
import tensorflow as tf
import numpy as np

# إعداد التطبيق
app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# قائمة الفواكه
image_classes = {
    'Apple': 'تفاح',
    'Avocado': 'أفوكادو',
    'Banana': 'موز',
    'Kiwi': 'كيوي',
    'Lemon': 'ليمون',
    'Lime': 'ليم',
    'Mango': 'مانجو',
    'Nectarine': 'نكتارين',
    'Orange': 'برتقال',
    'Papaya': 'بابايا',
    'Passion-Fruit': 'فاكهة العاطفة',
    'Peach': 'خوخ',
    'Pineapple': 'أناناس',
    'Plum': 'برقوق',
    'Pomegranate': 'رمان',
    'Red-Grapefruit': 'جريب فروت الأحمر',
    'Satsumas': 'ساتسوما'
}

# تحميل النموذج
model = tf.keras.models.load_model("model_4.h5")

# دالة للتنبؤ بالصورة
def image_predict(file_path, image_size=224):
    image = tf.io.read_file(file_path)
    image = tf.image.decode_image(image, channels=3)
    image = tf.image.resize(image, [image_size, image_size])
    image = tf.expand_dims(image, axis=0) / 255.0
    prediction = model.predict(image)
    return prediction, image.numpy()

# دالة قراءة شرح الفاكهة من ملف نصي
def get_fruit_description(fruit_name):
    file_path = os.path.join("descriptions", f"{fruit_name}.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    return "لا توجد معلومات متوفرة عن هذه الفاكهة حاليًا."

# دالة للحصول على مسار الصورة الافتراضية
def get_fruit_image_path(fruit_name):
    file_path = os.path.join("static/images", f"{fruit_name}.jpeg")
    if os.path.exists(file_path):
        return file_path
    return "static/images/default.jpg"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" in request.files and request.files["file"].filename != "":
            # تنبؤ عن طريق الصورة
            file = request.files["file"]
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            prediction, processed_image = image_predict(file_path)
            predicted_class = list(image_classes.keys())[np.argmax(prediction)]

            # قراءة النص من الملف
            description = get_fruit_description(predicted_class)

            # الحصول على الصورة
            image_path = get_fruit_image_path(predicted_class)

            return render_template("result.html", image_path=file_path, predicted_class=predicted_class, description=description)

        elif "fruit_name" in request.form and request.form["fruit_name"].strip() != "":
            # تنبؤ عن طريق إدخال اسم الفاكهة
            fruit_name = request.form["fruit_name"].strip()

            # البحث عن الاسم في القائمة (باللغتين)
            matched_class = None
            for en, ar in image_classes.items():
                if fruit_name.lower() in [en.lower(), ar]:
                    matched_class = en
                    break

            if matched_class:
                # قراءة النص من الملف
                description = get_fruit_description(matched_class)

                # الحصول على الصورة
                image_path = get_fruit_image_path(matched_class)

                return render_template("result.html", image_path=image_path, predicted_class=matched_class, description=description)
            else:
                return render_template("index.html", error="اسم الفاكهة غير معروف، حاول مجددًا.")

    return render_template("index.html")

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)