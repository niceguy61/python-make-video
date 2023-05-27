from gtts import gTTS
from moviepy.editor import ImageClip, VideoFileClip, CompositeVideoClip
from moviepy.editor import AudioFileClip
from moviepy.editor import concatenate_videoclips
from moviepy.video.fx.resize import resize
import moviepy.editor as mpy

audio_file = 'dixit.mp3'
img_start_size = 1
img_end_size = 1.3
img_array = ['img1.jpg', 'img2.jpg']
video_array = ['video6.mp4', 'video5.mp4','video4.mp4','video3.mp4']
audio_files = ['kebin.mp3', 'hello.mp3']
base_height = 1080
base_weight = 1920
base_fps = 30

def convert_text_to_speech(text, output='speech.mp3'):
    tts = gTTS(text, lang="ko")
    tts.save(output)

def create_zoom_in_effect(image_path, duration):
    clip = ImageClip(image_path, duration=duration).resize((base_weight, base_height))
    return clip.fx(resize, lambda t : img_start_size + (img_end_size - img_start_size) * t / duration)

def create_video_from_images_and_videos(image_files, video_files, audio_file, output_file, fps=24):
    clips = []
    audio = AudioFileClip(audio_file)
    duration = audio.duration
    num_items = len(image_files) + len(video_files)
    duration_per_item = duration / num_items
    
    for img in image_files:
        clip = create_zoom_in_effect(img, duration_per_item)
        clips.append(clip)

    for video in video_files:
        clip = VideoFileClip(video).subclip(0, duration_per_item)
        clips.append(clip.resize((base_weight,base_height)))  # Resize to the resolution you want all clips to have

    video = concatenate_videoclips(clips, method="compose")
    video.set_duration(duration)
    final_audio = audio.subclip(0, duration)
    final_clip = video.set_audio(final_audio)

    # Add fade in and fade out to the video
    final_clip = final_clip.fadein(2)
    final_clip = final_clip.fadeout(2)

    final_clip.write_videofile(output_file, codec='libx264', fps=fps)

def main():
    # You can use convert_text_to_speech function whenever you need
    # convert_text_to_speech('Hello, world!', 'speech.mp3')
    convert_text_to_speech('안녕하세요? 오늘도 즐거운 하루되세요!', 'hello.mp3')

    create_video_from_images_and_videos(img_array, video_array, audio_file, 'output.mp4',base_fps)

if __name__ == "__main__":
    main()