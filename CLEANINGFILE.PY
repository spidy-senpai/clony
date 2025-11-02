import json
import os

# --- Configuration ---
# Use os.path.join for robust path handling that works on any OS
INBOX_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "your_instagram_activity", "messages", "inbox")
try:
    all_chats = os.listdir(INBOX_PATH)
except FileNotFoundError:
    print(f"Error: The directory does not exist: {INBOX_PATH}")
    print("Please make sure your Instagram data is in the correct location.")
    all_chats = []

# The name that the script will use for the second participant (the user)
USER_NAME_PLACEHOLDER = "User"

def clean_chat_history(filepath):
    """
    Loads, cleans, and formats the Instagram JSON chat history into a simple,
    chronologically ordered 'Sender: Message' text format suitable for AI training.
    """
    if not os.path.exists(filepath):
        # This error is now more specific
        print(f"Warning: 'message_1.json' not found in this chat folder. Skipping.")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}. The file might be corrupted.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading {filepath}: {e}")
        return

    # 1. Identify participants and map the complex name to 'User'
    participants = data.get('participants', [])
    if not participants:
        print("Warning: No participants found in this chat. Skipping.")
        return
        
    participants = [p['name'] for p in participants]
    
    # Assuming 'Mr.Spidy' is the character name, the other name is the user.
    name_map = {}
    user_real_name = None

    for name in participants:
        # This special character name seems to be your identifier
        if name != "Ayush priyadarshi":
            name_map[name] = USER_NAME_PLACEHOLDER
            user_real_name = name
        else:
            name_map[name] = "ayush"

    print("--- Detected Participants and Mappings ---")
    print(f"Mr.Spidy (Clone): adi")
    if user_real_name:
        print(f"You (Original Name: {user_real_name}): {USER_NAME_PLACEHOLDER}")
    print("------------------------------------------\n")


    # 2. Extract and clean messages
    messages = data.get('messages', [])
    
    # Instagram JSON provides messages from newest to oldest, so we reverse it.
    messages.reverse()

    cleaned_history = []
    
    for message in messages:
        sender = message.get('sender_name')
        content = message.get('content')
        
        # Filter out system messages, attachments, and stories, and ensure content exists
        if content and not content.startswith("You sent an attachment.") and not content.startswith("You sent a photo.") and not content.startswith("You sent a video."):
            # Get the display name (e.g., 'User' or 'Mr.Spidy')
            display_sender = name_map.get(sender, sender)
            
            # Simple cleanup: remove extra newlines and ensure it's not too short
            cleaned_content = content.strip().replace('\n', ' ')
            
            if cleaned_content:
                cleaned_history.append(f"{display_sender}: {cleaned_content}")
    
    with open("cleaned_chat_wuthayush.txt", "a", encoding="utf-8") as outfile:
        outfile.write("\n".join(cleaned_history) + "\n\n------------------------ANOTHER CHAT IT COULD BE A DIECT MESSAGE OR A GROUP CHAT----------------------------------------\n\n")

    # 3. Print the final result
    print("--- CLEANED AND FORMATTED CHAT HISTORY (Ready for API) ---")
    print("\n".join(cleaned_history))
    print("------------------------ANOTHER CHAT IT COULD BE A DIECT MESSAGE OR A GROUP CHAT----------------------------------------\n")


if __name__ == "__main__":
    # if not all_chats:
    #     print("No chat folders found to process.")
    # else:
    #     verified_chats = []
    #     for chat in all_chats:
    #         # Make the check case-insensitive and check for digits
    #         chat_lower = chat.lower()
    #         if chat_lower.startswith("instagramuser") or any(chat.startswith(str(i)) for i in range(10)):
    #             # print(f"Skipping folder: {chat}")
    #             continue  # Skip this folder
    #         verified_chats.append(chat)
        
    #     print(f"\nFound {len(verified_chats)} chat(s) to process.\n")
    #     print(verified_chats)

    #     for chat in verified_chats:
    #         print(f"--- PROCESSING CHAT: {chat} ---")
    #         # Use os.path.join for creating the file path
    #         input_file = os.path.join(INBOX_PATH, chat, "message_1.json")
    #         clean_chat_history(input_file)
    #     else:
    #         print("--- All data processing complete. ---")
    clean_chat_history("C:/Users/HP/Downloads/your_instagram_activity/messages/inbox/ayushpriyadarshi_17985419861715694/message_1.json")
# import os
# import sys

# # --- CONFIGURATION ---
# INPUT_HISTORY_FILE = "cleaned_chat.txt"
# TARGET_SENDER_NAME = "adi" # This is the specific user whose dialogue we want to extract

# def filter_training_dialogue(filepath, sender_name):
#     """
#     Reads the cleaned chat history and filters it to extract ONLY the lines
#     spoken by the target clone ('adi').

#     This process is CRUCIAL for clone fidelity:
#     1. Reduces the total byte size (solving 'Request Entity Too Large').
#     2. Reduces cognitive load (solving '504 Deadline Exceeded').
#     3. Eliminates all other character voices (solving 'Confusion').
#     """
#     if not os.path.exists(filepath):
#         print(f"Error: Training file not found at {filepath}", file=sys.stderr)
#         return ""

#     adi_lines = []
#     try:
#         with open(filepath, 'r', encoding='utf-8') as f:
#             lines = f.readlines()

#             for line in lines:
#                 line = line.strip()
#                 # 1. Check if the line starts with the target name followed by a colon
#                 if line.startswith(f"{sender_name}:"):
#                     # 2. Remove the 'adi:' prefix and any surrounding whitespace
#                     dialogue = line.replace(f"{sender_name}:", "", 1).strip()
                    
#                     # 3. Filter out empty lines or system messages the cleaner missed
#                     if dialogue and not dialogue.lower().startswith(("liked a message", "sent an attachment")):
#                         adi_lines.append(dialogue)
                        
#     except Exception as e:
#         print(f"Error reading or processing file: {e}", file=sys.stderr)
#         return ""

#     return "\n".join(adi_lines)

# # --- Main Execution ---

# if __name__ == "__main__":
    
#     # 1. Execute the filtering process
#     raw_training_data = filter_training_dialogue(INPUT_HISTORY_FILE, TARGET_SENDER_NAME)

#     if not raw_training_data:
#         print("\n[--- ERROR ---] No relevant dialogue found. Check if the file exists and if the sender name is correct.", file=sys.stderr)
#     else:
#         # 2. Print the result clearly for easy copying
#         print("\n=======================================================")
#         print(f"  CLEANED RAW TRAINING DATA FOR '{TARGET_SENDER_NAME.upper()}' CLONE")
#         print("  (Copy this entire block for API injection)")
#         print("=======================================================\n")
        
#         # This is the pure, unfiltered text of Adi's lines, ready for injection.
#         print(raw_training_data)
#         with open("final_training_data.txt", "w", encoding="utf-8") as out_file:
#             out_file.write(raw_training_data)
        
#         print(f"\n=======================================================")
#         print(f"Successfully extracted {len(raw_training_data.splitlines())} lines of dialogue.")
#         print("=======================================================")
