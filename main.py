from flask import Flask, request, render_template_string
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Firebase başlatma
cred = credentials.Certificate("ornekdatabase-39322-firebase-adminsdk-o9t71-be6d13e691.json")  # Servis hesap dosyanız
firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route("/") #Ana sayfa ekleme
def home(): #Ana sayfada çalışacak fonksiyon
    return render_template_string("""
        <h1>Kullanıcı Bilgisi Girin</h1>
        <form action="/add" method="POST">
            <label for="name">Kullanıcı adı:</label>
            <input type="text" id="name" name="name" required><br><br>

            <label for="age">Yaş:</label>
            <input type="number" id="age" name="age" required><br><br>

            <label for="city">Şehir:</label>
            <input type="text" id="city" name="city" required><br><br>

            <input type="submit" value="Veriyi Gönder">
        </form>
    """)

@app.route("/add", methods=["POST"])
def add_user(): #Verileri veritabanına aktaracak fonksiyon
    try:
        name = request.form["name"]
        age = int(request.form["age"])
        city = request.form["city"]

        user_data = {
            "name": name,
            "age": age,
            "city": city
        }

        
        db.collection("users").add(user_data)

        return render_template_string("""
            <h1>Veri Başarıyla Eklendi!</h1>
            <p>Adı: {{ name }}</p>
            <p>Yaşı: {{ age }}</p>
            <p>Şehri: {{ city }}</p>
            <a href="/">Yeni Kullanıcı Ekle</a>
        """, name=name, age=age, city=city)
    except Exception as e:
        return f"Kullanıcı eklenemedi: {e}"

if __name__ == "__main__":
    app.run(debug=True)