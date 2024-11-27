from audiocraft.models import musicgen
import torch

class ChoiraGenerate:
    def __init__(self,socketio) -> None:
        self.socketio = socketio
        self.model = musicgen.MusicGen.get_pretrained('medium', device='cuda')
        self.socket_id = 0
        

    def generate_music_large(self,prompt,duration,user_socket_id):
        self.model.set_generation_params(duration)
        self.model.set_custom_progress_callback(self.progress_callback)
        self.model.generate([prompt],progress=True)
        self.socket_id = user_socket_id
        return 
    
    def progress_callback(self,generated,to_generate):
        # hit socket event
        print(f"generated:{generated},to_generate:{to_generate}")
        percentage = (generated/to_generate)*100
        self.socketio.emit('music-progress', {'progress':percentage},to=self.socket_id)
