import requests
import pickle
import webbrowser
import time

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
    credentials = load_user_credentials()

    if not credentials:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        usertype = input("Enter your user type (0 for System User, 1 for Staff, 2 for Student): ")

        save_user_credentials(username, password, usertype)
        credentials = load_user_credentials()

    username = credentials["username"]
    password = credentials["password"]
    usertype = credentials["usertype"]

    while True:
        cookies = sis_login(username, password, usertype)

        if cookies:
            moodle_session_url = get_moodle_session(cookies)
            if moodle_session_url:
                print("[+] Moodle Session URL Retrieved Successfully")
                open_moodle_in_browser(moodle_session_url)
        else:
            print("[-] Login Failed. Retrying in 5 minutes...")

        time.sleep(3600)  
        
if __name__ == "__main__":
    auto_login()
