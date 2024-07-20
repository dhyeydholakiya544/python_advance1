import mysql.connector
import datetime

class PharmacyManager:
    def __init__(self, db_config):
        self.db_config = db_config
        self.db = self.connect_to_db()
        self.cursor = self.db.cursor()

    def connect_to_db(self):
        try:
            db = mysql.connector.connect(**self.db_config)
            return db
        except mysql.connector.Error as error:
            print(f"Failed to connect to MySQL database: {error}")
            return None

    def register_new_manager(self, manager_name, pharmacy_name):
        """Registers a new manager in the system."""
        try:
            query = "INSERT INTO Manager (ManagerName, PharmacyName) VALUES (%s, %s)"
            values = (manager_name, pharmacy_name)
            self.cursor.execute(query, values)
            self.db.commit()
            print("Manager registered successfully!")
        except mysql.connector.Error as error:
            print(f"Error registering manager: {error}")

    def login(self, manager_name):
        """Logs in an existing manager."""
        try:
            query = "SELECT * FROM Manager WHERE ManagerName = %s"
            values = (manager_name,)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            if result:
                print(f"Welcome, {manager_name}!")
                return True
            else:
                print("Invalid manager name. Please try again.")
                return False
        except mysql.connector.Error as error:
            print(f"Error logging in: {error}")
            return False

    def add_medicine(self, medicine_name, quantity):
        """Adds a new medicine to the system."""
        try:
            query = "INSERT INTO Medicine (MedicineName, Qty, AddedDate, AddedBy) VALUES (%s, %s, %s, %s)"
            added_date = datetime.datetime.now().strftime("%Y-%m-%d")
            values = (medicine_name, quantity, added_date, "Pharmacy Manager")
            self.cursor.execute(query, values)
            self.db.commit()
            print("Medicine added successfully!")
        except mysql.connector.Error as error:
            print(f"Error adding medicine: {error}")

    def view_all_medicine(self):
        """Displays all available medicines."""
        try:
            query = "SELECT * FROM Medicine"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            if result:
                print("Available Medicines:")
                for row in result:
                    print(f"SR.No: {row[0]}, Medicine Name: {row[1]}, Qty: {row[2]}, Added Date: {row[3]}, Added By: {row[4]}, Price: {row[5]}")
            else:
                print("No medicines available.")
        except mysql.connector.Error as error:
            print(f"Error viewing medicines: {error}")

    def delete_medicine(self, medicine_id):
        """Deletes a medicine from the system."""
        try:
            query = "DELETE FROM Medicine WHERE SRNo = %s"
            values = (medicine_id,)
            self.cursor.execute(query, values)
            self.db.commit()
            print(f"Medicine with SR.No {medicine_id} deleted successfully!")
        except mysql.connector.Error as error:
            print(f"Error deleting medicine: {error}")

    def close_connection(self):
        """Closes the database connection."""
        self.cursor.close()
        self.db.close()
        print("Database connection closed.")

class Admin(PharmacyManager):
    def __init__(self, db_config):
        super().__init__(db_config)

    def view_all_managers(self):
        """Displays all registered managers."""
        try:
            query = "SELECT * FROM Manager"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            if result:
                print("Registered Managers:")
                for row in result:
                    print(f"SR.No: {row[0]}, Manager Name: {row[1]}, Pharmacy Name: {row[2]}")
            else:
                print("No managers registered.")
        except mysql.connector.Error as error:
            print(f"Error viewing managers: {error}")

def main():
    # Database configuration
    db_config = {
        'host': 'localhost',
        'user': 'your_username',
        'password': 'your_password',
        'database': 'pharmacy_management'
    }

    # Create instances of PharmacyManager and Admin
    pharmacy_manager = PharmacyManager(db_config)
    admin = Admin(db_config)

    # Main loop
    while True:
        print("\nPharmacy Management System")
        print("1. Pharmacy Manager")
        print("2. Admin")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Pharmacy Manager operations
            while True:
                print("\nPharmacy Manager Operations")
                print("1. Register")
                print("2. Login")
                print("3. Add Medicine")
                print("4. View All Medicine")
                print("5. Delete Medicine")
                print("6. Back")

                manager_choice = input("Enter your choice: ")

                if manager_choice == '1':
                    manager_name = input("Enter manager name: ")
                    pharmacy_name = input("Enter pharmacy name: ")
                    pharmacy_manager.register_new_manager(manager_name, pharmacy_name)
                elif manager_choice == '2':
                    manager_name = input("Enter manager name: ")
                    if pharmacy_manager.login(manager_name):
                        # Perform manager actions here
                        pass
                elif manager_choice == '3':
                    medicine_name = input("Enter medicine name: ")
                    quantity = int(input("Enter quantity: "))
                    pharmacy_manager.add_medicine(medicine_name, quantity)
                elif manager_choice == '4':
                    pharmacy_manager.view_all_medicine()
                elif manager_choice == '5':
                    medicine_id = int(input("Enter medicine ID to delete: "))
                    pharmacy_manager.delete_medicine(medicine_id)
                elif manager_choice == '6':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '2':
            # Admin operations
            while True:
                print("\nAdmin Operations")
                print("1. Register")
                print("2. Login")
                print("3. View All Managers")
                print("4. Back")

                admin_choice = input("Enter your choice: ")

                if admin_choice == '1':
                    # Admin registration (if needed)
                    pass
                elif admin_choice == '2':
                    # Admin login (if needed)
                    pass
                elif admin_choice == '3':
                    admin.view_all_managers()
                elif admin_choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '3':
            print("Exiting the program...")
            pharmacy_manager.close_connection()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()