from controllers.HirdetesController import HirdetesController
from controllers.FelhasznaloController import FelhasznaloController
from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'



HirdetesController = HirdetesController()
FelhasznaloController = FelhasznaloController()
def get_db_connection():
    """Funckio az adatbazis kapcsolodasahoz"""
    db_config = {
        'host': 'ingatlan-do-user-18278046-0.f.db.ondigitalocean.com',
        'user': 'doadmin',
        'port':25060,
        'password': 'AVNS_PUuxCgBKR5BpTimGZxi',
        'database': 'Ingatlanpont',
        'cursorclass': pymysql.cursors.DictCursor
    }
    connection = pymysql.connect(**db_config)
    return connection

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        rooms = request.form.get('rooms')
        area = request.form.get('area')
        search_term = request.form.get('search')
        location = request.form.get('location')
        results = HirdetesController.hirdetes_szures([rooms, area, search_term, location], get_db_connection())
    return render_template('index.html', results=results)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search']
        results = HirdetesController.hirdetes_kereses(search_term,  get_db_connection())
        return render_template('result.html', results=results)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('A jelszavak nem egyeznek, kérjük próbáld újra.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        try:
            connection = get_db_connection()
            FelhasznaloController.register_user(email, hashed_password, connection)
            connection.close()
            flash('Sikeres regisztráció! Most már bejelentkezhetsz.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Hiba a regisztráció során: ' + str(e), 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        connection = get_db_connection()

        try:
            # Fetch user data from the database
            user = FelhasznaloController.get_user_by_email(email, connection)
            print("User data:", user)  # Debug: check user data fetched from the database

            # Check if user exists and password is correct
            if user:
                password_match = check_password_hash(user['jelszo'], password)
                print("Password match:", password_match)  # Debug: check if password matches

                if password_match:
                    flash('Sikeres bejelentkezés!', 'success')
                    session['user_id'] = user['felhID']  # Store user ID in session
                    print("Session data:", session)  # Debug: check session data after login
                    return redirect(url_for('profil'))
                else:
                    flash('Hibás jelszó.', 'danger')
            else:
                flash('Nem található ilyen e-mail cím a rendszerben.', 'danger')

        except Exception as e:
            print(f"Error during login: {str(e)}")
            flash('Hiba történt a bejelentkezés során.', 'danger')

        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Remove the user session when logging out
    session.pop('user_id', None)  # Remove the user_id from the session

    flash('Sikeres kijelentkezés!', 'success')  # Optionally add a flash message
    return redirect(url_for('login'))  # Redirect to the login page

@app.route('/profil', methods=['GET', 'POST'])
def profil():
    if 'felhID' not in session:
        flash("Please log in to access your profile.")
        return redirect(url_for('login'))

    user_id = session['felhID']
    active_menu = request.args.get('menu', 'szemelyes_adatok')  # A profiloldal belső menüjének vezérlése

    nevEdit = request.args.get('nevEdit', 'False') == 'True'
    emailEdit = request.args.get('emailEdit', 'False') == 'True'
    telszamEdit = request.args.get('telszamEdit', 'False') == 'True'

    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST' and 'delete_profile' not in request.form:
        new_name = request.form.get('name')
        new_email = request.form.get('email')
        new_phone = request.form.get('phone')

        cursor.execute("""
            UPDATE Felhasznalo 
            SET nev = %s, email = %s, telefonszam = %s 
            WHERE felhID = %s
        """, (new_name, new_email, new_phone, user_id))
        connection.commit()
        flash("Profile updated successfully")
        return redirect(url_for('profil'))

    elif request.method == 'POST' and 'delete_profile' in request.form:
        cursor.execute("DELETE FROM Felhasznalo WHERE felhID = %s", (user_id,))
        connection.commit()
        cursor.close()
        connection.close()

        session.pop('user_id', None)
        flash("Profile deleted successfully")
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM Felhasznalo WHERE felhID = %s", (user_id,))
    profile_data = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template('profil.html', profile_data=profile_data, active_menu=active_menu,
                           nevEdit=nevEdit, emailEdit=emailEdit, telszamEdit=telszamEdit)

@app.route('/admin')
def admin():
    if 'felhID' not in session or session.get('admin_e') != 'TRUE':
        flash("Nincs megfelelő jogosultság.")
        return redirect(url_for('login'))

    active_menu_admin = request.args.get('menu2', 'felhasznalok-kezelese')  # For internal menu of admin page
    return render_template('admin.html', active_menu_admin=active_menu_admin)




@app.route('/hirdetes', methods=['GET', 'POST'])
def hirdetes():
    if request.method == 'POST' and 'delete_hirdetes' in request.form:
        hirdetes_id = request.form.get('id')
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Töröljük a hirdetést az adatbázisból
            cursor.execute("DELETE FROM Hirdetes WHERE id = %s", (hirdetes_id,))
            connection.commit()

            cursor.close()
            connection.close()

            flash("Hirdetés sikeresen törölve.")
            return redirect(url_for('index'))  # Redirect to the homepage

        except Exception as e:
            flash(f"Hiba történt a hirdetés törlésekor: {str(e)}")
            return redirect(url_for('index'))

    return render_template('hirdetes.html',
                           location="Budapest, X. kerület",
                           title="Eladó családi ház 4 szobás, Budapest X. kerület",
                           price="75 millió",
                           description=("Lorem Ipsum is simply dummy text of the printing and typesetting industry. "
                                        "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, "
                                        "when an unknown printer took a galley of type and scrambled it to make a type specimen book..."),
                           area=67,
                           all_are=312,
                           rooms=4,
                           hirdeto="Példa Péter",
                           ingatlanIroda="Házadlesz Ingatlaniroda")

if __name__ == '__main__':
    app.run()

