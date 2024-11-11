class FelhasznaloController:


    def register_user(self, email, password, connection):
        try:
            print(f"Attempting to register user with email: {email} and password: {password}")
            cursor = connection.cursor()

            # Check if the email already exists in the database
            cursor.execute("SELECT * FROM Felhasznalo WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                raise Exception("This email is already registered.")

            # Insert new user into the database
            cursor.execute(
                "INSERT INTO Felhasznalo (email, jelszo) VALUES (%s, %s)",
                (email, password)
            )
            connection.commit()
            print(f"User {email} registered successfully.")
        except Exception as e:
            print(f"Error during user registration: {str(e)}")
            raise e
