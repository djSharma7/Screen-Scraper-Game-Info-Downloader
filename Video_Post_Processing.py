from mutagen.mp4 import MP4
import subprocess
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import cv2

class VideoProcessing():
	def __init__(self,config_obj):
		self.trim_seconds = -1
		try:
			if config_obj.get('post_processing_overlay_enable', False):
				self.overlay_enabled = True
			else:
				self.overlay_enabled = False

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

	def insert_overlay(self,file_name,overlay_file_name):
		try:
			img = cv2.imread(overlay_file_name)
			img_height, img_width, _ = img.shape
			img = cv2.resize(img,(80,90),interpolation = cv2.INTER_AREA)
			img_height, img_width, _ = img.shape
			# Get Image dimensions
		except Exception as ee:
			return False,-1

		try:
			# Start Capture
			cap = cv2.VideoCapture(r'{}'.format(file_name))
			# Get frame dimensions
			fps = cap.get(5)

			frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
			frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
		except Exception as ee:
			return False,-1


		try:
			x = 0
			y = int(frame_height) - 10 - img_height

			size = (int(frame_width), int(frame_height))
			fourcc = cv2.VideoWriter_fourcc(*'mp4v')
			edited_file_name = file_name.split('.mp4')[0]
			edited_file_name = '{}_.mp4'.format(edited_file_name)

			result = cv2.VideoWriter(edited_file_name,
									 fourcc,
									 fps, size)
			while (True):
				ret, frame = cap.read()
				if ret == True:
					frame[y:y + img_height, x:x + img_width] = img
					result.write(frame)
				else:
					break

			# When everything done, release the capture
			cap.release()
			result.release()
			cv2.destroyAllWindows()
			return True,edited_file_name
		except Exception as ee:
			return False,-1



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

	def post_process(self, file_name, meta_title, overlay_file_name):

		if self.overlay_enabled:
			if overlay_file_name:
				if os.path.exists(overlay_file_name):
					status, val = self.insert_overlay(file_name, overlay_file_name)
					if status:
						os.remove(file_name)
						file_name = val
				else:
					print("Overlay file path doesnot exist -", overlay_file_name)
			else:
				pass

		if self.trim_seconds > 0:
			video_length = self.get_length(file_name)
			try:
				if video_length > self.trim_seconds:
					target_file = file_name
					target_file = target_file.replace('Video.MP4', 'Video__.MP4')
					target_file = target_file.replace('Video_.MP4', 'Video__.MP4')
					ffmpeg_extract_subclip(file_name,
										   self.trim_seconds, video_length, targetname=target_file)
					os.remove(file_name)
					file_name = target_file
			except Exception as ee:
				pass
		if meta_title:
			self.insert_meta_title_into_video(file_name, meta_title)
		return


