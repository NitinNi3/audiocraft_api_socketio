from audiocraft.models import musicgen
import torch
import torchaudio
import time
from openai import OpenAI 
import os


class ChoiraGenerate:
    def __init__(self,socketio) -> None:
        self.socketio = socketio
        self.model = musicgen.MusicGen.get_pretrained('large', device='cuda')
        self.socket_id = 0
        

    def generate_music_large(self,prompt,duration,user_socket_id):
        print("GENERATION STARTED.......")
        self.socket_id = user_socket_id
        self.model.set_generation_params(duration=duration)
        self.model.set_custom_progress_callback(self.progress_callback)

        enhanced_prompt = self.enhance_the_prompt(prompt)

        res = self.model.generate([enhanced_prompt],progress=True)
        tensor = res.cpu().squeeze(0)
        tensor = tensor / torch.max(torch.abs(tensor))
        sample_rate = 32000  # Replace with your actual sample rate
        file_name = self.generate_filename()
        torchaudio.save(f"audios/{file_name}", tensor, sample_rate)
        print(f"GENERATION FINISHED !. File saved as {file_name}")

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