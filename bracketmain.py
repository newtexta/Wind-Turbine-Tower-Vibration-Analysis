# -*- coding: utf-8 -*-
#-*- author: Wale Yu              -*-
#-*- update: 2023.5.21              -*-
#-*- email:  chuanqi_yu2021@126.com -*-

from PyQt5.QtGui import QPalette,QColor,QIcon,QPixmap
from PyQt5.QtWidgets import QVBoxLayout,QMainWindow,QApplication,QMessageBox,QFileDialog,QDialog
from PyQt5.Qt import QTimer,Qt
from bracketmainUI import Ui_MainWindow
from bracketmainUI import Ui_Dialog
import sys
import cv2
import math
import sys
import cgitb
import bracketgraphic
import os
import sqlite3
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import mpl_toolkits.axisartist as axisartist
from matplotlib.widgets import Cursor 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from qt_material import apply_stylesheet
class AboutDialog(QDialog,Ui_Dialog):
	def __init__(self):
		super(AboutDialog,self).__init__()
		self.setupUi(self)
		a = os.path.abspath('.')
		b = a.split("\\")
		c = tuple(b)
		d = '/'.join(c)
		iconpath = d + "/resource/data/icon.png"
		icon = QIcon(iconpath)
		self.setWindowIcon(icon)
		pixmap = QPixmap(iconpath) # 加载图片
		self.label.setPixmap(pixmap)
		self.pushButton.clicked.connect(self.closeB)
	def closeB(self):
		self.close()
