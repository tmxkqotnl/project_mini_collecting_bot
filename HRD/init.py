from dotenv import load_dotenv
from os.path import dirname,abspath,join
from sys import path


project_root_path = dirname(dirname(abspath(__file__)))

common_path = join(project_root_path,'common')
env_file_path = join(project_root_path,'.env')


load_dotenv(env_file_path)
path.append(common_path)