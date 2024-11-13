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

    def get_user_by_email(self, email, connection):
        cursor = connection.cursor()
        # Query to fetch the user based on email, including felhID (user ID)
        cursor.execute("SELECT felhID, email, jelszo FROM Felhasznalo WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()  # Make sure to close the cursor after the query
        return user

    def get_user_by_id(self, user_id, connection):
        cursor = connection.cursor()
        # Query to fetch the user based on user ID
        cursor.execute("SELECT felhID, email, jelszo FROM Felhasznalo WHERE felhID = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()  # Close the cursor
        return user