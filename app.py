import requests
from tkinter import *
from tkinter import messagebox
import pickle
import webbrowser
from PIL import Image, ImageTk

def save_cookies(cookies):
    with open('cookies.pkl', 'wb') as file:
        pickle.dump(cookies, file)
    print("[+] Cookies Saved Successfully")

def load_cookies():
    try:
        with open('cookies.pkl', 'rb') as file:
            return pickle.load(file)
    except (FileNotFoundError, pickle.PickleError):
        return None

def save_user_credentials(username, password, usertype):
    credentials = {
        "username": username,
        "password": password,
        "usertype": usertype,
    }
    with open('user_credentials.pkl', 'wb') as file:
        pickle.dump(credentials, file)
    print("[+] User Credentials Saved Successfully")

def load_user_credentials():
    try:
        with open('user_credentials.pkl', 'rb') as file:
            return pickle.load(file)
    except (FileNotFoundError, pickle.PickleError):
        return None

def sis_login(username, password, usertype):
    login_url = "https://sis.eelu.edu.eg/studentLogin"
    headers = {}
    data = {
        "UserName": username,
        "Password": password,
        "userType": usertype,
    }

    try:
        response = requests.post(login_url, data=data, headers=headers)
        response.raise_for_status()

        login_result = response.json()

        print(f"[DEBUG] Login Result: {login_result}")

        if login_result['rows'][0]['row']['LoginOK'] == "True":
            print("[+] Login Success")
            cookies = response.cookies.get_dict()
            save_cookies(cookies)
            save_user_credentials(username, password, usertype)
            return cookies
        else:
            return None

    except requests.exceptions.RequestException as err:
        print(f"[-] Error While Login: {err}")
        return None

def moodle_login(username, password, usertype):
    cookie = sis_login(username, password, usertype)

    if cookie:
        moodle_session_url = get_moodle_session(cookie)
        if moodle_session_url:
            return moodle_session_url
    return None

def get_moodle_session(cookie):
    url = "https://sis.eelu.edu.eg/getJCI"
    headers = {}
    data = {"param0": "stuAdmission.stuAdmission", "param1": "moodleLogin", "param2": "2"}

    try:
        response = requests.post(url, data=data, headers=headers, cookies=cookie)
        response.raise_for_status()
        result = response.json()
        return result['loginurl']

    except requests.exceptions.RequestException as err:
        print(f"[-] Error While Getting Moodle URL: {err}")
        return None

def open_moodle_in_browser(moodle_url):
    webbrowser.open(moodle_url)

def auto_login():
    username = username_var.get()
    password = password_var.get()
    usertype = user_type_var.get()

    cookies = sis_login(username, password, usertype)

    if cookies:
        moodle_session_url = get_moodle_session(cookies)
        if moodle_session_url:
            print("[+] Moodle Session URL Retrieved Successfully")
            open_moodle_in_browser(moodle_session_url)
    window.after(3600000, auto_login)

def login_button_click():
    username = entry_username.get()
    password = entry_password.get()
    usertype = user_type.get()

    username_var.set(username)
    password_var.set(password)
    user_type_var.set(usertype)

    result = moodle_login(username, password, usertype)

    if result:
        open_moodle_in_browser(result)
    else:
        messagebox.showerror("Login Failed", "Invalid credentials or Moodle connection issue.")

window = Tk()
window.title("Moodle EELU")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 600
window_height = 400
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2

window.geometry(f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')
window.configure(bg='#2b2b2b')
window.resizable(False, False)

username_var = StringVar()
password_var = StringVar()
user_type_var = StringVar()
user_type_var.set("2")

try:
    img = Image.open('avatar.png')
    img = img.resize((150, 150), Image.LANCZOS) 
    img = ImageTk.PhotoImage(img)
    image_label = Label(window, image=img, border=0, bg='#2b2b2b')
    image_label.photo = img
    image_label.place(x=(window_width - 100) // 2, y=20) 
except Exception as e:
    print(f"Image file 'avatar.png' not found or could not be loaded: {e}")

frame = Frame(window, width=400, height=200, bg='#3b3b3b', bd=5, relief=RIDGE)
frame.place(x=30, y=200)  

frame.propagate(False)

label_style = {'bg': '#3b3b3b', 'fg': '#ffffff', 'font': ('Arial', 12)}
entry_style = {'bg': '#ffffff', 'fg': '#000000', 'font': ('Arial', 12), 'width': 25}
button_style = {'bg': '#1a73e8', 'fg': '#ffffff', 'font': ('Arial', 12), 'activebackground': '#1a73e8', 'activeforeground': '#ffffff'}

Label(frame, text="Username:", **label_style).grid(row=0, column=0, padx=10, pady=5, sticky="e")
Label(frame, text="Password:", **label_style).grid(row=1, column=0, padx=10, pady=5, sticky="e")
Label(frame, text="User Type:", **label_style).grid(row=2, column=0, padx=10, pady=5, sticky="e")

entry_username = Entry(frame, **entry_style)
entry_username.grid(row=0, column=1, padx=10, pady=5)
entry_password = Entry(frame, show="*", **entry_style)
entry_password.grid(row=1, column=1, padx=10, pady=5)

user_type = StringVar()
user_type.set("2")

Radiobutton(frame, text="Student", variable=user_type, value="2", bg='#3b3b3b', fg='#ffffff', font=('Arial', 12), selectcolor='#2b2b2b').grid(row=2, column=1, padx=5, pady=5)
Radiobutton(frame, text="Staff", variable=user_type, value="1", bg='#3b3b3b', fg='#ffffff', font=('Arial', 12), selectcolor='#2b2b2b').grid(row=2, column=2, padx=5, pady=5)
Radiobutton(frame, text="System User", variable=user_type, value="0", bg='#3b3b3b', fg='#ffffff', font=('Arial', 12), selectcolor='#2b2b2b').grid(row=2, column=3, padx=5, pady=5)

login_button = Button(frame, text="Login", command=login_button_click, **button_style)
login_button.grid(row=3, column=0, columnspan=4, pady=10)

saved_credentials = load_user_credentials()
if saved_credentials:
    entry_username.insert(0, saved_credentials["username"])
    entry_password.insert(0, saved_credentials["password"])
    user_type.set(saved_credentials["usertype"])

window.after(3600000, auto_login)

window.mainloop()
