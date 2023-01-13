from pytube import YouTube
import os

download_history = []

def check_url(url: str) -> str:
    if not '.com' in url:
      return 'invalid'
    if 'youtube' in  url[:url.index('.com')]:
      return 'youtube'
    if 'soundcloud' in url[:url.index('.com')]:
      return 'soundcloud'
    
    return 'neither'

def download_yt(url, save_path) -> None:
  print(save_path)
  url = YouTube(url)
  audio = url.streams.filter(only_audio = True).first()
      
  output = audio.download(output_path = save_path)
      
  base, ext = os.path.splitext(output)
  new_file = base + '.mp3'
  os.rename(output, new_file)
      
  print(url.title, 'was downloaded')


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
#     get_audio_file()