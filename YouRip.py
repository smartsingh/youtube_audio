from pytube import YouTube
from pytube import Playlist
from moviepy.editor import *
import os
import eyed3
from urllib import request

class video:
    
    def __init__(self, url):
        
        self.yt = YouTube(url)

        self.track_title = self.yt.title
        self.uploader = self.yt.author

        self.thumbnail = request.urlopen(self.yt.thumbnail_url)
        self.cover = self.thumbnail.read()
        
        print(f"Added {self.track_title} from {self.uploader}")
        
    def rip(self):
        dl_stream = self.yt.streams.get_audio_only(subtype='mp4')
        
        out_file = dl_stream.download(output_path='output')
        
        print(f"Ripping audio to {os.path.realpath(out_file)}")

        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        
        conversion_file = AudioFileClip(out_file)
        conversion_file.write_audiofile(new_file)
        
        os.remove(out_file)
        
        finished_file = eyed3.load(new_file)

        finished_file.tag.title = self.track_title
        finished_file.tag.album = u"YouTube Downloads"
        finished_file.tag.artist = self.uploader
        finished_file.tag.images.set(type_=3, img_data=self.cover, mime_type="image/jpeg")
        finished_file.tag.save(version=eyed3.id3.ID3_V2_3)
        
        print(f"Finished downloading {self.track_title}")
    

class playlist:
    
    def __init__(self, url):
        self.plist = Playlist(url)
        
        self.p_title = self.plist.title
        self.owner = self.plist.owner
        
        print(f"Added playlist {self.p_title} from {self.owner}. This playlist contains {self.plist.length} videos.")
        
    def rip(self):
        for track in range(len(self.plist.video_urls)):
            p_track = video(self.plist.video_urls[track])
            p_track.rip()