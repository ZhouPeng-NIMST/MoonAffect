#coding:utf-8
import numpy as np
import sys
import os
import datetime
import WritrLog
from MoonAffect import MoonAffect
import xlrd
import xlwt
import numpy as np
#import copy
from xlutils.copy import  copy
# OBCInpath = r"F:\\MWHS\\DATA\OBC\\2017\\"
# L1Inpath = r"F:\\MWHS\\DATA\\DATA\\"
# OutPath = r"F:\\MWHS\\RESULT\\"
logger = WritrLog.log("Main.log")

def Write_Excel(filename, sheetname, strdate, data, overwrite):
    nrows = 0
    sheetname = "MoonAffect"
    if not os.path.isfile(filename):
        wfile = xlwt.Workbook(encoding="ascii")
        # 创建新表
        wtsheet = wfile.add_sheet(sheetname, cell_overwrite_ok = True)
    elif overwrite == 0:
        rdbook = xlrd.open_workbook(filename)
        table = rdbook.sheet_by_name(sheetname)
        nrows = table.nrows
        ncols = table.ncols
        wfile = copy(rdbook)
        wtsheet = wfile.get_sheet(sheetname)
    else:
        wfile = xlwt.Workbook(encoding="ascii")
        # 创建新表
        wtsheet = wfile.add_sheet(sheetname, cell_overwrite_ok = True)

    #写入日期和数据
    wtsheet.write(nrows, 0, strDate)
    wtsheet.write(nrows, 1, len(data))

    for i in range(len(data)):
        wtsheet.write(nrows + 1 + i, 3, data[i])

    # 保存Excel文件
    wfile.save(filename)

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
    myPro = MoonAffect()

    dt = starDate
    fout = open(r"F:\\MWHS\\RESULT\\Static.txt","w")
    flag = 1

    while dt <= endDate:
        strDate = dt.strftime("%Y%m%d")
        #print strDate

        # count, MoonAffectFile = myPro.Moon_Extract_Step1(dt)
        # myPro.Moon_Extract_Step2(dt)
        try:
            myPro.Moon_Extract_Step3(dt)
        except BaseException,e:
            logger.error(e.message)
            logger.info(strDate + " Handle Failed")
            logger.info("Moon_Extract_Step3 Failed")
        #myPro.Moon_Extract_Step4(dt)

        '''
        #Step1: 提取月球影响日期和轨道数
        try:
            count, MoonAffectFile = myPro.Moon_Extract_Step1(dt)
        except BaseException,e:
            logger.error(e.message)
            logger.info(strDate + " Handle Failed")
            logger.info("Moon_Extract_Step1 Failed")

        if count == 0 :
            dt += datetime.timedelta(days=1)
            continue

        Write_Excel("F:\\MWHS\\RESULT\\static.xls",str(dt.year), strDate, MoonAffectFile, flag)
        flag = 0

        fout.write(strDate + "    " + str(count) + "\n")
        for item in MoonAffectFile:
            fout.write(item + "\n")

        #Step2: 提取冷空观测计数值偏差
        try:
            myPro.Moon_Extract_Step2(dt)
        except BaseException,e:
            logger.error(e.message)
            logger.info(strDate + " Handle Failed")
            logger.info("Moon_Extract_Step2 Failed")

        #Step3: 提取视像量夹角
        try:
            myPro.Moon_Extract_Step3(dt)
        except BaseException,e:
            logger.error(e.message)
            logger.info(strDate + " Handle Failed")
            logger.info("Moon_Extract_Step3 Failed")

        #Step4: 提取重定标后的亮温差
        try:
            myPro.Moon_Extract_Step4(dt)
        except BaseException,e:
            logger.error(e.message)
            logger.info(strDate + " Handle Failed")
            logger.info("Moon_Extract_Step4 Failed")
        '''
        dt += datetime.timedelta(days=1)

    fout.close()


