
import os
import pandas as pd
import json
import requests
import shutil
from loginsystem import login_system
from dotenv import load_dotenv
load_dotenv()

# Gemini API (Google Generative AI)
# You need to install: pip install google-generativeai
import google.generativeai as genai

# Set your Gemini API key here
GEMINI_API_KEY =  os.getenv("gemini_key") # Or put your key directly as a string
genai.configure(api_key=GEMINI_API_KEY)

def send_gemini_prompt(prompt_text, model="gemini-2.5-flash"):
    try:
        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"an error occurred: {e}"

DEFAULT_PROFILE_PIC_URL = "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y"  # Placeholder image

def sanitize_filename(name):
    # Replace spaces and illegal characters with underscores
    import re
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name.strip().replace(' ', '_'))

def download_and_save_image(image_url, target_path):
    try:
        response = requests.get(image_url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(target_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            return True, "Image downloaded."
        else:
            return False, f"Failed to download image: {response.status_code}"
    except Exception as e:
        return False, f"Error downloading image: {e}"

def load_chat_history(username, clone_name):
    chat_history_path = f"C:/Users/HP/downloads/panda/clone project/users/{username}/{clone_name}/chat_history.json"
    if os.path.exists(chat_history_path):
        try:
            with open(chat_history_path, "r", encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

class clone:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def create_clone(self, clone_name, raw_data_string):
        clone_name = sanitize_filename(clone_name)
        clone_path = f"C:/Users/HP/downloads/panda/clone project/users/{self.username}/{clone_name}"
        if os.path.exists(clone_path):
            return False, "Clone already exists."
        folder_path = f"C:/Users/HP/downloads/panda/clone project/users/{self.username}"
        output = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
        if len(output) >= 2:
            if self.username != "aman":
                return False, "Maximum clone creation limit reached. Go with our plus for more clones and talks!"
        data_list = raw_data_string
        prompt = f'''representation” that can later be used to mimic their tone, style, and reasoning.

Your output should NOT be a short summary. 
Instead, produce a long (at least 1000 lines) behavioral dataset describing:

ocabulary, structure, tone, common phrases, and rhythm of speech.  
2. Emotional tendencies — how the person reacts to stress, humor, sadness, or anger.  
3. Values and beliefs — what things matter most to them, what they often talk about, what they avoid.  
4. Thinking and decision style — logical, emotional, impulsive, creative, reflective, etc.  
5. Conversational style — short replies or long stories? Do they use emojis or sarcasm?  
6. Common sentence patterns, filler words, and repeated ideas.  
7. Relationship dynamics — how they talk to friends vs strangers.  
8. Humor and personality energy — dry humor, dark jokes, flirty tone, caring tone, etc.  
9. Word frequency tendencies — common words or phrases that define their personality.  
10. Overall personality description in a way that another AI could read this and “become” this person.
11.also find a average no tokens in which the person replies. 

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
        final_prompt = prompt 
        response = send_gemini_prompt(final_prompt)
        try:
            os.makedirs(clone_path)
            # Download default profile image
            img_ok, img_msg = download_and_save_image(DEFAULT_PROFILE_PIC_URL, os.path.join(clone_path, "profile.jpg"))
            sub_files = ["clone.json", "chat_history.json", "data.json", "profile.jpg"]
            for fname in ["clone.json", "chat_history.json", "data.json"]:
                with open(os.path.join(clone_path, fname), 'w', encoding='utf-8') as f:
                    pass
            with open(os.path.join(clone_path, "data.json"), 'w', encoding='utf-8') as f:
                json.dump(data_list, f, indent=4)
            with open(os.path.join(clone_path, "clone.json"), 'w', encoding='utf-8') as f:
                f.write(response)
            return True, "Clone created and persona saved. " + (img_msg if img_ok else "Default image not set.")
        except Exception as e:
            if os.path.exists(clone_path):
                try:
                    for fname in os.listdir(clone_path):
                        os.remove(os.path.join(clone_path, fname))
                    os.rmdir(clone_path)
                except Exception:
                    pass
            return False, f"Error creating clone files: {e}"

    def chat_the_clone(self, clone_name, user_input):
        clone_name = sanitize_filename(clone_name)
        chat_history_path = f"C:/Users/HP/downloads/panda/clone project/users/{self.username}/{clone_name}/chat_history.json"
        clone_data_path = f"C:/Users/HP/downloads/panda/clone project/users/{self.username}/{clone_name}/clone.json"
        chat_history = []
        if os.path.exists(chat_history_path):
            with open(chat_history_path, "r", encoding='utf-8') as f:
                try:
                    chat_history = json.load(f)
                except Exception:
                    chat_history = []
        # Load clone persona data
        try:
            with open(clone_data_path, "r", encoding='utf-8') as f:
                clone_persona = f.read()
        except Exception:
            clone_persona = ""
        # Prepare last 30 messages for context
        previous_chat = chat_history[-60:] if len(chat_history) > 60 else chat_history
        # Build prompt for Gemini
        final_prompt = f'''You are {clone_name}, a digital clone of a real person.  
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
8. **Memory:** Assume you remember everything from the (PERSONALITY DATA), but don’t reference it like a file. Just act as if it’s part of your real past.  

### GOAL
Create the illusion of a real human chatting — natural, unpredictable, and emotionally expressive.
try to never give a large response   
Never sound like ChatGPT or any AI. Always sound like the person whose data you’re cloned from.
HERE IS PREVIOUS CHAT DEATIL MAKE THE CONVERSATION ONGOING ACCORDING TO RULES OF BEHAVIOUR AND DO NOT FORGWT YOUR GOAL !

### PREVIOUS CHAT
    {previous_chat}
### RECENT 10 MESSAGES
    {previous_chat[-10:]}
### GIVE RESPONSE IN FOLLOWING CRITARYIA
    GIVE RESPONSE ACCORDING TO AVG TOOKENS THAT IS MENTIONES IN PERSONALITY DATA AND IF NEEDED 
        TARGETD OUTPUT=5 TO 50 TOKENS 
        MAX (IF USER NEED EXPLANIATION OR ASKING SOMETHING THAT IS NEEDED TO EXPLAIN IN DETAIL)=75 TOKENS 
### USER INPUT
    {user_input}

'''
        
        # Get response from Gemini API
        ai_response = send_gemini_prompt(final_prompt)
        # Save both user message and response to chat history
        chat_history.append({"sender": "user", "text": user_input})
        chat_history.append({"sender": "clone", "text": ai_response})
        with open(chat_history_path, "w", encoding='utf-8') as f:
            json.dump(chat_history, f, indent=4)
        return True, ai_response

    def change_clonename(self, newclone_name, old_clonename):
        newclone_name = sanitize_filename(newclone_name)
        old_clonename = sanitize_filename(old_clonename)
        clone_names = os.listdir(f'C:/Users/HP/Downloads/panda/clone project/users/{self.username}')
        if old_clonename not in clone_names:
            return False, "Please enter a valid clone name."
        else:
            os.rename(f"C:/Users/HP/Downloads/panda/clone project/users/{self.username}/{old_clonename}",
                        f"C:/Users/HP/Downloads/panda/clone project/users/{self.username}/{newclone_name}")
            return True, "Name changed successfully."

    def delete_clone(self, clone_name):
        clone_name = sanitize_filename(clone_name)
        clone_names = os.listdir(f'C:/Users/HP/Downloads/panda/clone project/users/{self.username}')
        if clone_name not in clone_names:
            return False, "Please enter a valid clone name."
        else:
            clone_path = f"C:/Users/HP/Downloads/panda/clone project/users/{self.username}/{clone_name}"
            try:
                for fname in os.listdir(clone_path):
                    os.remove(os.path.join(clone_path, fname))
                os.rmdir(clone_path)
                return True, "Clone successfully deleted."
            except Exception as e:
                return False, f"Error deleting clone: {e}" 