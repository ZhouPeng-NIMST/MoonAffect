#coding:utf-8
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.basemap import Basemap
import numpy as np
from matplotlib.font_manager import FontProperties
import os
from matplotlib.dates import  DateFormatter, num2date, date2num, DayLocator, DayLocator, MonthLocator, YearLocator
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.gridspec as gridspec
import datetime

class Draw_Pic():

    def __init__(self):
        self.font = FontProperties(fname="simsun.ttf")

    def Plot_OBC_SP(self, FileName, srcTime, Data):
        print "Start Plot " +  FileName + " OBC Space View..."
        Data = Data.astype('float')
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

        file = os.path.basename(FileName)
        path = os.path.dirname(FileName)
        opath = os.path.join(path,"IMAGE_SP")
        if not os.path.isdir(opath):
            os.makedirs(opath)
        for ichan in range(15):
            ind = np.where(Data > OBC_lim[ichan][1])
            Data[ind] = np.nan
            ind = np.where(Data < OBC_lim[ichan][0])
            Data[ind] = np.nan
            title = file.replace(".png", "_CH") + str(ichan + 1)
            outFilename = os.path.join(opath, file.replace(".png", "_CH%s.png") %(str(ichan + 1)))
            self.Plot_Space_View(outFilename, srcTime, Data, ichan, title)

        print outFilename," output success..."

    def Plot_Space_View(self, outFilename, srctime, Data, ichan, title):
        print "Start Plot " +  outFilename + " Space View Time Order Picture..."
        s_dt = srctime[0]
        dt = srctime[-1]

        # 绘图
        #figure = matplotlib.figure.Figure()
        figure = plt.figure()
        figure.set_facecolor("#ffffff")

        w = 800
        h = 600
        w_inches = (w*1.0)/100
        h_inches = (h*1.0)/100
        figure.set_size_inches(w_inches, h_inches)

        right=50
        top=60
        bottom=50
        left=50
        figure.set_size_inches(w_inches, h_inches)
        FigureCanvasAgg(figure)

        # 设置axes0、axes1两个画板
        figure.clf()
        gs = gridspec.GridSpec(600, 800, left=0, right=1, bottom=0, top=1)
        axes0 = figure.add_subplot(gs[top:top+440, left:-right])
        axes1 = figure.add_subplot(gs[525:535, left:-right])
        #axes0.set_ylabel(u'Angle(°)', fontproperties=self.font)

        axes0.set_title(title, fontproperties=self.font, size=12)
        axes0.plot(srctime, Data[:,0,ichan], color='r', lw=0.5)
        axes0.plot(srctime, Data[:,1,ichan], color='g', lw=0.5)
        axes0.plot(srctime, Data[:,2,ichan], color='b', lw=0.5)
        # 设置格式
        #axes0.set_axis_bgcolor('#EBEBF3')
        # axes0.set_facecolor('#EBEBF3')
        # axes0.spines['left'].set_color('#FFFFFF')
        # axes0.spines['right'].set_color('#FFFFFF')
        # axes0.spines['top'].set_color('#FFFFFF')
        # axes0.spines['bottom'].set_color('#FFFFFF')
        # axes0.tick_params(color='#FFFFFF', which='both', top=False)
        # axes0.grid(True, axis='both', color='#FFFFFF', linestyle='-', zorder=1)

        # if  (dt - s_dt).days <=1:
        #     axes0.set_xlim(s_dt, dt+datetime.timedelta(days=1))
        #     axes1.set_xlim(s_dt, dt+datetime.timedelta(days=1))
        # else:

        # 设置X轴范围
        axes0.set_xlim(s_dt-datetime.timedelta(minutes=2), dt+datetime.timedelta(minutes=2))
        axes1.set_xlim(s_dt-datetime.timedelta(minutes=2), dt+datetime.timedelta(minutes=2))
        # axes0.set_xlim(s_dt, dt)
        # axes1.set_xlim(s_dt, dt)

        #设置Y轴范围
        ymax = Data.max()
        #axes0.set_ylim(ymin=0, ymax=ymax)

        #legend0 = matplotlib.lines.Line2D([0,0],[0,1], color='blue', linestyle='none', marker='o', markeredgecolor='none')
        #legend1 = matplotlib.lines.Line2D([0,0],[0,1], color='red', linestyle='none', marker='o', markeredgecolor='none')
        #axes0.legend([legend0, legend1], ['DAY', 'MONTH'], bbox_to_anchor=(0.4, -0.1), ncol=2, numpoints=1, framealpha=0, fontsize=12)
        formatter = DateFormatter('%H:%M')
        axes0.xaxis.set_major_formatter(formatter)

        axes1.yaxis.set_visible(False)
        axes1.spines['left'].set_color('#FFFFFF')
        axes1.spines['right'].set_color('#FFFFFF')
        axes1.spines['top'].set_visible(False)
        formatter = DateFormatter('%Y%m%d')
        axes1.xaxis.set_major_formatter(formatter)
        #axes1.xaxis.set_major_locator(YearLocator())
        axes1.xaxis.set_major_locator(DayLocator())


        #axes1.set_xlabel('%s_%s FY3D_MERSI'%(self.s_dt.strftime('%Y%m%d'), dt.strftime('%Y%m%d')), size=12)
        axes1.xaxis.set_label_coords(0.70, -2.5)

        figure.savefig(outFilename, dpi=200, bbox_inches='tight')
        figure.savefig(outFilename.replace(".png", ".eps"), dpi=200, bbox_inches='tight')
        plt.close(figure)
        print outFilename," output success..."

    def Plot_SP_Diff(self, filename, lon, lat, data):
        print "Start  " +  filename + " Space View Diff..."
        fig,[[axes1,axes2],[axes3,axes4]] = plt.subplots(2, 2 , figsize = (12,6))

        axes1.set_title(u"ch1(89GHz)  真实冷空观测值-冷空订正后值",fontproperties=self.font)
        self.Draw_Base(fig, axes1, lon, lat, data[:, 0])

        axes2.set_title(u"ch6(118.75±1.1GHz)  真实冷空观测值-冷空订正后值",fontproperties=self.font)
        self.Draw_Base(fig, axes2, lon, lat, data[:, 5])

        axes3.set_title(u"ch10(150GHz)  真实冷空观测值-冷空订正后值",fontproperties=self.font)
        self.Draw_Base(fig, axes3, lon, lat, data[:, 9])

        axes4.set_title(u"ch13(183±3GHz)  真实冷空观测值-冷空订正后值",fontproperties=self.font)
        self.Draw_Base(fig, axes4, lon, lat, data[:, 12])

        # fig = plt.figure(figsize=(20,10),dpi=200)
        # plt.subplot(221)
        # plt.title(u"ch1  真实冷空观测值-冷空订正后值",fontproperties=self.font)
        # m = self.Draw_Base(lon, lat, data[:, 0])
        #
        # plt.subplot(222)
        # plt.title(u"ch6  真实冷空观测值-冷空订正后值",fontproperties=self.font)
        # m = self.Draw_Base(lon, lat, data[:, 5])
        #
        # plt.subplot(223)
        # plt.title(u"ch10  真实冷空观测值-冷空订正后值",fontproperties=self.font)
        # m = self.Draw_Base(lon, lat, data[:, 9])
        #
        # plt.subplot(224)
        # plt.title(u"ch13  真实冷空观测值-冷空订正后值",fontproperties=self.font)
        # m = self.Draw_Base(lon, lat, data[:, 12])

        #保存图片

        fig.savefig(filename, dpi=200, bbox_inches='tight')
        fig.savefig(filename.replace(".jpg", ".eps"), dpi=200, bbox_inches='tight')
        plt.close(fig)
        print filename," output success..."

    def Draw_Base(self, fig, axes, lon, lat, data):
        m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c', ax=axes)
        m.drawparallels(range(-90, 91, 90), color='black', labels=[1, 0, 0, 0], dashes=[1, 1], linewidth=0.2, labelstyle = '+/-')
        m.drawmeridians(range(-180, 180, 180), color='black',labels=[0, 0, 0, 1], dashes=[1, 1], linewidth=0.2,labelstyle = '+/-')

        m.drawcoastlines(linewidth=0.5, linestyle='solid', color=(0, 0, 0, 0.8))
        #m.drawcountries(linewidth=0.2, linestyle='solid', color=(0, 0, 0, 1))
        sc = m.scatter(lon, lat, c=data, cmap=matplotlib.cm.jet, marker='.',s = 1)

        #加colorbar及colorbar的刻度
        cb = fig.colorbar(sc, orientation='vertical',  ax=axes)
        #cb = plt.colorbar(sc, orientation='horizontal',  ax=axes)
        #cb.set_label('$BT(K)$', size=20)
        cb.ax.tick_params(labelsize = 10)
        return m

    def Plot_SP_Moon_Angle(self, outFilename, srctime, Data, SV_Bias):
        print "Start Plot " +  outFilename + " Space View Moon Affect Angle..."
        s_dt = srctime[0]
        dt = srctime[-1]
        Data = np.array(Data)
        SV_Bias = np.array(SV_Bias)
        # 绘图
        #figure = matplotlib.figure.Figure()
        figure = plt.figure()
        figure.set_facecolor("#ffffff")

        w = 800
        h = 600
        w_inches = (w*1.0)/100
        h_inches = (h*1.0)/100
        figure.set_size_inches(w_inches, h_inches)

        right=50
        top=50
        bottom=50
        left=50
        figure.set_size_inches(w_inches, h_inches)
        FigureCanvasAgg(figure)

        # 设置axes0、axes1两个画板
        figure.clf()
        gs = gridspec.GridSpec(600, 800, left=0, right=1, bottom=0, top=1)
        axes0 = figure.add_subplot(gs[top:top+250, left:-right])

        axes0.plot(srctime, SV_Bias[:, 0], label = "First",  color='r', lw=0.5)
        axes0.plot(srctime, SV_Bias[:, 1], label = "Second", color='g', lw=0.5)
        axes0.plot(srctime, SV_Bias[:, 2], label = "Third",  color='b', lw=0.5)

        axes0.axhline(y=0, color = 'black', lw = 0.5)

        axes0.set_ylabel(u'Δ' + r'$C$$_{moon}(Counts)$', fontproperties=self.font, size=12)
        axes0.set_title(u"冷空观测计数值偏差", fontproperties=self.font, size=12)
        #设置X轴范围
        axes0.set_xlim(s_dt-datetime.timedelta(hours=1), dt+datetime.timedelta(hours=1))
        # 设置Y轴范围
        ymax = SV_Bias.max()
        #axes0.set_ylim(ymin=0, ymax=ymax)
        from matplotlib.ticker import NullFormatter
        nullfmt = NullFormatter()
        axes0.xaxis.set_major_formatter(nullfmt)
        #设置图例
        axes0.legend(loc = 'upper right')

        # 第二个图绘图
        axes1 = figure.add_subplot(gs[350:600,     left:-right])

        axes1.plot(srctime, Data[0,:], label = "First", color='r', lw=0.5)
        axes1.plot(srctime, Data[1,:], label = "Second",color='g', lw=0.5)
        axes1.plot(srctime, Data[2,:], label = "Third", color='b', lw=0.5)

        axes1.set_ylabel(r'$\beta$' + r"$_{Moon}(Degree)$", fontproperties=self.font, size = 12)
        axes1.set_title(u"月球视像量与冷空观测视像量夹角", fontproperties=self.font, size=12)
        #设置X轴范围
        axes1.set_xlim(s_dt-datetime.timedelta(hours=1), dt+datetime.timedelta(hours=1))
        # 设置Y轴范围
        ymax = Data.max() + 2
        axes1.set_ylim(ymin=0, ymax=ymax)
        axes1.legend(loc = 'upper right')

        formatter = DateFormatter('%H:%M')
        axes1.xaxis.set_major_formatter(formatter)

        # 设置格式
        #axes0.set_axis_bgcolor('#EBEBF3')
        # axes0.set_facecolor('#EBEBF3')
        # axes0.spines['left'].set_color('#FFFFFF')
        # axes0.spines['right'].set_color('#FFFFFF')
        # axes0.spines['top'].set_color('#FFFFFF')
        # axes0.spines['bottom'].set_color('#FFFFFF')
        # axes0.tick_params(color='#FFFFFF', which='both', top=False)
        # axes0.grid(True, axis='both', color='#FFFFFF', linestyle='-', zorder=1)

        # if  (dt - s_dt).days <=1:
        #     axes0.set_xlim(s_dt, dt+datetime.timedelta(days=1))
        #     axes1.set_xlim(s_dt, dt+datetime.timedelta(days=1))
        # else:

        #legend0 = matplotlib.lines.Line2D([0,0],[0,1], color='blue', linestyle='none', marker='o', markeredgecolor='none')
        #legend1 = matplotlib.lines.Line2D([0,0],[0,1], color='red', linestyle='none', marker='o', markeredgecolor='none')
        #axes0.legend([legend0, legend1], ['DAY', 'MONTH'], bbox_to_anchor=(0.4, -0.1), ncol=2, numpoints=1, framealpha=0, fontsize=12)
        # formatter = DateFormatter('%H:%M')
        #axes0.xaxis.set_major_formatter(formatter)
        # axes1.xaxis.set_major_formatter(formatter)

        #axes1.yaxis.set_visible(False)
        # axes1.spines['left'].set_color('#FFFFFF')
        # axes1.spines['right'].set_color('#FFFFFF')
        # axes1.spines['top'].set_visible(False)
        # formatter = DateFormatter('%Y%m%d')
        #axes1.xaxis.set_major_formatter(formatter)
        #axes1.xaxis.set_major_locator(YearLocator())
        #axes1.xaxis.set_major_locator(DayLocator())

        #axes1.set_xlabel('%s_%s FY3D_MERSI'%(self.s_dt.strftime('%Y%m%d'), dt.strftime('%Y%m%d')), size=12)
        #axes1.xaxis.set_label_coords(0.70, -2.5)

        figure.savefig(outFilename, dpi=200, bbox_inches='tight')
        figure.savefig(outFilename.replace(".png", ".eps"), dpi=200, bbox_inches='tight')

        plt.close(figure)
        print outFilename," output success..."

    def Plot_BT_Diff(self, filename, lon, lat, data1,data2,data3,data4):
        print "Start Plot " +  filename + " BT Diff ..."
        fig,[[axes1,axes2],[axes3,axes4]] = plt.subplots(2, 2 , figsize = (12,6))

        axes1.set_title(u"ch1(89GHz)",fontproperties=self.font)
        self.Draw_Base(fig, axes1, lon, lat, data1)

        axes2.set_title(u"ch6(118.75±1.1GHz)",fontproperties=self.font)
        self.Draw_Base(fig, axes2, lon, lat, data2)

        axes3.set_title(u"ch10(150GHz)",fontproperties=self.font)
        self.Draw_Base(fig, axes3, lon, lat, data3)

        axes4.set_title(u"ch13(183±3GHz)",fontproperties=self.font)
        self.Draw_Base(fig, axes4, lon, lat, data4)

        #保存图片
        fig.savefig(filename, dpi=200, bbox_inches='tight')
        #fig.savefig(filename.replace(".jpg", ".eps"), dpi=200, bbox_inches='tight')
        plt.close(fig)
        print filename," output success..."

        return 0
