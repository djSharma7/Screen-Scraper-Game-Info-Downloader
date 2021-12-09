import logging

class CustomFormatter(logging.Formatter):

	def __init__(self):
		self.blue = "\x1b[36m"
		self.purple = "\x1b[0;35m"
		self.bold_red = "\x1b[31;1m"
		self.reset = "\x1b[0m"
		self.green = "\x1b[32;1m"
		self.format_string = "%(asctime)s - %(levelname)s -******** %(message)s "
		self.format_string2 = "%(asctime)s - %(levelname)s -******* %(message)s "
		self.FORMATS = {
			logging.DEBUG: self.blue + self.format_string2 + self.reset,
			logging.INFO: self.green + self.format_string + self.reset,
			logging.ERROR: self.bold_red + self.format_string2 + self.reset,
			logging.CRITICAL: self.bold_red + self.format_string + self.reset,
			logging.WARNING : self.purple + self.format_string + self.reset
		}

	def format(self, record):
		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)

def getLogger(name):
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	ch.setFormatter(CustomFormatter())

	logger.addHandler(ch)
	return logger


