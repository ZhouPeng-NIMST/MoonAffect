#coding:utf-8
import h5py
import os
import sys
import datetime
from MoonAffect import MoonAffect
import shutil

def Read_HDF(filename, SDSname):
    with h5py.File(filename,'r') as fin:
        data = fin[SDSname][:]
        fin.close()

    return data

def LS_FILE(dirpath,fileType = ".HDF"):
    print dirpath
    file_ls = os.listdir(dirpath)
    file = []

    for item in file_ls:
        if not item.endswith(fileType):
            continue
        file.append(item)

    return file

def main(Inpath):

    if not os.path.exists(Inpath):
        print(Inpath, " is not exist, will be continue!!")
        return -1

    COMBPath = os.path.join(Inpath, "COMB")
    if not os.path.exists(COMBPath):
        print(COMBPath, " is not exist, will be create!!")
        os.makedirs(COMBPath)

    SourcePath = os.path.join(Inpath, "Source")

    SPBiasPath = os.path.join(Inpath, "SPBIAS")
    DiffAnglePath = os.path.join(Inpath, "DIFFANGLE")
    ReCalPath = os.path.join(Inpath, "ReCal")

    SourceFile = LS_FILE(SourcePath)
    for item in SourceFile:
        srcfile = os.path.join(SourcePath, item)
        dstfile = os.path.join(COMBPath, item)


        DiffAngleFile = os.path.join(DiffAnglePath, item)
        ReCalFile = os.path.join(ReCalPath, item)

        if not os.path.isfile(srcfile):
            print(srcfile, " is not exist!!!******************************************")
            continue

        if not os.path.isfile(DiffAngleFile):
            print(DiffAngleFile, " is not exist!!!******************************************")
            continue

        if not os.path.isfile(ReCalFile):
            print(ReCalFile, " is not exist!!!******************************************")
            continue

        # 开始合并数据文件
        shutil.copyfile(srcfile, dstfile)
        CombHDF(DiffAngleFile, dstfile)
        CombHDF(ReCalFile, dstfile)



def CombHDF(srcfile, dstfile):
    fin = h5py.File(srcfile, 'r')
    fout = h5py.File(dstfile, 'r+')

    for item in fin:
        if item in fout:
            continue
        else:
            fout[item] = fin[item][:]

    fin.close()
    fout.close()

def WriteHDF(filename, sdsname, data):
    fout = h5py.File(filename, "r+")

    fout[sdsname] = data
    fout.close()


if __name__ == '__main__':

    if len(sys.argv) == 3 :
        starDate = datetime.datetime.strptime(sys.argv[1],"%Y%m%d")
        endDate = datetime.datetime.strptime(sys.argv[2],"%Y%m%d")
    if len(sys.argv) == 2 :
        starDate = datetime.datetime.strptime(sys.argv[1],"%Y%m%d")
        endDate = datetime.datetime.strptime(sys.argv[1],"%Y%m%d")
    else:
        starDate = datetime.datetime.strptime("20130901","%Y%m%d")
        endDate = datetime.datetime.strptime("20181231","%Y%m%d")

    path = r"F:\MWHS\RESULT"

    dt = starDate
    while dt <= endDate:
        strDate = dt.strftime("%Y%m%d")
        strYear = str(dt.year)
        pathin = os.path.join(path,strYear, strDate)

        main(pathin)

        dt += datetime.timedelta(days=1)


