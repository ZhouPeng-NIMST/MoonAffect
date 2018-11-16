#coding:utf-8
import h5py
import os
import imageio
import sys
import datetime

if len(sys.argv) == 4 :
    model = sys.argv[1]
    starDate = datetime.datetime.strptime(sys.argv[2],"%Y%m%d")
    endDate = datetime.datetime.strptime(sys.argv[3],"%Y%m%d")
elif len(sys.argv) == 3 :
    model = sys.argv[1]
    starDate = datetime.datetime.strptime(sys.argv[2],"%Y%m%d")
    endDate = datetime.datetime.strptime(sys.argv[2],"%Y%m%d")
else:
    starDate = datetime.datetime.strptime("20180101","%Y%m%d")
    endDate = datetime.datetime.strptime("20180101","%Y%m%d")
    model = 'TG'

print starDate
#
# filename = r"F:\MWHS\RESULT\2013\20131023\Source\FY3C_MWHSX_GBAL_L1_20131023_2032_015KM_MS.HDF"
#
# fin = h5py.File(filename, 'r')
# for item in fin:
#     #print fin.get(item)
#     if item in fin:
#
#         pass
# fin.close()


