import numpy as np
import pandas as pd
import torch    
import time
import os
import json
from pipeline_trigger import status
from transformers import AutoTokenizer, AutoModelForCausalLM

def load_model(model_name):
    """
    Load the model and tokenizer.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code = True)
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code = True)
    
    tokenizer.pad_token = tokenizer.eos_token
    
    return tokenizer, model

def generate_question(few_shot_prompt, tokenizer, model, device, behavior, current_mood):
    """
    Generate a question based on the behavior and current mood."""
    behavior_str = json.dumps(behavior, indent=4)
    prompt = f"{few_shot_prompt}\nBehavior: {behavior_str}\nCurrent mood: {current_mood}\nQuestion: "
    inputs = tokenizer(prompt, return_tensors="pt")
    if device == "cuda":
        inputs = inputs .to(device)
        model = model.to(device)
    outputs = model.generate(inputs["input_ids"], max_length=500, temperature=0.7, top_p=0.9, num_return_sequences=1, do_sample=True)
    question = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extracting the actual question part from the output
    question = question.split('Question:')[-1].strip()
    return question

# Function to extract and format the data
def extract_and_format_data(data):
    """
    Extract and format the data.
    """
    extracted_data = []
    for item in data:
        for key, values in item.items():
            for value in values:
                for sub_key in value:
                    if sub_key != "verified":
                        extracted_data.append({key: sub_key})
    return extracted_data

def inference(model_name, data, current_mood):
    """
    Perform inference on the model and tokenizer.
    """

    few_shot_prompt = f"""
        Generate a witty, very short, and satirical yes/no question to validate the user data based on their current mood.

        Example 1:
        Behavior: "app_usages": ["music"],
        Current mood: happy,
        Question: "Do you really enjoy music or just pretending to be cool? Yes/No"

        Example 2:
        Behavior: "frequent_visits": ["landmarks","nature"],
        Current mood: sad,
        Question: "Are you visiting landmarks and nature spots to find happiness? Yes/No"

        Example 3:
        Behavior: "likes": ["pets"],
        Current mood: angry,
        Question: "Do you like pets to calm down or to train them to take over the world? Yes/No"
        """
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model, tokenizer = load_model(model_name)
    question = generate_question(few_shot_prompt, tokenizer, model, device, data, status(tokenizer, model))
    # formatted_data = extract_and_format_data(data)
    for key, value in data.items():
        # print({key:value})
        t1 = time.time() 
        question = generate_question({key: value}, current_mood)
        print(f"Generated question for {key}: {question}")
        print("Time taken:", time.time()-t1)
        


if __name__ == "__main__":
    model_name = "microsoft/Phi-3-mini-4k-instruct"
    with open('data.json', 'r') as f:
        user_data = json.load(f)
    current_mood = "sad"
    inference(model_name, user_data, current_mood)