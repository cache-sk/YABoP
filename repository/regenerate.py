import os

def delete_all_files(folder,skip):
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		if file_path in skip:
			try:
				if os.path.isfile(file_path): os.unlink(file_path)
				elif os.path.isdir(file_path): delete_all_files(file_path,skip)
			except Exception as e:
				print(e)

delete_all_files('.',['create_repository.py','regenerate.py'])
os.system("create_repository.py ../plugin.video.yabop/")