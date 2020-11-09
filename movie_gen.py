from moviepy.video.VideoClip import TextClip, ImageClip
from moviepy.editor import AudioFileClip, VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.editor import concatenate_videoclips
import re

import sys
from gtts import gTTS
import os

import shutil

background_image = "bg.jpg"


def make_tts(text, number):
    language = 'en'

    tts = gTTS(text=text, lang=language, slow=False)

    filename = "tmp/" + name + "/tts/" + name + number + ".mp3"
    tts.save(filename)
    return filename


def generate_text_clip(text, number):
    filename = "tmp/" + name + "/clips/" + name + number + ".mp4"

    if not os.path.exists(filename):
        audio_filename = make_tts(text, number)
        audio = AudioFileClip(audio_filename)
        image = ImageClip(background_image).set_fps(30)
        video = image.set_duration(audio.duration)
        withaudio = video.set_audio(audio)

        fontsize = (len(text)+10) / withaudio.w
        text_clip = TextClip(text, fontsize=fontsize, size=(withaudio.w, withaudio.h)).set_pos("center")

        final_clip = CompositeVideoClip([withaudio, text_clip.set_duration(video.duration)])

        final_clip.write_videofile(filename)
    return filename


def generate_ep_video(story_name):
    if not os.path.exists("tmp/" + name + "/clips"):
        os.makedirs("tmp/" + name + "/clips")

    if not os.path.exists("tmp/" + name + "/tts"):
        os.makedirs("tmp/" + name + "/tts")

    with open("stories/" + story_name + ".txt", "r") as f:
        story = f.read()

    script = []
    for line in re.split('; |, |! |\? |\. |\n', story):
        script.append(line)

    print("Making " + str(len(script)) + " clips...")

    files = []

    i = 0

    for l in script:

        l = l.replace("\n", "")
        if l != "":
            i += 1
            files.append(generate_text_clip(l, str(i)))

    clips = [VideoFileClip(file) for file in files]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile("render/" + story_name + ".mp4")

    shutil.rmtree("tmp/" + name)

    return "render/" + story_name + ".mp4"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("please provide arguments!")
    else:
        name = "".join(sys.argv[1:])
        generate_ep_video(name)
