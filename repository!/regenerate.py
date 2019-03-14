import os

def delete_all_files(folder,skip):
	print('processing '+folder)
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		#print(file_path)
		if file_path in skip:
			print(file_path)
			try:
				if os.path.isfile(file_path):
					print('unlinking '+file_path)
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					delete_all_files(file_path,skip)
					print('removing '+file_path)
					os.rmdir(file_path)
			except Exception as e:
				print(e)

SKIP = [os.path.join('.', 'create_repository.py'),
		os.path.join('.', 'regenerate.py')]

delete_all_files('.',SKIP)
os.system("create_repository.py ../plugin.video.yabop/")