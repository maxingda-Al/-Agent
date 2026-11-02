#为整个工程提供统一绝对路径
import os

def get_project_root()->str:
    #获得工程的所在根目录
    #：return：字符串根目录

    #当前文件绝对路径
    current_file_path=os.path.abspath(__file__)  #.abspath  获取绝对路径
    #获得工程的根目录，先获得文件所在文件夹绝对路径
    current_dir=os.path.dirname(current_file_path) #.dirname 获得文件夹的绝对路径
    #获得工程根目录
    project_root=os.path.dirname(current_dir) #取到了D:\Al大模型开发与Rag项目_Agent项目

    return project_root

def get_abs_path(relative_path:str)->str:
    #传递相对路径，得到绝对路径
    #：param relative——path：相对路径
    #：return绝对路径
    project_root=get_project_root()
    return os.path.join(project_root,relative_path)
if __name__=="__main__":
    print(get_abs_path("config/config.text"))