from pytube import YouTube
from sclib import SoundcloudAPI, Track
import os
from sys import platform

def check_url(url: str) -> str:
    if not '.com' in url:
      return 'invalid'
    if 'youtube' in  url[:url.index('.com')]:
      return 'youtube'
    if 'soundcloud' in url[:url.index('.com')]:
      return 'soundcloud'
    
    return 'neither'

def download_yt(url, save_path) -> None:
  choice = check_url(url)
  
  if choice == 'neither':
    return
  elif choice == 'youtube':
  # print(save_path)
    url = YouTube(url)
    audio = url.streams.filter(only_audio = True).first()
        
    output = audio.download(output_path = save_path)
        
    base, ext = os.path.splitext(output)
    new_file = base + '.mp3'
      
    # download_history.append (
    #   new_file[:(new_file.count('/'))]
    # )
    # print(new_file[new_file.rfind('/') + 1:])
    # os.rename(output, new_file)
    
    with open('history.txt', 'a') as file:
      file.write(new_file[new_file.rfind('/') + 1 : ] + '\n')
      file.close()
    
  else:
    api = SoundcloudAPI()
    track = api.resolve(url)
    
    name = f'{track.artist} - {track.title}.mp3'
    
    if platform == 'linux' or platform == 'linux2':
      output = f'{save_path}{name}'
    else:
      output = f'{save_path}{name}'
    
    
    with open(output, 'wb+') as file:
      track.write_mp3_to(file)
      file.close()
    
    with open('history.txt', 'a') as file:
      file.write(name + '\n')
      file.close()


# def get_audio_file() -> None:
#     url = input('Enter url = ')
    
#     if 'youtube' not in url[:url.index('.com')]:
#       return
    
#     url = YouTube(url)
        
#     audio = url.streams.filter(only_audio = True).first()
        
#     path = input('Enter download path = ')
        
#     output = audio.download(output_path = path)
        
#     base, ext = os.path.splitext(output)
#     new_file = base + '.mp3'
#     os.rename(output, new_file)
        
#     print(url.title, 'was downloaded')
#     download_history.append(url.title)
        
# if __name__ == '__main__':
#     download_yt(
#       'https://soundcloud.com/travisscott-2/a-man',
#       '/home/norby/Videos/'
#     )
