import os

import fleep


def get_audio_format(audio_path):
    with open(audio_path, 'rb') as file:
        info = fleep.get(file.read(128))
        return info.extension[0]


def ffmpeg_conversion(old_audio_path, new_audio_path):
    os.system(
        f'ffmpeg -i {old_audio_path} -hide_banner -loglevel error -vn -ar 44100 '
        f'-ac 2 -b:a 192k {new_audio_path}'
    )


def remove_audio(audio_path):
    os.system(f'rm {audio_path}')
