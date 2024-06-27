import json
import time
from inference import *

def status(data, specific_key=None, prompt_interval=None):
    """
    Iterate through the user data and decide when to ask for verification or clarification.
    If specific_key is provided, only print prompts related to that key.
    If prompt_interval is provided, print prompts based on the time interval.
    """
    current_time = time.time()
    
    for key, values in data.items():
        if specific_key and key != specific_key:
            continue  # Skip keys that are not the specific key
        
        for item in values:
            for sub_key, sub_value in item.items():
                if sub_key == "verified":
                    continue  # Skip the 'verified' key to only check the main value

                verified = item.get("verified")
                if sub_value and not verified:
                    if prompt_interval and (current_time - last_prompt_time < prompt_interval * 3600):
                        continue  # Skip if the interval has not passed
                    verification(key, sub_key)
                elif not sub_value and verified:
                    if prompt_interval and (current_time - last_prompt_time < prompt_interval * 3600):
                        continue  # Skip if the interval has not passed
                    clarification(key, sub_key)

def verification(category, item_name):
    """
    Verification process for items that are true but not yet verified.
    """
    global last_prompt_time
    prompt = f"Do you really like {item_name}?"
    print(prompt)  # Simulate sending the prompt
    response = input("Your Response: ")  # Simulate user input

    if response.lower() in ['yes', 'y']:
        update_data(category, item_name, True)
    else:
        update_data(category, item_name, False)
    
    last_prompt_time = time.time()  # Update the last prompt time

def clarification(category, item_name):
    """
    Clarification process for items that are verified but initially false.
    """
    global last_prompt_time
    prompt = f"You mentioned you don't like {item_name}, so what do you like?"
    print(prompt)  # Simulate sending the prompt
    response = input("Your Response: ")  # Simulate user input

    if response.lower() in ['yes', 'y']:
        update_data(category, item_name, False)
    else:
        update_data(category, item_name, True)
    
    last_prompt_time = time.time()  # Update the last prompt time

def update_data(category, item_name, status):
    """
    Update the data based on the response.
    """
    for item in user_data[category]:
        if item_name in item:
            item[item_name] = status
            item["verified"] = True
    save_data()

def save_data():
    """
    Save the updated user data back to the JSON file.
    """
    with open('data.json', 'w') as f:
        json.dump(user_data, f, indent=4)

if __name__ == "__main__":
    with open('data.json', 'r') as f:
        user_data = json.load(f)
    
    # Define the specific key you want to prompt for
    specific_key = None
    
    # Define the interval in hours
    prompt_interval = 1  # 1 hour

    # Initialize last prompt time
    last_prompt_time = 1719295667.3053992

    status(user_data, specific_key, prompt_interval)
    print("Updated User Data:")
    print(json.dumps(user_data, indent=4))
