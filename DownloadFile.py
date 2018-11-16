#coding:utf-8

# FTP操作
import ftplib
import os
import sys
import WritrLog

class DownloadFile:

    def __init__(self):
        self.host = '10.24.171.42'
        self.username = 'cosrun3d'
        self.password = 'cosrun3d'
        self.logger = WritrLog.log("DownloadFile.log")

    def Ftp_login(self):
        try:
            self.f = ftplib.FTP(self.host)  # 实例化FTP对象
            self.f.login(self.username, self.password)  # 登录
        except IOError:
            self.logger.error("Ftp Login Error!!!")

    def Ftp_Close(self):
        try:
            self.f.quit()
        except BaseException,e:
            self.logger.info(e.message)

    def ftp_download(self, f, file_remote, file_local):
        '''
        以二进制形式下载文件
        '''
        try:
            bufsize = 1024  # 设置缓冲器大小
            fp = open(file_local, 'wb')
            f.retrbinary('RETR %s' % file_remote, fp.write, bufsize)
            fp.close()
        except BaseException,e:
            self.logger.error(e.message)


    def ftp_upload(self, file_remote, file_local):
        '''以二进制形式上传文件'''
        bufsize = 1024  # 设置缓冲器大小
        fp = open(file_local, 'rb')
        self.f.storbinary('STOR ' + file_remote, fp, bufsize)
        fp.close()

if __name__ == '__main__':
    host = '10.24.171.42'
    username = 'cosrun3d'
    password = 'cosrun3d'


    # f = ftplib.FTP(host)  # 实例化FTP对象
    # f.login(username, password)  # 登录
    #
    # # 获取当前路径
    # pwd_path = f.pwd()
    # print("FTP当前路径:", pwd_path)
    #
    #
    # # 逐行读取ftp文本文件
    # ftp_download(f, "/D1BDATA/FY3D/MWHS/FY3D_MWHSX_GBAL_L1_20180324_0005_015KM_MS.HDF", "FY3D_MWHSX_GBAL_L1_20180324_0005_015KM_MS.HDF")
    # #ftp_upload()
    # f.quit()






# IP = "10.24.34.219"
# usr = "dpps01"
# password = "dpps01"
#
# dir = r"/COMDATA/BRDF/2018/20180101/"
# filename = "MCD43C1.A2018001.006.2018010055815.h5"
#
# ftp = ftplib.FTP(IP)
# #ftp.connect(IP)
# ftp.login(usr, password)
# print ftp.getwelcome()
# print ftp.dir()
# ftp.cwd(dir)
#
# out = open(filename, "wb")
# ftp.retrbinary("RETR " + filename, out.write)
# ftp.close()


# ftp相关命令操作
# ftp.cwd(pathname)                 #设置FTP当前操作的路径
# ftp.dir()                         #显示目录下所有目录信息
# ftp.nlst()                        #获取目录下的文件
# ftp.mkd(pathname)                 #新建远程目录
# ftp.pwd()                         #返回当前所在位置
# ftp.rmd(dirname)                  #删除远程目录
# ftp.delete(filename)              #删除远程文件
# ftp.rename(fromname, toname)#将fromname修改名称为toname。
# ftp.storbinaly("STOR filename.txt",file_handel,bufsize)  #上传目标文件
# ftp.retrbinary("RETR filename.txt",file_handel,bufsize)  #下载FTP文件


# server = "ftp.ngdc.noaa.gov"
# dir = "hazards/DART/20070815_peru"
# filename = "21415_from_20070727_08_55_15_tides.txt"
# ftp = ftplib.FTP(server)
# ftp.login()
# ftp.cwd(dir)
# out = open(filename, "wb")
# ftp.retrbinary("RETR " + filename, out.write)
# out.close()


