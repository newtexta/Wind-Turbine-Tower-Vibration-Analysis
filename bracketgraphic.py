# -*- coding: utf-8 -*-
#-*- author: Huangxingjian、Yuchuanqi、Pengjunming             -*-
#-*- update: 2023.5.21              -*-
#-*- email:  Xingjian_Huang@outlook.com、chuanqi_yu2021@126.com、1004631895@qq.com -*-

from PyQt5.QtGui import QColor,QIcon,QPen,QBrush,QLinearGradient,QPainter,QPalette,QFont,QPixmap,QPainterPath
from PyQt5.QtWidgets import QSpinBox,QWidget,QGraphicsScene,QGraphicsItem,QGraphicsView,QGraphicsRectItem,QGraphicsPixmapItem,QGraphicsPathItem,QDialog,QApplication,QShortcut,QMessageBox
from PyQt5.Qt import Qt,QTimer,QBasicTimer,QRectF,QKeySequence,QPointF
from PyQt5.QtCore import QThread,pyqtSignal,QRect
import math
import sys
import cgitb
from bracketgraphicUI import Ui_Form
from bracketgraphicUI import Ui_Dialog
import sqlite3
import os
import re
import cv2
import numpy as np
import numpy.fft as fft
import time
import csv
class MyScene(QGraphicsScene):
    pen_color=Qt.green
    pen_width = 5
    Eraser_pen_width=20
    def __init__(self):
        super(MyScene, self).__init__(parent=None)
        self.setSceneRect(0,0,1280,720)
        self.EraseMode=False
        self.shape= "Free pen"
    def drawBackground(self, painter: QPainter, rect: QRectF):
        painter.drawRect(0,0,1280,720)
    def Eraser(self,b=False):
        self.EraseMode = b
        return self.EraseMode
    def Shape(self, s):
         self.shape = s
         return self.Shape
    def ChangePenColor(self, color):
        self.pen_color = QColor(color)
    def ChangePenThickness(self, thickness):
        self.pen_width=thickness
    def ChangeEraserThickness(self,EraserThickness):
        self.Eraser_pen_width=EraserThickness
class GraphicView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        try:
            self.scene = MyScene()
            self.shape = "Free pen"
            self.pen_color = Qt.red
            self.pen_width = 3
            self.x=0
            self.y=0
            self.wx=0
            self.wy=0
            self.setScene(self.scene)
        except Exception as e:
            print(e)
    def Shape(self, s):
        self.shape = s
        if self.shape == "move":
            self.setDragMode(QGraphicsView.RubberBandDrag)
        else:
            self.setDragMode(QGraphicsView.NoDrag)
        return self.shape
    def ChangePenColor(self, color):
        self.pen_color = QColor(color)
        return self.pen_color
    def ChangePenThickness(self, thickness):
        self.pen_width=thickness
    def get_item_at_click(self, event):
        pos = event.pos()
        item = self.itemAt(pos)
        dataitem = str(item)
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        File = d + "/resource/data/positionData.sqlite3"
        conn = sqlite3.connect(File)
        cu = conn.cursor()
        cu.execute("SELECT * FROM isM")
        results = cu.fetchall()
        conn.commit()
        conn.close()
        resultL = list(results[0])
        result = resultL[1]
        if result == 0:
            conn=sqlite3.connect(File)
            cu=conn.cursor()
            cu.execute("SELECT * FROM test")
            results2 = cu.fetchall()
            itemlen = len(results2)
            conn.commit()
            conn.close()
            flag = False
            for t in results2:
                lt = list(t)
                if lt[-1] == dataitem:
                    flag = True
            if flag is False:
                data1 = (itemlen + 1,'0','0','0','0',dataitem)
                conn=sqlite3.connect(File)
                conn.execute("insert into test values (?,?,?,?,?,?)", data1)
                conn.commit()
                conn.close()
                goal = (dataitem,1)
                conn=sqlite3.connect(File)
                conn.execute("UPDATE goatitem SET item = ? WHERE id = ?", goal)
                conn.commit()
                conn.close()
        else:
            conn=sqlite3.connect(File)
            cu=conn.cursor()
            cu.execute("SELECT * FROM testM")
            results2 = cu.fetchall()
            itemlen = len(results2)
            conn.commit()
            conn.close()
            flag = False
            for t in results2:
                lt = list(t)
                if lt[-1] == dataitem:
                    flag = True
            if flag is False:
                data1 = (itemlen + 1,'0','0','0','0',dataitem)
                conn=sqlite3.connect(File)
                # cu=conn.cursor()
                conn.execute("insert into testM values (?,?,?,?,?,?)", data1)
                conn.commit()
                conn.close()
                goal = (dataitem,1)
                conn=sqlite3.connect(File)
                conn.execute("UPDATE goatitem SET item = ? WHERE id = ?", goal)
                conn.commit()
                conn.close()
        return item
 
 
    def mousePressEvent(self, event):
        super(GraphicView,self).mousePressEvent(event)
        try:
            self.lastPoint = event.pos()
            self.x = self.lastPoint.x()
            self.y = self.lastPoint.y()
            pos = event.pos()
            self.t=self.mapToScene(pos)
            item = self.get_item_at_click(event)
            if event.button() == Qt.RightButton:
                if isinstance(item, QGraphicsItem):
                    self.scene.removeItem(item)
            if event.button() == Qt.LeftButton:
                self.tempPath = QGraphicsPathItem()
                self.tempPath.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable
                                    | QtWidgets.QGraphicsItem.ItemIsMovable
                                    | QtWidgets.QGraphicsItem.ItemIsFocusable
                                    | QtWidgets.QGraphicsItem.ItemSendsGeometryChanges
                                    | QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
                self.path1 = QPainterPath()
                self.path1.moveTo(pos)
                if self.shape == "line":
                    self.a = Arrow(self.scene, self.pen_color, self.pen_width)
                    self.a.set_src(self.x, self.y)
                pp=QPen()
                pp.setColor(self.pen_color)
                pp.setWidth(self.pen_width)
                self.tempPath.setPen(pp)
                if item != None:
                    self.wl=item.boundingRect().width()
                    PaintBoard1().wc(self.wl) 
        except Exception as e:
            print(e)
    def mouseMoveEvent(self,event):
        super(GraphicView, self).mouseMoveEvent(event) 
        self.endPoint = event.pos()
        self.wx = self.endPoint.x()
        self.wy = self.endPoint.y()
        self.w = self.wx-self.x
        self.h = self.wy-self.y
        self.m = self.mapFromScene(event.pos())
        item = self.get_item_at_click(event)
        if event.buttons() & Qt.LeftButton : 
            try:
                if item != None and item.type() != 4:
                    super(GraphicView, self).mouseMoveEvent(event)
                elif self.shape=="circle":
                    self.setCursor(Qt.ArrowCursor)
                    if item == None:
                        pass
                    else:
                        item.setFlag(QGraphicsItem.ItemIsMovable,enabled=False)
                        item.setFlag(QGraphicsItem.ItemIsSelectable,enabled=False)
                    self.path2 = QPainterPath()
                    self.path2.addEllipse(self.t.x(), self.t.y(), self.w, self.h)
                    self.tempPath.setPath(self.path2)
                    self.scene.addItem(self.tempPath)
                elif self.shape=="rect":
                    self.setCursor(Qt.ArrowCursor)
                    if item == None:
                        pass
                    else:
                        item.setFlag(QGraphicsItem.ItemIsSelectable, enabled=False)
                        item.setFlag(QGraphicsItem.ItemIsMovable,enabled=False)
                    self.path3 = QPainterPath()
                    self.path3.addRect(self.x, self.y, self.w, self.h)
                    self.tempPath.setPath(self.path3)
                    self.scene.addItem(self.tempPath)
            except Exception as e:
                print(e)
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        item = self.get_item_at_click(event)
        try:
            if self.shape=="rect":
                if item.isSelected():
                    pass
                else:
                    self.scene.removeItem(self.tempPath)
                    print(self.tempPath.boundingRect())
                    self.r = RectItem(self.pen_color,self.pen_width,self.tempPath.boundingRect())
                    self.scene.addItem(self.r)
            elif self.shape == "circle":
                    self.scene.removeItem(self.tempPath)
                    self.e = EllipseItem(self.pen_color,self.pen_width,self.tempPath.boundingRect())
                    self.scene.addItem(self.e)
        except Exception as e:
            print(e)
    def get_items_at_rubber(self):
        area = self.graphicsView.rubberBandRect()
        return self.graphicsView.items(area)
