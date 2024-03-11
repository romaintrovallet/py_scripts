import os

downloads_path = os.path.expanduser("~/Downloads")
cmd = 'mkdir test'
os.chdir(downloads_path)
os.system(f'start cmd /k ; {cmd}')

