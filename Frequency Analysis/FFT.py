from pathlib import Path
import wave
import numpy as np
import matplotlib.pyplot as plt


class AudioFFTAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

        self.sample_rate = None
        self.num_channels = None
        self.sample_width_bytes = None
        self.num_frames = None
        self.duration_seconds = None
        self.samples = None

        self._check_file_type()
        self._unwrap_wav_file()

    def _check_file_type(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        if self.file_path.suffix.lower() != ".wav":
            raise ValueError("Only .wav files are currently supported.")

    def _unwrap_wav_file(self):
        with wave.open(str(self.file_path), "rb") as wav:
            self.num_channels = wav.getnchannels()
            self.sample_width_bytes = wav.getsampwidth()
            self.sample_rate = wav.getframerate()
            self.num_frames = wav.getnframes()
            self.duration_seconds = self.num_frames / self.sample_rate

            pcm_bytes = wav.readframes(self.num_frames)

        if self.sample_width_bytes == 1:
            dtype = np.uint8
        elif self.sample_width_bytes == 2:
            dtype = np.int16
        elif self.sample_width_bytes == 4:
            dtype = np.int32
        else:
            raise ValueError(f"Unsupported sample width: {self.sample_width_bytes} bytes")

        samples = np.frombuffer(pcm_bytes, dtype=dtype)

        if self.num_channels > 1:
            samples = samples.reshape(-1, self.num_channels)
            samples = samples[:, 0]  # use left channel for FFT

        self.samples = samples

    def print_info(self):
        print(f"File: {self.file_path}")
        print(f"Sample rate: {self.sample_rate} Hz")
        print(f"Channels: {self.num_channels}")
        print(f"Sample width: {self.sample_width_bytes * 8} bits")
        print(f"Frames: {self.num_frames}")
        print(f"Duration: {self.duration_seconds:.2f} seconds")

    def plot_time_domain(self):
        time = np.arange(len(self.samples)) / self.sample_rate

        plt.figure()
        plt.plot(time, self.samples)
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.title("Time-Domain Audio Signal")
        plt.grid(True)
        plt.show()

    def plot_fft(self):
        samples = self.samples.astype(float)

        # Remove DC offset
        samples = samples - np.mean(samples)

        fft_values = np.fft.rfft(samples)
        fft_magnitude = np.abs(fft_values)

        frequencies = np.fft.rfftfreq(len(samples), d=1 / self.sample_rate)

        plt.figure()
        plt.plot(frequencies, fft_magnitude)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude")
        plt.title("FFT of Audio Signal")
        plt.grid(True)
        plt.show()

    def plot_fft_db(self):
        samples = self.samples.astype(float)
        samples = samples - np.mean(samples)

        fft_values = np.fft.rfft(samples)
        fft_magnitude = np.abs(fft_values)

        fft_db = 20 * np.log10(fft_magnitude + 1e-12)
        frequencies = np.fft.rfftfreq(len(samples), d=1 / self.sample_rate)

        plt.figure()
        plt.plot(frequencies, fft_db)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude (dB)")
        plt.title("FFT of Audio Signal in dB")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    analyzer = AudioFFTAnalyzer("audio_outputs/airplane_chime_x.wav")

    analyzer.print_info()
    analyzer.plot_time_domain()
    analyzer.plot_fft()
    analyzer.plot_fft_db()