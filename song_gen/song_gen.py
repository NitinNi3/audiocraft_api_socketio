import time
import requests
# from openai import OpenAI 
from dotenv import load_dotenv
import os
import json
load_dotenv()


class ChoiraSongGenerate:
    def __init__(self) -> None:
        self.song_gen_version = "v1" # not in use
        

    def generate_song(self,prompt):
        print("SONG GENERATION STARTED...")
        # get song url,download that song and store into the folder
        music_data = self.song_gen(prompt)
        # file_name = self.generate_filename()
        # folder_path = "audios"
        # self.ensure_folder_exists(folder_path)
        # new_entry = {
        #     "user_prompt":prompt,"filename":file_name,"enchanted_prompt":""
        # }
        # self.save_history(new_entry)
        # print(f"GENERATION FINISHED :) File saved as {file_name}")

        return music_data
    
    def progress_callback(self,generated,to_generate):
        # hit socket event
        percentage = (generated/to_generate)*100
        self.socketio.emit('music-progress', {'progress':percentage},to=self.socket_id)

    def generate_filename(self):
        timestamp = int(time.time())
        return f"choira_gen_{timestamp}.wav"

    def song_gen(self,user_prompt):
        url = os.environ.get("song_gen_url") or "https://api.topmediai.com/v1"
        endpoint = "/music"
        api_key = os.environ.get("song_gen_key")

        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
    
        }
        body =  {
            "is_auto": 1,
            "prompt":user_prompt,
            "instrumental": 0,
        }

        response = requests.post(f"{url}{endpoint}", headers=headers, json=body)
        if response.status_code == 200:
            print("response")
            print(response)
            musicData = response.data[0]
            return {
                "audioUrl": musicData.audio_file,
                "imageUrl": musicData.image_file,
                "title": musicData.title,
                "lyric": musicData.lyric,
            }
        else:
            print(f"Error: {response.status_code}")

    # def enhance_the_prompt(self,user_prompt):
    #     MODEL="gpt-4o-mini"
    #     client = OpenAI(api_key=os.environ.get("o_key"))
    #     completion = client.chat.completions.create(
    #     model=MODEL,
    #     messages=[
    #         {"role": "system", "content": "You are a prompt creator for text to music models but prompt should be less than 200 characters. enhance the provide prompt by adding more detailed into it and give the one enhance prompt only does not include anything else"},
    #         {"role": "user", "content": user_prompt}  # <-- This is the user message for which the model will generate a response
    #     ]
    #     )
    #     return completion.choices[0].message.content

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