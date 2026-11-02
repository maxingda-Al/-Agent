import os , hashlib
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader ,TextLoader
from utils.logger_handler import logger
def get_file_md5_hex(filepath:str):  #获得文件的MD5字符串
    if not os.path.exists(filepath):
        logger.error(f"[md5计算]文件{filepath}不存在")
        return
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]路径{filepath}不是文件")
        return
    md5_obj=hashlib.md5()
    chunk_size=4096  #4kb分片，避免文件过大爆内存
    try:
        with open(filepath,"rb")   as f:  #rb:以只读的二进制方式打开文件。
            # 是打开的文件对象。f.read(n) 的意思是：从文件当前位置，往后读 n 个字节，返回读到的内容。
            #关键点：文件有个"读取指针"，读一次就往后退一次，下次接着上次的位置读。
            while chunk :=f.read(chunk_size):
                md5_obj.update(chunk)
            """
            ：=相当于
            chunk=f.read(chunk_size)
            while chunk:
                 md5_obj.update(chunk)
                 chunk=f.read(chunk_size)
            """
            md5_hex=md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"计算文件{filepath}md5失败，{str(e)}")
        return None
def listdir_with_allowed_type(path:str,allowed_types:tuple[str]):  #给一个文件夹路径，把里面符合指定后缀的文件都找出来，返回它们的完整路径。
    files=[]
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return ()
    for f in os.listdir(path):#os.listdir(path)：列出文件夹里所有文件和子文件夹的名字（只有名字，不含路径）
        if f.endswith(allowed_types):
            files.append(os.path.join(path,f)) #把文件夹路径 + 文件名拼成完整路径
    return tuple(files)

def pdf_loader(filepath:str,password=None) ->list[Document]:
    return PyPDFLoader(filepath,password).load()

def txt_loader(filepath:str) ->list[Document]:
    return TextLoader(filepath,encoding="utf-8").load()