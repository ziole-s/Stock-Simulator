import ttkbootstrap as ttk
import json
import bcrypt
import os
import csv

class Login:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.authenticated_user = False
        self.login = True
        self.signin = False

    def __str__(self):
        return "Login class made for login purposes in every project."

    def display_message(self, message_label, message, color="red"):
        message_label.config(text=message, foreground=color)

    def authenticate_user(self, username, password, window):
        self.username = username.get().strip().lower()
        self.password = password.get().strip().encode("utf-8")
        self.display_message(self.login_message_label, "")
        username_check = re.match(r"^[a-zA-Z0-9_]{1,30}$", self.username)
        if username_check:
            try:
                with open('User_data.json', 'r+') as user_data:
                    data = json.load(user_data)
                    if self.login == True and self.signin == False:
                        for user in data:
                            if user["username"] == self.username:
                                if bcrypt.checkpw(self.password, user["password"].encode("utf-8")):
                                    self.display_message(self.login_message_label, "Login successful!", "green")
                                    window.destroy()
                                    self.authenticated_user = True
                                    return
                                else:
                                    self.display_message(self.login_message_label, "Invalid password.")
                                    return
                    elif self.login == False and self.signin == True:
                            for user in data:
                                if user["username"] == self.username:
                                    self.login_message_label.config(text = "username exists")
                                    return
                            salt = bcrypt.gensalt()
                            hashed_pass = bcrypt.hashpw(self.password, salt).decode("utf-8")
                            new_entry = {"username": self.username, "password": hashed_pass}
                            data.append(new_entry)
                            user_data.seek(0)
                            json.dump(data, user_data, indent=4)
                            user_data.truncate()
                            self.create_user_stock_file(self.username)
                            self.display_message(self.login_message_label, "User added successfully!", "green")
                            window.destroy()
                            self.authenticated_user = True
                            return
            except FileNotFoundError:
                    self.display_message(self.login_message_label, "Server error")
            except json.JSONDecodeError:
                    self.display_message(self.login_message_label, "Server error")
        else:
            self.login_message_label.config(text = "Enter only letters, numbers and  _")
            return

    def create_user_stock_file(self, username):
        filename = f"{username}stock_data.csv"
        if not os.path.exists(filename):
            fieldnames = ['Day','Stock','Price','Cash','holdings']
            file_data = [{'Day':0,'Stock':'reliance','Price':100}, {'Day':0,'Stock':'tata motors','Price':100}, {'Day':0,'Stock':'itc','Price':100}, {'Day':0,'Stock':'mahindra','Price':100,'Cash':100000,'holdings':{}}]
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in file_data:
                    writer.writerow(row)

    def login_gui(self):
        login_window = ttk.Toplevel()
        login_window.resizable(False, False)
        login_window.title("TSA Login")
        login_window.geometry("400x250")

        ttk.Label(login_window, text="Welcome to TSA", font=("arial", 17, "bold")).pack()

        ttk.Label(login_window, text="Username: ", font=("arial", 12)).place(x=20, y=50)
        login_username_entry = ttk.Entry(login_window, width=30)
        login_username_entry.place(x=120, y=47)

        ttk.Label(login_window, text="Password: ", font=("arial", 12)).place(x=20, y=100)
        login_password_entry = ttk.Entry(login_window, show="*", width=30)
        login_password_entry.place(x=120, y=97)

        self.login_message_label = ttk.Label(login_window, text="", font=("arial", 10))
        self.login_message_label.place(x=20, y=130)

        login_button = ttk.Button(login_window, text="Login", style="primary-outline", width=13, command=lambda: self.authenticate_user(login_username_entry, login_password_entry, login_window))
        login_button.place(x=160, y=160)

        def transition_window():
            if self.login == True and self.signin == False:
                login_window.title("TSA Sign In")
                login_button.config(text = "Sign In")
                sign_in_label.config(text = "login")
                self.login, self.signin = False, True
                return
            elif self.login == False and self.signin == True:
                login_window.title("TSA Login")
                login_button.config(text="Login")
                sign_in_label.config(text = "sign in")
                self.login, self.signin = True, False
                return
        sign_in_label = ttk.Label(login_window, text = f"sign in", font = ("arial", 10), foreground = "blue")
        sign_in_label.place(x = 330, y =170)
        sign_in_label.bind("<Button-1>", lambda event: transition_window())
        login_window.wait_window()

