def coder(reply1):
    split1=reply1.split()
    # print(split1)
    list1=list(split1)
    # print(list1)
    code=[]
    import random
    chracters=("`1234567890-=/*789+456+12.0qwertyuiop[]asdfghjkl;'zxcvnbm,./,<>?:'")
    for i in list1:
        if len(i)<3:
            code.append(i[::-1])
        if len(i)>=3:
            shifted_word=i[1:]+i[0]
            random1="".join(random.choices(chracters,k=3))
            random2="".join(random.choices(chracters,k=3))
            str1=random1+shifted_word+random2
            code.append(str1)
    else:
       here=" ".join(code)
       return here

def decode(x):
    split1=x.split()
    # print(split1)
    list1=list(split1)
    # print(list1)
    decode=[]
    for i in split1:
        if len(i)<3:
            decode.append(i[::-1])
        if len(i) >=3 :
            remove=i[3:-3]
            # remove2=remove-i[-1,-3]
            unshifted=remove[-1]+remove[0:-1]
            decode.append(unshifted)
    else:
       here=" ".join(decode)
       return here
import os
import pandas as pd 
# creating  a user system class
class login_system:
    def __init__(self):
        pass

    def signup(self, username, password):
        # Username check: must start with alphanumeric, length 3-10, no special chars
        def checking_username(username):
            if not username[0].isalnum():
                return False, "pls follow user guideline"
            if len(username) < 3 or len(username) > 20:
                return False, "pls follow user guideline"
            for ch in username:
                if ch in "!~`#$%^&*+=|\\{}[]\" ":
                    return False, "pls follow user guideline"
            # Check if username already exists in CSV
            df = pd.read_csv("server.csv")
            if username in df["username"].values:
                return False, "username already exist "
            else:
                return True, " "

        # Password check: length >=8, only alphanumeric, no special chars
        def checking_password(password):
            if len(password) < 8:
                return False, "pls follow password guideline"
            for ch in password:
                if ch in "!~`#$%^&*+=|\\{}[]\" ":
                    return False, "pls follow password guideline"
            if not password.isalnum():
                return False, "pls follow password guideline"
            return True, ""

        # Generate a unique tag
        import random
        data = []
        while True:
            tag = random.randint(100, 9999)
            if tag not in data:
                data.append(tag)
                break

        # If both checks pass, add user to CSV
        valid_pass, pass_msg = checking_password(password)
        valid_user, user_msg = checking_username(username)
        if valid_pass and valid_user:
            try:
                df = pd.read_csv('server.csv')
            except Exception:
                df = pd.DataFrame(columns=["username", "password", "tag"])
            new_row = {"username": username, "password": coder(password), "tag": (str(tag))}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv('server.csv', index=False)
            # print("signup successful")
            # creating a folder for user
            import os
            if not os.path.exists("users"):
                os.makedirs("users")
            user_folder = os.path.join("users", username)
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            return True, "sign up done succesfully"
        else:
            # print("sign up get fail try again")
            if not valid_pass:
                return False, pass_msg
            else:
                return False, user_msg
    # creating sign in function
    def signin(self, username, password):
        try:
            df = pd.read_csv('server.csv')
            if username not in df['username'].values:
                return False, "sign up first"
            user_row = df[df['username'] == username]
            if password == decode(user_row["password"].values[0]):
                return True, "sign in done succesfully"
            else:
                return False, "Incorrect password"
        except Exception as ex:
            print(f"something went wrong, try later :) Error: {ex}")
            return False, "Something went wrong  pls try again later"
     # delete account
    def delete_account(self, username):
        try:
            df = pd.read_csv('server.csv')
            if username not in df['username'].values:
                # print("sign up first")
                return False and "Sign up first"
            df = df[df['username'] != username]
            df.to_csv('server.csv', index=False)
            # print("account deleted successfully")
            return True and "account deleted succesfully"
        except Exception as ex:
            # print("something went wrong")
            return False and "Something went wrong"
    # change username
    def change_username(self, old_username, new_username):
        def checking_username(username):
            if not username[0].isalnum():
                return False and "pls follow username guideline"
            if len(username) < 3 or len(username) > 20:
                return False and "pls follow username guideline"
            for ch in username:
                if ch in "!~`#$%^&*+=|\\{}[]\" ":
                    return False and "pls follow username guideline"
            try:
                df = pd.read_csv("server.csv")
                if username in df["username"].values:
                    # print("username already exist ")
                    return False and "Username already exist "
            except Exception:
                pass
            return True
        if checking_username(new_username):
            df = pd.read_csv("server.csv")
            df.loc[df["username"] == old_username, "username"] = new_username
            df.to_csv("server.csv", index=False)
            print("change done successfully", new_username)
            os.rename(os.rename(f"C:/Users/HP/Downloads/panda/clone project/users/{self.username}/{old_username}",f"C:/Users/HP/Downloads/panda/clone project/users/{new_username}"))
            return True and "change done succesfully"
        else: 
            # print("pls follow username guidelines ")
            return False and "pls follow username guideline"
    #change passsword
    def change_password(self, username, old_password, new_password):
        df = pd.read_csv('server.csv')
        # 1. Filter the DataFrame for the user
        user_row = df[df['username'] == username]
        if user_row.empty:
            # print("Username not found.")
            return False and "username not found"
        # 2. Decode the stored password and compare with old_password
        stored_encoded_password = user_row['password'].values[0]
        if decode(stored_encoded_password) != old_password:
            # print("Old password is incorrect.")
            return False and "Old password is incorrect"
        # 3. Encode the new password and update the DataFrame
        def checking_password(password):
            if len(password) < 8:
                return False and "pls follow password guideline"
            for ch in password:
                if ch in "!~`#$%^&*+=|\\{}[]\" ":
                    return False and "pls follow password guideline"
            if not password.isalnum():
                return False and "pls follow password guideline"
            return True
        if not checking_password(new_password):
            # print("New password does not meet the requirements.")
            return False  and "pls follow password guideline"
        else:
            df.loc[df['username'] == username, 'password'] = coder(new_password)
            df.to_csv('server.csv', index=False)
            # print("Password changed successfully.")
            return True and "Password changed succesfylly"



# user=login_system()
# a=user.signup('alok',"anmolmilk")
# print(a)

            