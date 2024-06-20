import pyrebase

#Configure and Connext to Firebase

firebaseConfig = {apiKey: "AIzaSyD1HBW89Z1-DWj1d8byVQoiS1dFXY6yNDw",
authDomain: "ambulancego-5a9d5.firebaseapp.com",
projectId: "ambulancego-5a9d5",
storageBucket: "ambulancego-5a9d5.appspot.com",
messagingSenderId: "824728932698",
appId: "1:824728932698:web:269e4a9ae00ae669472363",
measurementId: "G-ZFLJ12T1SC"}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

#Login function

def login():
    print("Log in...")
    email=input("Enter email: ")
    password=input("Enter password: ")
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        print("Successfully logged in!")
        # print(auth.get_account_info(login['idToken']))
       # email = auth.get_account_info(login['idToken'])['users'][0]['email']
       # print(email)
    except:
        print("Invalid email or password")
    return

#Signup Function

def signup():
    print("Sign up...")
    email = input("Enter email: ")
    password=input("Enter password: ")
    try:
        user = auth.create_user_with_email_and_password(email, password)
        ask=input("Do you want to login?[y/n]")
        if ask=='y':
            login()
    except: 
        print("Email already exists")
    return

#Main

ans=input("Are you a new user?[y/n]")

if ans == 'n':
    login()
elif ans == 'y':
    signup()