class PItem(QGraphicsRectItem):
    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8
    handleSize = +10.0
    handleSpace = -4.0
    handleCursors = {
        handleTopLeft: Qt.SizeFDiagCursor,
        handleTopMiddle: Qt.SizeVerCursor,
        handleTopRight: Qt.SizeBDiagCursor,
        handleMiddleLeft: Qt.SizeHorCursor,
        handleMiddleRight: Qt.SizeHorCursor,
        handleBottomLeft: Qt.SizeBDiagCursor,
        handleBottomMiddle: Qt.SizeVerCursor,
        handleBottomRight: Qt.SizeFDiagCursor,
    }
 
    def __init__(self, filename, *args):
        super().__init__(*args)
        self.filename = filename
        self.setZValue(-1)
        self.pix = QPixmap(filename)
        self.g = PaintBoard1()
        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()
    def type(self):
        type = 4
        return type
    def handleAt(self, point):
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None
    def hoverMoveEvent(self, moveEvent):
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)
    def hoverLeaveEvent(self, moveEvent):
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)
    def mousePressEvent(self, mouseEvent):
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)
    def mouseMoveEvent(self, mouseEvent):
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)
    def mouseReleaseEvent(self, mouseEvent):
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()
    def boundingRect(self):
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)
    def updateHandlesPos(self):
        s = self.handleSize
        b = self.boundingRect()
        self.handles[self.handleTopLeft] = QRectF(b.left(), b.top(), s, s)
        self.handles[self.handleTopMiddle] = QRectF(b.center().x() - s / 2, b.top(), s, s)
        self.handles[self.handleTopRight] = QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handleMiddleLeft] = QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handleMiddleRight] = QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handleBottomLeft] = QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handleBottomMiddle] = QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        self.handles[self.handleBottomRight] = QRectF(b.right() - s, b.bottom() - s, s, s)
    def interactiveResize(self, mousePos):
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QPointF(0, 0)
        self.prepareGeometryChange()
        if self.handleSelected == self.handleTopLeft:
            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setTop(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)
        elif self.handleSelected == self.handleTopMiddle:
            fromY = self.mousePressRect.top()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setTop(toY)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)
        elif self.handleSelected == self.handleTopRight:
            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setTop(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)
        elif self.handleSelected == self.handleMiddleLeft:
            fromX = self.mousePressRect.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setLeft(toX)
            rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)
        elif self.handleSelected == self.handleMiddleRight:
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)
        elif self.handleSelected == self.handleBottomLeft:
            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setBottom(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)
        elif self.handleSelected == self.handleBottomMiddle:
            fromY = self.mousePressRect.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setBottom(toY)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)
        elif self.handleSelected == self.handleBottomRight:
            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)
        self.updateHandlesPos()
 
    def shape(self):
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path
    def paint(self, painter, option, widget=None):
        point = QPointF(0, 0)
        self.w = self.rect().width()
        self.h = self.rect().height()
        self.pixfixed = self.pix.scaled(self.w,self.h)
        painter.drawPixmap(point, self.pixfixed, self.rect())
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for shape in self.handles.values():
            if self.isSelected():
                painter.drawEllipse(shape)
    def w_and_h_show(self):
        pass
class RectHandle(QGraphicsRectItem):
    handle_names = ('left_top', 'middle_top', 'right_top', 'right_middle',
                    'right_bottom', 'middle_bottom', 'left_bottom', 'left_middle')
    handle_cursors = {
        0: Qt.SizeFDiagCursor,
        1: Qt.SizeVerCursor,
        2: Qt.SizeBDiagCursor,
        3: Qt.SizeHorCursor,
        4: Qt.SizeFDiagCursor,
        5: Qt.SizeVerCursor,
        6: Qt.SizeBDiagCursor,
        7: Qt.SizeHorCursor
    }
    offset = 6.0
    def update_handles_pos(self):
        o = self.offset
        s = o*2
        b = self.rect()
        x1, y1 = b.left(), b.top()
        offset_x = b.width()/2
        offset_y = b.height()/2
        self.handles[0] = QRectF(x1-o, y1-o, s, s)
        self.handles[1] = self.handles[0].adjusted(offset_x, 0, offset_x, 0)
        self.handles[2] = self.handles[1].adjusted(offset_x, 0, offset_x, 0)
        self.handles[3] = self.handles[2].adjusted(0, offset_y, 0, offset_y)
        self.handles[4] = self.handles[3].adjusted(0, offset_y, 0, offset_y)
        self.handles[5] = self.handles[4].adjusted(-offset_x, 0, -offset_x, 0)
        self.handles[6] = self.handles[5].adjusted(-offset_x, 0, -offset_x, 0)
        self.handles[7] = self.handles[6].adjusted(0, -offset_y, 0, -offset_y)
