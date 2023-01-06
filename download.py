from pytube import YouTube
import os

def check_url(url: str) -> str:
    if 'youtube' in  url[:url.index('.com')]:
        return 'youtube'
    elif 'soundcloud' in url[:url.index('.com')]:
        return 'soundcloud'
    
    return 'neither'

def get_audio_file() -> None:
    url = input('Enter url = ')
    
    if 'youtube' not in url[:url.index('.com')]:
        return
    
    url = YouTube(url)
        
    audio = url.streams.filter(only_audio = True).first()
        
    path = input('Enter download path = ')
        
    output = audio.download(output_path = path)
        
    base, ext = os.path.splitext(output)
    new_file = base + '.mp3'
    os.rename(output, new_file)
        
    print(url.title, ' a fost descarcata')
        
if __name__ == '__main__':
    get_audio_file()
