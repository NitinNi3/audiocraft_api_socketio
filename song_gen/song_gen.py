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
        music_data = self.song_gen(prompt)
        folder_path = "audios"
        self.ensure_folder_exists(folder_path)
        file_name1 = self.generate_filename()
        file_name = os.path.join(folder_path, f"{file_name1}.mp3")
        ack_status = self.download_and_store(music_data['audioUrl'],file_name)
        if(ack_status):
            new_entry = {"user_prompt":prompt,"filename":f"{file_name1}.mp3","enchanted_prompt":""}
            self.save_history(new_entry)
            print(f"GENERATION FINISHED :) File saved as {file_name1}")
            return music_data
        else:
            return False
    
    def progress_callback(self,generated,to_generate):
        # hit socket event
        percentage = (generated/to_generate)*100
        self.socketio.emit('music-progress', {'progress':percentage},to=self.socket_id)

    def generate_filename(self):
        timestamp = int(time.time())
        return f"choira_gen_{timestamp}"

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
            print(response)
            print("response",response.json())
            print("response",response.json()["data"])
            musicData = response.json()["data"][0]
            return {
                "audioUrl": musicData['audio_file'],
                "imageUrl": musicData['image_file'],
                "title": musicData['title'],
                "lyric": musicData['lyric'],
            }
        else:
            print(f"Error: {response.status_code}")

    
    def download_and_store(self,url,file_name):
        print("Downloading started")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an error for bad status codes
            # Write the file to the specified folder
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):  # Download in chunks
                    file.write(chunk)
            print("Downloading Finished and stored the file")
            return True

        except Exception as e:
            print("ERRRR",e)
            return False
        
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
