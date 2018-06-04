import os

# file_directory="D:\\Users\\EX-ZHANGLIANG011\\Desktop\\pingan"

#给出指定的目录读取该目录中各个文本的内容： 级别：目录
def file_names(file_dir):
    filecontents = []
    files =os.listdir(file_dir)
    for file in files:
        if not os.path.isdir(file):
            try:
                f=open(file_dir + "\\" + file, mode="r", encoding="utf-8")
                content=f.read()
                file=file[:-8]
                filecontent=(file,content)
                filecontents.append(filecontent)
            except IOError:
                print("没有找到文件或读取文件失败")
            finally:
                f.close()
    return filecontents


#读取指定的文本内容： 级别：文本
def content(file):
    try:
        f = open(file, encoding="utf-8", mode="r")
        content = f.read()
    except IOError:
        print("没有找到文件或读取文件失败")
    finally:
        f.close()
    return  content





