from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # EZT CSAK TESZTELÉS KÉPPEN ALKALMAZTAM, INNENTŐL KELL A BACKENDET CSINÁLNI
        print(f"Received data: Email: {email}, Password: {password}")
        return jsonify({'message': 'Data received successfully'})
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # EZT CSAK TESZTELÉS KÉPPEN ALKALMAZTAM, INNENTŐL KELL A BACKENDET CSINÁLNI
        print(f"Received data: Email: {email}, Password: {password}")
        return jsonify({'message': 'Data received successfully'})
    return render_template('login.html')



@app.route('/profil', methods=['GET', 'POST'])
def profil():
    active_menu = request.args.get('menu', 'szemelyes_adatok')  #profil oldal belső menüjéhez
    #személyes adatoknál listázás és szerkesztés közti váltáshoz változók
    nevEdit = request.args.get('nevEdit', 'False') == 'True'
    emailEdit = request.args.get('emailEdit', 'False') == 'True'
    telszamEdit = request.args.get('telszamEdit', 'False') == 'True'
    return render_template('profil.html', active_menu=active_menu, nevEdit=nevEdit, emailEdit=emailEdit, telszamEdit=telszamEdit)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    active_menu_admin = request.args.get('menu2', 'felhasznalok-kezelese')  #admin oldal belső menüjéhez
    return render_template('admin.html', active_menu_admin=active_menu_admin)


@app.route('/hirdetes', methods=['GET'])
def hirdetes():
    return render_template('hirdetes.html',
                           location="Budapest, X. kerület",
                           title="Eladó családi ház 4 szobás, Budapest X. kerület",
                           price="75 millió",
                           description="Lorem Ipsum is simply dummy text of the printing and typesetting industry."
                                       "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,"
                                       "when an unknown printer took a galley of type and scrambled it to make a type specimen book...",
                           area=67,
                           all_are=312,
                           rooms=4,
                           hirdeto="Példa Péter",
                           ingatlanIroda="Házadlesz Ingatlaniroda"
                           )


if __name__ == '__main__':
    app.run(debug=True)