from audiocraft.models import musicgen
import torch
import torchaudio
import time
from openai import OpenAI 
from dotenv import load_dotenv
import os
import json
load_dotenv()


class ChoiraGenerate:
    def __init__(self,socketio) -> None:
        self.socketio = socketio
        self.model = musicgen.MusicGen.get_pretrained('large', device='cuda')
        self.socket_id = 0
        

    def generate_music_large(self,original_prompt,prompt,duration,user_socket_id):
        print("GENERATION STARTED.......")
        self.socket_id = user_socket_id
        self.model.set_generation_params(duration=duration)
        self.model.set_custom_progress_callback(self.progress_callback)

        enhanced_prompt = self.enhance_the_prompt(prompt)
        print("Enhanced prompt :",enhanced_prompt)

        res = self.model.generate([enhanced_prompt],progress=True)
        tensor = res.cpu().squeeze(0)
        tensor = tensor / torch.max(torch.abs(tensor))
        sample_rate = 32000  # Replace with your actual sample rate
        file_name = self.generate_filename()
        folder_path = "audios"
        self.ensure_folder_exists(folder_path)
        torchaudio.save(f"audios/{file_name}", tensor, sample_rate)
        new_entry = {
            "user_prompt":original_prompt,"filename":file_name,"enchanted_prompt":enhanced_prompt
        }
        self.save_history(new_entry)
        print(f"GENERATION FINISHED :) File saved as {file_name}")

        return file_name
    
    def progress_callback(self,generated,to_generate):
        # hit socket event
        percentage = (generated/to_generate)*100
        self.socketio.emit('music-progress', {'progress':percentage},to=self.socket_id)

    def generate_filename(self):
        timestamp = int(time.time())
        return f"choira_gen_{timestamp}.wav"

    def enhance_the_prompt(self,user_prompt):
        MODEL="gpt-4o-mini"
        client = OpenAI(api_key=os.environ.get("o_key"))
        completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a prompt creator for text to music models but prompt should be less than 200 characters. enhance the provide prompt by adding more detailed into it and give the one enhance prompt only does not include anything else"},
            {"role": "user", "content": user_prompt}  # <-- This is the user message for which the model will generate a response
        ]
        )
        return completion.choices[0].message.content

    def ensure_folder_exists(self,folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created.")
    
    def save_history(self,new_entry):
        try:
            with open("history.json", "r") as file:
                data = json.load(file)  # Load existing JSON content
        except FileNotFoundError:
            # Initialize data if the file doesn't exist
            data = {"generations": []}

        # Add the new entry to the 'generations' array
        data["generations"].append(new_entry)

        with open("history.json", "w") as file:
            json.dump(data, file, indent=4)

        print("New entry added successfully!")
