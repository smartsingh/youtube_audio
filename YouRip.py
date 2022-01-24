from pytube import YouTube
from pytube import Playlist
from moviepy.editor import *
import os
import eyed3
from urllib import request

#creating video class using code that I developed in the audio scraper notebook
class video:
    
    def __init__(self, url):
        
        self.yt = YouTube(url)

        #storing track details for later
        self.track_title = self.yt.title
        self.uploader = self.yt.author

        #grabbing image for album cover

        self.thumbnail = request.urlopen(self.yt.thumbnail_url)
        self.cover = self.thumbnail.read()
        
        print(f"Added {self.track_title} from {self.uploader}")
        
    def rip(self):
        #gets stream with highest audio quality
        dl_stream = self.yt.streams.get_audio_only(subtype='mp4')
        
        #downloads stream
        out_file = dl_stream.download(output_path='output')
        
        print(f"Ripping audio to {os.path.realpath(out_file)}")

        #splits the extension for the output and gives us a name for the new file. Necessary for later
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        
        #done with pytube, working with moviepy now

        conversion_file = AudioFileClip(out_file)
        conversion_file.write_audiofile(new_file)
        
        #delete out file for space constraints
        os.remove(out_file)
        
        #working with eyed3 now
        finished_file = eyed3.load(new_file)

        #saves info from YouTube over to MP3
        finished_file.tag.title = self.track_title
        finished_file.tag.album = u"YouTube Downloads"
        finished_file.tag.artist = self.uploader
        finished_file.tag.images.set(type_=3, img_data=self.cover, mime_type="image/jpeg")
        finished_file.tag.save(version=eyed3.id3.ID3_V2_3)
        
        print(f"Finished downloading {self.track_title}")    

class playlist:
    
    def __init__(self, url):
        self.plist = Playlist(url)
        
        #making sure we're getting the right playlist
        self.p_title = self.plist.title
        self.owner = self.plist.owner
        
        print(f"Added playlist {self.p_title} from {self.owner}. This playlist contains {self.plist.length} videos.")
        
    def rip(self):
        for track in range(len(self.plist.video_urls)):
            p_track = video(self.plist.video_urls[track])
            p_track.rip()
        
        print(f"Finished downloading audio from Playlist {self.p_title}")
        os.system('afplay /System/Library/Sounds/Glass.aiff')
            
dvid = input("Enter a Youtube link:")

if dvid.find('watch') != -1:
    vid_link = video(dvid)
    vid_link.rip()
elif dvid.find('playlist') != -1:
    p_link = playlist(dvid)
    p_link.rip()
else:
    print("This is not a valid link for download")