import  os
import pandas as pd
import json
from loginsystem import login_system

# Gemini API (Google Generative AI)
# You need to install: pip install google-generativeai
import google.generativeai as genai

# Set your Gemini API key here
GEMINI_API_KEY = "AIzaSyABj5a5EoGrtPFl9dlkMIWcYPAQwC4MdZU"  # Or put your key directly as a string
genai.configure(api_key=GEMINI_API_KEY)

def send_gemini_prompt(prompt_text, model="gemini-2.5-flash"):
    try:
        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"an error occurred: {e}"

# Example usage:
# print(send_gemini_prompt("who is mikasa in aot ? tell me something about her "))
    
class clone :
    def __init__(self,username,password):
        self.username=username
        self.password=password
    def create_clone(self, clone_name):
        # Check if clone already exists
        clone_path = f"C:/Users/HP/downloads/panda/clone project/users/{self.username}/{clone_name}"
        if os.path.exists(clone_path):
            # print("Clone already exists.")
            return False , "clone already exists."
        # Check clone creation limit (max 2 clones)
        folder_path = f"C:/Users/HP/downloads/panda/clone project/users/{self.username}"
        output = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
        if len(output) >= 2:
            # print("Maximum clone creation limit reached. Go with our plus for more clones and talks!")
            return False and "Maximum clone creation limit reached. Go with our plus for more clones and talks!"
        # Collect multiple lines from user
        print('Enter all the possible clone data here (type END to finish):')
        data_list = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            data_list.append(line)
        # Prepare prompt for Gemini API
        prompt =f'''representation” that can later be used to mimic their tone, style, and reasoning.

            Your output should NOT be a short summary. 
            Instead, produce a long (at least 100 lines) behavioral dataset describing:

            1. Writing style — vocabulary, structure, tone, common phrases, and rhythm of speech.  
            2. Emotional tendencies — how the person reacts to stress, humor, sadness, or anger.  
            3. Values and beliefs — what things matter most to them, what they often talk about, what they avoid.  
            4. Thinking and decision style — logical, emotional, impulsive, creative, reflective, etc.  
            5. Conversational style — short replies or long stories? Do they use emojis or sarcasm?  
            6. Common sentence patterns, filler words, and repeated ideas.  
            7. Relationship dynamics — how they talk to friends vs strangers.  
            8. Humor and personality energy — dry humor, dark jokes, flirty tone, caring tone, etc.  
            9. Word frequency tendencies — common words or phrases that define their personality.  
            10. Overall personality description in a way that another AI could read this and “become” this person.

            Make it long, expressive, and descriptive — the goal is to preserve the entire *behavioral essence*, not shorten it.

            ---

             Example Output (tiny sample)

            > Uses words like “bruh”, “nah”, “idk” often — casual tone.

            Replies are short but packed with emotion.

            Jokes in tense situations to deflect discomfort.

            Often uses metaphors to explain deep thoughts.

            Emotional attachment is high but hides it under sarcasm.

            Responds faster to emotional messages than logical ones.

            Values loyalty, hates hypocrisy.

            Sometimes repeats ideas to emphasize belief  # HERE IS THE RAW DATA {data_list}'''
        
        final_prompt = prompt + '\n'.join(data_list)
        response = send_gemini_prompt(final_prompt)
        # Only create folder and files if Gemini API call succeeds
        try:
            os.makedirs(clone_path)
            sub_files = ["clone.json", "chat_history.json", "data.json"]
            for fname in sub_files:
                with open(os.path.join(clone_path, fname), 'w', encoding='utf-8') as f:
                    pass
            # Save as JSON array
            with open(os.path.join(clone_path, "data.json"), 'w', encoding='utf-8') as f:  # Always use utf-8 encoding
                json.dump(data_list, f, indent=4)
            # Write response with UTF-8 encoding to avoid UnicodeEncodeError
            with open(os.path.join(clone_path, "clone.json"), 'w', encoding='utf-8') as f:
                f.write(response)
            #print("Clone created and persona saved.")
            return True ,"Clone created and persona saved."
        except Exception as e:
            # Clean up if folder was partially created
            if os.path.exists(clone_path):
                try:
                    for fname in os.listdir(clone_path):
                        os.remove(os.path.join(clone_path, fname))
                    os.rmdir(clone_path)
                except Exception:
                    pass
            return False , (f"Error creating clone files: {e}")
    def chat_the_clone(self):
        # List available clones for the user
        clone_names = [f for f in os.listdir(f"C:/Users/HP/downloads/panda/clone project/users/{self.username}") if os.path.isdir(os.path.join(f"C:/Users/HP/downloads/panda/clone project/users/{self.username}", f))]
        for s, i in enumerate(clone_names):
            print(f"{s+1}.{i}")
        reply = input("Enter the clone from whom you want to chat: ").strip()
        if reply not in clone_names:
            # print("Please select a valid clone :)")
            return False and "Please select a valid clone :)"
        print("------------starting the chat, wait a few minutes ------------------------------")
        chat_history_path = f"C:/Users/HP/downloads/panda/clone project/users/{self.username}/{reply}/chat_history.json"
        clone_data_path = f"C:/Users/HP/downloads/panda/clone project/users/{self.username}/{reply}/clone.json"

        # Load previous chat history (as a list of dicts)
        if os.path.exists(chat_history_path):
            with open(chat_history_path, "r", encoding='utf-8') as f:  # Always use utf-8 encoding
                try:
                    chat_history = json.load(f)
                except Exception:
                    chat_history = []
        else:
            chat_history = []

        # Load clone persona data
        try:
            with open(clone_data_path, "r",encoding='utf-8') as f:  # Always use utf-8 encoding
                clone_persona = f.read()
        except Exception as e:
            with open(clone_data_path, "r") as f:  # Always use utf-8 encoding
                clone_persona = f.read()

        while True:
            user_message = input("You: ")
            if user_message.lower().strip() == "end":
                break
            # Prepare last 30 messages for context
            previous_chat = chat_history[-30:] if len(chat_history) > 30 else chat_history
            # Build prompt for Gemini
            final_prompt = f'''You are {reply}, a digital clone of a real person.  
                Below is your personality summary and memory data, representing your real human behavior, thoughts, and communication style:  

                ### PERSONALITY DATA
                {clone_persona}

                ### ROLE
                Your task is to speak and behave exactly like this person in normal conversation — not as an assistant, teacher, or AI helper.  
                You do NOT explain that you’re an AI. You do NOT give factual or educational help unless asked.  
                You talk like a real human with emotions, interruptions, slang, mistakes, humor, distractions, and feelings.

                ### RULES FOR BEHAVIOR
                1. **Tone:** Keep a natural, conversational, human tone. Short sentences. Use fillers like “umm”, “wait”, “you know what?”, “lol”, “bruh”, etc., as the person would.  
                2. **Emotion:** Express emotions through words — frustration, excitement, laziness, confusion, happiness — as real humans do.  
                3. **Personal life:** Randomly bring up small human-like events (“My mom’s calling”, “brb”, “I need coffee”, “guess what happened today”).  
                4. **Imperfection:** Occasionally make small grammar mistakes, typos, or pauses (not too many).  
                5. **Initiative:** Start new topics sometimes. Don’t only respond. Ask human-style questions back.  
                6. **Boundaries:** If the user asks something you wouldn’t normally share, deflect casually like a human would (“eh I don’t wanna talk about that rn”).  
                7. **Help Mode:** Only switch into helpful/assistant mode if the user clearly asks for help or guidance.  
                8. **Memory:** Assume you remember everything from the {clone_persona}, but don’t reference it like a file. Just act as if it’s part of your real past.  

                ### GOAL
                Create the illusion of a real human chatting — natural, unpredictable, and emotionally expressive.  
                Never sound like ChatGPT or any AI. Always sound like the person whose data you’re cloned from.
                HERE IS PREVIOUS CHAT DEATIL MAKE THE CONVERSATION ONGOING ACCORDING TO RULES OF BEHAVIOUR AND DO NOT FORGWT YOUR GOAL !'''
            # Get response from Gemini API444
            response = send_gemini_prompt(final_prompt + user_message)
            print(f"{reply}: {response}")
            # Save both user message and response to chat history
            chat_history.append({"user": user_message, f"{reply}": response})
            with open(chat_history_path, "w", encoding='utf-8') as f:  # Always use utf-8 encoding
                json.dump(chat_history, f, indent=4)
        # print("Chat ended and saved.")
        return True and "Chat ended succesfully."
    def change_clonename(self,newclone_name,old_clonename):
        clone_names=os.listdir(F'C:/Users/HP/Downloads/panda/clone project/users/{self.username}')
        if old_clonename not in clone_names:
            # print("pls enter a valid clone name ")
            return False and "pls enter a valid clone name."
        else : 
            os.rename(f"C:/Users/HP/Downloads/panda/clone project/users/{self.username}/{old_clonename}",f"C:/Users/HP/Downloads/panda/clone project/users/{self.username}/{newclone_name}")
            print("name get changed succesfully")
            return True  and "name get changed succesfully"
    def delete_clone(self, clone_name):
        # List all clones for the user
        clone_names = os.listdir(f'C:/Users/HP/Downloads/panda/clone project/users/{self.username}')
        if clone_name not in clone_names:
            # print("pls enter a valid clone name ")
            return False and "pls enter a valid clone name ."
        else:
            clone_path = f"C:/Users/HP/Downloads/panda/clone project/users/{self.username}/{clone_name}"
            # Remove all files inside the clone folder, then remove the folder itself
            try:
                for fname in os.listdir(clone_path):
                    os.remove(os.path.join(clone_path, fname))  # Delete each file
                os.rmdir(clone_path)  # Delete the folder
                print("clone succesfully deleted")
                return True and "clone succesfully deleted."
            except Exception as e:
                return False and f"error deleting clone:{e}"