class RectItem(RectHandle):
    def __init__(self, color,width,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handles = {}
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsItem.ItemIsSelectable |  
                      QGraphicsItem.ItemSendsGeometryChanges | 
                      QGraphicsItem.ItemIsFocusable |  
                      QGraphicsItem.ItemIsMovable)  
        self.update_handles_pos()  
        self.reset_Ui()  
        self.pen_color=color
        self.pen_width=width
    def reset_Ui(self):
        self.handleSelected = None  
        self.mousePressPos = None  
    def boundingRect(self):
        o = self.offset
        return self.rect().adjusted(-o,-o,o,o)
    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(self.pen_color, self.pen_width, Qt.SolidLine))
        painter.drawRect(self.rect())
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 255, 0, 200)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 0,
                                  Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for shape in self.handles.values():
            if self.isSelected():
                painter.drawEllipse(shape)
    def handle_at(self, point):
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return
    def hoverMoveEvent(self, event):
        super().hoverMoveEvent(event)
        handle = self.handle_at(event.pos())
        cursor = self.handle_cursors[handle] if handle in self.handles else Qt.ArrowCursor
        self.setCursor(cursor)
    def hoverLeaveEvent(self, event):
        super().hoverLeaveEvent(event)
        self.setCursor(Qt.ArrowCursor)  # 设定鼠标光标形状
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.handleSelected = self.handle_at(event.pos())
        if self.handleSelected in self.handles:
            self.mousePressPos = event.pos()
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.update()
        self.reset_Ui()
        scenePosstr = str(self.scenePos())
        rectPosstr = str(self.rect())
        sceneposinit = re.findall(r"\d+\.?\d*",scenePosstr)
        if len(sceneposinit) < 2:
            sceneposinit.append('0')
            sceneposinit.append('0')
        scenepos = []
        scenepos.append(float(sceneposinit[1]))
        scenepos.append(float(sceneposinit[2]))
        rect = re.findall(r"\d+\.?\d*",rectPosstr)
        rectpos = []
        for i in range(1,5):
            rectpos.append(float(rect[i]))
        sceneposx = scenepos[0] + rectpos[0]
        sceneposy = scenepos[1] + rectpos[1]
        scenex = str(int(sceneposx * 3 / 2))
        sceney = str(int(sceneposy * 3 / 2))
        w = str(int(rectpos[2] * 3 / 2))
        h = str(int(rectpos[3] * 3 / 2))
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        File = d + "/resource/data/positionData.sqlite3"
        conn=sqlite3.connect(File)
        cu=conn.cursor()
        cu.execute("SELECT * FROM goatitem")
        results2 = cu.fetchall()
        conn.commit()
        conn.close()
        itemlist = list(results2[0])
        itemname = itemlist[1]
        data = (w,h,scenex,sceney,itemname)
        conn = sqlite3.connect(File)
        cu = conn.cursor()
        cu.execute("SELECT * FROM isM")
        isM = cu.fetchall()
        conn.commit()
        conn.close()
        isML = list(isM[0])
        M = isML[1]
        print(M)
        if M == 0:
            conn=sqlite3.connect(File)
            conn.execute("UPDATE test SET w = ? , h = ? , corx = ? , cory = ? WHERE item = ?", data)
            conn.commit()
            conn.close()
            savetemp = d + "/resource/temp/SOI.png"
            picturepath = d + "/resource/temp/First_picture.png"
            image = cv2.imread(picturepath)
            b_mask = np.zeros((1080, 1920, 3), dtype=np.uint8)
            y1 = int(sceney)
            y2 = int(sceney) + int(h)
            x1 = int(scenex)
            x2 = int(scenex) + int(w)
            b_mask[y1:y2, x1:x2] = 255
            rec_mask_img = cv2.bitwise_and(image, b_mask)
            cv2.imwrite(savetemp,rec_mask_img)
        else:
            conn=sqlite3.connect(File)
            conn.execute("UPDATE testM SET w = ? , h = ? , corx = ? , cory = ? WHERE item = ?", data)
            conn.commit()
            conn.close()
            savetemp = d + "/resource/temp/SOIM.png"
            picturepath = d + "/resource/temp/First_picture_1.png"
            image = cv2.imread(picturepath)
            b_mask = np.zeros((1080, 1920, 3), dtype=np.uint8)
            y1 = int(sceney)
            y2 = int(sceney) + int(h)
            x1 = int(scenex)
            x2 = int(scenex) + int(w)
            b_mask[y1:y2, x1:x2] = 255
            rec_mask_img = cv2.bitwise_and(image, b_mask)
            cv2.imwrite(savetemp,rec_mask_img)
    def mouseMoveEvent(self, event):
        if self.handleSelected in self.handles:
            self.interactiveResize(event.pos())
        else:
            super().mouseMoveEvent(event)
    def interactiveResize(self, mousePos):
        rect = self.rect()
        self.prepareGeometryChange()
        if self.handleSelected == 0:
            rect.setTopLeft(mousePos)
        elif self.handleSelected == 1:
            rect.setTop(mousePos.y())
        elif self.handleSelected == 2:
            rect.setTopRight(mousePos)
        elif self.handleSelected == 3:
            rect.setRight(mousePos.x())
        elif self.handleSelected == 4:
            rect.setBottomRight(mousePos)
        elif self.handleSelected == 5:
            rect.setBottom(mousePos.y())
        elif self.handleSelected == 6:
            rect.setBottomLeft(mousePos)
        elif self.handleSelected == 7:
            rect.setLeft(mousePos.x())
        self.setRect(rect)
        self.update_handles_pos()
