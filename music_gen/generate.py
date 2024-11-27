from audiocraft.models import musicgen
import torch
import torchaudio
import time


class ChoiraGenerate:
    def __init__(self,socketio) -> None:
        self.socketio = socketio
        self.model = musicgen.MusicGen.get_pretrained('medium', device='cuda')
        self.socket_id = 0
        

    def generate_music_large(self,prompt,duration,user_socket_id):
        self.socket_id = user_socket_id
        self.model.set_generation_params(duration)
        self.model.set_custom_progress_callback(self.progress_callback)
        res = self.model.generate([prompt],progress=True)
        print(res)
        print(res[0])
        print(res[1])
        sample_rate = 32000  # Replace with your actual sample rate
        audio_tensor = torch.rand(1, sample_rate * duration)  # 5 seconds of mono audio
        torchaudio.save(f"audios/{self.generate_filename()}", audio_tensor, sample_rate)
        return res
    
    def progress_callback(self,generated,to_generate):
        # hit socket event
        percentage = (generated/to_generate)*100
        print(f"Percentage:{percentage}%")

        self.socketio.emit('music-progress', {'progress':percentage},to=self.socket_id)


    def generate_filename(extension="wav"):
        timestamp = int(time.time())
        return f"choira_gen_{timestamp}.{extension}"
