from pathlib import Path # Import Path class which treats file paths as objects
import wave #Import PyCharm's wave library for interfacing with .wav files


class PCMToWavHandler:
    def __init__(
        self,
        sample_rate: int = 44100,
        num_channels: int = 1,
        sample_width_bytes: int = 2,  # 2 bytes = 16-bit PCM
    ): #Define initialization method with 3 input arguments
        self.sample_rate = sample_rate
        self.num_channels = num_channels
        self.sample_width_bytes = sample_width_bytes
        #Define class attributes


    def save( # This is a method that takes the raw pcm data and saves it to a folder and .wav file you specify
        self,
        pcm_bytes: bytes,
        output_folder: str,
        filename: str = "output.wav",
    ) -> Path:
        output_path = Path(output_folder) # Instantiate path object
        output_path.mkdir(parents=True, exist_ok=True) # Make new directory if one doesn't exist already

        wav_path = output_path / filename #Create .wav file path

        with wave.open(str(wav_path), "wb") as wav_file: #Write .wav headers into file
            wav_file.setnchannels(self.num_channels)
            wav_file.setsampwidth(self.sample_width_bytes)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(pcm_bytes)

        return wav_path # This method returns your .wav files path


if __name__ == "__main__":
    # Example: 1 second of silence
    sample_rate = 44100
    duration_seconds = 1

    pcm_silence = b"\xFF\x00" * sample_rate * duration_seconds

    handler = PCMToWavHandler(
        sample_rate=44100,
        num_channels=1,
        sample_width_bytes=2,
    )

    saved_file = handler.save(
        pcm_bytes=pcm_silence,
        output_folder="audio_outputs",
        filename="test_output(2).wav",
    )

    print(f"Saved to {saved_file}")