class run(QMainWindow,Ui_MainWindow):
	def __init__(self):
		super(run,self).__init__()
		self.setupUi(self)
		self.timer = QTimer()
		self.AboutDialog = AboutDialog()
		a = os.path.abspath('.')
		b = a.split("\\")
		c = tuple(b)
		d = '/'.join(c)
		iconpath = d + "/resource/data/icon.png"
		icon = QIcon(iconpath)
		self.setWindowIcon(icon)
		self.vboxlayout_1 = QVBoxLayout(self.groupBox)
		self.figure_1 = plt.figure(figsize = (8,8))
		self.canvas_1 = FigureCanvas(self.figure_1)
		self.toolbar_1 = NavigationToolbar(self.canvas_1, self)
		self.vboxlayout_1.addWidget(self.toolbar_1)
		self.vboxlayout_1.addWidget(self.canvas_1)
		self.vboxlayout_2 = QVBoxLayout(self.groupBox_2)
		self.figure_2 = plt.figure(figsize = (8,8))
		self.canvas_2 = FigureCanvas(self.figure_2)
		self.toolbar_2 = NavigationToolbar(self.canvas_2, self)
		self.vboxlayout_2.addWidget(self.toolbar_2)
		self.vboxlayout_2.addWidget(self.canvas_2)
		self.vboxlayout_3 = QVBoxLayout(self.groupBox_3)
		self.figure_3 = plt.figure(figsize = (8,8))
		self.canvas_3 = FigureCanvas(self.figure_3)
		self.toolbar_3 = NavigationToolbar(self.canvas_3, self)
		self.vboxlayout_3.addWidget(self.toolbar_3)
		self.vboxlayout_3.addWidget(self.canvas_3)
		self.vboxlayout_4 = QVBoxLayout(self.groupBox_4)
		self.figure_4 = plt.figure(figsize = (8,8))
		self.canvas_4 = FigureCanvas(self.figure_4)
		self.toolbar_4 = NavigationToolbar(self.canvas_4, self)
		self.vboxlayout_4.addWidget(self.toolbar_4)
		self.vboxlayout_4.addWidget(self.canvas_4)
		self.actionOpen.triggered.connect(self.open_image)
		self.actionQuit.triggered.connect(self.close_image)
		self.action_Dark.triggered.connect(self.DarkTheme)
		self.action_Blue.triggered.connect(self.BlueTheme)
		self.action_Light.triggered.connect(self.LightTheme)
		self.action_Indigo.triggered.connect(self.IndigoTheme)
		self.action_Original.triggered.connect(self.OriginalTheme)
		self.actionAbout.triggered.connect(self.About)
		self.timer.timeout.connect(self.determine)
		self.timer.start(1000)
	def About(self):
		self.AboutDialog.show()
	def close_image(self):
		reply = QMessageBox.question(self,'Message','是否退出？',QMessageBox.Yes,QMessageBox.No)
		if reply == QMessageBox.Yes:
			a = os.path.abspath('.')
			b = a.split("\\")
			c = tuple(b)
			d = '/'.join(c)
			datafile = d + "/resource/data/positionData.sqlite3"
			conn = sqlite3.connect(datafile)
			cu = conn.cursor()
			cu.execute("DELETE FROM test;")
			cu.execute("DELETE FROM testM;")
			cu.execute("UPDATE isM SET isM = ? WHERE id = ?", (0,1))
			cu.execute("UPDATE isClear SET isC = ? WHERE id = ?", (0,1))
			conn.commit()
			conn.close()
			sys.exit()
		else:
			pass
	def DarkTheme(self):
		apply_stylesheet(self, theme='dark_lightgreen.xml')
	def BlueTheme(self):
		apply_stylesheet(self, theme='dark_cyan.xml')
	def LightTheme(self):
		apply_stylesheet(self, theme='light_blue.xml')
	def IndigoTheme(self):
		apply_stylesheet(self, theme='light_orange.xml')
	def OriginalTheme(self):
		default_palette = QPalette()
		default_palette.setColor(QPalette.Window, QColor(240, 240, 240))
		default_palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
		self.setPalette(default_palette)
		self.setAutoFillBackground(True)
		self.setStyleSheet('')
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_P:
			self.plot1()
	def open_image(self):
		fnames,_ = QFileDialog.getOpenFileName(self,'OpenFile','.','Image(*.mp4)')
		if fnames:
			a = os.path.abspath('.')
			b = a.split("\\")
			c = tuple(b)
			d = '/'.join(c)
			datafile = d + "/resource/data/positionData.sqlite3"
			data = (fnames,1)
			conn=sqlite3.connect(datafile)
			cu=conn.cursor()
			cu.execute("UPDATE orignalPicture SET picturePath = ? WHERE id = ?", data)
			conn.commit()
			conn.close()
			conn=sqlite3.connect(datafile)
			cu=conn.cursor()
			cu.execute("UPDATE dddd SET id = ? WHERE id = ?", (1,0))
			conn.commit()
			conn.close()
			self.graphics = bracketgraphic.PaintBoard1()
			self.graphics.show()
	def determine(self):
		a = os.path.abspath('.')
		b = a.split("\\")
		c = tuple(b)
		d = '/'.join(c)
		datafile = d + "/resource/data/positionData.sqlite3"
		conn=sqlite3.connect(datafile)
		cu=conn.cursor()
		cu.execute("SELECT * FROM determine")
		determineresult = list(cu.fetchall()[0])
		conn.commit()
		conn.close()
		if determineresult[0] == 0:
			pass
		else:
			self.plot1()
			conn=sqlite3.connect(datafile)
			cu=conn.cursor()
			cu.execute("UPDATE determine SET determine = ? WHERE determine = ?", (0,1))
			results2 = cu.fetchall()
			conn.commit()
			conn.close()
	def plot1(self):
		a = os.path.abspath('.')
		b = a.split("\\")
		c = tuple(b)
		d = '/'.join(c)
		savefileCSV1= d + "/resource/result/Displacement.csv"
		savefileCSV2 = d + "/resource/result/fft.csv"
		df1 = pd.read_csv(savefileCSV1, header=0)
		df2 = pd.read_csv(savefileCSV2, header=0)
		xdata = np.array(df1['frame_number'].tolist())
		ydata_u = np.array(df1['avg_u'].tolist())
		ydata_v = np.array(df1['avg_v'].tolist())
		ydata_f = np.array(df1['feature_matching'].tolist())
		xdata_fo = np.array(df2['frequency'].tolist())
		ydata_fo = np.array(df2['amplitude'].tolist())
		if a:
			self.isDrawn = True
			self.figure_1.clear()
			self.ax1 = self.figure_1.add_subplot(111)
			self.ax1.set_xlabel('Time/s')
			self.ax1.set_ylabel('Displacement')
			self.ax1.set_title('Average-U')
			self.ax1.title.set_size(20)
			self.ax1.xaxis.set_label_coords(1, 0)
			self.ax1.yaxis.set_label_coords(0, 1)
			self.ax1.xaxis.label.set_size(15)
			self.ax1.yaxis.label.set_size(10)
			self.figure_1.tight_layout(pad=2)
			self.ax1.plot(xdata, ydata_u, '-',color="#000000",lw=2)
			lineprops = dict(color="red",lw=2)
			self.cursor = Cursor(self.ax1,useblit=True,**lineprops)
			self.isDrawn = True
			self.figure_2.clear()
			self.ax2 = self.figure_2.add_subplot(111)
			self.ax2.set_xlabel('Time/s')
			self.ax2.set_ylabel('Displacement')
			self.ax2.set_title('Average-V')
			self.ax2.title.set_size(20)
			self.ax2.xaxis.set_label_coords(1, 0)
			self.ax2.yaxis.set_label_coords(0, 1)
			self.ax2.xaxis.label.set_size(15)
			self.ax2.yaxis.label.set_size(10)
			self.figure_2.tight_layout(pad=2)
			self.ax2.plot(xdata, ydata_v, '-',color="#000000",lw=2)
			lineprops_1 = dict(color="red",lw=2)
			self.cursor_1 = Cursor(self.ax2,useblit=True,**lineprops_1)
			self.isDrawn = True
			self.figure_3.clear()
			self.ax3 = self.figure_3.add_subplot(111)
			self.ax3.set_xlabel('Frequency')
			self.ax3.set_ylabel('Amplitude')
			self.ax3.set_title('FFT-U')
			self.ax3.title.set_size(20)
			self.ax3.xaxis.set_label_coords(1, 0)
			self.ax3.yaxis.set_label_coords(0.03, 1)
			self.ax3.xaxis.label.set_size(10)
			self.ax3.yaxis.label.set_size(10)
			self.figure_3.tight_layout(pad=2)
			self.ax3.plot(xdata_fo, ydata_fo, '-',color="#000000",lw=2)
			lineprops_2 = dict(color="red",lw=2)
			self.cursor_2 = Cursor(self.ax3,useblit=True,**lineprops_2)
			self.isDrawn = True
			self.figure_4.clear()
			self.ax4 = self.figure_4.add_subplot(111)
			self.ax4.set_xlabel('Time/s')
			self.ax4.set_ylabel('y')
			self.ax4.set_title('Title')
			self.ax4.title.set_size(20)
			self.ax4.xaxis.set_label_coords(1, 0)
			self.ax4.yaxis.set_label_coords(0, 1)
			self.ax4.xaxis.label.set_size(15)
			self.ax4.yaxis.label.set_size(15)
			self.figure_4.tight_layout(pad=2)
			self.ax4.scatter(xdata, ydata_f,s = 2)
			lineprops_3 = dict(color="red",lw=2)
			self.cursor_3 = Cursor(self.ax4,useblit=True,**lineprops_3)
	def closeEvent(self,event):
		reply = QMessageBox.question(self,'Message','是否退出？',QMessageBox.Yes,QMessageBox.No)
		if reply == QMessageBox.Yes:
			a = os.path.abspath('.')
			b = a.split("\\")
			c = tuple(b)
			d = '/'.join(c)
			datafile = d + "/resource/data/positionData.sqlite3"
			conn = sqlite3.connect(datafile)
			cu = conn.cursor()
			cu.execute("DELETE FROM test;")
			cu.execute("DELETE FROM testM;")
			cu.execute("UPDATE isM SET isM = ? WHERE id = ?", (0,1))
			cu.execute("UPDATE isClear SET isC = ? WHERE id = ?", (0,1))
			conn.commit()
			conn.close()
			event.accept()
			sys.exit()
		else:
			event.ignore()
if __name__ == '__main__':
	app = QApplication(sys.argv)
	win = run()
	win.show()
	sys.exit(app.exec())