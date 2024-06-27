import json
from inference import *

def status(data):
    """
    Iterate through the user data and decide when to ask for verification or clarification.
    """
    for key, values in data.items():
        for item in values:
            for sub_key, sub_value in item.items():
                if sub_key == "verified":
                    continue  # Skip the 'verified' key to only check the main value

                verified = item.get("verified")
                if sub_value and not verified:
                    verification(key, sub_key)
                elif not sub_value and verified:
                    clarification(key, sub_key)

def verification(category, item_name):
    """
    Verification process for items that are true but not yet verified.
    """
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # model_name = "microsoft/Phi-3-mini-4k-instruct"
    # model, tokenizer = model_load(model_name)    
    # prompt = prompt_ubts(model, tokenizer, item_name, device)
    prompt = f"Do you really like {item_name}?"
    print(prompt)  # Simulate sending the prompt
    response = input("Your Response: ")  # Simulate user input

    if response.lower() in ['yes', 'y']:
        update_data(category, item_name, True)
    else:
        update_data(category, item_name, False)

def clarification(category, item_name):
    """
    Clarification process for items that are verified but initially false.
    """
    prompt = f"You mentioned you don't like {item_name}, so what do you like?"
    print(prompt)  # Simulate sending the prompt
    response = input("Your Response: ")  # Simulate user input

    if response.lower() in ['yes', 'y']:
        update_data(category, item_name, False)
    else:
        update_data(category, item_name, True)

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
    
    status(user_data)
    print("Updated User Data:")
    print(json.dumps(user_data, indent=4))