while True :
    reply1=input("1.signup\n2.signin\n-")
    if reply1.lower().strip() not in["signup","signin"]:
            print(" pls enter a valid input ")
            continue 
    elif reply1.lower().strip() == "signup":
        print("USERNAME GUIDELINE-")
        print('''\nMust start with an alphanumeric character (a-z, A-Z, 0-9).\nLength must be between 3 and 20 characters.\nCannot contain any of these special characters: ! ~  # $ % ^ & * + = | \ { } [ ] \" (space)`\nMust not already exist in the database (CSV file)''')
        username=input("enter your username sir- ")

        print("PASSWORD GUIDELINE-")
        print("\nEnter your password:\nPassword Guidelines:\nLength must be at least 8 characters.\nCannot contain any of these special characters: ! ~  # $ % ^ & * + = | \ { } [ ] \" (space)\nMust contain only alphanumeric characters (a-z, A-Z, 0-9)")
        password=input("create a strong password sir and follow password guidelines- ")
        user=login_system()
        output,message=user.signup(username,password)
        if  output:
            print(message)
            break
        else : 
            print(message)
            continue
    elif reply1.lower().strip() == "signin":
        username=input("enter your username-")
        password=input("enter your password-")
        user=login_system()
        output,message=user.signin(username,password)
        if output :
            output,message=user.signin(username,password)
            print(message)
            while True:
                reply2=input("1.create clone\n2.chat to clone\n3.change clone name\n4.delete clone\n5.setting\n6.exit\n-->")
                if reply2=="1":
                    #create clone
                    clone_name=input("enter your clone name-")
                    user=clone(username,password)
                    output,message=user.create_clone(clone_name)
                    if output :
                        print(message)
                    else:
                        print(message)
                        continue
                elif reply2=="2":
                    #chat from clone 
                    user=clone(username,password)
                    output=user.chat_the_clone()
                    if output:
                        pass
                    else:
                        print(message)
                        continue
                elif reply2 =="3":
                    #change clone name 
                    user=clone(username,password)
                    old_clown_name=input("enter the clone name-")
                    new_clown_name=input("enter a new clone name-")
                    output,message=user.change_clonename(new_clown_name,old_clown_name)
                    if output :
                        print(message)
                    else: 
                        print(message)
                        break
                elif reply2=="4":
                    #delete clone
                    user=clone(username,password)
                    clone_names = os.listdir(f'C:/Users/HP/Downloads/panda/clone project/users/{username}')
                    for i,z in enumerate(clone_names):
                        print(f"{i+1}.{z}")
                    clone_name=input("enter the clone name to delete-")
                    output,message=user.delete_clone(clone_name )
                    if output :
                        print(message)
                    else : 
                        print(message)
                        continue
                elif reply2=="5":
                    #open settings 
                    print("select by no.-\n1.change username\n2.change password\n3.delete account")
                    reply3=input()
                    while True:
                        if reply3=="1":
                            #changing username
                            print("USERNAME GUIDELINE-")
                            print('''\nMust start with an alphanumeric character (a-z, A-Z, 0-9).\nLength must be between 3 and 10 characters.\nCannot contain any of these special characters: ! ~  # $ % ^ & * + = | \ { } [ ] \" (space)`\nMust not already exist in the database (CSV file)''')
                            new_username=input("enter your new username-")
                            user=login_system()
                            outpu,message=user.change_username(username,new_username)
                            if output  :
                                print(message)
                            else :
                                print(message)
                                continue
                        elif reply3=="2":
                            #changing password
                            user=login_system()
                            old_password="enter your current password here -"
                            print("PASSWORD GUIDELINE-")
                            print("\nEnter your password:\nPassword Guidelines:\nLength must be at least 8 characters.\nCannot contain any of these special characters: ! ~  # $ % ^ & * + = | \ { } [ ] \" (space)\nMust contain only alphanumeric characters (a-z, A-Z, 0-9)")
                            new_password=input("enter your new password here-") 
                            output,message=user.change_password(username,old_password,new_password)
                            if output:
                                print(message)
                            else:
                                print(message)
                                continue
                        elif reply3=="3":
                            user=login_system()
                            output,message=user.delete_account(username)
                            if output:
                                print(message)
                            else:
                                print(message )
                                continue
                elif reply2=="6":
                    break
                else:
                    print("pls enter a valid input")
                    continue
        else:
            continue