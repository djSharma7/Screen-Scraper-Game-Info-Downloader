from mutagen.mp4 import MP4
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import moviepy.editor as mp
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

	def insert_overlay_moviepy(self, file_name, overlay_file_name):
		try:
			img = cv2.imread(overlay_file_name)
			img_height, img_width, _ = img.shape
			video = mp.VideoFileClip(file_name)
			w = video.w
			h = video.h
			hh = h - 120
			edited_file_name = file_name.split('.mp4')[0]
			edited_file_name = '{}_.mp4'.format(edited_file_name)
			logo = (mp.ImageClip(overlay_file_name)
					.set_duration(video.duration)
					.resize(height=100)
					.margin(left=20, top=hh, opacity=0)
					.set_pos('left', 'bottom'))
			final = mp.CompositeVideoClip([video, logo])
			final.subclip(0).write_videofile(edited_file_name)
			return True, edited_file_name
		except Exception as ee:
			return False, -1

	def get_length(self,file_name):
		try:
			try:
				data = cv2.VideoCapture(file_name)
			except Exception as video_exp:
				from os import path
				file_name = path.abs(file_name)
				data = cv2.VideoCapture(file_name)

			frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
			fps = int(data.get(cv2.CAP_PROP_FPS))

			# calculate dusration of the video
			seconds = int(frames / fps)
			return float(seconds)

		except Exception as ee:
			print ("Excpetion occurred in here",ee)
			return -1

	def post_process(self, file_name, meta_title, overlay_file_name):

		if self.overlay_enabled:
			if overlay_file_name:
				if os.path.exists(overlay_file_name):
					status, val = self.insert_overlay_moviepy(file_name, overlay_file_name)
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
					target_file = target_file.replace('Video.mp4', 'Video__.mp4')
					target_file = target_file.replace('Video_.mp4', 'Video__.mp4')
					ffmpeg_extract_subclip(file_name,
										   int(self.trim_seconds), int(video_length), targetname=target_file)
					os.remove(file_name)
					file_name = target_file
			except Exception as ee:
				pass
		if meta_title:
			self.insert_meta_title_into_video(file_name, meta_title)
		return
