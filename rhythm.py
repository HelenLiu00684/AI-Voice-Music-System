from pydub import AudioSegment
import numpy as np


def analyze_energy(filepath):

    audio = AudioSegment.from_file(filepath)

    # 转 mono
    samples = audio.set_channels(1)

    # 转 numpy array
    data = np.array(samples.get_array_of_samples())

    # chunk size（200ms）
    chunk_size = int(audio.frame_rate * 0.2)

    energy_list = []

    for i in range(0, len(data), chunk_size):

        chunk = data[i:i+chunk_size]

        if len(chunk) == 0:
            continue

        # calucate energy
        energy = np.abs(chunk).mean()

        energy_list.append(energy)

    return energy_list