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
    results = HirdetesController.hirdetes_szures(connection=get_db_connection())
    user_logged_in = 'user_id' in session  # Check if user is logged in
    if request.method == 'POST':
        rooms = request.form.get('rooms')
        area = request.form.get('area')
        search_term = request.form.get('search')
        location = request.form.get('location')
        results = HirdetesController.hirdetes_szures([rooms, area, search_term, location], get_db_connection())
    return render_template('index.html', results=results, user_logged_in=user_logged_in)


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

        hashed_password = generate_password_hash(password,method = 'pbkdf2')
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
    if 'user_id' not in session:
        return redirect(url_for('login'))
    active_menu = request.args.get('menu', 'szemelyes_adatok')  # Default to 'szemelyes_adatok' if no menu is specified

    # Validate the menu value
    valid_menus = ['szemelyes_adatok', 'jelszo_modositas', 'hirdeteseim', 'fok']
    if active_menu not in valid_menus:
        active_menu = 'szemelyes_adatok'  # Default to 'szemelyes_adatok' if invalid menu is passed

    connection = get_db_connection()
    user_id = session['user_id']
    user = FelhasznaloController.get_user_by_id(user_id, connection)

    if not user:
        flash('Hiba történt, nem található a felhasználó!', 'danger')
        return redirect(url_for('login'))

    return render_template('profil.html', user=user, active_menu=active_menu)

    return render_template('profil.html', user=user, active_menu=active_menu)
@app.route('/admin')
def admin():
    #if 'felhID' not in session or session.get('admin_e') != 'TRUE':
       #flash("Nincs megfelelő jogosultság.")
        #return redirect(url_for('login'))

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


@app.route('/create_hirdetes', methods=['GET', 'POST'])
def create_hirdetes():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        rooms = request.form['rooms']
        area = request.form['area']
        location = request.form['location']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Hirdetes (title, description, price, rooms, area, location) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (title, description, price, rooms, area, location))
        connection.commit()
        cursor.close()
        connection.close()

        flash('Hirdetés sikeresen hozzáadva!', 'success')
        return redirect(url_for('index'))

    return render_template('create_hirdetes.html')


@app.route('/hirdetes/<int:id>', methods=['GET'])
def hirdetes_reszletek(id):
    try:
        # Establish database connection
        connection = get_db_connection()
        # Fetch the specific listing using HirdetesController
        hirdetes = HirdetesController.get_hirdetes_by_id(id, connection)
        connection.close()

        # Check if the listing exists
        if not hirdetes:
            flash("A hirdetés nem található.", "danger")
            return redirect(url_for('index'))

        # Render the detailed view page for this listing
        return render_template('hirdetes_reszletek.html', hirdetes=hirdetes)

    except Exception as e:
        flash(f"Hiba történt a hirdetés megjelenítésekor: {str(e)}", "danger")
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

