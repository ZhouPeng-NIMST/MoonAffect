#coding:utf-8
import WritrLog
from Draw_Pic import Draw_Pic
import os
import math
import h5py
import numpy as np
import datetime
from BTProcess import BTpro

class MoonAffect():
    def __init__(self):
        self.logger = WritrLog.log("MoonAffect.log")
        self.Draw = Draw_Pic()
        self.L1DataSet = {
            "Geolocation":  ["Latitude",
                             "Longitude",
                             "SolarAzimuth",
                             "SolarZenith",
                             "SensorAzimuth",
                             "SensorZenith",
                             "Scnlin_daycnt",
                             "Scnlin_mscnt"],
            "Data":[        "Earth_Obs_BT",
                             "LandSeaMask"]
        }

        self.OBCDataSet = {
            "Geolocation":["EVC_LON_LAT",
                            "CV_Moon_Vector",
                            "CV_Sun_Vector",
                            "EVS_orb_pos",
                            "EVS_orb_vel",
                            "EVS_Attitude_angles"],
            "Calibration":["Cal_Coefficient",
                            "Raw_DN_Data",
                            "Black_Body_View",
                            "Space_View",
                            "Space_View_Ang",
                            "BB_PRT",
                            "PRT_Tavg",
                            "Inst_Temp",
                            "SPBB_DN_Avg",
                            "AGC"]
        }
        self.OBCInpath = r"F:\\MWHS\\DATA\OBC\\"
        self.L1Inpath = r"F:\\MWHS\\DATA\\DATA\\"
        self.OutPath = r"F:\\MWHS\\RESULT\\"
        self.FilePath = {
            "OBCInpath": r"F:\\MWHS\\DATA\OBC\\%s\\%s\\",
            "L1Inpath":  r"F:\\MWHS\\DATA\\DATA\\%s\\%s\\",
            "Source": r"F:\\MWHS\\RESULT\\%s\\%s\\Source\\",
            "SPBIAS": r"F:\\MWHS\\RESULT\\%s\\%s\\SPBIAS\\",
            "DIFFANGLE": r"F:\\MWHS\\RESULT\\%s\\%s\\DIFFANGLE\\",
            "ReCal": r"F:\\MWHS\\RESULT\\%s\\%s\\ReCal\\",
            "L1FileName": "FY3C_MWHSX_GBAL_L1_20160625_2240_015KM_MS.HDF",
            "SPBIASFileName": "FY3C_MWHSX_GBAL_L1_YYYYMMDD_015KM_SPBIAS.HDF",
            "DIFFANGLEFileName": "FY3C_MWHSX_GBAL_L1_YYYYMMDD_015KM_DIFFANGLE.HDF",
            "ReCalFileName": "FY3C_MWHSX_GBAL_L1_YYYYMMDD_015KM_BT.HDF"
        }

        self.pmd = {
            "viewScope": 1.1,
             "moonScope": 1,
             "deltaAngle": 3.1,
             "moonZenith": 72.9,
             "mooAzimuth": 90
        }
        self.SP_Angle = {
            0: 73.14,
            1: 72.9,
            2: 72.46
        }

        # 根据月球视像量求月球的天顶角、方位角
        self.Moon_Affect_Scans = []
        self.Moon_Zenith = []
        self.Moon_Azimuth = []

    def Moon_Extract_Step1(self, dt):
        '''
        Step1:提取受冷空影像的日期和轨道
        :param dt:
        :return:
        '''
        MoonAffectFile = []
        count = 0
        strDate = dt.strftime("%Y%m%d")
        year = dt.year

        # path = os.path.join(self.OBCInpath,str(year))
        # path = os.path.join(path, strDate)

        # 拼接OBC输入文件目录
        path = self.FilePath["OBCInpath"] %(str(year), strDate)

        if not os.path.isdir(path):
            print path, " is not file path!!!"
            return count, MoonAffectFile

        ls = os.listdir(path)

        # 对每轨数据进行判断是否受到月球污染
        for item in ls :
            OBCFileName = os.path.join(path, item)
            # print OBCFileName
            if not  OBCFileName.endswith(".HDF"):
                continue

            try:
                #月球污染判断
                CV_Moon_Vector = self.ReadHDF(OBCFileName, r"/Geolocation/CV_Moon_Vector/")
            except BaseException,e:
                print OBCFileName, "is a problem file, will be continue!!!"
                self.logger.error(OBCFileName + "is a problem file, will be continue!!!" )
                self.logger.error(e.message)
                continue

            # Step1:提取受冷空影像的日期和轨道
            Affect_Flag = self.Moon_Angle_Affect(OBCFileName, CV_Moon_Vector)
            if Affect_Flag == 0 :
                continue

            print "******Moon Affect File Name :******",OBCFileName
            count += 1
            MoonAffectFile.append(os.path.basename(OBCFileName))

            # just for test
            #continue


            # 拼接L1文件名
            L1path = self.FilePath["L1Inpath"] %(str(year), strDate)
            L1FileName = item.replace("OBCXX", "015KM")
            L1FileName = os.path.join(L1path, L1FileName)

            #对L1与OBC扫描线一致性判断，如果两个文件的扫描线不相同，则该轨数据跳过
            Latitude = self.ReadHDF(L1FileName, r"/Geolocation/Latitude/")
            EVC_LON_LAT = self.ReadHDF(OBCFileName, r"/Geolocation/EVC_LON_LAT/")
            L1scans = np.array(Latitude).shape[0]
            OBCscans = np.array(EVC_LON_LAT).shape[0]
            if L1scans != OBCscans:
                print OBCFileName, " Scans is not equeal!!!"
                self.logger.error(OBCFileName)
                self.logger.error("L1scans:" + str(L1scans) + " OBCscans:" + str(OBCscans) + " is not equeal!!!")
                continue

            # 拼接输出目录，如果不存在，则新建
            outpath_tmp = self.FilePath["Source"] %(str(year), strDate)
            if not os.path.isdir(outpath_tmp):
                print outpath_tmp, " is not exist, will be created!!"
                os.makedirs(outpath_tmp)

            outFileName= os.path.join(outpath_tmp, os.path.basename(L1FileName))

            # print "L1FileName:",L1FileName
            # print "OBCFileName:",OBCFileName
            # print "outFileName:",outFileName

            #从L1、OBC文件中读取相关数据集写入Source文件
            self.ReadAndWrite(L1FileName, OBCFileName, outFileName)
            print "Write ",outFileName, " success!!"

            # 绘制OBC Space View曲线图
            Space_View = self.ReadHDF(outFileName,"Space_View")
            Space_View = Space_View.astype("float")

            #绘制OBC Space View计数值
            startime =  datetime.datetime.strptime("20000101 12:00:00", "%Y%m%d %H:%M:%S")
            Scnlin_daycnt = self.ReadHDF(outFileName, "Scnlin_daycnt")
            Scnlin_mscnt = self.ReadHDF(outFileName, "Scnlin_mscnt")
            srcTime = []
            for iscan in range(len(Scnlin_daycnt)):
                datediff = Scnlin_daycnt[iscan] + Scnlin_mscnt[iscan] * 0.001 / 3600.0 / 24.0
                srcTime.append(startime + datetime.timedelta(days=datediff))
            # print np.array(srcTime).shape
            # print np.array(Space_View).shape
            myDraw = Draw_Pic()
            myDraw.Plot_OBC_SP(outFileName.replace(".HDF", "_SP.png"), srcTime, Space_View)

        return count, MoonAffectFile

    def Moon_Extract_Step2(self, dt):
        '''
        提取冷空计数值偏差
        :param dt:
        :return:
        '''
        strDate = dt.strftime("%Y%m%d")
        year = dt.year
        myDraw = Draw_Pic()

        # 拼接输入、输出目录
        pathin = self.FilePath["Source"] %(str(year), strDate)
        pathout = self.FilePath["SPBIAS"] %(str(year), strDate)

        if not os.path.isdir(pathin):
            #print pathin, " is not file path!!!"
            return -1

        if not os.path.isdir(pathout):
            os.makedirs(pathout)

        ls = os.listdir(pathin)
        lat = []
        lon = []
        data = []
        for item in ls :
            L1FileName = os.path.join(pathin, item)
            if not  L1FileName.endswith(".HDF"):
                continue

            EVC_LON_LAT = self.ReadHDF(L1FileName,"EVC_LON_LAT")
            Diff_SP = self.ReadHDF(L1FileName,"Diff_SP")
            Moon_Affect_Scans = self.ReadHDF(L1FileName,"Moon_Affect_Scans")

            ind = np.where(Moon_Affect_Scans == 0)
            Diff_SP[ind, :] = np.nan

            # 提取星下点经纬度
            temp1 = list(EVC_LON_LAT[:, 0])
            temp2 = list(EVC_LON_LAT[:, 1])
            temp3 = list(Diff_SP)

            lat = lat + temp1
            lon = lon + temp2
            data = data + temp3

        lat = np.array(lat)
        lon = np.array(lon)
        data =  np.array(data)

        #绘制月球影响的计数值偏差
        outHDFName = self.FilePath["SPBIASFileName"].replace("YYYYMMDD", strDate)
        outHDFName = os.path.join(pathout, outHDFName)
        self.WriteHDF(outHDFName, "Diff_SP", data, 1)
        self.WriteHDF(outHDFName, "Latitude", lat, 0)
        self.WriteHDF(outHDFName, "Longitude", lon, 0)

        outImageName = outHDFName.replace(".HDF", ".jpg")
        myDraw.Plot_SP_Diff(outImageName,lon, lat, data)


    def Moon_Extract_Step3(self, dt):
        '''
        提取冷空、月球视像量夹角
        :return:
        '''
        strDate = dt.strftime("%Y%m%d")
        year = dt.year
        myDraw = Draw_Pic()

        # 拼接输入、输出目录
        pathin = self.FilePath["Source"] %(str(year), strDate)
        pathout = self.FilePath["DIFFANGLE"] %(str(year), strDate)

        if not os.path.isdir(pathin):
            print pathin, " is not file path!!!"
            return -1

        # 如果输出目录不存在，则创建
        if not os.path.isdir(pathout):
            os.makedirs(pathout)

        ls = os.listdir(pathin)
        startime =  datetime.datetime.strptime("20000101 12:00:00", "%Y%m%d %H:%M:%S") # FY3 天计数的起始日期
        srcTime = []
        srcSpace_View = []
        srcMoon_vector = []
        srcSV_Bias = []
        for item in ls :
            L1FileName = os.path.join(pathin, item)
            if not  L1FileName.endswith(".HDF"):
                continue

            # 从Source文件中读取数据
            Space_View = self.ReadHDF(L1FileName, "Space_View")
            CV_Moon_Vector = self.ReadHDF(L1FileName, "CV_Moon_Vector")
            Scnlin_daycnt = self.ReadHDF(L1FileName, "Scnlin_daycnt")
            Scnlin_mscnt = self.ReadHDF(L1FileName, "Scnlin_mscnt")
            SPBB_DN_Avg = self.ReadHDF(L1FileName, "SPBB_DN_Avg")

            # 剔除异常冷空值
            Space_View = Space_View.astype(dtype="float")
            ind = np.where(Space_View > 12000)
            Space_View[ind] = np.nan
            ind = np.where(Space_View < 1000)
            Space_View[ind] = np.nan

            # 提取剔除月球污染后第一通道冷空计数值
            BB_Avg = SPBB_DN_Avg[:,15]

            # 取第1通道的冷空
            srcSpace_View += list(Space_View[:, :, 0])
            srcMoon_vector += list(CV_Moon_Vector)

            # 计算冷空偏差
            SV_Bias = []
            for i in range(3):
                SV_Bias1 = Space_View[:,i,0] - BB_Avg
                SV_Bias.append(SV_Bias1)
            SV_Bias = np.array(SV_Bias).T
            srcSV_Bias += list(SV_Bias)

            strdiff = []
            for iscan in range(len(Scnlin_daycnt)):
                datediff = Scnlin_daycnt[iscan] + Scnlin_mscnt[iscan] * 0.001 / 3600.0 / 24.0
                strdiff.append((startime + datetime.timedelta(days=datediff)).strftime("%Y-%m-%d %H:%M:%S"))
                srcTime.append(startime + datetime.timedelta(days=datediff))

            strDiffAngle = []
            for i in range(3):
                diff_ang = self.Angle(srcMoon_vector, i)
                strDiffAngle.append(diff_ang)

            strfile = os.path.join(pathout, item)

            self.WriteHDF(strfile,"Date", strdiff, 1)
            self.WriteHDF(strfile,"Diff_Angle", strDiffAngle, 0)
            self.WriteHDF(strfile,"SV_Bias", SV_Bias, 0)
        return 0
        # 计算冷空偏差
        # SP_Mean = np.nanmean(srcSpace_View)
        # SV_Bias = srcSpace_View - SP_Mean

        # 计算三次采样点的冷空、月球夹角
        diff = []
        for i in range(3):
            diff_ang = self.Angle(srcMoon_vector, i)
            diff.append(diff_ang)

        # 拼接输出文件名
        outname = self.FilePath["DIFFANGLEFileName"].replace("YYYYMMDD", strDate)
        outHDFFilename = os.path.join(pathout, outname)
        strTime = []
        for item in srcTime:
            strTime.append(item.strftime("%Y-%m-%d %H:%M:%S"))

        # 输出绘图相关数据
        self.WriteHDF(outHDFFilename,"Date", strTime, 1)
        self.WriteHDF(outHDFFilename,"Diff_Angle", diff, 0)
        self.WriteHDF(outHDFFilename,"SV_Bias", SV_Bias, 0)

        # 调用绘图
        outFilename = outHDFFilename.replace(".HDF", ".png")
        myDraw.Plot_SP_Moon_Angle(outFilename, srcTime, diff, srcSV_Bias)

        return 0

    def Moon_Extract_Step4(self,dt):
        '''
        FY3C MWHS定标重处理，进行定标系数计算以及亮温计算、亮温偏差计算
        :return:
        '''
        strDate = dt.strftime("%Y%m%d")
        year = dt.year

        # 拼接输入、输出目录
        pathin = self.FilePath["Source"] %(str(year), strDate)
        pathout = self.FilePath["ReCal"] %(str(year), strDate)

        if not os.path.isdir(pathin):
            print pathin, " is not file path!!!"
            return -1

        if not os.path.isdir(pathout):
            os.makedirs(pathout)

        ls = os.listdir(pathin)
        ls.sort()

        Longitude=[]
        Latitude=[]
        BT_Datach1=[]
        BT_Datach6=[]
        BT_Datach10=[]
        BT_Datach13=[]
        Diff_BT1=[]
        Diff_BT6=[]
        Diff_BT10=[]
        Diff_BT13=[]

        for item in ls :
            L1FileName = os.path.join(pathin, item)
            if not  L1FileName.endswith(".HDF"):
                continue

            outfilename = os.path.join(pathout, item)
            print outfilename
            lon, lat, bt, diffbt = BTpro(L1FileName,outfilename)
            # lon = list(lon)
            # lat = list(lat)
            # bt = list(bt)
            # diffbt = list(diffbt)
            Longitude += list(lon)
            Latitude += list(lat)
            BT_Datach1 = BT_Datach1 + list(bt[0,:,:])
            BT_Datach6 = BT_Datach6 + list(bt[5,:,:])
            BT_Datach10 += list(bt[9,:,:])
            BT_Datach13 += list(bt[12,:,:])
            Diff_BT1 += list(diffbt[0,:,:])
            Diff_BT6 += list(diffbt[5,:,:])
            Diff_BT10 += list(diffbt[9,:,:])
            Diff_BT13 += list(diffbt[12,:,:])

        Longitude = np.array(Longitude)
        Latitude = np.array(Latitude)
        BT_Datach1 = np.array(BT_Datach1)
        BT_Datacch6 = np.array(BT_Datach6)
        BT_Datacch10 = np.array(BT_Datach10)
        BT_Datacch13 = np.array(BT_Datach13)
        Diff_BT1 = np.array(Diff_BT1)
        Diff_BT6 = np.array(Diff_BT6)
        Diff_BT10 = np.array(Diff_BT10)
        Diff_BT13 = np.array(Diff_BT13)

        print Longitude.shape
        print Latitude.shape
        print(BT_Datach1.min())
        print(Diff_BT1.max())

        outname = self.FilePath["ReCalFileName"].replace("YYYYMMDD", strDate)
        outimgname = os.path.join(pathout, outname)

        myDraw = Draw_Pic()
        myDraw.Plot_BT_Diff(outimgname.replace("_BT.HDF", "_BT.jpg"), Longitude, Latitude, BT_Datach1, BT_Datacch6,BT_Datacch10,BT_Datacch13)
        myDraw.Plot_BT_Diff(outimgname.replace("_BT.HDF", "_DIFF.jpg"), Longitude, Latitude, Diff_BT1, Diff_BT6, Diff_BT10, Diff_BT13)

        return 0

    def SP_Diff(self, filename):
        '''
        计算Space View 剔除前后差值
        :param filename:
        :return:
        '''
        OBC_lim = {
            0:[1000,12000],
            1:[1000,10000],
            2:[1000,12000],
            3:[1000,12000],
            4:[1000,10000],
            5:[1000,10000],
            6:[1000,10000],
            7:[1000,10000],
            8:[1000,10000],
            9:[1000,10000],
            10:[1000,12000],
            11:[1000,12000],
            12:[1000,10000],
            13:[1000,10000],
            14:[1000,10000]
        }
        Data_Diff = []
        SPBB_DN_Avg = self.ReadHDF(filename, "SPBB_DN_Avg")
        Space_View = self.ReadHDF(filename, "Space_View")
        Space_View = Space_View.astype("float")
        for ichan in range(15):
            ind = np.where(Space_View > OBC_lim[ichan][1])
            Space_View[ind] = np.nan
            ind = np.where(Space_View < OBC_lim[ichan][0])
            Space_View[ind] = np.nan

            Data_Diff.append((Space_View[:, 0, ichan] + Space_View[:, 1, ichan] + Space_View[:, 2, ichan] ) / 3 - SPBB_DN_Avg[:, 15+ichan])

        return Data_Diff


    def ReadAndWrite(self, L1FileName, OBCFileName, outFileName):
        '''
        读写HDF文件
        :param L1FileName: L1文件名
        :param OBCFileName: OBC文件名
        :param outFileName: 输出提取数据后的文件名
        :return:
        '''
        if not os.path.isfile(L1FileName) :
            print L1FileName, " is not exist!!"
            return  -1
        if not os.path.isfile(OBCFileName) :
            print OBCFileName, " is not exist!!"
            return  -1

        overwrite = 1
        # L1 File 获取相关数据
        for key,value in self.L1DataSet.items() :
            for dset in value:
                sdsname =  "/" + key + "/" + dset
                data = self.ReadHDF(L1FileName,sdsname)
                status = self.WriteHDF(outFileName,dset, data, overwrite)
                overwrite = 0

        # OBC File 获取相关数据
        for key,value in self.OBCDataSet.items() :
            for dset in value:
                sdsname =  "/" + key + "/" + dset
                data = self.ReadHDF(OBCFileName,sdsname)
                status = self.WriteHDF(outFileName,dset, data, overwrite)
                overwrite = 0
        status = self.WriteHDF(outFileName,"Moon_Affect_Scans", self.Moon_Affect_Scans, 0)
        status = self.WriteHDF(outFileName,"Moon_Zenith", self.Moon_Zenith, 0)
        status = self.WriteHDF(outFileName,"Moon_Azimuth", self.Moon_Azimuth, 0)
        Moon_SP_Angle = abs(np.array(self.Moon_Azimuth) - self.pmd["moonZenith"])
        status = self.WriteHDF(outFileName,"Moon_SP_Angle", Moon_SP_Angle, 0)
        Diff_SP = self.SP_Diff(outFileName)
        Diff_SP = np.array(Diff_SP).T
        status = self.WriteHDF(outFileName,"Diff_SP", Diff_SP, 0)

        return 0


    def ReadHDF(self, filename, sdsname):
        '''
        读取HDF5文件
        :param filename: 输入文件名
        :param sdsname: 获取数据集名
        :return: 数据集数据
        '''
        fin = h5py.File(filename, "r")
        data = fin[sdsname][:]
        fin.close()

        return data


    def WriteHDF(self, filename, sdsname, data, overwrite):
        if overwrite == 1 :
            fout = h5py.File(filename, "w")
        else:
            fout = h5py.File(filename, "r+")

        fout[sdsname] = data
        #fout[sdsname].attrs["slope"] = 999
        fout.close()

        return 0


    def Moon_Angle_Affect(self, filename, CV_Moon_Vector):
        Affect_Scans_Temp = np.zeros((CV_Moon_Vector.shape[0] / 3))
        Moon_Zenith_Temp = []
        Moon_Azimuth_Temp = []
        ind = np.where(CV_Moon_Vector > 900)
        CV_Moon_Vector[ind] = np.nan
        #iscan = 2379
        Affect_Flag = 0
        for iscan in range(CV_Moon_Vector.shape[0] / 3):
            x = CV_Moon_Vector[3*iscan+1, 0]
            y = CV_Moon_Vector[3*iscan+1, 1]
            z = CV_Moon_Vector[3*iscan+1, 2]
            zenith = math.acos(z) * 180.0 / math.pi
            azimuth = math.acos(x/np.sqrt(x*x+ y*y)) * 180.0 / math.pi

            Moon_Azimuth_Temp.append(azimuth)
            Moon_Zenith_Temp.append(zenith)

            if y >= 0.0 :
                scope = (self.pmd["viewScope"] + self.pmd["moonScope"] + self.pmd["deltaAngle"])/2.0
                if(zenith >(self.pmd["moonZenith"]-scope) and zenith<(self.pmd["moonZenith"] +scope) and azimuth>(self.pmd["mooAzimuth"]-scope) and azimuth<(self.pmd["mooAzimuth"]+scope)):
                    Affect_Scans_Temp[iscan] = 1
                    Affect_Flag = 1

        self.Moon_Affect_Scans = Affect_Scans_Temp
        self.Moon_Zenith = Moon_Azimuth_Temp
        self.Moon_Azimuth = Moon_Zenith_Temp

        return Affect_Flag


    def Vector_Angle_Dims3(self, X, Y):
        '''
        计算三维矢量夹角
        :param X:
        :param Y:
        :return:
        '''
        x1 = X[0]
        x2 = X[1]
        x3 = X[2]

        y1 = Y[0]
        y2 = Y[1]
        y3 = Y[2]

        X_len = math.sqrt(x1**2 + x2**2 + x3**2)
        Y_len = math.sqrt(y1**2 + y2**2 + y3**2)

        print math.acos((x1*y1 + x2*y2 + x3*y3) / (X_len * Y_len)) * 180 / math.pi


    def Vector_Angle_Dims2(self, X, Y):
        '''
        计算二维矢量夹角
        :param X:
        :param Y:
        :return:
        '''
        x1 = X[0]
        x2 = X[1]

        y1 = Y[0]
        y2 = Y[1]

        X_len = math.sqrt(x1**2 + x2**2)
        Y_len = math.sqrt(y1**2 + y2**2)

        print math.acos((x1*y1 + x2*y2) / (X_len * Y_len)) * 180 / math.pi


    def Angle(self, CV_Moon_Vector, obs_num):
        CV_Moon_Vector = np.array(CV_Moon_Vector)
        diff = []

        diff_ang = 0
        for i in range(CV_Moon_Vector.shape[0]/3):
            x = CV_Moon_Vector[i*3 + obs_num, 0]
            y = CV_Moon_Vector[i*3 + obs_num, 1]
            z = CV_Moon_Vector[i*3 + obs_num, 2]
            if x>1 or y>1 or z>1:
                diff.append(diff_ang)
                continue

            moon2sp = self.SP_Angle[obs_num] - math.acos(z / math.sqrt(y**2 + z**2)) * 180.0 / math.pi
            diff_ang = math.acos(0.5 - 0.5 * (x**2 + y**2 + z**2) + math.sqrt(y**2 + z**2) * math.cos(moon2sp * math.pi / 180.0)) *180.0 / math.pi
            diff.append(diff_ang)


        return diff