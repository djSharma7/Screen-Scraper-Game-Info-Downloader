from mutagen.mp4 import MP4
import subprocess
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os

class VideoProcessing():
	def __init__(self,config_obj):
		self.trim_seconds = -1
		try:
			if config_obj.get('post_processing_overlay_enable', False):
				self.trim_seconds = float(config_obj.get('remove_seconds_video',-1))
			return
		except Exception as ee:
			return

	def insert_meta_title_into_video(self,file_name, meta_title):
		try:
			file = MP4(file_name)
			file['©nam'] = meta_title
			file.save()
		except Exception as ee:
			pass

	def get_length(self,file_name):
		try:
			result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
									 "format=duration", "-of",
									 "default=noprint_wrappers=1:nokey=1", file_name],
									stdout=subprocess.PIPE,
									stderr=subprocess.STDOUT)

			return float(result.stdout)
		except Exception as ee:
			return -1

	def trim(self,file_name):
		pass

	def post_process(self,file_name,meta_title):
		if meta_title:
			self.insert_meta_title_into_video(file_name,meta_title)
		if self.trim_seconds != -1:
			video_length = self.get_length(file_name)
			try:
				if video_length >self.trim_seconds:

					target_file = file_name
					target_file = target_file.replace('VIDEO.MP4','VIDEO_.MP4')
					ffmpeg_extract_subclip(file_name,
										   self.trim_seconds, video_length, targetname=target_file)
					os.remove(file_name)
			except Exception as ee:
				pass
		return