class MyRect(QGraphicsItem):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable |  
                      QGraphicsItem.ItemSendsGeometryChanges | 
                      QGraphicsItem.ItemIsFocusable) 
        self.rect = QRectF(x, y, width, height)
    def boundingRect(self):
        return self.rect
    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.red, 2))
        painter.drawRect(self.rect)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 255, 0, 200)))
        painter.setPen(QPen(QColor(255, 255, 0, 255), 0,
                                  Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
class HandleMP4(QThread):
    featurePointnumber = pyqtSignal(str)
    avg_uS = pyqtSignal(str)
    avg_vS = pyqtSignal(str)
    time_dataS = pyqtSignal(str)
    frame_numberS = pyqtSignal(str)
    def run(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        datafile = d + "/resource/data/positionData.sqlite3"
        savefileCSV1= d + "/resource/result/Displacement.csv"
        savefileCSV2 = d + "/resource/result/fft.csv"
        conn=sqlite3.connect(datafile)
        cu=conn.cursor()
        cu.execute("SELECT * FROM test")
        results2 = cu.fetchall()
        conn.commit()
        conn.close()
        conn=sqlite3.connect(datafile)
        cu=conn.cursor()
        cu.execute("SELECT * FROM orignalPicture")
        results3 = cu.fetchall()
        conn.commit()
        conn.close()
        conn=sqlite3.connect(datafile)
        cu=conn.cursor()
        cu.execute("SELECT * FROM testM")
        results4 = cu.fetchall()
        conn.commit()
        conn.close()
        for resultItem2 in results4:
            resultItemList2 = list(resultItem2)
            a = int(resultItemList2[1]) * int(resultItemList2[2]) * int(resultItemList2[3]) * int(resultItemList2[4])
            if a != 0:
                x_feature_1 = int(resultItemList2[3])
                y_feature_1 = int(resultItemList2[4])
                width_1 = int(resultItemList2[1])
                height_1 = int(resultItemList2[2])
                w_1 = width_1
                h_1 = height_1
                coordinate_top_left_1 = [x_feature_1,y_feature_1]
        orignalpicturePaths = list(results3[0])
        orignalpicturePath = orignalpicturePaths[1]
        text_cap = cv2.VideoCapture(orignalpicturePath)
        ret, frame = text_cap.read()
        fps = text_cap.get(cv2.CAP_PROP_FPS)
        lst_goal = []
        lst_feature = []
        time_list = []
        avg_u_list = []
        avg_v_list = []
        data_list = []
        frame_number = 1
        for resultItem in results2:
            resultItemList = list(resultItem)
            a = int(resultItemList[1]) * int(resultItemList[2]) * int(resultItemList[3]) * int(resultItemList[4])
            if a != 0:
                x_feature = int(resultItemList[3])
                y_feature = int(resultItemList[4])
                width = int(resultItemList[1])
                height = int(resultItemList[2])
                w = width
                h = height
                coordinate_top_left = [x_feature,y_feature]
        feature = frame[y_feature:y_feature + height, x_feature:x_feature + width]
        feature = cv2.copyMakeBorder(feature, int(width * 0.2), int(width * 0.2), int(width * 0.2), int(width * 0.2),
                                     cv2.BORDER_CONSTANT, value=[0, 0, 0])
        feature = cv2.cvtColor(feature, cv2.COLOR_BGR2GRAY)
        if text_cap.isOpened():
            op, frame = text_cap.read()
        else:
            op = False
        while op:
            ret, frame = text_cap.read()
            if frame is None:
                break
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            b_mask = np.zeros((1080, 1920, 3), dtype=np.uint8)
            y1 = coordinate_top_left_1[1]
            y2 = coordinate_top_left_1[1] + h_1
            x1 = coordinate_top_left_1[0]
            x2 = coordinate_top_left_1[0] + w_1
            b_mask[y1:y2, x1:x2] = 255
            rec_mask_img = cv2.bitwise_and(frame, b_mask)
            n = 0.7
            goal_gray_img = rec_mask_img
            feature_img = feature

            orb = cv2.ORB_create()
            key1, des1 = orb.detectAndCompute(feature_img, None)
            key2, des2 = orb.detectAndCompute(goal_gray_img, None)
            bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
            pairs_of_matches = bf_matcher.knnMatch(des1, des2, k=2)
            matches_knn = [element[0] for element in pairs_of_matches
                           if len(element) > 1 and element[0].distance < n * element[1].distance]
            matches = matches_knn
            key_feature = key1
            key_goal = key2
            img_match = cv2.drawMatches(feature, key_feature, gray_frame, key_goal, matches[:], gray_frame,
                                        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            lst_goal = []
            lst_feature = []
            for i in range(len(matches)):
                x = key_goal[matches[i].trainIdx].pt
                y = key_feature[matches[i].queryIdx].pt
                y = y[0] + x_feature, y[1] + y_feature
                lst_goal.append(x)
                lst_feature.append(y)
            if len(lst_goal) == 0:
                continue
            featurePoint = str(len(matches))
            self.featurePointnumber.emit(featurePoint)
            u, v, m, n = 0, 0, 0, 0
            for j in range(len(lst_goal)):
                u = lst_feature[j][0] - lst_goal[j][0]
                v = lst_feature[j][1] - lst_goal[j][1]
                m = m + u
                n = n + v
            avg_u = round(m / len(lst_goal), 3)
            avg_v = round(n / len(lst_goal), 3)
            stravg_u = str(avg_u)
            stravg_v = str(avg_v)
            self.avg_uS.emit(stravg_u)
            self.avg_vS.emit(stravg_v)
            frame_numberT = str(frame_number)
            self.frame_numberS.emit(frame_numberT)
            time_data = float(frame_number / fps)
            time_dataT = str(time_data)
            self.time_dataS.emit(time_dataT)
            avg_u_list.append(avg_u)
            avg_v_list.append(avg_v)
            time_list.append(time_data)
            data_list.append((frame_number, time_data, round(avg_u - avg_u_list[0], 3),
                              round(avg_v - avg_v_list[0], 3), len(matches)))
            frame_number += 1
        text_cap.release()
        csvfile = open(savefileCSV1, 'w', newline='')
        writer = csv.writer(csvfile)
        writer.writerow(('frame_number', 'Time', 'avg_u', 'avg_v', 'feature_matching'))
        writer.writerows(data_list)
        csvfile.close()
        need_fft_list=avg_u_list[:]
        T=time_list[:]
        fft_result = fft.fft(need_fft_list)
        abs_fft = np.abs(fft_result)
        normalize = abs_fft / len(need_fft_list) * 2 
        amplitude = normalize[0:int(len(need_fft_list) / 2)]
        amplitude[0] = 0
        label_x = np.linspace(0, int(len(need_fft_list) / 2) - 1, int(len(need_fft_list) / 2))
        fs = 1 / (T[2] - T[1])
        frequency = label_x / len(need_fft_list) * fs
        amplitude_u = amplitude
        frequency_u = frequency
        amplitude = list(amplitude_u)
        frequency = list(frequency_u)
        fft_list_u = zip(frequency, amplitude)
        csvfile_u = open(savefileCSV2, 'w', newline='')
        writer = csv.writer(csvfile_u)
        writer.writerow(('frequency', 'amplitude'))
        writer.writerows(fft_list_u)
        csvfile_u.close()
        need_fft_list=avg_v_list[:]
        T=time_list[:]
        fft_result = fft.fft(need_fft_list)
        abs_fft = np.abs(fft_result)
        normalize = abs_fft / len(need_fft_list) * 2
        amplitude = normalize[0:int(len(need_fft_list) / 2)]
        amplitude[0] = 0
        label_x = np.linspace(0, int(len(need_fft_list) / 2) - 1, int(len(need_fft_list) / 2))
        fs = 1 / (T[2] - T[1])
        frequency = label_x / len(need_fft_list) * fs
        amplitude_v = amplitude
        frequency_v = frequency
        amplitude = list(amplitude_v)
        frequency = list(frequency_v)
        fft_list_v = zip(frequency, amplitude)
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        datafile = d + "/resource/data/positionData.sqlite3"
        conn=sqlite3.connect(datafile)
        cu=conn.cursor()
        cu.execute("UPDATE determine SET determine = ? WHERE determine = ?", (1,0))
        conn.commit()
        conn.close()
class SOIpicture(QThread):
    w_num = pyqtSignal(int)
    h_num = pyqtSignal(int)
    coordinate_top_left_list = pyqtSignal(list)
    def run(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        datafile = d + "/resource/data/positionData.sqlite3"
        conn = sqlite3.connect(datafile)
        cu = conn.cursor()
        cu.execute("SELECT * FROM isM")
        results = cu.fetchall()
        conn.commit()
        conn.close()
        isML = list(results[0])
        M = isML[1]
        if M == 0:
            conn=sqlite3.connect(datafile)
            cu=conn.cursor()
            cu.execute("SELECT * FROM test")
            results2 = cu.fetchall()
            conn.commit()
            conn.close()
            for resultItem in results2:
                resultItemList = list(resultItem)
                a = int(resultItemList[1]) * int(resultItemList[2]) * int(resultItemList[3]) * int(resultItemList[4])
                if a != 0:
                    x_feature = int(resultItemList[3])
                    y_feature = int(resultItemList[4])
                    width = int(resultItemList[1])
                    height = int(resultItemList[2])
                    w = width
                    h = height
                    coordinate_top_left = [x_feature,y_feature]
                    savetemp = d + "/resource/temp/SOI.png"
                    picturepath = d + "/resource/temp/First_picture.png"
                    img = cv2.imread(picturepath)
                    y1 = coordinate_top_left[1]
                    y2 = coordinate_top_left[1] + h
                    x1 = coordinate_top_left[0]
                    x2 = coordinate_top_left[0] + w
                    height, width, channels = img.shape
                    y_start, y_end = y1, y2
                    x_start, x_end = x1, x2
                    crop_img = img[y_start:y_end, x_start:x_end]
                    cv2.imwrite(savetemp,crop_img)
                    self.w_num.emit(w)
                    self.h_num.emit(h)
                    self.coordinate_top_left_list.emit(coordinate_top_left)
        else:
            conn=sqlite3.connect(datafile)
            cu=conn.cursor()
            cu.execute("SELECT * FROM testM")
            results2 = cu.fetchall()
            conn.commit()
            conn.close()
            for resultItem in results2:
                resultItemList = list(resultItem)
                a = int(resultItemList[1]) * int(resultItemList[2]) * int(resultItemList[3]) * int(resultItemList[4])
                if a != 0:
                    x_feature = int(resultItemList[3])
                    y_feature = int(resultItemList[4])
                    width = int(resultItemList[1])
                    height = int(resultItemList[2])
                    w = width
                    h = height
                    coordinate_top_left = [x_feature,y_feature]
                    savetemp = d + "/resource/temp/SOIM.png"
                    picturepath = d + "/resource/temp/First_picture_1.png"
                    img = cv2.imread(picturepath)
                    y1 = coordinate_top_left[1]
                    y2 = coordinate_top_left[1] + h
                    x1 = coordinate_top_left[0]
                    x2 = coordinate_top_left[0] + w
                    height, width, channels = img.shape
                    y_start, y_end = y1, y2
                    x_start, x_end = x1, x2
                    crop_img = img[y_start:y_end, x_start:x_end]
                    cv2.imwrite(savetemp,crop_img)
                    self.w_num.emit(w)
                    self.h_num.emit(h)
                    self.coordinate_top_left_list.emit(coordinate_top_left)
class SOIDialog(QDialog,Ui_Dialog):
    def __init__(self):
        super(SOIDialog,self).__init__()
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.initUI)
        self.timer.start(1000)
        self.pushButton.clicked.connect(self.ok)
        self.pushButton_2.clicked.connect(self.cancel)
    def initUI(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        datafile = d + "/resource/data/positionData.sqlite3"
        savetemp = d + "/resource/temp/SOI.png"
        savetempM = d + "/resource/temp/SOIM.png"
        conn = sqlite3.connect(datafile)
        cu = conn.cursor()
        cu.execute("SELECT * FROM isM")
        results3 = cu.fetchall()
        conn.commit()
        conn.close()
        result3 = list(results3[0])
        MN = result3[1]
        if MN == 0:
            pixmap = QPixmap(savetemp)
            self.label.setPixmap(pixmap)
        else:
            pixmap = QPixmap(savetempM)
            self.label.setPixmap(pixmap)
    def ok(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        datafile = d + "/resource/data/positionData.sqlite3"
        picturepath = d + "/resource/temp/First_picture_1.png"
        conn=sqlite3.connect(datafile)
        cu=conn.cursor()
        cu.execute("SELECT * FROM isM")
        results = cu.fetchall()
        conn.commit()
        conn.close()
        result = list(results[0])
        M = result[1]
        if not M:
            conn=sqlite3.connect(datafile)
            cu=conn.cursor()
            cu.execute("UPDATE isM SET isM = ? WHERE id = ?", (1,1))
            conn.commit()
            conn.close()
            conn = sqlite3.connect(datafile)
            cu = conn.cursor()
            cu.execute("UPDATE isClear SET isC = ? WHERE id = ?", (1,1))
            conn.commit()
            conn.close()
            conn = sqlite3.connect(datafile)
            cu = conn.cursor()
            cu.execute("SELECT * FROM test")
            results2 = cu.fetchall()
            conn.commit()
            conn.close()
            for resultItem in results2:
                resultItemList = list(resultItem)
                a = int(resultItemList[1]) * int(resultItemList[2]) * int(resultItemList[3]) * int(resultItemList[4])
                if a != 0:
                    x_feature = int(resultItemList[3])
                    y_feature = int(resultItemList[4])
                    width = int(resultItemList[1])
                    height = int(resultItemList[2])
                    w = width
                    h = height
                    coordinate_top_left = [x_feature,y_feature]
                    savetemp = d + "/resource/temp/First_picture.png"
                    img = cv2.imread(savetemp)
                    y1 = coordinate_top_left[1]
                    y2 = coordinate_top_left[1] + h
                    x1 = coordinate_top_left[0]
                    x2 = coordinate_top_left[0] + w
                    start_point = (x1, y1)
                    end_point = (x2, y2)
                    color = (0, 0, 255) # 红色
                    thickness = 2 # 线宽
                    img_with_rect = cv2.rectangle(img, start_point, end_point, color, thickness)
                    cv2.imwrite(picturepath,img_with_rect)
            self.close()
        if M:
            conn=sqlite3.connect(datafile)
            cu=conn.cursor()
            cu.execute("UPDATE isM SET isM = ? WHERE id = ?", (0,1))
            conn.commit()
            conn.close()
            self.close()
    def cancel(self):
        self.close()
class PaintBoard1(QWidget, Ui_Form):
    def __init__(self):
        super(PaintBoard1, self).__init__()
        self.setupUi(self)
        self.timer = QTimer()
        self.graphics = GraphicView(self)
        self.graphics.setGeometry(QRect(0, 0,1285, 725))
        self.scene = self.graphics.scene
        self.graphics.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.pix = None
        self.pixfixed = None
        self.pw = None
        self.ph = None
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        datafile = d + "/resource/data/positionData.sqlite3"
        iconpath = d + "/resource/data/icon.png"
        icon = QIcon(iconpath)
        self.setWindowIcon(icon)
        self.SOIDialog = SOIDialog()
        bg_brush = QBrush(QLinearGradient(0, 0, 0, self.height()))
        bg_brush.gradient().setColorAt(0, QColor(50, 200, 50))
        bg_brush.gradient().setColorAt(1, QColor(85, 85, 255))
        palette = self.palette()
        palette.setBrush(QPalette.Window, bg_brush)
        self.setPalette(palette)
        self.setWindowOpacity(0.9)
        self.adjustpositionlabel_x = QSpinBox(self)
        self.adjustpositionlabel_x.setSingleStep(1)
        self.adjustpositionlabel_x.resize(60,20)
        self.adjustpositionlabel_x.move(220,750)
        self.adjustpositionlabel_x.setVisible(False)
        self.adjustpositionlabel_x.setMinimum(0)
        self.adjustpositionlabel_x.setMaximum(1920)
        self.adjustpositionlabel_y = QSpinBox(self)
        self.adjustpositionlabel_y.setSingleStep(1)
        self.adjustpositionlabel_y.resize(60,20)
        self.adjustpositionlabel_y.move(290,750)
        self.adjustpositionlabel_y.setVisible(False)
        self.adjustpositionlabel_y.setMinimum(0)
        self.adjustpositionlabel_y.setMaximum(1080)
        self.adjustresizelabel_w = QSpinBox(self)
        self.adjustresizelabel_w.setSingleStep(1)
        self.adjustresizelabel_w.resize(60,20)
        self.adjustresizelabel_w.move(590,750)
        self.adjustresizelabel_w.setVisible(False)
        self.adjustresizelabel_w.setMinimum(0)
        self.adjustresizelabel_h = QSpinBox(self)
        self.adjustresizelabel_h.setSingleStep(1)
        self.adjustresizelabel_h.resize(60,20)
        self.adjustresizelabel_h.move(660,750)
        self.adjustresizelabel_h.setVisible(False)
        self.adjustresizelabel_h.setMinimum(0)
        font = QFont()
        font.setBold(True)
        font.setWeight(50)
        self.progressBar.setFont(font)
        self.pv = 0
        self.timer1 = QBasicTimer()
        self.progressBar.setStyleSheet("QProgressBar { border: 2px solid orange; border-radius: 5px; color: rgb(20,20,20);  background-color: #FFFFFF; text-align: center;}QProgressBar::chunk {background-color: rgb(100,200,200); border-radius: 25px; margin: 0.1px;  width: 1px;}")
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(int(self.pv))
        self.progressBar.setFormat('Loaded %p%'.format(self.progressBar.value()-self.progressBar.minimum()))
        self.pushButton.clicked.connect(self.on_rect_btn_clicked)
        self.pushButton_2.clicked.connect(self.drawRect)
        self.pushButton_4.clicked.connect(self.sceneclear)
        self.pushButton_5.clicked.connect(self.confirmSOI)
        self.handleButton.clicked.connect(self.resultImage)
        self.timer.timeout.connect(self.initUI)
        self.timer.start(1000)
        QTimer.singleShot(500, self.on_btn_Open_Clicked)
        QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Z), self, self.drawback)
    def initUI(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        datafile = d + "/resource/data/positionData.sqlite3"
        conn = sqlite3.connect(datafile)
        cu = conn.cursor()
        cu.execute("SELECT * FROM isM")
        results2 = cu.fetchall()
        conn.commit()
        conn.close()
        result = list(results2[0])
        MN = result[1]
        conn = sqlite3.connect(datafile)
        cu = conn.cursor()
        cu.execute("SELECT * FROM isClear")
        results3 = cu.fetchall()
        conn.commit()
        conn.close()
        result3 = list(results3[0])
        CN = result3[1]
        if MN == 1:
            self.SOIpicture = SOIpicture()
            self.SOIpicture.w_num.connect(self.w_number)
            self.SOIpicture.h_num.connect(self.h_number)
            self.SOIpicture.coordinate_top_left_list.connect(self.coordinate_top_left_show)
            self.SOIpicture.start()
            if CN == 1:
                QTimer.singleShot(500, self.on_btn_Open_Clicked_1)
        else:
            self.SOIpicture = SOIpicture()
            self.SOIpicture.w_num.connect(self.w_number)
            self.SOIpicture.h_num.connect(self.h_number)
            self.SOIpicture.coordinate_top_left_list.connect(self.coordinate_top_left_show)
            self.SOIpicture.start()
    def w_number(self,w_num):
        w = str(w_num)
        self.lineEdit_3.setText(w)
    def h_number(self,h_num):
        h = str(h_num)
        self.lineEdit_4.setText(h)
    def coordinate_top_left_show(self,coordinate_top_left_list):
        x = str(coordinate_top_left_list[0])
        y = str(coordinate_top_left_list[1])
        self.lineEdit.setText(x)
        self.lineEdit_2.setText(y)
    def on_btn_Open_Clicked_1(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        datafile = d + "/resource/data/positionData.sqlite3"
        savefileFirst = d + "/resource/temp/First_picture_1.png"
        self.pix = QPixmap()
        self.pix.load(savefileFirst)
        self.pixfixed = self.pix.scaled(1280, 720,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        item1=PItem(savefileFirst,0,0,1280,720)
        self.scene.addItem(item1)
        item=QGraphicsPixmapItem(self.pixfixed)
        item.setFlag(QGraphicsItem.ItemIsMovable)
        item.setZValue(-1)
        self.pw = self.pixfixed.width()
        self.ph = self.pixfixed.height()
        conn = sqlite3.connect(datafile)
        cu = conn.cursor()
        cu.execute("SELECT * FROM isClear")
        results3 = cu.fetchall()
        conn.commit()
        conn.close()
        result3 = list(results3[0])
        CN = result3[1]
        if CN == 1:
            conn = sqlite3.connect(datafile)
            cu = conn.cursor()
            cu.execute("UPDATE isClear SET isC = ? WHERE id = ?", (0,1))
            conn.commit()
            conn.close()

    def on_btn_Open_Clicked(self):
        # try:
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        datafile = d + "/resource/data/positionData.sqlite3"
        conn=sqlite3.connect(datafile)
        cu=conn.cursor()
        cu.execute("SELECT * FROM dddd")
        results = list(cu.fetchall()[0])
        conn.commit()
        conn.close()
        i = results[0]
        if i == 1:
            a = os.path.abspath('.')
            b = a.split("\\")
            c = tuple(b)
            d = '/'.join(c)
            datafile = d + "/resource/data/positionData.sqlite3"
            savefileFirst = d + "/resource/temp/First_picture.png"
            conn=sqlite3.connect(datafile)
            cu=conn.cursor()
            cu.execute("SELECT * FROM orignalPicture")
            results = cu.fetchall()
            conn.commit()
            conn.close()
            filepath = list(results[0])
            filename = filepath[1]
            text_cap = cv2.VideoCapture(filename)
            fps = text_cap.get(cv2.CAP_PROP_FPS)
            size = (int(text_cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(text_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            ret, frame = text_cap.read()
            cv2.imwrite(savefileFirst,frame)
            self.pix = QPixmap()
            self.pix.load(savefileFirst)
            self.pixfixed = self.pix.scaled(1280, 720,Qt.KeepAspectRatio,Qt.SmoothTransformation)
            item1=PItem(savefileFirst,0,0,1280,720)
            self.scene.addItem(item1)
            item=QGraphicsPixmapItem(self.pixfixed)
            item.setFlag(QGraphicsItem.ItemIsMovable)
            item.setZValue(-1)
            self.pw = self.pixfixed.width()
            self.ph = self.pixfixed.height()
            conn=sqlite3.connect(datafile)
            cu=conn.cursor()
            cu.execute("UPDATE dddd SET id = ? WHERE id = ?", (0,1))
            conn.commit()
            conn.close()
    def confirmSOI(self):
        self.SOIDialog.show()
    def on_rect_btn_clicked(self, *shape):
        items = self.scene.items()
        for i in range(len(items)-1):
            item = items[0]
            self.scene.removeItem(item)
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        datafile = d + "/resource/data/positionData.sqlite3"
        conn = sqlite3.connect(datafile)
        cu = conn.cursor()
        cu.execute("SELECT * FROM isM")
        results2 = cu.fetchall()
        conn.commit()
        conn.close()
        result2 = list(results2[0])
        result = result2[1]
        if result == 0:
            conn=sqlite3.connect(datafile)
            cu=conn.cursor()
            cu.execute("DELETE FROM test;")
            conn.commit()
            conn.close()
        else:
            conn=sqlite3.connect(datafile)
            cu=conn.cursor()
            cu.execute("DELETE FROM testM;")
            conn.commit()
            conn.close()
        shape ="rect"
        self.graphics.Shape(shape)
    def drawback(self,*item):
        try:
            items = self.scene.items()
            item = items[0]
            if len(items) > 1:
                self.scene.removeItem(item)
        except Exception as e:
            reply = QMessageBox.warning(self,u'警告',u'已撤销到最后一步，撤销失败！',QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                pass
    def featureNumberDisplay(self,text):
        self.label_3.setText(text)
    def avg_uDisplay(self,text):
        text1 = text[0:5]
        self.lineEdit_7.setText(text1)
    def avg_vDisplay(self,text):
        text1 = text[0:5]
        self.lineEdit_8.setText(text1)
    def time_dataDisplay(self,text):
        text1 = text[0:5]
        self.lineEdit_6.setText(text1)
    def frame_numberDisplay(self,text):
        self.lineEdit_5.setText(text)
    def timerEvent(self, e):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        datafile = d + "/resource/data/positionData.sqlite3"
        conn=sqlite3.connect(datafile)
        conn=sqlite3.connect(datafile)
        cu=conn.cursor()
        cu.execute("SELECT * FROM orignalPicture")
        results3 = cu.fetchall()
        conn.commit()
        conn.close()
        orignalpicturePaths = list(results3[0])
        orignalpicturePath = orignalpicturePaths[1]
        text_cap = cv2.VideoCapture(orignalpicturePath)
        frame_count = int(text_cap.get(cv2.CAP_PROP_FRAME_COUNT))#总帧数
        text = self.lineEdit_5.text()
        if text:
            finish = int(text)
            self.pv = finish/frame_count*100
            if (frame_count - finish) <= 5:
                self.timer1.stop()
                self.pv = 100
                self.progressBar.setValue(self.pv)
            else:
                self.progressBar.setValue(int(self.pv))
    def resultImage(self):
        self.handlemp4 = HandleMP4()
        coordinate_center = [897,522]
        dataDict = {1:[],2:[],3:[]}
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        datafile = d + "/resource/data/positionData.sqlite3"
        conn=sqlite3.connect(datafile)
        cu=conn.cursor()
        cu.execute("SELECT * FROM test")
        results2 = cu.fetchall()
        conn.commit()
        conn.close()
        conn=sqlite3.connect(datafile)
        cu=conn.cursor()
        cu.execute("SELECT * FROM orignalPicture")
        results3 = cu.fetchall()
        conn.commit()
        conn.close()
        orignalpicturePaths = list(results3[0])
        orignalpicturePath = orignalpicturePaths[1]
        text_cap = cv2.VideoCapture(orignalpicturePath)
        fps = str(int(text_cap.get(cv2.CAP_PROP_FPS)))
        frame_count = int(text_cap.get(cv2.CAP_PROP_FRAME_COUNT))#总帧数
        v = 1/frame_count
        self.timer1.start(int(v),self)
        self.label_6.setText(fps)
        self.handlemp4.featurePointnumber.connect(self.featureNumberDisplay)
        self.handlemp4.avg_uS.connect(self.avg_uDisplay)
        self.handlemp4.avg_vS.connect(self.avg_vDisplay)
        self.handlemp4.time_dataS.connect(self.time_dataDisplay)
        self.handlemp4.frame_numberS.connect(self.frame_numberDisplay)
        self.handlemp4.frame_numberS.connect(self.timerEvent)
        self.handlemp4.start()
    def drawRect(self):
        if self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_3.text() and self.lineEdit_4.text():
            if self.adjustpositionlabel_x.isVisible() == False:
                self.adjustpositionlabel_x.setVisible(True)
                self.adjustpositionlabel_y.setVisible(True)
                self.adjustresizelabel_w.setVisible(True)
                self.adjustresizelabel_h.setVisible(True)
                w_max = 1920 - int(self.lineEdit.text())
                h_max = 1080 - int(self.lineEdit_2.text())
                self.adjustpositionlabel_x.setValue(int(self.lineEdit.text()))
                self.adjustpositionlabel_y.setValue(int(self.lineEdit_2.text()))
                self.adjustresizelabel_w.setValue(int(self.lineEdit_3.text()))
                self.adjustresizelabel_h.setValue(int(self.lineEdit_4.text()))
                self.adjustresizelabel_w.setMaximum(w_max)
                self.adjustresizelabel_h.setMaximum(h_max)
                self.lineEdit.setVisible(False)
                self.lineEdit_2.setVisible(False)
                self.lineEdit_3.setVisible(False)
                self.lineEdit_4.setVisible(False)
            else:
                self.adjustpositionlabel_x.setVisible(False)
                self.adjustpositionlabel_y.setVisible(False)
                self.adjustresizelabel_w.setVisible(False)
                self.adjustresizelabel_h.setVisible(False)
                self.lineEdit.setVisible(True)
                self.lineEdit_2.setVisible(True)
                self.lineEdit_3.setVisible(True)
                self.lineEdit_4.setVisible(True)
                self.lineEdit.setText(self.adjustpositionlabel_x.text())
                self.lineEdit_2.setText(self.adjustpositionlabel_y.text())
                self.lineEdit_3.setText(self.adjustresizelabel_w.text())
                self.lineEdit_4.setText(self.adjustresizelabel_h.text())
                a = os.path.abspath('.')
                b = a.split("\\")
                c = tuple(b)
                d = '/'.join(c)
                datafile = d + "/resource/data/positionData.sqlite3"
                x_pos = eval(self.lineEdit.text())*2/3
                y_pos = eval(self.lineEdit_2.text())*2/3
                w = eval(self.lineEdit_3.text())*2/3
                h = eval(self.lineEdit_4.text())*2/3
                if (x_pos*y_pos*w*h):
                    conn = sqlite3.connect(datafile)
                    cu = conn.cursor()
                    cu.execute("SELECT * FROM isM")
                    isM = cu.fetchall()
                    conn.commit()
                    conn.close()
                    isML = list(isM[0])
                    M = isML[1]
                    if M == 0:
                        conn = sqlite3.connect(datafile)
                        cu = conn.cursor()
                        cu.execute("DELETE FROM test;")
                        conn.commit()
                        conn.close()
                        items = self.scene.items()
                        for i in range(len(items)):
                            item = items[0]
                            self.scene.removeItem(item)
                        rect = MyRect(x_pos, y_pos, w, h)
                        self.scene.addItem(rect)
                        savetemp = d + "/resource/temp/SOI.png"
                        picturepath = d + "/resource/temp/First_picture.png"
                        image = cv2.imread(picturepath)
                        b_mask = np.zeros((1080, 1920, 3), dtype=np.uint8)  # △ mask need 3D
                        y1 = int(y_pos*3/2)
                        y2 = int(y_pos*3/2) + int(h*3/2)
                        x1 = int(x_pos*3/2)
                        x2 = int(x_pos*3/2) + int(w*3/2)
                        b_mask[y1:y2, x1:x2] = 255
                        rec_mask_img = cv2.bitwise_and(image, b_mask)  # The mask is superimposed on the original image
                        cv2.imwrite(savetemp,rec_mask_img)
                        conn=sqlite3.connect(datafile)
                        cu=conn.cursor()
                        cu.execute("SELECT * FROM test")
                        results2 = cu.fetchall()
                        itemlen = len(results2)
                        conn.commit()
                        conn.close()
                        data1 = (itemlen + 1,int(w*3/2),int(h*3/2),x1,y1,'MyRect')
                        conn=sqlite3.connect(datafile)
                        conn.execute("insert into test values (?,?,?,?,?,?)", data1)
                        conn.commit()
                        conn.close()
                    else:
                        conn = sqlite3.connect(datafile)
                        cu = conn.cursor()
                        cu.execute("DELETE FROM testM;")
                        conn.commit()
                        conn.close()
                        items = self.scene.items()
                        for i in range(len(items)):
                            item = items[0]
                            self.scene.removeItem(item)
                        rect = MyRect(x_pos, y_pos, w, h)
                        self.scene.addItem(rect)
                        savetemp = d + "/resource/temp/SOI.png"
                        picturepath = d + "/resource/temp/First_picture.png"
                        image = cv2.imread(picturepath)
                        b_mask = np.zeros((1080, 1920, 3), dtype=np.uint8)  # △ mask need 3D
                        y1 = int(y_pos*3/2)
                        y2 = int(y_pos*3/2) + int(h*3/2)
                        x1 = int(x_pos*3/2)
                        x2 = int(x_pos*3/2) + int(w*3/2)
                        b_mask[y1:y2, x1:x2] = 255
                        rec_mask_img = cv2.bitwise_and(image, b_mask)  # The mask is superimposed on the original image
                        cv2.imwrite(savetemp,rec_mask_img)
                        conn=sqlite3.connect(datafile)
                        cu=conn.cursor()
                        cu.execute("SELECT * FROM testM")
                        results2 = cu.fetchall()
                        itemlen = len(results2)
                        conn.commit()
                        conn.close()
                        data1 = (itemlen + 1,int(w*3/2),int(h*3/2),x1,y1,'MyRect')
                        conn=sqlite3.connect(datafile)
                        conn.execute("insert into testM values (?,?,?,?,?,?)", data1)
                        conn.commit()
                        conn.close()

                    x_pos = int(int(self.lineEdit.text())*2/3) - self.adjustresizelabel_offset_x.value() + 6
                    y_pos = int(int(self.lineEdit_2.text())*2/3) - self.adjustresizelabel_offset_y.value() + 6
                    w = int(int(self.lineEdit_3.text())*2/3) + self.adjustresizelabel_offset_x.value()*2 - 6
                    h = int(int(self.lineEdit_4.text())*2/3) + self.adjustresizelabel_offset_y.value()*2 - 6
                    rect = MyRect(x_pos, y_pos, w, h)
                    self.scene.addItem(rect)
    def sceneclear(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        if a:
            datafile = d + "/resource/data/positionData.sqlite3"
            conn = sqlite3.connect(datafile)
            cu = conn.cursor()
            cu.execute("DELETE FROM test;")
            conn.commit()
            conn.close()
            items = self.scene.items()
            for i in range(len(items)-1):
                item = items[0]
                self.scene.removeItem(item)
            reply = QMessageBox.information(self,u'提示',u'已全部清空！',QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                pass
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_E:
            self.sceneclear()
        elif event.key() == Qt.Key_R:
            self.on_rect_btn_clicked()
        elif event.key() == Qt.Key_C:
            self.on_circle_btn_clicked()
        elif event.key() == Qt.Key_B:
            self.drawback()
        elif event.key() == Qt.Key_P:
            self.drawRect()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PaintBoard1()
    win.show()
    sys.exit(app.exec())