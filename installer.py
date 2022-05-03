import sys
import subprocess
import pkg_resources
packages = [p.project_name for p in pkg_resources.working_set]
if 'colorama' not in packages:
    print("Я не нашел colorama, устанавливаю...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'colorama'])
if 'termcolor' not in packages:
    print("Я не нашел termcolor, устанавливаю...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'termcolor'])
# # a = subprocess.check_call([sys.executable, '-m', 'pip', 'list'])
# # print(a)
# input()


