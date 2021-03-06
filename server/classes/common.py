# -*- coding: utf-8 -*-

import zipfile,os,time,random,hashlib,json,ConfigParser,const,sys,constTable

class Common:
    CONST=const
    CONST.RUNTIME_PATH=os.path.dirname(os.path.realpath(__file__))+"/../runtime"
    CONST.CONF_PATH=os.path.dirname(os.path.realpath(__file__))+"/../config"
    CONST.ERROR=constTable.constTable().ERROR

    def __init__(self):
        pass

    def dp(self,obj):
        print(obj)
        sys.exit(-1)

    def tanslate(self,str,form_code="utf-8",to_code="cp936"):
        return str.decode(form_code).encode(to_code)

    def dict2json(self,dict):
        return json.dumps(dict)

    def json2dict(self,json_str):
        return json.loads(json_str)

    def readBinFile(self,fs,length):
            return fs.read(length)

    def writeBinFile(self,path,text,mode="wb"):
        pass

    def readFile(self,path,mode):
        file = open(path, mode)
        try:
           text = file.read()
        finally:
            file.close()
        return text

    def writeFile(self,path,text,mode):
        file = open(path, mode)
        try:
            file.write(text)
        finally:
            file.close()

    def baleZip(self,form_file_path,to_file_path):
        to_file_path+=".zip"
        z = zipfile.ZipFile(to_file_path, 'w', zipfile.ZIP_DEFLATED)
        startdir = form_file_path
        child_list=[]
        self.baleFolder(startdir,child_list)

        for filename in child_list:
            pre_len = len(os.path.dirname(filename))
            arcname = filename[pre_len:].strip(os.path.sep)   #相对路径
            z.write(filename, arcname)
        z.close()
        return to_file_path

    def baleFolder(self,dir_path,child_list):
        parents = os.listdir(dir_path)
        for parent in parents:
            child = os.path.join(dir_path,parent)
            if os.path.isdir(child):
                if os.stat(child).st_size<=0:
                    child_list.append(child)
                else:
                    child_list =  self.baleFolder(child,child_list)
            else:
                child_list.append(child)
        return child_list

    def getRuntimeDir(self,sub_dir=".",isFull=False,isTemp=""):
        runTimePath=self.CONST.RUNTIME_PATH

        if isFull:
           runTimePath += "/"+sub_dir+"/"+time.strftime("%Y/%m/%d", time.localtime())

        if len(isTemp)>0:
            runTimePath+="/"+isTemp

        if not os.path.exists(runTimePath):
            os.makedirs(runTimePath)

        return runTimePath

    def md5(self,str):
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def getConf(self,conf_path,section,option):
        cf = ConfigParser.ConfigParser()
        cf.read(conf_path)
        return cf.get(section,option)

    def getClientConf(self,section,option):
        return self.getConf(self.CONST.CONF_PATH,section,option)

    def createPacket(self,data,package_num,method="",status=""):
        head={
                "method":method,
                "package_num":package_num,
                "size":len(data),
                "md5":self.md5(data),
                "data":data,
                "status":status
             }

        packet=""
        for key, value in head.items():
            if(str(value)!=""):
                packet+=str(key)+":"+str(value)+"\n"
        return packet+"\0"

    def createRetStrPackage(self,package_num,error,size):
        if not self.CONST.ERROR.has_key(error):
            error="FAIL"
        error_num=self.CONST.ERROR[error]

        return self.createPacket(error+"|"+str(size),package_num,status=error_num)

    def getDirSize(self,path):
        size=0
        for root, dirs, files in os.walk(path):
            for f in files:
                size += os.path.getsize(os.path.join(root, f))
        return size

    def getFileSize(self,path):
        return os.path.getsize(path)