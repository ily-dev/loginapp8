
##################################
# CODE:       I.Cxxxx           #
# PROJECT:    Messungen          #
# PURPOSE:    WINDOWS/LINUX      #
# MACOS FLAT MODERN UI           #
# BASED ON QT DESIGNER, PySide6    #
# USE CASE:   TEMPLATE FOR       #
# SOFTWARES                      #
# LICENCE:    MIT OPENSOURCE     #
##################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QTimer, QUrl, Qt, QLineF)
from PySide6.QtGui import (QBrush, QColor, QPen, QConicalGradient, QCursor, QFont, QMouseEvent,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,QMovie,
    QPixmap, QRadialGradient)
from PySide6.QtWidgets import *
from PySide6 import QtCore

from ui_dialog import Ui_Dialog

import Style as s
import pyqtgraph as pg
import numpy as np
#from pyqtgraph import *

#import panel as gp
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backend_tools import ToolBase, RubberbandBase

from class100 import *

import definition as Def
import snap7
import time
import sys


_enable = False
_debug = False
_matplot = False


plt.rcParams['toolbar'] = 'toolmanager'

#--------------------------------------------------------------------------
# Class MainWindow
#--------------------------------------------------------------------------

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        global _enable

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        #MainWindow.resize(1100, 550)
        #MainWindow.setMinimumSize(QSize(1000, 690))

        if sys.platform =='linux1':
            self.height = 1918 
            self.width = 1080 
        else:
            self.height = 500
            self.width = 960
            MainWindow.setMinimumSize(QSize(self.width, self.height))
            MainWindow.resize(self.width, self.height)
        
        self.linux = self.height
        self.linux1_5 = int(self.height/1.5)
        self.linux2 = int(self.height/2)
        self.linux3 = int(self.height/3)
        self.linux4 = int(self.height/4)
        self.linux5 = int(self.height/5)
        self.linux6 = int(self.height/6)
        self.linux7 = int(self.height/7)
        self.linux8 = int(self.height/8)
        self.linux9= int(self.height/9)
        self.linux10 = int(self.height/10)
        self.linux12 = int(self.height/12)
        self.linux14 = int(self.height/14)
        self.linux16 = int(self.height/16)
        self.linux18 = int(self.height/18)
        self.linux20 = int(self.height/20)
        
        self.linux22 = int(self.height/22)
        self.linux32 = int(self.height/32)
        self.linux40 = int(self.height/40)
        
        self.linuxW2 = int(self.width/2)
        self.linuxW3 = int(self.width/3)
        self.linuxW4 = int(self.width/4)
        self.linuxW5 = int(self.width/5)
        self.linuxW6 = int(self.width/6)
        self.linuxW7 = int(self.width/7)
        self.linuxW8 = int(self.width/8)
        self.linuxW9 = int(self.width/9)
        self.linuxW10 = int(self.width/10)
        self.linuxW16 = int(self.width/16)

        #variable Snap 7 Kommunikation
        self.plc           = None               #PLC Verbindung aufgebaut dann ID Nummer sonst None
        self.plc_connected = False              #plc verbunden
        self.plc_running_f = True               #einmal ausfuehren - am Anfang bis Progressbar wieder neu anfaengt
        self.plc_stop_f = True                  #einmal ausfuehren - Meldung Errormeldung wenn Aufzeichnung
        self.plc_running   = False              #plc running (CPU laueft)
        self.abbruch = False                    #Abbruch Aufzeichnung ohne Dialog "Warte Aufzeichnung"
        self.meldung_sek = 0                    #Meldung nach x sekunden Anzeigen
        #self.plc_state = 0                      #Zustand CPU S7
        self.plc_text = 'Aus'                   #Text Zustandmaschine        

        self.animation = None                   #Animation Frame Top

        self.stop = False                       #Daten wurde im Zyklusabtastung gelesen (PLC)
        self.liste_time = []

      
# -------------------------------------------------------------------------
# Hauptfenster erstellen
# -------------------------------------------------------------------------

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background:rgb(51,51,51);")

        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0,0,0,0)
        
        self.frame_top = QFrame(self.centralwidget)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(16777215, self.linux16))
        self.frame_top.setFrameShape(QFrame.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Plain)


#--------------------------------------------------------------------------
# Central Menu Buttons - StackWidget
#--------------------------------------------------------------------------

        self.horizontalLayout = QHBoxLayout(self.frame_top)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.frame_menu = QFrame(self.frame_top)
        self.frame_menu.setObjectName(u"frame_frame_menu")
        self.frame_menu.setMinimumSize(QSize(self.linux16, self.linux16)) 
        
        self.frame_menu.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_menu.setFrameShape(QFrame.NoFrame)
        self.frame_menu.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_3 = QHBoxLayout(self.frame_menu)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

#--------------------------------------------------------------------------
# bn_menu Button & Frame
#--------------------------------------------------------------------------

        self.bn_menu = QPushButton(self.frame_menu)
        self.bn_menu.setObjectName(u"bn_menu")
        self.bn_menu.setMinimumSize(QSize(self.linux16, self.linux16)) 
        
        self.bn_menu.setStyleSheet(s.StyleButton)

        icon = QIcon()
        icon.addFile(u"icons/1x/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_menu.setIcon(icon)
        #self.bn_menu.setIconSize(QSize(66, 66))
        self.bn_menu.setFlat(True)
        self.bn_menu.setCheckable(True)
        self.bn_menu.setChecked(False)

        self.horizontalLayout_3.addWidget(self.bn_menu)
        self.horizontalLayout.addWidget(self.frame_menu)

        self.frame_top_east = QFrame(self.frame_top)
        self.frame_top_east.setObjectName(u"frame_top_east")
        self.frame_top_east.setMinimumSize(QSize(0, 0))
        self.frame_top_east.setMaximumSize(QSize(16777215, self.linux16))
        self.frame_top_east.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_top_east.setFrameShape(QFrame.NoFrame)
        self.frame_top_east.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_4 = QHBoxLayout(self.frame_top_east)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)

        self.frame_appname = QFrame(self.frame_top_east)
        self.frame_appname.setObjectName(u"frame_appname")
        self.frame_appname.setFrameShape(QFrame.NoFrame)
        self.frame_appname.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_10 = QHBoxLayout(self.frame_appname)
        self.horizontalLayout_10.setSpacing(7)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)

        self.lab_appname = QLabel(self.frame_appname)
        self.lab_appname.setObjectName(u"lab_appname")
        self.lab_appname.setFont(s.font)
        self.lab_appname.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_appname.setMinimumWidth(self.linuxW16)
        self.lab_appname.setMaximumWidth(self.linuxW16)
        
        self.horizontalLayout_10.addWidget(self.lab_appname)
        self.horizontalLayout_4.addWidget(self.frame_appname)

#--------------------------------------------------------------------------
# Button amcik- verschwinden
#--------------------------------------------------------------------------
        
        self.frame_amcik= QFrame(self.frame_top_east)
        self.frame_amcik.setObjectName(u"frame_amcik")
        self.frame_amcik.setMaximumSize(QSize(self.linux16, self.linux16))
        self.frame_amcik.setFrameShape(QFrame.NoFrame)
        self.frame_amcik.setFrameShadow(QFrame.Plain)

        self.hor_frame_amcik= QHBoxLayout(self.frame_amcik)
        self.hor_frame_amcik.setSpacing(0)
        self.hor_frame_amcik.setObjectName(u"hor_frame_amcik")
        self.hor_frame_amcik.setContentsMargins(0, 0, 0, 0)

        self.bn_amcik = QPushButton()
        self.bn_amcik.setObjectName(u"bn_amcik")
        self.bn_amcik.setMaximumSize(QSize(self.linux16, self.linux16))
        self.bn_amcik.setStyleSheet(s.StyleButton)

        icon77 = QIcon()
        icon77.addFile(u"icons/1x/cil_matplot.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_amcik.setIcon(icon77)
        self.bn_amcik.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_amcik.setFlat(True)
        self.bn_amcik.setCheckable(True)
       
        self.hor_frame_amcik.addWidget(self.bn_amcik)
        
#--------------------------------------------------------------------------
# Button yarak- verschwinden
#--------------------------------------------------------------------------
        
        self.frame_yarak= QFrame(self.frame_top_east)
        self.frame_yarak.setObjectName(u"frame_yarak")
        self.frame_yarak.setMaximumSize(QSize(self.linux16, self.linux16))
        self.frame_yarak.setFrameShape(QFrame.NoFrame)
        self.frame_yarak.setFrameShadow(QFrame.Plain)

        self.hor_frame_yarak= QHBoxLayout(self.frame_yarak)
        self.hor_frame_yarak.setSpacing(0)
        self.hor_frame_yarak.setObjectName(u"hor_frame_yarak")
        self.hor_frame_yarak.setContentsMargins(0, 0, 0, 0)

        self.bn_yarak = QPushButton()
        self.bn_yarak.setObjectName(u"bn_yarak")
        self.bn_yarak.setMaximumSize(QSize(self.linux16, self.linux16))
        self.bn_yarak.setStyleSheet(s.StyleButton)

        icon1 = QIcon()
        icon1.addFile(u"icons/1x/gameAsset 61.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_yarak.setIcon(icon1)
        #self.bn_yarak.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_yarak.setFlat(True)
        self.bn_yarak.setCheckable(True)
       
        self.hor_frame_yarak.addWidget(self.bn_yarak)
       
#--------------------------------------------------------------------------
# Button oma - verschwinden
#--------------------------------------------------------------------------
         
        self.frame_oma = QFrame(self.frame_top_east)
        self.frame_oma.setObjectName(u"frame_oma")
        self.frame_oma.setMaximumSize(QSize(self.linux16, self.linux16))
        self.frame_oma.setFrameShape(QFrame.NoFrame)
        self.frame_oma.setFrameShadow(QFrame.Plain)

        self.hor_frame_oma= QHBoxLayout(self.frame_oma)
        self.hor_frame_oma.setSpacing(0)
        self.hor_frame_oma.setObjectName(u"hor_frame_oma")
        self.hor_frame_oma.setContentsMargins(0, 0, 0, 0)

        self.bn_oma = QPushButton()
        self.bn_oma.setObjectName(u"bn_oma")
        self.bn_oma.setMaximumSize(QSize(self.linux16, self.linux16))
        self.bn_oma.setStyleSheet(s.StyleButton)

        icon1 = QIcon()
        icon1.addFile(u"icons/1x/cleanAsset 59.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_oma.setIcon(icon1)
        #self.bn_oma.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_oma.setFlat(True)
        self.bn_oma.setCheckable(True)
       
        self.hor_frame_oma.addWidget(self.bn_oma)

#--------------------------------------------------------------------------
# Button Meldung - verschwinden
#--------------------------------------------------------------------------
        
        self.frame_opa = QFrame(self.frame_top_east)
        self.frame_opa.setObjectName(u"frame_opa")
        self.frame_opa.setMaximumSize(QSize(self.linux16, self.linux16))
        self.frame_opa.setFrameShape(QFrame.NoFrame)
        self.frame_opa.setFrameShadow(QFrame.Plain)

        self.hor_frame_opa= QHBoxLayout(self.frame_opa)
        self.hor_frame_opa.setSpacing(0)
        self.hor_frame_opa.setObjectName(u"hor_frame_opa")
        self.hor_frame_opa.setContentsMargins(0, 0, 0, 0)

        self.bn_opa = QPushButton()
        self.bn_opa.setObjectName(u"bn_opa")
        self.bn_opa.setMaximumSize(QSize(self.linux16, self.linux16))
        self.bn_opa.setStyleSheet(s.StyleButton)

        icon1 = QIcon()
        icon1.addFile(u"icons/1x/smile2Asset 1.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_opa.setIcon(icon1)
        #self.bn_opa.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_opa.setFlat(True)
        self.bn_opa.setCheckable(True)
       
        self.hor_frame_opa.addWidget(self.bn_opa)


#--------------------------------------------------------------------------
# Button person
#--------------------------------------------------------------------------

        self.frame_person = QFrame(self.frame_top_east)
        self.frame_person.setObjectName(u"frame_person")
        
        self.frame_person.setMaximumSize(QSize(self.linux16, self.linux16))
        self.frame_person.setFrameShape(QFrame.NoFrame)
        self.frame_person.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_8 = QHBoxLayout(self.frame_person)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)

        self.bn_lab_person = QPushButton(self.frame_person)
        self.bn_lab_person.setObjectName(u"bn_lab_person")
        self.bn_lab_person.setMaximumSize(QSize(self.linux16, self.linux16))
        self.bn_lab_person.setStyleSheet(s.StyleButton)
        self.bn_lab_person.setIcon(QIcon(u"icons/1x/peple.ico"))
        
        self.bn_lab_person.setFlat(True)
        self.bn_lab_person.setCheckable(True)
       
        self.bn_lab_person.setText("IC")
        self.horizontalLayout_8.addWidget(self.bn_lab_person)
      

        self.frame_min = QFrame(self.frame_top_east)
        self.frame_min.setObjectName(u"frame_min")
        self.frame_min.setMinimumSize(QSize(self.linux16, self.linux16))
        self.frame_min.setMaximumSize(QSize(self.linux16, self.linux16))
        self.frame_min.setFrameShape(QFrame.NoFrame)
        self.frame_min.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_7 = QHBoxLayout(self.frame_min)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)

#--------------------------------------------------------------------------
# Minimieren Button
#--------------------------------------------------------------------------

        self.bn_min = QPushButton(self.frame_min)
        self.bn_min.setObjectName(u"bn_min")
        self.bn_min.setMaximumSize(QSize(self.linux16, self.linux16))
        self.bn_min.setStyleSheet(s.StyleButton)

        icon1 = QIcon()
        icon1.addFile(u"icons/1x/hideAsset 53.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_min.setIcon(icon1)
        #self.bn_min.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_min.setFlat(True)

        self.horizontalLayout_7.addWidget(self.bn_min)
        
        self.frame_max = QFrame(self.frame_top_east)
        self.frame_max.setObjectName(u"frame_max")
        self.frame_max.setMinimumSize(QSize(self.linux16, self.linux16))
        self.frame_max.setMaximumSize(QSize(self.linux16, self.linux16))
        self.frame_max.setFrameShape(QFrame.NoFrame)
        self.frame_max.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_6 = QHBoxLayout(self.frame_max)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)

#--------------------------------------------------------------------------
# Maximieren Button
#--------------------------------------------------------------------------

        self.bn_max = QPushButton(self.frame_max)
        self.bn_max.setObjectName(u"bn_max")
        self.bn_max.setMaximumSize(QSize(self.linux16, self.linux16))
        self.bn_max.setStyleSheet(s.StyleButton)

        icon2 = QIcon()
        icon2.addFile(u"icons/1x/max.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_max.setIcon(icon2)
        #self.bn_max.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_max.setFlat(True)

        self.horizontalLayout_6.addWidget(self.bn_max)
    
# -------------------------------------------------------------------------

        self.frame_close = QFrame(self.frame_top_east)
        self.frame_close.setObjectName(u"frame_close")
        self.frame_close.setMinimumSize(QSize(self.linux16, self.linux16))
        self.frame_close.setMaximumSize(QSize(self.linux16, self.linux16))
        self.frame_close.setFrameShape(QFrame.NoFrame)
        self.frame_close.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_5 = QHBoxLayout(self.frame_close)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)

#--------------------------------------------------------------------------
# Close Button
#--------------------------------------------------------------------------

        self.bn_close = QPushButton(self.frame_close)
        self.bn_close.setObjectName(u"bn_close")
        self.bn_close.setMaximumSize(QSize(self.linux16, self.linux16))
        self.bn_close.setStyleSheet(s.StyleButton)

        icon3 = QIcon()
        icon3.addFile(u"icons/1x/closeAsset 43.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_close.setIcon(icon3)
        #self.bn_close.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_close.setFlat(True)

        self.horizontalLayout_5.addWidget(self.bn_close)
      

# -------------------------------------------------------------------------

        self.horizontalLayout.addWidget(self.frame_top_east)
 
# -------------------------------------------------------------------------

        self.verticalLayout.addWidget(self.frame_top)

        self.frame_bottom = QFrame(self.centralwidget)
        self.frame_bottom.setObjectName(u"frame_bottom")
        self.frame_bottom.setStyleSheet(u"background:rgb(51,51,51);")     #51,51,51
        self.frame_bottom.setFrameShape(QFrame.NoFrame)
        self.frame_bottom.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_2 = QHBoxLayout(self.frame_bottom)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.frame_bottom_west = QFrame(self.frame_bottom)
        self.frame_bottom_west.setObjectName(u"frame_bottom_west")
        #self.frame_bottom_west.setMinimumSize(QSize(0, 0))
        self.frame_bottom_west.setMaximumSize(QSize(self.linux8, 16777215))
        self.frame_bottom_west.setStyleSheet(u"background:rgb(51,51,51);")     #51,51,51
        self.frame_bottom_west.setFrameShape(QFrame.NoFrame)
        self.frame_bottom_west.setFrameShadow(QFrame.Plain)

        self.verticalLayout_3 = QVBoxLayout(self.frame_bottom_west)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)

#--------------------------------------------------------------------------
# Home Button & Frame
#--------------------------------------------------------------------------

        self.frame_home = QFrame(self.frame_bottom_west)
        self.frame_home.setObjectName(u"frame_home")
        self.frame_home.setMinimumSize(QSize(self.linux8, self.linux16))
        self.frame_home.setMaximumSize(QSize(160, self.linux16))
        self.frame_home.setFrameShape(QFrame.NoFrame)
        self.frame_home.setFrameShadow(QFrame.Plain)
       

        self.bn_home = QPushButton(self.frame_home)  
        self.bn_home.setObjectName(u"bn_home")
        self.bn_home.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_home.setMaximumSize(QSize(160, self.linux16))
        self.bn_home.setStyleSheet(s.StyleButton_1)


        icon4 = QIcon()
        icon4.addFile(u"icons/1x/homeAsset 46.ico",QSize(), QIcon.Normal, QIcon.Off)
        self.bn_home.setIcon(icon4)
        self.bn_home.setIconSize(QSize(self.linux22, self.linux22))
   
#-------------------------------------------------------------------------
# Bug Button & Frame
#-------------------------------------------------------------------------

        self.frame_daten = QFrame(self.frame_bottom_west)
        self.frame_daten.setObjectName(u"frame_daten")
        self.frame_daten.setMinimumSize(QSize(self.linux8, self.linux16))
        self.frame_daten.setMaximumSize(QSize(160, self.linux16))
        self.frame_daten.setFrameShape(QFrame.NoFrame)
        self.frame_daten.setFrameShadow(QFrame.Plain)

        self.bn_daten = QPushButton(self.frame_daten)            
        self.bn_daten.setObjectName(u"bn_daten")
        self.bn_daten.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_daten.setMaximumSize(QSize(160, self.linux16))
        self.bn_daten.setStyleSheet(s.StyleButton_1)

        icon5 = QIcon()
        icon5.addFile(u"icons/1x/bugAsset 47.ico",QSize(), QIcon.Normal, QIcon.Off)
        self.bn_daten.setIcon(icon5)
        self.bn_daten.setIconSize(QSize(self.linux22, self.linux22))
        
#--------------------------------------------------------------------------
# Graph Live Button & Frame
#--------------------------------------------------------------------------

        self.frame_live = QFrame(self.frame_bottom_west)
        self.frame_live.setObjectName(u"frame_live")
        self.frame_live.setMinimumSize(QSize(self.linux8, self.linux16))
        self.frame_live.setMaximumSize(QSize(160, self.linux16))
        self.frame_live.setFrameShape(QFrame.NoFrame)
        self.frame_live.setFrameShadow(QFrame.Plain)

        self.bn_live = QPushButton(self.frame_live)
        self.bn_live.setObjectName(u"bn_live")
        self.bn_live.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_live.setMaximumSize(QSize(160, self.linux16))
        self.bn_live.setStyleSheet(s.StyleButton_1)


        icon6 = QIcon()
        icon6.addFile(u"icons/1x/cil_matplot.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_live.setIcon(icon6)
        self.bn_live.setIconSize(QSize(self.linux22, self.linux22))
        self.bn_live.setFlat(True)

#--------------------------------------------------------------------------
# Zoom Button & Frame
#--------------------------------------------------------------------------

        self.frame_gpanel = QFrame(self.frame_bottom_west)
        self.frame_gpanel.setObjectName(u"frame_gpanel")
        self.frame_gpanel.setMinimumSize(QSize(self.linux8, self.linux16))
        self.frame_gpanel.setMaximumSize(QSize(160, self.linux16))
        self.frame_gpanel.setFrameShape(QFrame.NoFrame)
        self.frame_gpanel.setFrameShadow(QFrame.Plain)

        self.bn_gpanel = QPushButton(self.frame_gpanel)
        self.bn_gpanel.setObjectName(u"bn_gpanel")
        self.bn_gpanel.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_gpanel.setMaximumSize(QSize(160, self.linux16))
        self.bn_gpanel.setStyleSheet(s.StyleButton_1)


        icon12 = QIcon()
        icon12.addFile(u"icons/1x/cil_plotview.ico", QSize(), QIcon.Normal, QIcon.Off)   #androidAsset 49.ico
        self.bn_gpanel.setIcon(icon12)
        self.bn_gpanel.setIconSize(QSize(self.linux22, self.linux22))
        self.bn_gpanel.setFlat(True)

#--------------------------------------------------------------------------
# Setting Button & Frame
#--------------------------------------------------------------------------

        self.frame_setting = QFrame(self.frame_bottom_west)
        self.frame_setting.setObjectName(u"frame_setting")
        self.frame_setting.setMinimumSize(QSize(self.linux8, self.linux16))
        self.frame_setting.setMaximumSize(QSize(160, self.linux16))
        self.frame_setting.setFrameShape(QFrame.NoFrame)
        self.frame_setting.setFrameShadow(QFrame.Plain)

        self.bn_setting = QPushButton(self.frame_setting)
        self.bn_setting.setObjectName(u"bn_setting")
        self.bn_setting.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_setting.setMaximumSize(QSize(160, self.linux16))
        self.bn_setting.setStyleSheet(s.StyleButton_1)


        icon13 = QIcon()
        icon13.addFile(u"icons/1x/cil-settings.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_setting.setIcon(icon13)
        self.bn_setting.setIconSize(QSize(self.linux22, self.linux22))
        self.bn_setting.setFlat(True)

#--------------------------------------------------------------------------
# graph Button & Frame
#--------------------------------------------------------------------------

        self.frame_graph = QFrame(self.frame_bottom_west)
        self.frame_graph.setObjectName(u"frame_graph")
        self.frame_graph.setMinimumSize(QSize(self.linux8, self.linux16))
        self.frame_graph.setMaximumSize(QSize(160, self.linux16))
        self.frame_graph.setFrameShape(QFrame.NoFrame)
        self.frame_graph.setFrameShadow(QFrame.Plain)

        self.bn_graph = QPushButton(self.frame_graph)
        self.bn_graph.setObjectName(u"bn_graph")
        self.bn_graph.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_graph.setMaximumSize(QSize(160, self.linux16))
        self.bn_graph.setStyleSheet(s.StyleButton_1)


        icon14 = QIcon()
        icon14.addFile(u"icons/1x/cil_plots_graph.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_graph.setIcon(icon14)
        self.bn_graph.setIconSize(QSize(self.linux22, self.linux22))
        self.bn_graph.setFlat(True)

#--------------------------------------------------------------------------
# Power Button & Frame
#--------------------------------------------------------------------------

        self.frame_power = QFrame(self.frame_bottom_west)
        self.frame_power.setObjectName(u"frame_power")
        self.frame_power.setMinimumSize(QSize(self.linux8, self.linux16))
        self.frame_power.setMaximumSize(QSize(160, self.linux16))
        self.frame_power.setFrameShape(QFrame.NoFrame)
        self.frame_power.setFrameShadow(QFrame.Plain)

        self.bn_power = QPushButton(self.frame_power)
        self.bn_power.setObjectName(u"bn_power")
        self.bn_power.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_power.setMaximumSize(QSize(160, self.linux16))
        self.bn_power.setStyleSheet(s.StyleButton_1)
        self.bn_power.setCheckable(False)               
        self.bn_power.setEnabled(True)

        icon15 = QIcon()
        icon15.addFile(u"icons/1x/cil-power-standby.ico", QSize(), QIcon.Disabled)
        icon15.addFile(u"icons/1x/cil-power-standby_2.ico", QSize(), QIcon.Normal, QIcon.On)
        icon15.addFile(u"icons/1x/cil-power-standby_1.ico", QSize(), QIcon.Normal, QIcon.Off)

        self.bn_power.setIcon(icon15)
        self.bn_power.setIconSize(QSize(self.linux22, self.linux22))
        self.bn_power.setFlat(True)

#--------------------------------------------------------------------------
# Stop/Start Aufzeichnung Button & Frame
#--------------------------------------------------------------------------

        self.frame_auf_on = QFrame(self.frame_top_east)    
        self.frame_auf_on.setObjectName(u"frame_auf_on")
        #self.frame_auf_on.setMinimumSize(QSize(self.linux16, self.linux16))

        self.frame_auf_on.setFrameShape(QFrame.NoFrame)
        self.frame_auf_on.setFrameShadow(QFrame.Plain)

        self.bn_auf = QPushButton(self.frame_auf_on)
        self.bn_auf.setObjectName(u"bn_auf")
        self.bn_auf.setMaximumSize(QSize(self.linux22, self.linux22))
        
        self.bn_auf.setStyleSheet(s.StyleButton_rot)
        

        #self.bn_auf.setIcon(icon0)
        self.bn_auf.setIconSize(QSize(self.linux22, self.linux22))
        self.bn_auf.setCheckable(False)               
        self.bn_auf.setEnabled(False)
        self.bn_auf.setDisabled(True)

        #auf (Aufzeichnung beenden)
        self.h_frame_auf = QHBoxLayout(self.frame_auf_on)
        self.h_frame_auf.setSpacing(3)
        self.h_frame_auf.setObjectName(u"h_frame_auf")
        self.h_frame_auf.setContentsMargins(0, 0, 0, 0)
        self.h_frame_auf.addWidget(self.bn_auf)
        
        self.hor_spacer_appname = QSpacerItem(40, 20, QSizePolicy.Expanding , QSizePolicy.Minimum)  
        
        self.horizontalLayout_4.addItem(self.hor_spacer_appname)  
          
        self.horizontalLayout_4.addWidget(self.frame_auf_on)


        self.hor_spacer_slid = QSpacerItem(40, 20, QSizePolicy.Expanding , QSizePolicy.Minimum)  
        self.horizontalLayout_4.addItem(self.hor_spacer_slid)
        
        self.horizontalLayout_4.addWidget(self.frame_amcik)  
        self.horizontalLayout_4.addWidget(self.frame_yarak)
        self.horizontalLayout_4.addWidget(self.frame_oma)
        self.horizontalLayout_4.addWidget(self.frame_opa)
        self.horizontalLayout_4.addWidget(self.frame_person)
        self.horizontalLayout_4.addWidget(self.frame_min)
        self.horizontalLayout_4.addWidget(self.frame_max)
        self.horizontalLayout_4.addWidget(self.frame_close)
        
        #self.hor_spacer_buttons = QSpacerItem(40, 20, QSizePolicy.Expanding , QSizePolicy.Minimum)  
        #self.hor_frame_buttons.addItem(self.hor_spacer_buttons)  

#--------------------------------------------------------------------------
# Exit/Zurueck  Button & Frame
#--------------------------------------------------------------------------

        self.frame_back = QFrame(self.frame_bottom_west)
        self.frame_back.setObjectName(u"frame_back")
        self.frame_back.setMinimumSize(QSize(self.linux8, self.linux16))
        self.frame_back.setMaximumSize(QSize(160, self.linux16))
        self.frame_back.setFrameShape(QFrame.NoFrame)
        self.frame_back.setFrameShadow(QFrame.Plain)


        self.bn_exit = QPushButton(self.frame_back)
        self.bn_exit.setObjectName(u"bn_exit")
        self.bn_exit.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_exit.setMaximumSize(QSize(160, self.linux16))
        self.bn_exit.setStyleSheet(s.StyleButton_5)
        
        icon36 = QIcon()
        icon36.addFile(u"icons/1x/cil_exit.ico", QSize(), QIcon.Normal, QIcon.On)
        icon36.addFile(u"icons/1x/cil_exit.ico", QSize(), QIcon.Normal, QIcon.Off)

        self.bn_exit.setIcon(icon36)
        self.bn_exit.setIconSize(QSize(self.linux22, self.linux22))
        self.bn_exit.setFlat(True)
        self.bn_exit.setCheckable(False)               
        self.bn_exit.setEnabled(True)


#--------------------------------------------------------------------------
# plc Button & Frame
#--------------------------------------------------------------------------

        self.frame_plc = QFrame(self.frame_bottom_west)
        self.frame_plc.setObjectName(u"frame_plc")
        self.frame_plc.setMinimumSize(QSize(self.linux8, self.linux16))
        self.frame_plc.setMaximumSize(QSize(160, self.linux16))
        self.frame_plc.setFrameShape(QFrame.NoFrame)
        self.frame_plc.setFrameShadow(QFrame.Plain)

        self.bn_plc = QPushButton(self.frame_plc)
        self.bn_plc.setObjectName(u"bn_plc")
        self.bn_plc.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_plc.setMaximumSize(QSize(160, self.linux16))
        self.bn_plc.setStyleSheet(s.StyleButton_1)


        icon16 = QIcon()
        icon16.addFile(u"icons/1x/cil_plc", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_plc.setIcon(icon16)
        self.bn_plc.setIconSize(QSize(22, 22))
        self.bn_plc.setFlat(True)

#--------------------------------------------------------------------------

        self.frame_8 = QFrame(self.frame_bottom_west)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Plain)

        self.verticalLayout_4 = QVBoxLayout(self.frame_8)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_3.addWidget(self.frame_8)
        self.horizontalLayout_2.addWidget(self.frame_bottom_west)

        self.frame_bottom_east = QFrame(self.frame_bottom)
        self.frame_bottom_east.setObjectName(u"frame_bottom_east")
        self.frame_bottom_east.setStyleSheet(u"background:rgb(51,51,51);")     #51,51,51
        self.frame_bottom_east.setFrameShape(QFrame.NoFrame)
        self.frame_bottom_east.setFrameShadow(QFrame.Plain)

        self.verticalLayout_2 = QVBoxLayout(self.frame_bottom_east)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)

        self.frame = QFrame(self.frame_bottom_east)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)

        self.ver_central = QVBoxLayout(self.frame)
        self.ver_central.setObjectName(u"horizontalLayout_14")
        self.ver_central.setContentsMargins(0, 0, 0, 0)
        self.ver_central.setSpacing(0)

        self.stackedWidget = QStackedWidget(self.frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(0, self.linux16))
        self.stackedWidget.setStyleSheet(u"background:rgb(51,51,51);")     #51,51,51
        self.stackedWidget.setContentsMargins(0, 0, 0, 0)

# -------------------------------------------------------------------------
# page home
# -------------------------------------------------------------------------

        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.page_home.setStyleSheet(u"background:rgb(91,90,90);")

        self.hor_page_home= QHBoxLayout(self.page_home)
        self.hor_page_home.setSpacing(0)
        self.hor_page_home.setObjectName(u"hor_page_home")
        self.hor_page_home.setContentsMargins(0, 0, 0, 0)

        self.frame_home_main = QFrame()
        self.frame_home_main.setObjectName(u"frame_home_main")
        self.frame_home_main.setFrameShape(QFrame.NoFrame)
        self.frame_home_main.setFrameShadow(QFrame.Plain)
        self.frame_home_main.setMinimumWidth(0)

        self.verticalLayout_5 = QVBoxLayout(self.frame_home_main)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)

        self.lab_home_main_hed = QLabel(self.frame_home_main)
        self.lab_home_main_hed.setObjectName(u"lab_home_main_hed")
        

        self.lab_home_main_hed.setFont(s.font1)
        self.lab_home_main_hed.setStyleSheet(u"QLabel {\n"
        "	color:rgb(255,255,255);\n"
        "}")

        self.lab_home_main_hed.setTextFormat(Qt.RichText)
        self.lab_home_main_hed.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Profile1234</span></p></body></html>", None))

        self.verticalLayout_5.addWidget(self.lab_home_main_hed)

        self.lab_home_main_disc = QLabel(self.frame_home_main)
        self.lab_home_main_disc.setObjectName(u"lab_home_main_disc")

        self.lab_home_main_disc.setFont(s.font2)
        self.lab_home_main_disc.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_home_main_disc.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.lab_home_main_disc.setWordWrap(True)
        self.lab_home_main_disc.setMargin(5)

        self.lab_home_main_disc.setText(QCoreApplication.translate("MainWindow", None))
        self.verticalLayout_5.addWidget(self.lab_home_main_disc)


        self.vert_divide = QFrame()
        self.vert_divide.setObjectName(u"vert_divide")
        self.vert_divide.setFrameShape(QFrame.VLine)
        self.vert_divide.setFrameShadow(QFrame.Sunken)
        self.ver_splitter = Splitter()
        self.ver_splitter.setHandleWidth(self.linux20)
        self.ver_splitter.setStyleSheet(s.StyleSplitter)
        self.hor_splitter = Splitter()
        self.hor_splitter.setHandleWidth(self.linux20)
        self.hor_splitter.setStyleSheet(s.StyleSplitter)
        
        self.frame_home_stat = QFrame(self.page_home)
        self.frame_home_stat.setObjectName(u"frame_home_stat")
        
        self.frame_home_stat.setFrameShape(QFrame.NoFrame)
        self.frame_home_stat.setFrameShadow(QFrame.Plain)
        self.frame_home_stat.setMinimumWidth(0)

        self.verticalLayout_6 = QVBoxLayout(self.frame_home_stat)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)

        self.lab_home_stat_hed = QLabel(self.frame_home_stat)
        self.lab_home_stat_hed.setObjectName(u"lab_home_stat_hed")
        
        self.lab_home_stat_hed.setMaximumSize(QSize(16777215, self.linux10))
        self.lab_home_stat_hed.setFont(s.font1)
        self.lab_home_stat_hed.setStyleSheet(u"QLabel {\n"
        "	color:rgb(255,255,255);\n"
        "}")

        self.lab_home_stat_hed.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_6.addWidget(self.lab_home_stat_hed)

        self.lab_home_stat_disc = QLabel(self.frame_home_stat)
        self.lab_home_stat_disc.setObjectName(u"lab_home_stat_disc")
        self.lab_home_stat_disc.setFont(s.font2)
        self.lab_home_stat_disc.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.lab_home_stat_disc.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Weather: Rainy<br/>Skys: Cloudy<br/>Wind: blowing Fast<br/>Temperature: 32 Degree Celcious</span></p></body></html>", None))
        
        self.verticalLayout_6.addWidget(self.lab_home_stat_disc)
        
        button = QPushButton('start')
        button1= QPushButton('start1')
        button2= QPushButton('start2')
        
        self.ver_splitter.addWidget(self.frame_home_main)
        self.ver_splitter.addWidget(self.frame_home_stat)
        self.ver_splitter.setOrientation(Qt.Horizontal)
        self.hor_splitter.setOrientation(Qt.Vertical)
        
      
        #self.hor_page_home.addWidget(self.frame_home_main)
        #self.hor_page_home.addWidget(self.vert_divide)
        self.hor_page_home.addWidget(self.ver_splitter)
        #self.hor_page_home.addWidget(self.frame_home_stat)
        
# -------------------------------------------------------------------------
# page pyqtgraph
# -------------------------------------------------------------------------

        self.page_graph = QWidget()
        self.page_graph.setObjectName(u"page_graph")
        self.page_graph.setStyleSheet(u"background:rgb(91,90,90);")  #91,90,90
   
        self.horizontalLayout_30 = QHBoxLayout(self.page_graph)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")

       
        self.win1 = MyApp(title='Messungen', icon='icons/1x/icon.ico')

        #ScrollBar
        self.h_bar_scroll = QScrollBar()  #self.graph_frame_scroll
        self.h_bar_scroll.setOrientation(Qt.Horizontal)
        self.h_bar_scroll.setInvertedControls(True)

        self.h_bar_scroll.setObjectName(u"h_bar_scroll")
        self.h_bar_scroll.setSizeIncrement(5,5)
        self.h_bar_scroll.setStyleSheet(s.StyleScrollBar_hor)
        

        #ScrollBar
        self.v_bar_scroll = QScrollBar()  #self.graph_frame_scroll
        self.v_bar_scroll.setOrientation(Qt.Vertical)
        self.v_bar_scroll.setInvertedControls(False)
        
        self.v_bar_scroll.setObjectName(u"v_bar_scroll")
        self.v_bar_scroll.setStyleSheet(s.StyleScrollBar_ver)

        self.scroll_graph = QScrollArea()   
        
        self.scroll_graph.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_graph.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_graph.setWidgetResizable(True)
        
        self.scroll_graph.setHorizontalScrollBar(self.h_bar_scroll)
        self.scroll_graph.setVerticalScrollBar(self.v_bar_scroll)

        self.horizontalLayout_30.setContentsMargins(0,0,0,0)
        self.horizontalLayout_30.setSpacing(0)

        self.scroll_graph.setWidget(self.win1) 
        
        
       
        self.horizontalLayout_30.addWidget(self.scroll_graph)
        
# -------------------------------------------------------------------------
# page_plc
# -------------------------------------------------------------------------

        self.page_plc = QWidget()
        self.page_plc.setObjectName(u"page_plc")
        self.page_plc.setStyleSheet(u"background:rgb(91,90,90);") 

        self.page_plc_2 = QWidget(self.page_plc)
        self.page_plc_2.setObjectName(u"page_plc_2")
        self.page_plc_2.setStyleSheet(u"background:rgb(91,90,90);")
        #self.page_plc_2.setMinimumSize(QSize(3000,400))
        #self.page_plc_2.setMaximumSize(QSize(3000,400))
    
        self.page_plc_vbox = QVBoxLayout(self.page_plc_2)
        self.page_plc_vbox.setContentsMargins(2,2,2,2)
        
        self.frame_scroll = QFrame(self.page_plc_2)
        self.frame_scroll.setObjectName(u"frame_scroll")
        self.frame_scroll.setStyleSheet(u"background:rgb(91,90,90);")
        self.frame_scroll.setFrameShape(QFrame.StyledPanel)
        self.frame_scroll.setFrameShadow(QFrame.Raised)

        
        self.frame_scroll1 = QFrame(self.page_plc_2)
        self.frame_scroll1.setObjectName(u"frame_scroll")
        self.frame_scroll1.setStyleSheet(u"background:rgb(91,90,90);")
        self.frame_scroll1.setFrameShape(QFrame.StyledPanel)
        self.frame_scroll1.setFrameShadow(QFrame.Raised)
        
        
        self.scroll = QScrollArea()   
        
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        
        self.ver_page_plc = QVBoxLayout(self.page_plc)  
        self.hor_page_plc = QHBoxLayout()  

        self.ver_page_plc.setContentsMargins(0, 0, 0, 0)
        self.ver_page_plc.setSpacing(2)

        self.ver_page_plc.setObjectName(u"ver_page_plc")
        self.hor_page_plc.setObjectName(u"hor_page_plc")
        self.hor_page_plc.setSpacing(2)

        self.gridLayout_1 = QGridLayout() 
        self.gridLayout_1.setObjectName(u"gridLayout_1")

        #ScrollBar
        self.page_plc_scroll = QScrollBar(self.frame_scroll)  
        self.page_plc_scroll.setOrientation(Qt.Horizontal)
        
        self.page_plc_scroll.setInvertedControls(True)

        self.page_plc_scroll.setObjectName(u"page_plc_scroll")
        self.page_plc_scroll.setSizeIncrement(5,5)
        self.page_plc_scroll.setStyleSheet(s.StyleScrollBar_hor)

        #ScrollBar
        self.page_plc_scroll1 = QScrollBar(self.frame_scroll1)  
        self.page_plc_scroll1.setOrientation(Qt.Vertical)
        
        self.page_plc_scroll1.setInvertedControls(False)
        

        self.page_plc_scroll1.setObjectName(u"page_plc_scroll1")
        self.page_plc_scroll1.setStyleSheet(s.StyleScrollBar_ver)
     

        self.scroll.setHorizontalScrollBar(self.page_plc_scroll)
        self.scroll.setVerticalScrollBar(self.page_plc_scroll1)
      
        
#--------------------------------------------------------------------------
# QVBoxLayout
#--------------------------------------------------------------------------

        liste_werte =("0.00", "0.00", "0.00", "0.00", "0.00", "0.00",  "0.00", "0.00")
            
        liste_lab2 = ("mm" ,  "mm" , "mm" ,  "mm","mm" ,  "mm" , "mm" ,  "mm")
        
        liste_lab1 = ("Leitgeber" ,  "Antrieb1" , "Antrieb2" ,  "Antrieb3", "Antrieb4" ,  "Antrieb5" , "Antrieb6" ,  "Antrieb7")
        
        self.antbox = GroupLine( minimumSize=(QSize(250, 350)), maximumSize=(QSize(250, 1000)), value=8 )
        self.antbox.setTitle('S7 Verbindungen aufbauen')
        self.antbox.setLineText(liste_werte)
        self.antbox.setLabelText(liste_lab1, liste_lab2)
        
        self.hor_page_plc.addWidget(self.antbox)
        
#--------------------------------------------------------------------------
# Slider einfueden
#--------------------------------------------------------------------------

        self.group_Slider    = QGroupBox()                     
        self.hor_Slider      = QHBoxLayout()
        self.hor_Slider.setContentsMargins(5,15,5,10)

        self.group_Slider.setMinimumSize(QSize(200, 200))
        self.group_Slider.setMaximumSize(QSize(200, 1000))
        self.group_Slider.setFont(s.font6)
        self.group_Slider.setStyleSheet(s.Stylegroup)
        self.group_Slider.setAlignment(Qt.AlignHCenter)
       

        self.group_Slider.setTitle(QCoreApplication.translate("MainWindow", 'Abtastung', None))

        self.group_Slider.setCheckable(False)
        self.group_Slider.setChecked(False)
        self.group_Slider.setDisabled(True)

        self.w1 = Slider(30, 100 , 50)
        
        self.hor_Slider.addWidget(self.w1)

        self.w2 = Slider(50, 200, 50)
        self.hor_Slider.addWidget(self.w2)

        self.group_Slider.setLayout(self.hor_Slider)

        self.hor_page_plc.addWidget(self.group_Slider)
        

#--------------------------------------------------------------------------
#  GroupBox GroupCheck - 'minimumSize', 'maximumSize', 'title'
#--------------------------------------------------------------------------
        boxen = 16  #16 Boxen
        self.Box=[]
        #Anzahl an max Groupboxen 16Stueck
        self.LBox=[]
      
        for i in range(0, boxen):
                self.xbox  = GroupCheckBox( minimumSize=(QSize(100, 100)), maximumSize=(QSize(100, 1000)), value=16)
                self.Box.append(self.xbox) 

        for i in range(0, 2):
                self.ybox = GroupLine( minimumSize=(QSize(200, 350)), maximumSize=(QSize(200, 1000)), value=8 )
                self.LBox.append(self.ybox)        
                 
        #print(self.Box)
        #self.Box1.setValue(21845,16)
        #self.Box1.setVisible(False)
        #self.Box1.setTitleCheck(Group_Liste)
        #self.ui.Box2.setTitleCheck(Group_Liste1)
      
      
        #Reihenfolge Module
        #hoehe flexible bis 500
        #self.group_Slider_spacer  = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #self.hor_page_plc.addItem(self.group_Slider_spacer )
        
        b=0
        for i in self.Box:
               
                b +=1
                self.hor_page_plc.addWidget(i)
        b=0
        for i in self.LBox:
               
                b +=1
                self.hor_page_plc.addWidget(i)


        self.hor_page_plc_spacer  = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hor_page_plc.addItem( self.hor_page_plc_spacer )

        self.hor_page_plc.addWidget(self.page_plc_scroll1)
        
        #QWidget einfuegen
       
        self.page_plc_vbox.addLayout(self.hor_page_plc)

        #Scrollbar einfuegen (Vertical BoxLayout)
        self.page_plc_vbox.addWidget(self.page_plc_scroll)
        
        self.page_plc_2.setLayout(self.page_plc_vbox)

        self.scroll.setWidget(self.page_plc_2) 
       
        self.ver_page_plc.addWidget(self.scroll)
        
        #horizontal Divider
        self.hor_divide_1 = QFrame(self.page_plc)
        self.hor_divide_1.setObjectName(u"hor_divide_1")
        self.hor_divide_1.setFrameShape(QFrame.HLine)
        self.hor_divide_1.setFrameShadow(QFrame.Sunken)

        self.ver_page_plc.addWidget(self.hor_divide_1)
        
# -------------------------------------------------------------------------

        self.frame_page_plc_menu = QFrame(self.page_plc)
        self.frame_page_plc_menu.setObjectName(u"frame_page_plc_menu")
        self.frame_page_plc_menu.setMaximumSize(QSize(16777215, self.linux16))
        self.frame_page_plc_menu.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_page_plc_menu.setFrameShape(QFrame.NoFrame)
        self.frame_page_plc_menu.setFrameShadow(QFrame.Plain)

        self.hor_page_plc_menu= QHBoxLayout(self.frame_page_plc_menu)
        self.hor_page_plc_menu.setSpacing(0)
        self.hor_page_plc_menu.setObjectName(u"hor_page_plc_menu")
        self.hor_page_plc_menu.setContentsMargins(0, 0, 0, 0)

        self.frame_s7_steuer = QFrame(self.frame_page_plc_menu)
        self.frame_s7_steuer.setObjectName(u"frame_s7_steuer")
        self.frame_s7_steuer.setMinimumSize(QSize(self.linux16, self.linux16))
        self.frame_s7_steuer.setFrameShape(QFrame.NoFrame)
        self.frame_s7_steuer.setFrameShadow(QFrame.Plain)

        self.hor_s7_steuer = QHBoxLayout(self.frame_s7_steuer)
        self.hor_s7_steuer.setSpacing(0)
        self.hor_s7_steuer.setObjectName(u"hor_s7_steuer")
        self.hor_s7_steuer.setContentsMargins(0, 0, 0, 0)

        self.bn_s7_steuer = QPushButton()
        self.bn_s7_steuer.setObjectName(u"bn_s7_steuer")
        self.bn_s7_steuer.setMinimumSize(QSize(self.linux16, self.linux16))
        self.bn_s7_steuer.setStyleSheet(s.StyleButton_3)
        self.bn_s7_steuer.setFlat(True)
        icon_s7= QIcon()
        icon_s7.addFile(u"icons/1x/cil_automatik.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_s7_steuer.setIcon(icon_s7)
        
        self.bn_s7_steuer.setIconSize(QSize(30, 30))

        self.hor_s7_steuer.addWidget(self.bn_s7_steuer)
        self.hor_page_plc_menu.addWidget(self.frame_s7_steuer)

        ## Button Aufzeichung
        self.frame_aufzeichnung = QFrame(self.frame_page_plc_menu)
        self.frame_aufzeichnung.setObjectName(u"frame_aufzeichnung")
        self.frame_aufzeichnung.setMinimumSize(QSize(self.linux16, self.linux16))
        self.frame_aufzeichnung.setFrameShape(QFrame.NoFrame)
        self.frame_aufzeichnung.setFrameShadow(QFrame.Plain)

        self.hor_frame_aufzeichnung = QHBoxLayout(self.frame_aufzeichnung)
        self.hor_frame_aufzeichnung.setSpacing(0)
        self.hor_frame_aufzeichnung.setObjectName(u"hor_frame_aufzeichnung")
        self.hor_frame_aufzeichnung.setContentsMargins(0, 0, 0, 0)

        self.bn_aufzeichnung = QPushButton(self.frame_aufzeichnung)
        self.bn_aufzeichnung.setObjectName(u"bn_aufzeichnung")
        self.bn_aufzeichnung.setMinimumSize(QSize(self.linux16, self.linux16))
        self.bn_aufzeichnung.setStyleSheet(s.StyleButton_3)

        icon_auf= QIcon()
        icon_auf.addFile(u"icons/1x/cil_led_disabled.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_aufzeichnung.setIcon(icon_auf)
        
        self.bn_aufzeichnung.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_aufzeichnung.setFlat(True)

        self.hor_frame_aufzeichnung.addWidget(self.bn_aufzeichnung)
        self.hor_page_plc_menu.addWidget(self.frame_aufzeichnung)
        
        ## Button plc_steuer
        self.frame_plc_steuer = QFrame(self.frame_page_plc_menu)
        self.frame_plc_steuer.setObjectName(u"frame_plc_steuer")
        self.frame_plc_steuer.setMinimumSize(QSize(self.linux16, self.linux16))
       
        self.frame_plc_steuer.setFrameShape(QFrame.NoFrame)
        self.frame_plc_steuer.setFrameShadow(QFrame.Plain)

        self.hor_plc_steuer = QHBoxLayout(self.frame_plc_steuer)
        self.hor_plc_steuer.setSpacing(0)
        self.hor_plc_steuer.setObjectName(u"hor_plc_steuer")
        self.hor_plc_steuer.setContentsMargins(0, 0, 0, 0)

        self.bn_plc_steuer = QPushButton(self.frame_plc_steuer)
        self.bn_plc_steuer.setObjectName(u"bn_plc_steuer")
        self.bn_plc_steuer.setMinimumSize(QSize(self.linux16, self.linux16))
       
        self.bn_plc_steuer.setStyleSheet(s.StyleButton_3)

        icon_steuer= QIcon()
        icon_steuer.addFile(u"icons/1x/cil-power-standby.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_plc_steuer.setIcon(icon_steuer)
        
        self.bn_plc_steuer.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_plc_steuer.setFlat(True)

        self.hor_plc_steuer.addWidget(self.bn_plc_steuer)
        self.hor_page_plc_menu.addWidget(self.frame_plc_steuer)

        ## Button bn_S7_timer
        self.frame_S7_timer = QFrame(self.frame_page_plc_menu)
        self.frame_S7_timer.setObjectName(u"frame_S7_timer")
        self.frame_S7_timer.setMinimumSize(QSize(self.linux16, self.linux16))
        
        self.frame_S7_timer.setFrameShape(QFrame.NoFrame)
        self.frame_S7_timer.setFrameShadow(QFrame.Plain)

        self.hor_S7_timer = QHBoxLayout(self.frame_S7_timer)
        self.hor_S7_timer.setSpacing(0)
        self.hor_S7_timer.setObjectName(u"hor_S7_timer")
        self.hor_S7_timer.setContentsMargins(0, 0, 0, 0)

        self.bn_S7_timer = QPushButton(self.frame_S7_timer)
        self.bn_S7_timer.setObjectName(u"bn_S7_timer")
        self.bn_S7_timer.setMinimumSize(QSize(self.linux16, self.linux16))
       
        self.bn_S7_timer.setStyleSheet(s.StyleButton_3)

        icon_timer= QIcon()
        icon_timer.addFile(u"icons/1x/cil-av-timer.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_S7_timer.setIcon(icon_timer)
        
        self.bn_S7_timer.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_S7_timer.setFlat(True)

        self.hor_S7_timer.addWidget(self.bn_S7_timer)
        self.hor_page_plc_menu.addWidget(self.frame_S7_timer)

        ## Button bn_auswahl
        self.frame_bn_auswahl = QFrame(self.frame_page_plc_menu)
        self.frame_bn_auswahl.setObjectName(u"frame_bn_auswahl")
        self.frame_bn_auswahl.setMinimumSize(QSize(self.linux16, self.linux16))
       
        self.frame_bn_auswahl.setFrameShape(QFrame.NoFrame)
        self.frame_bn_auswahl.setFrameShadow(QFrame.Plain)

        self.hor_bn_auswahl = QHBoxLayout(self.frame_bn_auswahl)
        self.hor_bn_auswahl.setSpacing(0)
        self.hor_bn_auswahl.setObjectName(u"hor_bn_auswahl")
        self.hor_bn_auswahl.setContentsMargins(0, 0, 0, 0)

        self.bn_auswahl  = QPushButton(self.frame_bn_auswahl)
        self.bn_auswahl .setObjectName(u"bn_auswahl ")
        self.bn_auswahl .setMinimumSize(QSize(self.linux16, self.linux16))
       
        self.bn_auswahl .setStyleSheet(s.StyleButton_3)

        icon_graph= QIcon()
        icon_graph.addFile(u"icons/1x/cil_grid.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_auswahl.setIcon(icon_graph)
        
        self.bn_auswahl.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_auswahl .setFlat(True)

        self.hor_bn_auswahl.addWidget(self.bn_auswahl )
        self.hor_page_plc_menu.addWidget(self.frame_bn_auswahl)
        
        ## Button bn_dial
        self.frame_bn_dial = QFrame(self.frame_page_plc_menu)
        self.frame_bn_dial.setObjectName(u"frame_bn_auswahl")
        self.frame_bn_dial.setMinimumSize(QSize(self.linux16, self.linux16))
       
        self.frame_bn_dial.setFrameShape(QFrame.NoFrame)
        self.frame_bn_dial.setFrameShadow(QFrame.Plain)

        self.hor_bn_dial = QHBoxLayout(self.frame_bn_dial)
        self.hor_bn_dial.setSpacing(0)
        self.hor_bn_dial.setObjectName(u"hor_bn_auswahl")
        self.hor_bn_dial.setContentsMargins(0, 0, 0, 0)

        self.bn_dial  = QPushButton(self.frame_bn_dial)
        self.bn_dial .setObjectName(u"bn_auswahl ")
        self.bn_dial .setMinimumSize(QSize(self.linux16, self.linux16))
        
        self.bn_dial .setStyleSheet(s.StyleButton_3)

        icon_dial= QIcon()
        icon_dial.addFile(u"icons/1x/cil_aus_1.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_dial.setIcon(icon_dial)
        
        self.bn_dial.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_dial.setFlat(True)

        self.hor_bn_dial.addWidget(self.bn_dial )
        self.hor_page_plc_menu.addWidget(self.frame_bn_dial)


        self.hor_spacer_setting_trig = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hor_page_plc_menu.addItem(self.hor_spacer_setting_trig)

#--------------------------------------------------------------------------
      
        #hauptpage android
        self.stackedWidget_plc = QStackedWidget(self.page_plc)
        self.stackedWidget_plc.setObjectName(u"stackedWidget_plc")
        self.stackedWidget_plc.setStyleSheet(u"background:rgb(91,90,90);")

# -------------------------------------------------------------------------
# Page Steuer S7
# -------------------------------------------------------------------------

        self.page_steuer_S7 = QWidget()
        self.page_steuer_S7.setObjectName(u"page_steuer_S7")
        self.page_steuer_S7.setStyleSheet(u"background:rgb(91,90,90);")
       

        self.ver_page_steuer_S7 = QVBoxLayout(self.page_steuer_S7)
        self.ver_page_steuer_S7.setSpacing(0)
        self.ver_page_steuer_S7.setObjectName(u"ver_page_steuer_S7")
        self.ver_page_steuer_S7.setContentsMargins(5, 5, 5, 5)
        

#--------------------------------------------------------------------------
# Button Aus, Stop, Hand und Automatik einfuegen
#--------------------------------------------------------------------------

        self.group_Button = QGroupBox() 
        self.group_Button.setMaximumHeight(self.linux4)
       
        self.ver_Button = QVBoxLayout(self.group_Button)
        self.ver_Button.setContentsMargins(5,20,5,10)
        self.ver_Button.setSpacing(0)
       
        self.hor_Button1 = QHBoxLayout()
        self.hor_Button1.setContentsMargins(0,0,15,0)
        self.hor_Button1.setSpacing(3)


        self.group_Button.setFont(s.font6)
        self.group_Button.setStyleSheet(s.Stylegroup)
        self.group_Button.setAlignment(Qt.AlignHCenter)
        
        self.group_Button.setCheckable(False)
        self.group_Button.setChecked(False)
        self.group_Button.setDisabled(True)

        self.group_Button.setTitle(QCoreApplication.translate("MainWindow", 'S7 Steuer_Buttons', None))

        self.bn_Aus = QPushButton(self.group_Button)
        self.bn_Aus.setObjectName(u"bn_Aus")
        self.bn_Aus.setMinimumSize(QSize(self.linux8, self.linux8))
    
        icon22 = QIcon()
        icon22.addFile(u"icons/1x/Aus_On.ico", QSize(), QIcon.Normal, QIcon.On)
        icon22.addFile(u"icons/1x/Aus_Off.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_Aus.setIcon(icon22)
        self.bn_Aus.setIconSize(QSize(self.linux8, self.linux8))
        
        self.bn_Aus.setFlat(True)
        self.bn_Aus.setCheckable(False)  #True
        self.bn_Aus.setEnabled(True)

        self.hor_Button1.addWidget(self.bn_Aus)

#--------------------------------------------------------------------------
# Button Aus, Stop, Hand und Automatik einfuegen
#--------------------------------------------------------------------------

        self.bn_Stop = QPushButton(self.group_Button)
        self.bn_Stop.setObjectName(u"bn_Stop")
        self.bn_Stop.setMaximumSize(QSize(self.linux8, self.linux8))

        icon23 = QIcon()
        icon23.addFile(u"icons/1x/Stop_On.ico", QSize(), QIcon.Normal, QIcon.On)
        icon23.addFile(u"icons/1x/Stop_Off.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_Stop.setIcon(icon23)
        self.bn_Stop.setIconSize(QSize(self.linux8, self.linux8))

        self.bn_Stop.setFlat(True)
        self.bn_Stop.setCheckable(False)  #True
        self.bn_Stop.setEnabled(True)

        self.hor_Button1.addWidget(self.bn_Stop)

#--------------------------------------------------------------------------
# Button Aus, Stop, Hand und Automatik einfuegen
#--------------------------------------------------------------------------

        self.bn_Hand = QPushButton(self.group_Button)
        self.bn_Hand.setObjectName(u"bn_Hand")
        self.bn_Hand.setMaximumSize(QSize(self.linux8, self.linux8))

        icon24 = QIcon()
        icon24.addFile(u"icons/1x/Hand_On.ico", QSize(), QIcon.Normal, QIcon.On)
        icon24.addFile(u"icons/1x/Hand_Off.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_Hand.setIcon(icon24)
        self.bn_Hand.setIconSize(QSize(self.linux8, self.linux8))
        
        self.bn_Hand.setFlat(True)
        self.bn_Hand.setCheckable(False)  #True
        self.bn_Hand.setEnabled(True)

        self.hor_Button1.addWidget(self.bn_Hand)

#--------------------------------------------------------------------------
# Button Aus, Stop, Hand und Automatik einfuegen
#--------------------------------------------------------------------------

        self.bn_Auto = QPushButton(self.group_Button)
        self.bn_Auto.setObjectName(u"bn_Auto")
        self.bn_Auto.setMaximumSize(QSize(self.linux8, self.linux8))

        icon25 = QIcon()
        icon25.addFile(u"icons/1x/Automatik_On.ico", QSize(), QIcon.Normal, QIcon.On)
        icon25.addFile(u"icons/1x/Automatik_Off.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_Auto.setIcon(icon25)
        self.bn_Auto.setIconSize(QSize(self.linux8, self.linux8))

        self.bn_Auto.setFlat(True)
        self.bn_Auto.setCheckable(False)  #True
        self.bn_Auto.setEnabled(True)

        self.hor_Button1.addWidget(self.bn_Auto)

#--------------------------------------------------------------------------
# Button Produktion einfuegen
#--------------------------------------------------------------------------

        self.bn_Prod = QPushButton(self.group_Button)
        self.bn_Prod.setObjectName(u"bn_Prod")
        self.bn_Prod.setMaximumSize(QSize(self.linux8, self.linux8))
   
        icon28 = QIcon()
        icon28.addFile(u"icons/1x/Prod1_On.ico", QSize(), QIcon.Normal, QIcon.On)
        icon28.addFile(u"icons/1x/Prod1_Off.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_Prod.setIcon(icon28)
        self.bn_Prod.setIconSize(QSize(self.linux8, self.linux8))

        self.bn_Prod.setFlat(True)
        self.bn_Prod.setCheckable(False)  #True
        self.bn_Prod.setEnabled(True)

        self.hor_Button1.addWidget(self.bn_Prod)

        #horizontal Spacer
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hor_Button1.addItem(self.horizontalSpacer_12)


        self.lab_Button = QLabel()
        self.lab_Button.setFont(s.font7)
        self.lab_Button.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_Button.setText('Code = 0000 ')
        self.lab_Button.setAlignment(Qt.AlignHCenter)

        self.ver_Button.addLayout(self.hor_Button1)
        self.ver_Button.addWidget(self.lab_Button)

        #in group einfuegen
        self.group_Button.setLayout(self.ver_Button)

        self.ver_page_steuer_S7.addWidget(self.group_Button)

        #Page Steuer S7  im Stack - Nummer 0
        self.stackedWidget_plc.addWidget(self.page_steuer_S7)
        self.stackedWidget_plc.setMaximumHeight(self.linux4)

        #haupseite page plc
        self.ver_page_plc.addWidget(self.stackedWidget_plc)
        
        self.ver_page_plc.addWidget(self.frame_page_plc_menu)

# -------------------------------------------------------------------------
# Page Aufzeichung 
# -------------------------------------------------------------------------

        self.page_aufzeichnung = QWidget()
        self.page_aufzeichnung.setObjectName(u"page_aufzeichnung")
        self.page_aufzeichnung.setStyleSheet(u"background:rgb(91,90,90);")
       

        self.ver_page_aufzeichnung = QVBoxLayout(self.page_aufzeichnung)
        self.ver_page_aufzeichnung.setSpacing(0)
        self.ver_page_aufzeichnung.setObjectName(u"ver_page_aufzeichnung")
        self.ver_page_aufzeichnung.setContentsMargins(5, 5, 5, 5)

#--------------------------------------------------------------------------
# group fuer Aufzeichnung
#--------------------------------------------------------------------------

        self.group_Aufzeichnung = QGroupBox() 
        self.hor_Aufzeichnung = QHBoxLayout()
        self.hor_Aufzeichnung.setContentsMargins(0,0,15,0)
        self.hor_Aufzeichnung.setSpacing(3)

        self.ver_Aufzeichnung = QVBoxLayout(self.group_Aufzeichnung)
        self.ver_Aufzeichnung.setContentsMargins(5,20,5,10)
        self.ver_Aufzeichnung.setSpacing(0)

        self.group_Aufzeichnung.setFont(s.font6)
        self.group_Aufzeichnung.setStyleSheet(s.Stylegroup)
        self.group_Aufzeichnung.setAlignment(Qt.AlignHCenter)
        
        self.group_Aufzeichnung.setCheckable(False)
        self.group_Aufzeichnung.setChecked(False)
        self.group_Aufzeichnung.setDisabled(True)  #True

        self.group_Aufzeichnung.setTitle(QCoreApplication.translate("MainWindow", 'Aufzeichnung', None))
#--------------------------------------------------------------------------
# Button Start Aufzeichnung einfuegen
#--------------------------------------------------------------------------

        self.bn_Start_Auf = QPushButton(self.group_Aufzeichnung)
        self.bn_Start_Auf.setObjectName(u"bn_Start_Auf")
        self.bn_Start_Auf.setMaximumSize(QSize(self.linux8, self.linux8))

        icon29 = QIcon()
        icon29.addFile(u"icons/1x/Zyklus_On.ico", QSize(), QIcon.Normal, QIcon.On)
        icon29.addFile(u"icons/1x/Zyklus_Off.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_Start_Auf.setIcon(icon29)
        self.bn_Start_Auf.setIconSize(QSize(self.linux8, self.linux8))
        self.bn_Start_Auf.setFlat(True)
        self.bn_Start_Auf.setCheckable(False)  #True
        self.bn_Start_Auf.setEnabled(True)

#--------------------------------------------------------------------------
# Button Stop Aufzeichnung einfuegen
#--------------------------------------------------------------------------

        self.bn_Stop_Auf = QPushButton(self.group_Aufzeichnung)
        self.bn_Stop_Auf.setObjectName(u"bn_Stop_Auf")
        self.bn_Stop_Auf.setMaximumSize(QSize(self.linux8, self.linux8))

        icon30 = QIcon()
        icon30.addFile(u"icons/1x/Aus_On.ico", QSize(), QIcon.Normal, QIcon.On)
        icon30.addFile(u"icons/1x/Aus_Off.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_Stop_Auf.setIcon(icon30)
        self.bn_Stop_Auf.setIconSize(QSize(self.linux8, self.linux8))
        self.bn_Stop_Auf.setFlat(True)
        self.bn_Stop_Auf.setCheckable(False)  #True
        self.bn_Stop_Auf.setEnabled(True)

#--------------------------------------------------------------------------
# Button Loesch Aufzeichnung einfuegen
#--------------------------------------------------------------------------

        self.bn_laden_Auf = QPushButton(self.group_Aufzeichnung)
        self.bn_laden_Auf.setObjectName(u"bn_laden_Auf")
        self.bn_laden_Auf.setMaximumSize(QSize(self.linux8, self.linux8))

        icon31 = QIcon()
        icon31.addFile(u"icons/1x/Loesch_On.ico", QSize(), QIcon.Normal, QIcon.On)
        icon31.addFile(u"icons/1x/Loesch_Off.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_laden_Auf.setIcon(icon31)
        self.bn_laden_Auf.setIconSize(QSize(self.linux8, self.linux8))
        self.bn_laden_Auf.setFlat(True)
        self.bn_laden_Auf.setCheckable(False)  #True
        self.bn_laden_Auf.setEnabled(True)

#--------------------------------------------------------------------------
# LED Start Aufzeichnung blinken einfuegen
#--------------------------------------------------------------------------

        self.bn_Start_Led = QPushButton(self.group_Aufzeichnung)
        self.bn_Start_Led.setObjectName(u"bn_Start_Led")
        self.bn_Start_Led.setMinimumSize(QSize(self.linux16, self.linux16))

        self.bn_Start_Led.setStyleSheet(s.StyleButton_rot)
       
        #Speicher Blinken (Background)
        self.bn_Start_Led_blink = False

        self.bn_Start_Led.setFlat(False)       #True
        self.bn_Start_Led.setCheckable(True)  #false
        #self.bn_Start_Led.setChecked(False)
        self.bn_Start_Led.setEnabled(True)   #false

        #horizontal Spacer
        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        #Reihenfolge Start Aufzeichnung Buttons
        self.hor_Aufzeichnung.addWidget(self.bn_Stop_Auf)
        self.hor_Aufzeichnung.addWidget(self.bn_Start_Auf)
        self.hor_Aufzeichnung.addWidget(self.bn_laden_Auf)
        self.hor_Aufzeichnung.addWidget(self.bn_Start_Led)
        self.hor_Aufzeichnung.addItem(self.horizontalSpacer_14)

        self.lab_Aufzeichnung = QLabel()
        self.lab_Aufzeichnung.setFont(s.font6)
        self.lab_Aufzeichnung.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_Aufzeichnung.setText('stop Aufzeichnung ')
        self.lab_Aufzeichnung.setAlignment(Qt.AlignHCenter)

        self.ver_Aufzeichnung.addLayout(self.hor_Aufzeichnung)
        self.ver_Aufzeichnung.addWidget(self.lab_Aufzeichnung)

        #Gruppe Aufzeichnung einfuegen
        #in group einfuegen
        self.group_Aufzeichnung.setLayout(self.ver_Aufzeichnung)

        self.ver_page_aufzeichnung.addWidget(self.group_Aufzeichnung)

        #Page_aufzeichnung  im Stack - Nummer 1
        self.stackedWidget_plc.addWidget(self.page_aufzeichnung)
        self.stackedWidget_plc.setMaximumHeight(self.linux4)
       
# -------------------------------------------------------------------------
# Page plc_steuer 
# -------------------------------------------------------------------------

        self.page_plc_steuer= QWidget()
        self.page_plc_steuer.setObjectName(u"page_plc_steuer")
        self.page_plc_steuer.setStyleSheet(u"background:rgb(91,90,90);")
       
        self.ver_page_plc_steuer = QVBoxLayout(self.page_plc_steuer)
        self.ver_page_plc_steuer.setSpacing(0)
        self.ver_page_plc_steuer.setObjectName(u"ver_page_steuer_S7page_plc_steuer")
        self.ver_page_plc_steuer.setContentsMargins(5, 5, 5, 5)
 
#--------------------------------------------------------------------------
#  GroupBox PLC Start/Stop
#--------------------------------------------------------------------------

        self.group_plc = QGroupBox()

        self.hor_plc = QHBoxLayout()
        self.hor_plc.setContentsMargins(0, 0, 5, 5)
        self.hor_plc.setSpacing(0)

        self.ver_plc = QVBoxLayout(self.group_plc)
        self.ver_plc.setContentsMargins(10, 20, 10, 5)
        self.ver_plc.setSpacing(10)
             
        self.group_plc.setFont(s.font6)
        self.group_plc.setStyleSheet(s.Stylegroup)
        self.group_plc.setAlignment(Qt.AlignHCenter)
        self.group_plc.setCheckable(True)
        self.group_plc.setChecked(True)
        self.group_plc.setDisabled(False)  

        self.group_plc.setTitle(QCoreApplication.translate("MainWindow", 'PLC Steuer', None))
        
#--------------------------------------------------------------------------
# Button Power On/Off
#--------------------------------------------------------------------------

        self.bn_On = QPushButton(self.group_plc)
        self.bn_On.setObjectName(u"bn_On")
        self.bn_On.setMinimumSize(QSize(self.linux8, self.linux8))
        self.bn_On.setCheckable(False)  #True
        self.bn_On.setEnabled(True)
        self.bn_On.setStyleSheet(s.StyleButton_1)

        icon26 = QIcon()
        icon26.addFile(u"icons/1x/cil-power-standby.ico", QSize(), QIcon.Disabled)
        icon26.addFile(u"icons/1x/cil-power-standby_2.ico", QSize(), QIcon.Normal, QIcon.On)
        icon26.addFile(u"icons/1x/cil-power-standby_1.ico", QSize(), QIcon.Normal, QIcon.Off)

        self.bn_On.setIcon(icon26)
        self.bn_On.setIconSize(QSize(self.linux8, self.linux8))
        self.bn_On.setFlat(False)     #True

#--------------------------------------------------------------------------
# Button Start PLC einfuegen
#--------------------------------------------------------------------------

        self.bn_plc_start = QPushButton(self.group_plc)
        self.bn_plc_start.setMinimumSize(QSize(self.linux8, self.linux8))
        self.bn_plc_start.setStyleSheet(s.StyleButton_1)
        icon34 = QIcon()
        icon34.addFile(u"icons/1x/Automatik_On.ico", QSize(), QIcon.Normal, QIcon.On)
        icon34.addFile(u"icons/1x/Automatik_Off.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_plc_start.setIcon(icon34)
        self.bn_plc_start.setIconSize(QSize(self.linux8, self.linux8))
        self.bn_plc_start.setFlat(True)
        self.bn_plc_start.setCheckable(False)  #True
        self.bn_plc_start.setEnabled(True)

      
#--------------------------------------------------------------------------
# Button Stop PLC einfuegen
#--------------------------------------------------------------------------

        self.bn_plc_stop = QPushButton(self.group_plc)

        self.bn_plc_stop.setMinimumSize(QSize(self.linux8, self.linux8))
        self.bn_plc_stop.setStyleSheet(s.StyleButton_1)
        
        icon33 = QIcon()
        icon33.addFile(u"icons/1x/Aus_On.ico", QSize(), QIcon.Normal, QIcon.On)
        icon33.addFile(u"icons/1x/Aus_Off.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_plc_stop.setIcon(icon33)
        self.bn_plc_stop.setIconSize(QSize(self.linux8, self.linux8))
        self.bn_plc_stop.setFlat(True)
        self.bn_plc_stop.setCheckable(False)  #True
        self.bn_plc_stop.setEnabled(True)

        self.lab_plc = QLabel()
        
        self.lab_plc.setFont(s.font6)
        self.lab_plc.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_plc.setAlignment(Qt.AlignHCenter)

        self.lab_plc.setText(QCoreApplication.translate("MainWindow", u"Zustand PLC", None))

#--------------------------------------------------------------------------
# Button Reset PLC einfuegen  (Fehlermeldungen quittieren)
#--------------------------------------------------------------------------

        self.bn_plc_reset = QPushButton(self.group_plc)
        self.bn_plc_reset.setMinimumSize(QSize(self.linux8, self.linux8))

        self.bn_plc_reset.setStyleSheet(s.StyleButton_1)
        icon37 = QIcon()
        icon37.addFile(u"icons/1x/cil_restore.ico", QSize(), QIcon.Normal, QIcon.On)
        icon37.addFile(u"icons/1x/cil_restore.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_plc_reset.setIcon(icon37)
        self.bn_plc_reset.setIconSize(QSize(self.linux8, self.linux8))
        self.bn_plc_reset.setFlat(True)
        self.bn_plc_reset.setCheckable(False)  #True
        self.bn_plc_reset.setEnabled(True)


        #horizontal Spacer
        self.hor_plc_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        

        #Widget (group_plc)
        self.hor_plc.addWidget(self.bn_On)
        self.hor_plc.addWidget(self.bn_plc_stop)
        self.hor_plc.addWidget(self.bn_plc_start)
        self.hor_plc.addItem(self.hor_plc_spacer)
        self.hor_plc.addWidget(self.bn_plc_reset)
       
        self.ver_plc.addLayout(self.hor_plc)
        self.ver_plc.addWidget(self.lab_plc)

        #in group einfuegen
        self.group_plc.setLayout(self.ver_plc)

        self.ver_page_plc_steuer.addWidget(self.group_plc)

        #page_plc_steuer  im Stack - Nummer 2
        self.stackedWidget_plc.addWidget(self.page_plc_steuer)
        self.stackedWidget_plc.setMaximumHeight(self.linux4)

# -------------------------------------------------------------------------
# Page Timer s7
# -------------------------------------------------------------------------

        self.page_timer_S7 = QWidget()
        self.page_timer_S7.setObjectName(u"page_timer_S7")
        self.page_timer_S7.setStyleSheet(u"background:rgb(91,90,90);")
       
        self.ver_page_timer_S7 = QVBoxLayout(self.page_timer_S7)
        self.ver_page_timer_S7.setSpacing(0)
        self.ver_page_timer_S7.setObjectName(u"ver_page_timer_S7")
        self.ver_page_timer_S7.setContentsMargins(5, 5, 5, 5)

#--------------------------------------------------------------------------
#  GroupBox Timer aktiv
#--------------------------------------------------------------------------

        self.group_timer = QGroupBox()

        self.grid_timer = QGridLayout(self.group_timer)
     
        self.grid_timer.setContentsMargins(5,20,5,10)
           
        self.group_timer.setFont(s.font6)
        self.group_timer.setStyleSheet(s.Stylegroup)
        self.group_timer.setAlignment(Qt.AlignHCenter)
       
        self.group_timer.setCheckable(True)
        self.group_timer.setChecked(True)
        self.group_timer.setDisabled(False)  
       
        self.group_timer.setTitle(QCoreApplication.translate("MainWindow", 'Timer', None))

        self.bn_timer = QPushButton(self.group_timer)
        self.bn_timer.setText('Timer')
        self.bn_timer.setFont(s.font7)
        self.bn_timer.setStyleSheet(s.StyleButton_2)
        self.bn_timer.setCheckable(True)
        self.bn_timer.setEnabled(False)
     
        self.bn_timer_0 = QPushButton(self.group_timer)
        self.bn_timer_0.setText('Timer 0')
        self.bn_timer_0.setFont(s.font7)
        self.bn_timer_0.setStyleSheet(s.StyleButton_2)
        self.bn_timer_0.setCheckable(True)
        self.bn_timer_0.setEnabled(False)
       
        self.bn_timer_1 = QPushButton(self.group_timer)
        self.bn_timer_1.setText('Timer 1')
        self.bn_timer_1.setFont(s.font7)
        self.bn_timer_1.setStyleSheet(s.StyleButton_2)
        self.bn_timer_1.setCheckable(True)
        self.bn_timer_1.setEnabled(False)
       
        self.bn_timer_2 = QPushButton(self.group_timer)
        self.bn_timer_2.setText('Timer 2')
        self.bn_timer_2.setFont(s.font7)
        self.bn_timer_2.setStyleSheet(s.StyleButton_2)
        self.bn_timer_2.setCheckable(True)
        self.bn_timer_2.setEnabled(False)
        
        self.bn_timer_5 = QPushButton(self.group_timer)
        self.bn_timer_5.setText('Timer 5')
        self.bn_timer_5.setFont(s.font7)
        self.bn_timer_5.setStyleSheet(s.StyleButton_2)
        self.bn_timer_5.setCheckable(True)
        self.bn_timer_5.setEnabled(False)
        
      
        self.bn_timer_6 = QPushButton(self.group_timer)
        self.bn_timer_6.setText('Timer 6')
        self.bn_timer_6.setFont(s.font7)
        self.bn_timer_6.setStyleSheet(s.StyleButton_2)
        self.bn_timer_6.setCheckable(True)
        self.bn_timer_6.setEnabled(False)
      
        self.bn_timer_7 = QPushButton(self.group_timer)
        self.bn_timer_7.setText('Timer 7')
        self.bn_timer_7.setFont(s.font7)
        self.bn_timer_7.setStyleSheet(s.StyleButton_2)
        self.bn_timer_7.setCheckable(True)
        self.bn_timer_7.setEnabled(False)
        
        self.bn_timer_8 = QPushButton(self.group_timer)
        self.bn_timer_8.setText('Timer 8')
        self.bn_timer_8.setFont(s.font7)
        self.bn_timer_8.setStyleSheet(s.StyleButton_2)
        self.bn_timer_8.setCheckable(True)
        self.bn_timer_8.setEnabled(False)
      
        self.grid_timer.addWidget(self.bn_timer   , 0, 0, 1, 1)
        self.grid_timer.addWidget(self.bn_timer_0 , 1, 0, 1, 1)
        self.grid_timer.addWidget(self.bn_timer_1 , 2, 0, 1, 1)
        self.grid_timer.addWidget(self.bn_timer_2 , 0, 1, 1, 1)
        self.grid_timer.addWidget(self.bn_timer_6 , 1, 1, 1, 1)
        self.grid_timer.addWidget(self.bn_timer_7 , 2, 1, 1, 1)
        self.grid_timer.addWidget(self.bn_timer_5 , 0, 2, 1, 1)
        self.grid_timer.addWidget(self.bn_timer_8 , 1, 2, 1, 1)
        


        self.group_timer.setLayout(self.grid_timer)

        self.ver_page_timer_S7.addWidget(self.group_timer)

        #page_timer_S7  im Stack - Nummer 3
        self.stackedWidget_plc.addWidget(self.page_timer_S7)
        self.stackedWidget_plc.setMaximumHeight(self.linux4)

# -------------------------------------------------------------------------
# page_graphenauswahl
# -------------------------------------------------------------------------

        self.page_graphenauswahl = QWidget()
        self.page_graphenauswahl.setObjectName(u"page_graphenauswahl")
        self.page_graphenauswahl.setStyleSheet(u"background:rgb(91,90,90);")
       
        self.ver_page_graphenauswahl = QVBoxLayout(self.page_graphenauswahl)
        self.ver_page_graphenauswahl.setSpacing(0)
        self.ver_page_graphenauswahl.setObjectName(u"ver_page_graphenauswahl")
        self.ver_page_graphenauswahl.setContentsMargins(5, 5, 5, 5)

#--------------------------------------------------------------------------
#  GroupBox Plotterauswahl
#--------------------------------------------------------------------------

        self.group_Plotter = QGroupBox()

        self.hor_Plotter = QHBoxLayout(self.group_Plotter )

        self.hor_Plotter.setSpacing(5)
     
        self.group_Plotter.setFont(s.font6)
        self.group_Plotter.setStyleSheet(s.Stylegroup)
        self.group_Plotter.setAlignment(Qt.AlignHCenter)
        
        self.group_Plotter.setCheckable(False)
        self.group_Plotter.setChecked(False)
        self.group_Plotter.setDisabled(True)  #True

        self.group_Plotter.setTitle(QCoreApplication.translate("MainWindow", 'Plotterauswahl', None))

# -------------------------------------------------------------------------
#   RadioButton Matplotlib
# -------------------------------------------------------------------------

        self.matplotlib = QRadioButton(self.group_Plotter)
        self.matplotlib.setObjectName(u"matplotlib")

        self.matplotlib.setFont(s.font6)
        self.matplotlib.setStyleSheet(s.StyleRadio)

        self.matplotlib.setAutoRepeat(False)
        self.matplotlib.setAutoExclusive(True)

        self.matplotlib.setText(QCoreApplication.translate("MainWindow", u"matplotlib", None))

        self.hor_Plotter.addWidget(self.matplotlib)

# -------------------------------------------------------------------------
#   RadioButton Gpanel
# -------------------------------------------------------------------------

        self.gpanel = QRadioButton(self.group_Plotter)
        self.gpanel.setObjectName(u"gpanel")

        self.gpanel.setFont(s.font6)
        self.gpanel.setStyleSheet(s.StyleRadio)

        self.gpanel.setAutoRepeat(False)
        self.gpanel.setAutoExclusive(True)

        self.gpanel.setText(QCoreApplication.translate("MainWindow", u"Gpanel", None))

        self.hor_Plotter.addWidget(self.gpanel)

# -------------------------------------------------------------------------
#   RadioButton Graph
# -------------------------------------------------------------------------

        self.graph = QRadioButton(self.group_Plotter)
        self.graph.setObjectName(u"graph")

        self.graph.setFont(s.font6)
        self.graph.setStyleSheet(s.StyleRadio)

        self.graph.setAutoRepeat(False)
        self.graph.setAutoExclusive(True)
        self.graph.setChecked(True)

        self.graph.setText(QCoreApplication.translate("MainWindow", u"Graph", None))

        self.hor_Plotter.addWidget(self.graph)

        #group Plotter einfuegen

        self.group_Plotter.setLayout(self.hor_Plotter)

        self.ver_page_graphenauswahl.addWidget(self.group_Plotter)

        #page_graphenauswahl  im Stack - Nummer 4
        self.stackedWidget_plc.addWidget(self.page_graphenauswahl)
        self.stackedWidget_plc.setMaximumHeight(self.linux4)

# -------------------------------------------------------------------------
# page_dial
# -------------------------------------------------------------------------

        self.page_dial = QWidget()
        self.page_dial.setObjectName(u"page_dial")
        self.page_dial.setStyleSheet(u"background:rgb(91,90,90);")
       
        self.ver_page_dial = QVBoxLayout(self.page_dial)
        self.ver_page_dial.setSpacing(0)
        self.ver_page_dial.setObjectName(u"ver_page_dial")
        self.ver_page_dial.setContentsMargins(5,5,5,5)
        
#--------------------------------------------------------------------------
#  GroupBox ValueDial
#--------------------------------------------------------------------------

        self.group_dialer = QGroupBox() 

        self.hor_dialer = QHBoxLayout()

        self.hor_dialer.setSpacing(25)
        self.hor_dialer.setContentsMargins(0,0,0,0)

        self.group_dialer.setFont(s.font6)
        self.group_dialer.setStyleSheet(s.Stylegroup)
        self.group_dialer.setAlignment(Qt.AlignHCenter)
        
        self.group_dialer.setCheckable(False)
        self.group_dialer.setChecked(False)
        self.group_dialer.setDisabled(True)  #True

        self.group_dialer.setTitle(QCoreApplication.translate("MainWindow", 'Dialer', None))

#--------------------------------------------------------------------------
#  Dial1 einfuegen
#--------------------------------------------------------------------------

        self.dreh1 = ValueDial(minimum=-5, maximum=5, value=0, notchesVisible=True )
        self.dreh1.setMinimumSize(QSize(5, 5))
        self.dreh1.setMaximumSize(QSize(150, 150))

        self.dreh1.close()
        self.hor_dialer.addWidget(self.dreh1)
        
#--------------------------------------------------------------------------
#  Dial2 einfuegen
#--------------------------------------------------------------------------

        self.dreh2 = ValueDial(minimum=-5, maximum=5, value=0, notchesVisible=True )
        self.dreh2.setMinimumSize(QSize(5, 5))
        self.dreh2.setMaximumSize(QSize(150, 150))

        self.hor_dialer.addWidget(self.dreh2)

        #Gruppe Dialer einfuegen
        #in group einfuegen
        self.group_dialer.setLayout(self.hor_dialer)
        
        self.ver_page_dial.addWidget(self.group_dialer)

        #page_dial  im Stack - Nummer 5
        self.stackedWidget_plc.addWidget(self.page_dial)
        self.stackedWidget_plc.setMaximumHeight(self.linux4)
    
# -------------------------------------------------------------------------
# page gpanel
# -------------------------------------------------------------------------

        self.page_gpanel = QWidget()
        self.page_gpanel.setObjectName(u"page_gpanel")
        self.page_gpanel.setStyleSheet(u"background:rgb(91,90,90);")      #91,90,90

        self.horizontalLayout_34 = QHBoxLayout(self.page_gpanel)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setSpacing(0) #setContentsMargins(0,0,0,0)
        self.horizontalLayout_34.setContentsMargins(0,0,0,0)


        #self.win2 = gp.GPanel(icon='icons/1x/icon.ico')

       
        #self.horizontalLayout_34.addWidget(self.win2)

# -------------------------------------------------------------------------
# page Daten
# -------------------------------------------------------------------------

        self.page_daten = QWidget()
        self.page_daten.setObjectName(u"page_daten")
        self.page_daten.setStyleSheet(u"background:rgb(91,90,90);")

        self.page_daten_2 = QWidget()
        self.page_daten_2.setObjectName(u"page_daten_2")
        self.page_daten_2.setStyleSheet(u"background:rgb(91,90,90);")
        #self.page_daten_2.setMinimumSize(QSize(500,500))
        self.page_daten_2.setContentsMargins(0,0,0,0)
                
        self.frame_daten_scroll = QFrame(self.page_daten_2)
        self.frame_daten_scroll.setObjectName(u"frame_daten_scroll")
        self.frame_daten_scroll.setStyleSheet(u"background:rgb(91,90,90);")
        self.frame_daten_scroll.setFrameShape(QFrame.StyledPanel)
        self.frame_daten_scroll.setFrameShadow(QFrame.Raised)
      
        self.frame_daten_scroll1 = QFrame(self.page_daten_2)
        self.frame_daten_scroll1.setObjectName(u"frame_daten_scroll1")
        self.frame_daten_scroll1.setStyleSheet(u"background:rgb(91,90,90);")
        self.frame_daten_scroll1.setFrameShape(QFrame.StyledPanel)
        self.frame_daten_scroll1.setFrameShadow(QFrame.Raised)
          
        self.daten_scroll = QScrollArea()   
        
        self.daten_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.daten_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.daten_scroll.setWidgetResizable(True)

        #ScrollBar
        self.page_daten_scroll = QScrollBar(self.frame_daten_scroll)  
        self.page_daten_scroll.setOrientation(Qt.Horizontal)
        self.page_daten_scroll.setInvertedControls(True)
        self.page_daten_scroll.setObjectName(u"page_daten_scroll")
        self.page_daten_scroll.setSizeIncrement(5,5)
        self.page_daten_scroll.setStyleSheet(s.StyleScrollBar_hor)
        self.page_daten_scroll.setMinimumHeight(self.linux32)

        #ScrollBar
        self.page_daten_scroll1 = QScrollBar(self.frame_daten_scroll1)  
        self.page_daten_scroll1.setOrientation(Qt.Vertical)
        self.page_daten_scroll1.setInvertedControls(False)
        self.page_daten_scroll1.setObjectName(u"page_daten_scroll1")
        self.page_daten_scroll1.setStyleSheet(s.StyleScrollBar_ver)
        self.page_daten_scroll1.setMinimumHeight(self.linux32)
     
        self.daten_scroll.setHorizontalScrollBar(self.page_daten_scroll)
        self.daten_scroll.setVerticalScrollBar(self.page_daten_scroll1)

        self.ver_daten = QVBoxLayout(self.page_daten)
        self.ver_daten.setObjectName(u"ver_daten")
        self.ver_daten.setContentsMargins(0,0,0,0)
        self.ver_daten.setSpacing(0)

        self.vbox_daten = QVBoxLayout(self.page_daten_2)
        self.vbox_daten.setObjectName(u"vbox_daten")
        self.vbox_daten.setContentsMargins(0, 0, 0, 0)
        self.vbox_daten.setSpacing(0)

        self.hor_daten = QHBoxLayout()
        self.hor_daten.setObjectName(u"hor_daten")
        self.hor_daten.setContentsMargins(0, 0, 0, 0)
        self.hor_daten.setSpacing(5)

        
        Group_Box1=('Box1', 'Box2', 'Box3', 'Box4', 'Box5', 'Box6', 'Box7', 'Box8') 
        Group_lineBox1=(Def.Box1[0], Def.Box1[1], Def.Box1[2], Def.Box1[3], Def.Box1[4], Def.Box1[5], Def.Box1[6], Def.Box1[7])
        self.G_Box1      = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True, setlabel1=Group_Box1, setline=Group_lineBox1)
        self.G_Box1.setTitle('Box1')

        Group_Box2=('Box9', 'Box10', 'Box11', 'Box12', 'Box13', 'Box14', 'Box15', 'Box16') 
        Group_lineBox2=(Def.Box2[0], Def.Box2[1], Def.Box2[2], Def.Box2[3], Def.Box2[4], Def.Box2[5], Def.Box2[6], Def.Box2[7])
        self.G_Box2      = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True,setlabel1=Group_Box2, setline=Group_lineBox2)
        self.G_Box2.setTitle('Box2')    

        Group_Real1=('Leit:', 'Ant1:', 'Ant2:', 'Ant3:', 'Ant4:', 'Ant5:', 'Ant6:', 'Ant7:') 
        Group_LineReal=(Def.Real[0], Def.Real[1], Def.Real[2], Def.Real[3], Def.Real[4], Def.Real[5], Def.Real[6], Def.Real[7])
        self.D_Real      = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True, setlabel1=Group_Real1, setline=Group_LineReal)
        self.D_Real.setTitle('Antriebe')
       

        Group_Integer1=('Int1:', 'Int2:', 'Int3:', 'Int4:', 'Int5:', 'Int6:', 'Int7:', 'Int8:') 
        self.Integer1  = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True, setlabel1=Group_Integer1)
        self.Integer1.setTitle('Integer1')
        self.Integer1.setLineText(Def.Integer1)

        Group_Integer1=('Int9:', 'Int10:', 'Int11:', 'Int12:', 'Int13:', 'Int14:', 'Int15:', 'Int16:') 
        self.Integer2  = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True, setlabel1=Group_Integer1)
        self.Integer2.setTitle('Integer2')
        self.Integer2.setLineText(Def.Integer2)

        Group_Real1=('Real1:', 'Real2:', 'Real3:', 'Real4:', 'Real5:', 'Real6:', 'Real7:', 'Real8:') 
        self.Real1      = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True,setlabel1=Group_Real1 )
        self.Real1.setTitle('Real1')
        self.Real1.setLineText(Def.Real1)

        Group_Real1=('Real9:', 'Real10:', 'Real11:', 'Real12:', 'Real13:', 'Real14:', 'Real15:', 'Real16:') 
        self.Real2      = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True,setlabel1=Group_Real1 )
        self.Real2.setTitle('Real2')
        self.Real2.setLineText(Def.Real2)

        Group_Word1=('Word1:', 'Word2:', 'Word3:', 'Word4:', 'Word5:', 'Word6:', 'Word7:', 'Word8:') 
        self.Word1      = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True, setlabel1=Group_Word1 )
        self.Word1.setTitle('Word1')
        self.Word1.setLineText(Def.Word1)

        Group_Word2=('Word9:', 'Word10:', 'Word11:', 'Word12:', 'Word13:', 'Word14:', 'Word15:', 'Word16:') 
        self.Word2      = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True,setlabel1=Group_Word2 )
        self.Word2.setTitle('Word2')
        self.Word2.setLineText(Def.Word2)

        Group_Word3=('Word17:', 'Word18:', 'Word19:', 'Word20:', 'Word21:', 'Word22:', 'Word23:', 'Word24') 
        self.Word3      = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True,setlabel1=Group_Word3 )
        self.Word3.setTitle('Word3')
        self.Word3.setLineText(Def.Word3)

        Group_Word4=('Word25:', 'Word26:', 'Word27:', 'Word28:', 'Word29:', 'Word30:', 'Word31:', 'Word32') 
        self.Word4      = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True,setlabel1=Group_Word4 )
        self.Word4.setTitle('Word4')
        self.Word4.setLineText(Def.Word4)

        Group_DB1=('DB1:', 'DB2:', 'DB3:', 'DB4:', 'DB5:', 'DB6:', 'DB7:', 'DB8') 
        self.DB1      = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True,setlabel1=Group_DB1 )
        self.DB1.setTitle('DB1')
        self.DB1.setLineText(Def.DB1)

        Group_DB2=('DB9:', 'DB10:', 'DB11:', 'DB12:', 'DB13:', 'DB14', 'DB15:', 'DB16') 
        self.DB2      = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True,setlabel1=Group_DB2 )
        self.DB2.setTitle('DB2')
        self.DB2.setLineText(Def.DB2)

        Group_DB3=('DB17:', 'DB18:', 'DB19:', 'DB20:', 'DB21:', 'DB22', 'DB23:', 'DB24') 
        self.DB3      = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True,setlabel1=Group_DB3 )
        self.DB3.setTitle('DB3')
        self.DB3.setLineText(Def.DB3)

        Group_DB4=('DB25:', 'DB26:', 'DB27:', 'DB28:', 'DB29:', 'DB30', 'DB31:', 'DB32') 
        self.DB4      = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True,setlabel1=Group_DB4 )
        self.DB4.setTitle('DB4')
        self.DB4.setLineText(Def.DB4)

        self.sbox  = GroupCheckBox( minimumSize=(QSize(self.linuxW8, self.linux1_5)), maximumSize=(QSize(self.linuxW8, 16777215)), value=16)
        self.sbox.setTitle('Auswahl')
        self.sbox.setTitleCheck(Def.liste_auswahl)
        self.sbox.groupCheckBox.setEnabled(True)

        Group_Bed1=('T_Aus', 'A_Aus', 'T_Stop', 'A_Stop', 'T_Hand', 'A_Hand', 'T_Auto', 'A_Auto') 
        Group_lineBed1=(Def.Bed[0], Def.Bed[1], Def.Bed[2], Def.Bed[3], Def.Bed[4], Def.Bed[5], Def.Bed[6], Def.Bed[7])
       
        self.G_Bed1 = GroupLine( minimumSize=(QSize(self.linuxW5, self.linux1_5)), maximumSize=(QSize(self.linuxW6, 16777215)), value=8, setcheck=True,setlabel1=Group_Bed1, setline=Group_lineBed1)
        self.G_Bed1.setTitle('Bedienung')
        
        #unsichtbar
        self.D_Real.setVisible(False)
        self.G_Box1.setVisible(False)
        self.G_Box2.setVisible(False)
        self.G_Bed1.setVisible(False)
        self.Real1.setVisible(False)
        self.Real2.setVisible(False)
        self.Integer1.setVisible(False)
        self.Integer2.setVisible(False)
        self.Word1.setVisible(False)
        self.Word2.setVisible(False)
        self.Word3.setVisible(False)
        self.Word4.setVisible(False)
        self.DB1.setVisible(False)
        self.DB2.setVisible(False)
        self.DB3.setVisible(False)
        self.DB4.setVisible(False)

        #Frame Scroll tree
        self.frame_tree_scroll = QFrame()
        self.frame_tree_scroll.setObjectName(u"frame_tree_scroll")
        self.frame_tree_scroll.setStyleSheet(u"background:rgb(91,90,90);")
        self.frame_tree_scroll.setFrameShape(QFrame.StyledPanel)
        self.frame_tree_scroll.setFrameShadow(QFrame.Raised)
        
        #ScrollBar
        self.tree_scroll = QScrollBar(self.frame_tree_scroll)  
        self.tree_scroll.setOrientation(Qt.Vertical)
        
        self.tree_scroll.setInvertedControls(True)

        self.tree_scroll.setObjectName(u"tree_scroll")
        self.tree_scroll.setSizeIncrement(5,5)
        self.tree_scroll.setStyleSheet(s.StyleScrollBar_ver)

         
        header_list =['  Absolut  ', '  Symbol  ', 'Farbe  ' , '  Online  ', 'Zahlenanzeige', 'Signalanzeige']
        
        header = QTreeWidgetItem(header_list)  
       
        #header.setTextColor(0, QColor('#000000') )
        header.setFirstColumnSpanned(True)
        header.setDisabled(False)
        header.setToolTip(0, u'Absolute Adresse PLC')
        header.setTextAlignment(0, Qt.AlignCenter)
        header.setExpanded(True)
        #header.setIcon(0, QIcon("icons/1x/icon.ico"))
        
        self.tree       = QTreeWidget()
        self.tree.setMinimumWidth(self.linuxW2)
        self.tree.setContentsMargins(5,5,5,5)
            
        self.tree.setFont(s.font6)
        self.tree.setStyleSheet(s.Styletree)
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tree.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tree.setVerticalScrollBar(self.tree_scroll)
        self.tree.setHeaderItem(header)
        self.tree.setColumnWidth(0,int(self.tree.width()/5))
        self.tree.setColumnWidth(1,int(self.tree.width()/5))
        self.tree.setColumnWidth(2,int(self.tree.width()/16))
        self.tree.setColumnWidth(3,int(self.tree.width()/12))
        self.tree.setColumnWidth(4,int(self.tree.width()/7))
        self.tree.setColumnWidth(5,int(self.tree.width()/7))
        self.tree.setEnabled(True)           #deaktiviert (False -> Bedienung aus)


#--------------------------------------------------------------------------
# QTextEdit einfuegen
#--------------------------------------------------------------------------
        
        self.textedit = QListWidget()
        self.textedit.setFont(s.font6) 
        self.textedit.setMinimumWidth(150)
        self.textedit.setContentsMargins(5,5,5,5)
              
        self.textedit2 = QListWidget()
        self.textedit2.setFont(s.font6) 
        self.textedit2.setMinimumWidth(50)
        self.textedit2.setContentsMargins(5,5,5,5)

        self.textedit3 = QListWidget()
        self.textedit3.setFont(s.font6) 
        self.textedit3.setMinimumWidth(25)
        self.textedit3.setContentsMargins(5,5,5,5)
        
                            
        self.hor_daten.addWidget(self.sbox)
        self.hor_daten.addWidget(self.D_Real)
        self.hor_daten.addWidget(self.G_Box1)
        self.hor_daten.addWidget(self.G_Box2)
        self.hor_daten.addWidget(self.G_Bed1)
        self.hor_daten.addWidget(self.Real1)
        self.hor_daten.addWidget(self.Real2)
        self.hor_daten.addWidget(self.Integer1)
        self.hor_daten.addWidget(self.Integer2)
        self.hor_daten.addWidget(self.Word1)
        self.hor_daten.addWidget(self.Word2)
        self.hor_daten.addWidget(self.Word3)
        self.hor_daten.addWidget(self.Word4)
        self.hor_daten.addWidget(self.DB1)
        self.hor_daten.addWidget(self.DB2)
        self.hor_daten.addWidget(self.DB3)
        self.hor_daten.addWidget(self.DB4)
        self.hor_daten.addWidget(self.tree)
        #self.hor_daten.addWidget(self.textedit)
        #self.hor_daten.addWidget(self.textedit2)
        #self.hor_daten.addWidget(self.textedit3)

        self.hor_Spacer_daten = QSpacerItem(1000, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hor_daten.addItem(self.hor_Spacer_daten)
        self.hor_daten.addWidget(self.page_daten_scroll1)
        
#--------------------------------------------------------------------------
# Daten- Frame Edit / Save Button
#--------------------------------------------------------------------------

        self.frame_Daten = QFrame(self.page_daten)                                 
        self.frame_Daten.setObjectName(u"frame_Daten")
        self.frame_Daten.setMaximumHeight(self.linux4)
        self.frame_Daten.setFrameShape(QFrame.StyledPanel)
        self.frame_Daten.setFrameShadow(QFrame.Raised)

#--------------------------------------------------------------------------
# Daten- Label Absolut einfuegen
#--------------------------------------------------------------------------

        self.lab_absolut = QLabel()
        self.lab_absolut.setMinimumHeight(self.linux32)
        self.lab_absolut.setMaximumHeight(self.linux16)
        self.lab_absolut.setFont(s.font6)
        self.lab_absolut.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_absolut.setAlignment(Qt.AlignLeft)

        self.lab_absolut.setText(QCoreApplication.translate("MainWindow", u"Absolut: ", None))

        self.line_absolut = QLineEdit()
        self.line_absolut.setObjectName(u"line_absolut")
        self.line_absolut.setFont(s.font6)
        self.line_absolut.setAlignment(Qt.AlignCenter)
        self.line_absolut.setMinimumHeight(self.linux32)
        self.line_absolut.setMaximumHeight(self.linux16)
        self.line_absolut.setStyleSheet(s.StyleLineEdit)
        self.line_absolut.setEnabled(True)

#--------------------------------------------------------------------------
# Daten- Label Symbol einfuegen
#--------------------------------------------------------------------------

        self.lab_symbol = QLabel()
        self.lab_symbol.setMinimumHeight(self.linux32)
        self.lab_symbol.setMaximumHeight(self.linux16)
        self.lab_symbol.setFont(s.font6)
        self.lab_symbol.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_symbol.setAlignment(Qt.AlignLeft)

        self.lab_symbol.setText(QCoreApplication.translate("MainWindow", u"Symbol: ", None))

        self.line_symbol = QLineEdit()
        self.line_symbol.setObjectName(u"line_symbol")
        self.line_symbol.setFont(s.font6)
        self.line_symbol.setAlignment(Qt.AlignCenter)
        self.line_symbol.setMinimumHeight(self.linux32)
        self.line_symbol.setMaximumHeight(self.linux16)
       
        self.line_symbol.setStyleSheet(s.StyleLineEdit)
        self.line_symbol.setEnabled(True)

#--------------------------------------------------------------------------
# Button1 Layout Daten
#--------------------------------------------------------------------------
        
        self.frame_Button1_Daten = QFrame(self.page_daten)                                 
        self.frame_Button1_Daten.setObjectName(u"frame_Button1_Daten")
        
        self.frame_Button1_Daten.setFrameShape(QFrame.StyledPanel)
        self.frame_Button1_Daten.setFrameShadow(QFrame.Raised)
        
        self.hor_button1_daten = QHBoxLayout(self.frame_Button1_Daten)
        self.hor_button1_daten.setObjectName(u"hor_button1_daten")
        self.hor_button1_daten.setSpacing(0)
        self.hor_button1_daten.setContentsMargins(0, 0, 0, 0)

#--------------------------------------------------------------------------
# Button2 Layout Daten
#--------------------------------------------------------------------------
        
        self.frame_Button2_Daten = QFrame(self.page_daten)                                 
        self.frame_Button2_Daten.setObjectName(u"frame_Button2_Daten")
        
        self.frame_Button2_Daten.setFrameShape(QFrame.StyledPanel)
        self.frame_Button2_Daten.setFrameShadow(QFrame.Raised)
        
        self.hor_button2_daten = QHBoxLayout(self.frame_Button2_Daten)
        self.hor_button2_daten.setObjectName(u"hor_button2_daten")
        self.hor_button2_daten.setSpacing(0)
        self.hor_button2_daten.setContentsMargins(0, 0, 0, 0)

#--------------------------------------------------------------------------
# Daten- Button Check einfuegen
#--------------------------------------------------------------------------

        self.bn_check_Daten = QPushButton()
        self.bn_check_Daten.setObjectName(u"bn_check_Daten")
        self.bn_check_Daten.setMinimumHeight(self.linux16)
        self.bn_check_Daten.setMaximumHeight(self.linux10)
        self.bn_check_Daten.setMinimumWidth(self.linux10)
        
        icon94 = QIcon()
        icon94.addFile(u"icons/1x/cil-circle.ico", QSize(), QIcon.Normal, QIcon.Off)
        icon94.addFile(u"icons/1x/cil-check-circle.ico", QSize(), QIcon.Normal, QIcon.On)
        
        self.bn_check_Daten.setIcon(icon94)
        self.bn_check_Daten.setIconSize(QSize(self.linux20, self.linux20))
   

        self.bn_check_Daten.setFont(s.font6)
        self.bn_check_Daten.setStyleSheet(s.StyleButton11)
        self.bn_check_Daten.setCheckable(True)

#--------------------------------------------------------------------------
# Daten- Button Reserve einfuegen
#--------------------------------------------------------------------------

        self.bn_auswahl_Daten = QPushButton()
        self.bn_auswahl_Daten.setObjectName(u"bn_auswahl_Daten")
        self.bn_auswahl_Daten.setMinimumHeight(self.linux16)
        self.bn_auswahl_Daten.setMaximumHeight(self.linux10)
        
        icon95 = QIcon()
        icon95.addFile(u"icons/1x/cil-media-stop.ico", QSize(), QIcon.Normal, QIcon.On)
        icon95.addFile(u"icons/1x/cil-check-alt.ico", QSize(), QIcon.Normal, QIcon.Off)
       
        
        self.bn_auswahl_Daten.setIcon(icon95)
        self.bn_auswahl_Daten.setIconSize(QSize(self.linux20, self.linux20))
   
        self.bn_auswahl_Daten.setFont(s.font6)
        self.bn_auswahl_Daten.setStyleSheet(s.StyleButton11)
        self.bn_auswahl_Daten.setCheckable(True)

#--------------------------------------------------------------------------
# Daten- Button Edit einfuegen
#--------------------------------------------------------------------------

        self.bn_edit_Daten = QPushButton()
        self.bn_edit_Daten.setObjectName(u"bn_edit_Daten")
        self.bn_edit_Daten.setMinimumHeight(self.linux16)
        self.bn_edit_Daten.setMaximumHeight(self.linux10)
   
        self.bn_edit_Daten.setFont(s.font6)
        self.bn_edit_Daten.setStyleSheet(s.StyleButton)
        self.bn_edit_Daten.setText('Edit')

#-------------------------------------------------------------------------
# Daten- Button einfuegen
#-------------------------------------------------------------------------

        self.bn_einfuegen_Daten = QPushButton()
        self.bn_einfuegen_Daten.setObjectName(u"bn_einfuegen_Daten")
        self.bn_einfuegen_Daten.setMinimumHeight(self.linux16)
        self.bn_einfuegen_Daten.setMaximumHeight(self.linux10)
    
        self.bn_einfuegen_Daten.setFont(s.font6)
        self.bn_einfuegen_Daten.setStyleSheet(s.StyleButton)
        
        icon93 = QIcon()
        icon93.addFile(u"icons/1x/cil-cloud-upload.ico", QSize(), QIcon.Normal, QIcon.Off)
        
        
        self.bn_einfuegen_Daten.setIcon(icon93)
        self.bn_einfuegen_Daten.setIconSize(QSize(self.linux20, self.linux20))
        

#--------------------------------------------------------------------------
# Daten- Button loeschen
#--------------------------------------------------------------------------

        self.bn_loeschen_Daten = QPushButton()
        self.bn_loeschen_Daten.setObjectName(u"bn_loeschen_Daten")
        self.bn_loeschen_Daten.setMinimumHeight(self.linux16)
        self.bn_loeschen_Daten.setMaximumHeight(self.linux10)
     
        self.bn_loeschen_Daten.setFont(s.font6)
        self.bn_loeschen_Daten.setStyleSheet(s.StyleButton)
        
        icon92 = QIcon()
        icon92.addFile(u"icons/1x/cil-cloud-download.ico", QSize(), QIcon.Normal, QIcon.Off)
        
        self.bn_loeschen_Daten.setIcon(icon92)
        self.bn_loeschen_Daten.setIconSize(QSize(self.linux20, self.linux20))
        
        
#--------------------------------------------------------------------------
# Daten - Button Save einfuegen
#--------------------------------------------------------------------------

        self.bn_save_Daten = QPushButton()
        self.bn_save_Daten.setObjectName(u"bn_save_Daten")
        self.bn_save_Daten.setMinimumHeight(self.linux16)
        self.bn_save_Daten.setMaximumHeight(self.linux10)
   
        self.bn_save_Daten.setFont(s.font6)
        self.bn_save_Daten.setStyleSheet(s.StyleButton)
        self.bn_save_Daten.setText('Save')
        self.bn_save_Daten.setEnabled(False)
        
#--------------------------------------------------------------------------
# Daten - Button Laden einfuegen
#--------------------------------------------------------------------------

        self.bn_laden_Daten = QPushButton()
        self.bn_laden_Daten.setObjectName(u"bn_laden_Daten")
        self.bn_laden_Daten.setMinimumHeight(self.linux16)
        self.bn_laden_Daten.setMaximumHeight(self.linux10)
   
        self.bn_laden_Daten.setFont(s.font6)
        self.bn_laden_Daten.setStyleSheet(s.StyleButton)
        self.bn_laden_Daten.setText('Laden')
        
#--------------------------------------------------------------------------
# Daten - Button Speichern einfuegen
#--------------------------------------------------------------------------

        self.bn_speichern_Daten = QPushButton()
        self.bn_speichern_Daten.setObjectName(u"bn_speichern_Daten")
        self.bn_speichern_Daten.setMinimumHeight(self.linux16)
        self.bn_speichern_Daten.setMaximumHeight(self.linux10)
   
        self.bn_speichern_Daten.setFont(s.font6)
        self.bn_speichern_Daten.setStyleSheet(s.StyleButton)
        self.bn_speichern_Daten.setText('Speichern')
        
        
        #Button1 einfuegen
        self.hor_button1_daten.addWidget(self.bn_einfuegen_Daten)
        self.hor_button1_daten.addWidget(self.bn_loeschen_Daten)
        self.hor_button1_daten.addWidget(self.bn_laden_Daten)
        self.hor_button1_daten.addWidget(self.bn_speichern_Daten)
        
        self.ver_daten.addWidget(self.frame_Button1_Daten)
        
        

        self.vbox_daten.addLayout(self.hor_daten)
        self.ver_spacer_daten4 = QSpacerItem(0, 0 , QSizePolicy.MinimumExpanding,  QSizePolicy.Minimum)
        self.vbox_daten.addItem(self.ver_spacer_daten4)
        self.vbox_daten.addWidget(self.page_daten_scroll)
        
        self.page_daten_2.setLayout(self.vbox_daten)
        self.daten_scroll.setWidget(self.page_daten_2) 
      
        self.ver_daten.addWidget(self.daten_scroll)
        
        # Button2
        self.hor_button2_daten.addWidget(self.bn_auswahl_Daten )
        self.hor_button2_daten.addWidget(self.bn_check_Daten )

        self.hor_button2_daten.addWidget(self.bn_edit_Daten )
        self.hor_button2_daten.addWidget(self.bn_save_Daten )
        
        
        
        self.grid_daten = QGridLayout(self.frame_Daten)

        self.grid_daten.addWidget(self.lab_absolut , 2,0,1,1)
        self.grid_daten.addWidget(self.line_absolut , 2,2,1,1)
        self.grid_daten.addWidget(self.lab_symbol , 3,0,1,1)
        self.grid_daten.addWidget(self.line_symbol , 3,2,1,1)

        self.ver_daten.addWidget(self.frame_Daten)
        self.ver_daten.addWidget(self.frame_Button2_Daten)
    

# -------------------------------------------------------------------------
# page Live
# -------------------------------------------------------------------------l

        self.page_live = QWidget()
        self.page_live.setObjectName(u"page_live")
        self.page_live.setStyleSheet(u"background:rgb(91,90,90);")
    
        self.ver_page_live = QVBoxLayout(self.page_live)
        self.ver_page_live.setObjectName(u"ver_page_live")
        self.ver_page_live.setSpacing(0)
        self.ver_page_live.setContentsMargins(0, 0, 0, 0)
        

        self.hor_page_live = QHBoxLayout()
        self.hor_page_live.setObjectName(u"hor_page_live")
        self.hor_page_live.setSpacing(0)
        self.hor_page_live.setContentsMargins(0, 0, 0, 0)
        

        self.stackedWidget_live = QStackedWidget(self.page_live)
        self.stackedWidget_live.setObjectName(u'stackedWidget_live')
        self.stackedWidget_live.setStyleSheet('background:rgb(91,90,90);')

        #neu ab 6.06.2023 -Testversuch
        self.grafi = [] 
        
        self.pltc   = []    #Platzhalter Plots live Graph
        self.pltc_lab1 = []
        self.pltc_lab2 = []
        #self.l   = []    #Platzhalter Plots label live Graph
        #self.l2  = []    #Platzhalter Plots labe vor live Graph 270Grad
        
        self.dat = []
        self.curve = []
        self.farbe = []

        self.plt = []
        self.lab1 =[]
        self.lab2 =[]
        self.winc=[]

# -------------------------------------------------------------------------
# Frame Live Graph Region
# -------------------------------------------------------------------------

        self.frame_Region = QFrame(self.page_live)                                 
        self.frame_Region.setObjectName(u"frame_Region")
        self.frame_Region.setMaximumHeight(self.linux9)
        self.frame_Region.setFrameShape(QFrame.StyledPanel)
        self.frame_Region.setFrameShadow(QFrame.Raised)
        
        self.ver_Region = QVBoxLayout(self.frame_Region)
        self.ver_Region.setObjectName(u"ver_Region")
        self.ver_Region.setContentsMargins(0, 0, 0, 0)
        self.ver_Region.setSpacing(0)

        self.win = pg.GraphicsLayoutWidget(size=None)
        self.win.ci.setSpacing(0)
        self.win.ci.setContentsMargins(0, 0, 0, 0)
        self.win.setBackground(QColor('#705050'))  
        #self.win.ci.setBorder((51, 51, 51),width=4)
        self.win.setObjectName('win')
        #self.winc.append(self.win)
        #self.stackedWidget_live.addWidget(self.winc[0])
        self.ver_Region.addWidget(self.win)

        for c in range(1,10):
            win = pg.GraphicsLayoutWidget(size=None)
            win.ci.setSpacing(0)
            win.ci.setContentsMargins(0, 0, 0, 0)
            win.setBackground(QColor('#5B5A5A')) 
            win.setObjectName('live'+str(c))
            self.winc.append(win)
            self.pltc.append ([])
            self.pltc_lab1.append([])
            self.pltc_lab2.append([])
            self.stackedWidget_live.addWidget(self.winc[c-1])
        

        self.vb = QCustomViewBox(enableMenu=True)
      
        #initialisieren (live daten)
        self.curves2 = []
       
        self.ptr5 = 0
        
        #Frame Scroll live

        self.frame_live_scroll = QFrame()
        self.frame_live_scroll.setObjectName(u"frame_live_scroll")
        self.frame_live_scroll.setStyleSheet(u"background:rgb(91,90,90);")
        self.frame_live_scroll.setFrameShape(QFrame.StyledPanel)
        self.frame_live_scroll.setFrameShadow(QFrame.Raised)

        #ScrollBar
        self.hor_bar_live = QScrollBar(self.frame_scroll)  
        self.hor_bar_live.setOrientation(Qt.Horizontal)
        
        self.hor_bar_live.setInvertedControls(True)

        self.hor_bar_live.setObjectName(u"hor_bar_live")
        self.hor_bar_live.setSizeIncrement(5,5)
        self.hor_bar_live.setStyleSheet(s.StyleScrollBar_hor)
        

        #ScrollBar
        self.ver_bar_live = QScrollBar(self.frame_live_scroll)  
        self.ver_bar_live.setOrientation(Qt.Vertical)
        
        self.ver_bar_live.setInvertedControls(True)

        self.ver_bar_live.setObjectName(u"ver_bar_live")
        self.ver_bar_live.setSizeIncrement(5,5)
        self.ver_bar_live.setStyleSheet(s.StyleScrollBar_ver)
        

        #Scrollfunktion einbauen
        self.scroll_live = QScrollArea()   
        
        self.scroll_live.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_live.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_live.setWidgetResizable(True)
        
        self.scroll_live.setHorizontalScrollBar(self.hor_bar_live)
        self.scroll_live.setVerticalScrollBar(self.ver_bar_live)
        
        self.frame_live_menu = QFrame(self.page_live)
        self.frame_live_menu.setObjectName(u"frame_live_menu")
        self.frame_live_menu.setMaximumSize(QSize(16777215, self.linux16))
        self.frame_live_menu.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_live_menu.setFrameShape(QFrame.NoFrame)
        self.frame_live_menu.setFrameShadow(QFrame.Plain)

        self.hor_live_menu= QHBoxLayout(self.frame_live_menu)
        self.hor_live_menu.setSpacing(0)
        self.hor_live_menu.setObjectName(u"hor_Einstellungen_menu")
        self.hor_live_menu.setContentsMargins(0, 0, 0, 0)

        self.frame_prev_live = QFrame(self.frame_live_menu)
        self.frame_prev_live.setObjectName(u"frame_prev_live")
        
        self.frame_prev_live.setMaximumHeight(self.linux16)
        
        self.frame_prev_live.setFrameShape(QFrame.NoFrame)
        self.frame_prev_live.setFrameShadow(QFrame.Plain)
        
        self.hor_prev_live = QHBoxLayout(self.frame_prev_live)
        self.hor_prev_live.setSpacing(0)
        self.hor_prev_live.setObjectName(u"hor_prev_live")
        self.hor_prev_live.setContentsMargins(0, 0, 0, 0)
        
        self.bn_prev_live = QPushButton()
        self.bn_prev_live.setObjectName(u"bn_prev_live")
        self.bn_prev_live.setMinimumHeight(self.linux16)
        
        self.bn_prev_live.setStyleSheet(s.StyleButton)
        
        icon97 = QIcon()
        icon97.addFile(u"icons/1x/cil-chevron-double-left.ico", QSize(), QIcon.Normal, QIcon.Off)
        
        self.bn_prev_live.setIcon(icon97)

        self.bn_prev_live.setFlat(True)
        self.bn_prev_live.setText('')
        
        self.hor_prev_live.addWidget(self.bn_prev_live)

        self.hor_live_menu.addWidget(self.frame_prev_live)
        
        #Button next
        self.frame_next_live = QFrame()
        self.frame_next_live.setObjectName(u"frame_next_live")
        
        self.frame_next_live.setMaximumHeight( self.linux16)
        self.frame_next_live.setFrameShape(QFrame.NoFrame)
        self.frame_next_live.setFrameShadow(QFrame.Plain)
        
        self.hor_next_live = QHBoxLayout(self.frame_next_live)
        self.hor_next_live.setSpacing(10)
        self.hor_next_live.setObjectName(u"hor_next_live")
        self.hor_next_live.setContentsMargins(0, 0, 0, 0)
        
        self.bn_next_live = QPushButton()
        self.bn_next_live.setObjectName(u"bn_next_live")
        self.bn_next_live.setMinimumHeight( self.linux16)
        self.bn_next_live.setStyleSheet(s.StyleButton)
        
        icon98 = QIcon()
        icon98.addFile(u"icons/1x/cil-chevron-double-right.ico", QSize(), QIcon.Normal, QIcon.Off)
        
        self.bn_next_live.setIcon(icon98)
        

        self.bn_next_live.setFlat(True)
        self.bn_next_live.setText('')
        
        self.hor_next_live.addWidget(self.bn_next_live)
        
        # Seite Nummer 0 bis 5
        seite = 0
        self.lab_seite_live = QLabel()
        self.lab_seite_live.setText(str(seite))
        self.lab_seite_live.setStyleSheet(s.StyleLabel1)
        self.lab_seite_live.setFont(s.font7)
        self.lab_seite_live.setAlignment(Qt.AlignCenter)
        
        self.hor_live_menu.addWidget(self.lab_seite_live)
        
        
        # Seite Name 
        page = 'live1'
        self.lab_name_live = QLabel()
        self.lab_name_live.setText(page)
        self.lab_name_live.setStyleSheet(s.StyleLabel1)
        self.lab_name_live.setFont(s.font7)
        self.lab_name_live.setAlignment(Qt.AlignCenter)
        
        self.hor_live_menu.addWidget(self.lab_name_live)
        self.hor_live_menu.addWidget(self.frame_next_live)
       

        self.scroll_live.setWidget(self.stackedWidget_live)
        
        self.ver_page_live.addWidget(self.frame_Region)
        self.ver_page_live.addWidget(self.scroll_live)
        self.ver_page_live.addWidget(self.frame_live_menu)

# -------------------------------------------------------------------------
# page setting
# -------------------------------------------------------------------------

        self.page_setting = QWidget()
        self.page_setting.setObjectName(u"page_setting")
        self.page_setting.setStyleSheet(u"background:rgb(91,90,90);")

        self.ver_page_setting = QVBoxLayout(self.page_setting)
        self.ver_page_setting.setSpacing(0)
        self.ver_page_setting.setObjectName(u"ver_page_setting")
        self.ver_page_setting.setContentsMargins(0, 0, 0, 0)

        self.frame_Einstellungen_menu = QFrame(self.page_setting)
        self.frame_Einstellungen_menu.setObjectName(u"frame_Einstellungen_menu")
        self.frame_Einstellungen_menu.setMaximumSize(QSize(16777215, self.linux16))
        self.frame_Einstellungen_menu.setStyleSheet(u"background:rgb(91,90,90);")
        self.frame_Einstellungen_menu.setFrameShape(QFrame.NoFrame)
        self.frame_Einstellungen_menu.setFrameShadow(QFrame.Plain)

        self.hor_Einstellungen_menu= QHBoxLayout(self.frame_Einstellungen_menu)
        self.hor_Einstellungen_menu.setSpacing(0)
        self.hor_Einstellungen_menu.setObjectName(u"hor_Einstellungen_menu")
        self.hor_Einstellungen_menu.setContentsMargins(0, 0, 0, 0)

        self.frame_ip_setting = QFrame(self.frame_Einstellungen_menu)
        self.frame_ip_setting.setObjectName(u"frame_ip_setting")
        
        self.frame_ip_setting.setMaximumSize(QSize(self.linux8, self.linux16))
        self.frame_ip_setting.setFrameShape(QFrame.NoFrame)
        self.frame_ip_setting.setFrameShadow(QFrame.Plain)

        self.hor_ip_setting = QHBoxLayout(self.frame_ip_setting)
        self.hor_ip_setting.setSpacing(0)
        self.hor_ip_setting.setObjectName(u"hor_ip_setting")
        self.hor_ip_setting.setContentsMargins(0, 0, 0, 0)

        self.bn_ip_setting = QPushButton(self.frame_ip_setting)
        self.bn_ip_setting.setObjectName(u"bn_ip_setting")
        self.bn_ip_setting.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_ip_setting.setStyleSheet(s.StyleButton_3)

        self.bn_ip_setting.setFlat(True)

        self.hor_ip_setting.addWidget(self.bn_ip_setting)
        self.hor_Einstellungen_menu.addWidget(self.frame_ip_setting)

        ## Button android game

        self.frame_android_game = QFrame(self.frame_Einstellungen_menu)
        self.frame_android_game.setObjectName(u"frame_android_game")
        self.frame_android_game.setMaximumSize(QSize(self.linux8, self.linux16))
        self.frame_android_game.setFrameShape(QFrame.NoFrame)
        self.frame_android_game.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_22 = QHBoxLayout(self.frame_android_game)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)

        self.bn_android_game = QPushButton(self.frame_android_game)
        self.bn_android_game.setObjectName(u"bn_android_game")
        self.bn_android_game.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_android_game.setStyleSheet(s.StyleButton_3)

        icon9 = QIcon()
        icon9.addFile(u"icons/1x/gameAsset 61.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_android_game.setIcon(icon9)
        self.bn_android_game.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_android_game.setFlat(True)

        self.horizontalLayout_22.addWidget(self.bn_android_game)
        self.hor_Einstellungen_menu.addWidget(self.frame_android_game)
        
        ## Button setting trigger

        self.frame_setting_trig = QFrame(self.frame_Einstellungen_menu)
        self.frame_setting_trig.setObjectName(u"frame_setting_trig")
        self.frame_setting_trig.setMaximumSize(QSize(self.linux8, self.linux16))
        self.frame_setting_trig.setFrameShape(QFrame.NoFrame)
        self.frame_setting_trig.setFrameShadow(QFrame.Plain)

        self.hor_setting_trig = QHBoxLayout(self.frame_setting_trig)
        self.hor_setting_trig.setSpacing(0)
        self.hor_setting_trig.setObjectName(u"hor_setting_trig")
        self.hor_setting_trig.setContentsMargins(0, 0, 0, 0)

        self.bn_setting_trig = QPushButton(self.frame_setting_trig)
        self.bn_setting_trig.setObjectName(u"bn_setting_trig")
        self.bn_setting_trig.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_setting_trig.setStyleSheet(s.StyleButton_3)

        icon10 = QIcon()
        icon10.addFile(u"icons/1x/cil-av-timer.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_setting_trig.setIcon(icon10)
        self.bn_setting_trig.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_setting_trig.setFlat(True)

        self.hor_setting_trig.addWidget(self.bn_setting_trig)
        self.hor_Einstellungen_menu.addWidget(self.frame_setting_trig)
        
        ## Button setting Filesystem

        self.frame_setting_file = QFrame(self.frame_Einstellungen_menu)
        self.frame_setting_file.setObjectName(u"frame_setting_file")
        self.frame_setting_file.setMaximumSize(QSize(self.linux8, self.linux16))
        self.frame_setting_file.setFrameShape(QFrame.NoFrame)
        self.frame_setting_file.setFrameShadow(QFrame.Plain)

        self.hor_setting_file = QHBoxLayout(self.frame_setting_file)
        self.hor_setting_file.setSpacing(0)
        self.hor_setting_file.setObjectName(u"hor_setting_file")
        self.hor_setting_file.setContentsMargins(0, 0, 0, 0)

        self.bn_setting_file = QPushButton(self.frame_setting_file)
        self.bn_setting_file.setObjectName(u"bn_setting_file")
        self.bn_setting_file.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_setting_file.setStyleSheet(s.StyleButton_3)

        icon44 = QIcon()
        icon44.addFile(u"icons/1x/cil-file.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_setting_file.setIcon(icon44)
        self.bn_setting_file.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_setting_file.setFlat(True)

        self.hor_setting_file.addWidget(self.bn_setting_file)
        self.hor_Einstellungen_menu.addWidget(self.frame_setting_file)
        
          ## Button setting Frei

        self.frame_setting_frei = QFrame(self.frame_Einstellungen_menu)
        self.frame_setting_frei.setObjectName(u"frame_setting_frei")
        self.frame_setting_frei.setMaximumSize(QSize(self.linux8, self.linux16))
        self.frame_setting_frei.setFrameShape(QFrame.NoFrame)
        self.frame_setting_frei.setFrameShadow(QFrame.Plain)

        self.hor_setting_frei = QHBoxLayout(self.frame_setting_frei)
        self.hor_setting_frei.setSpacing(0)
        self.hor_setting_frei.setObjectName(u"hor_setting_frei")
        self.hor_setting_frei.setContentsMargins(0, 0, 0, 0)

        self.bn_setting_frei = QPushButton(self.frame_setting_frei)
        self.bn_setting_frei.setObjectName(u"bn_setting_frei")
        self.bn_setting_frei.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_setting_frei.setStyleSheet(s.StyleButton_3)

        icon45 = QIcon()
        icon45.addFile(u"icons/1x/cil-check-alt.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_setting_frei.setIcon(icon45)
        self.bn_setting_frei.setIconSize(QSize(self.linux16, self.linux16))
        self.bn_setting_frei.setFlat(True)

        self.hor_setting_frei.addWidget(self.bn_setting_frei)
        self.hor_Einstellungen_menu.addWidget(self.frame_setting_frei)
        

        self.hor_spacer_setting = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hor_Einstellungen_menu.addItem(self.hor_spacer_setting)

#-------------------------------------------------------------------------
      
        #hauptpage android
        self.stackedWidget_setting = QStackedWidget(self.page_setting)
        self.stackedWidget_setting.setObjectName(u"stackedWidget_setting")
        self.stackedWidget_setting.setStyleSheet(u"background:rgb(91,90,90);")

# -------------------------------------------------------------------------
# Page Ip Setting
# -----------------------------------------------------------------------

        self.page_ip_setting = QWidget()
        self.page_ip_setting.setObjectName(u"page_ip_setting")
        self.page_ip_setting.setStyleSheet(u"background:rgb(91,90,90);")

        self.ver_page_ip_setting = QVBoxLayout(self.page_ip_setting)
        self.ver_page_ip_setting.setSpacing(20)
        self.ver_page_ip_setting.setObjectName(u"ver_page_ip_setting")
        self.ver_page_ip_setting.setContentsMargins(5, 5, 5, 5)
        
# -------------------------------------------------------------------------
# group Zielstation
# -------------------------------------------------------------------------

        self.group_Ziel = QGroupBox()
        self.group_Ziel.setObjectName(u"group_Ziel")
     
        self.group_Ziel.setFont(s.font7)
        self.group_Ziel.setStyleSheet(s.Stylegroup)
        self.group_Ziel.setMinimumHeight(self.linux2)

        self.group_Ziel.setAlignment(Qt.AlignLeft)
        self.group_Ziel.setFlat(True)
        self.group_Ziel.setCheckable(False)

        self.group_Ziel.setTitle(QCoreApplication.translate("MainWindow", u"Zielstation", None))

# -------------------------------------------------------------------------
#  Label + Editfeld
# -------------------------------------------------------------------------
      
        self.gridLayout_7 = QGridLayout(self.group_Ziel)
        self.gridLayout_7.setSpacing(5)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(10, 10, 10, 10)


        self.label_11 = QLabel()                                            #self.frame_android_field
        self.label_11.setObjectName(u"label_11")

        self.label_11.setFont(s.font7)
        self.label_11.setStyleSheet(u"color:rgb(255,255,255);")

        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Stationsadresse:", None))

        self.gridLayout_7.addWidget(self.label_11, 0, 1, 1, 1)

        self.label_12 = QLabel()                         #self.frame_android_field
        self.label_12.setObjectName(u"label_12")

        self.label_12.setFont(s.font7)
        self.label_12.setStyleSheet(u"color:rgb(255,255,255);")

        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Segment ID:", None))

        self.gridLayout_7.addWidget(self.label_12, 1, 1, 1, 1)

        self.label_13 = QLabel()
        self.label_13.setObjectName(u"label_13")

        self.label_13.setFont(s.font7)
        self.label_13.setStyleSheet(u"color:rgb(255,255,255);")

        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Steckplatz:", None))

        self.gridLayout_7.addWidget(self.label_13, 2, 1, 1, 1)

        self.label_14 = QLabel()
        self.label_14.setObjectName(u"label_14")

        self.label_14.setFont(s.font7)
        self.label_14.setStyleSheet(u"color:rgb(255,255,255);")

        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Racknummer:", None))

        self.gridLayout_7.addWidget(self.label_14, 3, 1, 1, 1)

#--------------------------------------------------------------------------
#Editfeld Station
#--------------------------------------------------------------------------
       
        self.line_Station = QLineEdit()
        self.line_Station.setObjectName(u"line_Station")
        self.line_Station.setEnabled(False)

        self.line_Station.setAlignment(Qt.AlignCenter)

        self.line_Station.setFont(s.font7)
        self.line_Station.setStyleSheet(s.StyleLineEdit)

        self.line_Station.setText(QCoreApplication.translate("MainWindow", Def.Ip_Adresse, None))
        self.gridLayout_7.addWidget(self.line_Station, 0, 3, 1, 1)

#--------------------------------------------------------------------------
#Editfeld Segment ID
#--------------------------------------------------------------------------

        self.line_Segment = QLineEdit()
        self.line_Segment.setObjectName(u"line_Segment")
        self.line_Segment.setEnabled(False)

        self.line_Segment.setAlignment(Qt.AlignCenter)

        self.line_Segment.setFont(s.font7)
        self.line_Segment.setStyleSheet(s.StyleLineEdit)

        self.line_Segment.setText(QCoreApplication.translate("MainWindow", Def.Seg_ID, None))
        self.gridLayout_7.addWidget(self.line_Segment, 1, 3, 1, 1)

#--------------------------------------------------------------------------
#Editfeld Steckplatz
#-------------------------------------------------------------------------

        self.line_Steckplatz = QLineEdit()
        self.line_Steckplatz.setObjectName(u"line_Steckplatz")
        self.line_Steckplatz.setEnabled(False)

        self.line_Steckplatz.setAlignment(Qt.AlignCenter)

        self.line_Steckplatz.setFont(s.font7)
        self.line_Steckplatz.setStyleSheet(s.StyleLineEdit)

        self.line_Steckplatz.setText(QCoreApplication.translate("MainWindow", Def.Slot, None))
        self.gridLayout_7.addWidget(self.line_Steckplatz, 2, 3, 1, 1)

#--------------------------------------------------------------------------
#Editfeld Racknummer
#--------------------------------------------------------------------------

        self.line_Rack = QLineEdit()
        self.line_Rack.setObjectName(u"line_Rack")
        self.line_Rack.setEnabled(False)

        self.line_Rack.setAlignment(Qt.AlignCenter)

        self.line_Rack.setFont(s.font7)
        self.line_Rack.setStyleSheet(s.StyleLineEdit)

        self.line_Rack.setText(QCoreApplication.translate("MainWindow", Def.Rack, None))
        self.gridLayout_7.addWidget(self.line_Rack, 3, 3, 1, 1)

#--------------------------------------------------------------------------
#Editfeld - Button Edit einfuegen
#--------------------------------------------------------------------------

        self.bn_IP_edit = QPushButton()
        self.bn_IP_edit.setObjectName(u"bn_IP_edit")
        self.bn_IP_edit.setMaximumWidth(self.linuxW6)
       
        self.bn_IP_edit.setFont(s.font7)
        self.bn_IP_edit.setStyleSheet(s.StyleButton_2)

        self.bn_IP_edit.setText('Edit')
        self.gridLayout_7.addWidget(self.bn_IP_edit, 4, 1, 1, 1)

#--------------------------------------------------------------------------
#Editfeld - Button Save einfuegen
#--------------------------------------------------------------------------

        self.bn_IP_save = QPushButton()
        self.bn_IP_save.setObjectName(u"bn_IP_save")
        self.bn_IP_save.setMaximumWidth(self.linuxW6)
        
        self.bn_IP_save.setFont(s.font7)
        self.bn_IP_save.setStyleSheet(s.StyleButton_2)
        self.bn_IP_save.setEnabled(False)
        

        self.bn_IP_save.setText('Save')
        self.gridLayout_7.addWidget(self.bn_IP_save, 4, 3, 1, 1)


        self.ver_page_ip_setting.addWidget(self.group_Ziel)
        
        
# -------------------------------------------------------------------------
# group Ersatzstation
# -------------------------------------------------------------------------

        self.group_Ersatzstation = QGroupBox()
        self.group_Ersatzstation.setObjectName(u"group_Ersatzstation")
     
        self.group_Ersatzstation.setFont(s.font7)
        self.group_Ersatzstation.setStyleSheet(s.Stylegroup)

        self.group_Ersatzstation.setAlignment(Qt.AlignLeft)
        self.group_Ersatzstation.setFlat(True)
        self.group_Ersatzstation.setCheckable(False)
        self.group_Ersatzstation.setMaximumHeight(self.linux8)

        self.group_Ersatzstation.setTitle(QCoreApplication.translate("MainWindow", u"Ersatzstation", None))
        
        self.ver_page_ip_setting.addWidget(self.group_Ersatzstation)


        #hauptpage
        self.stackedWidget_setting.addWidget(self.page_ip_setting)

# -------------------------------------------------------------------------
# page game
# -------------------------------------------------------------------------

        self.page_zyklus_setting = QWidget()
        self.page_zyklus_setting.setObjectName(u"page_zyklus_setting")
        self.page_zyklus_setting.setStyleSheet(u"background:rgb(91,90,90);")

        self.ver_setting_zyklus = QVBoxLayout(self.page_zyklus_setting)
        self.ver_setting_zyklus.setSpacing(5)
        self.ver_setting_zyklus.setObjectName(u"ver_setting_zyklus")
        self.ver_setting_zyklus.setContentsMargins(5, 5, 5, 5)

        self.hor_setting_zyklus = QHBoxLayout()
        self.hor_setting_zyklus.setSpacing(5)
        self.hor_setting_zyklus.setObjectName(u"hor_setting_zyklus")
        self.hor_setting_zyklus.setContentsMargins(5, 5, 5, 5)

        self.group_zyklus1 = QGroupBox()
        self.group_zyklus1.setObjectName(u"group_zyklus1")
       
        self.group_zyklus1.setFont(s.font7)
        self.group_zyklus1.setStyleSheet(s.Stylegroup)

        self.group_zyklus1.setAlignment(Qt.AlignLeft)
        
        self.group_zyklus1.setCheckable(True)
        self.group_zyklus1.setChecked(False)

        self.verticalLayout_22 = QVBoxLayout(self.group_zyklus1)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(5, 40, 5, 5)

        self.group_zyklus1.setTitle(QCoreApplication.translate("MainWindow", u"Zyklusgenaue Erfassung", None))

        self.horizontalSpacer_10 = QSpacerItem(10, 20, QSizePolicy.Maximum , QSizePolicy.Maximum)  #Expanding , Minimum   #40,20
        self.verticalLayout_22.addItem(self.horizontalSpacer_10)

# -------------------------------------------------------------------------
#   CheckBox Zeitstempel
# -------------------------------------------------------------------------

        self.Zeitstempel = QCheckBox(self.group_zyklus1)
        self.Zeitstempel.setObjectName(u"Zeitstempel")
        self.Zeitstempel.setFont(s.font7)

        self.Zeitstempel.setStyleSheet(s.StyleCheckBox)

        self.Zeitstempel.setText(QCoreApplication.translate("MainWindow", u"Zeitstempel generieren", None))
        self.Zeitstempel.setTristate(False)
        self.Zeitstempel.setEnabled(True)

        self.verticalLayout_22.addWidget(self.Zeitstempel)

# -------------------------------------------------------------------------
#   CheckBox AG_Sicherheitsstop
# -------------------------------------------------------------------------

        self.AG_Sicher = QCheckBox(self.group_zyklus1)
        self.AG_Sicher.setObjectName(u"AG_Sicher")
        self.AG_Sicher.setFont(s.font7)
        self.AG_Sicher.setStyleSheet(s.StyleCheckBox)

        self.AG_Sicher.setTristate(False)
        self.AG_Sicher.setText(QCoreApplication.translate("MainWindow", u"Mit AG Sicherheitsstop", None))
        self.verticalLayout_22.addWidget(self.AG_Sicher)

# -------------------------------------------------------------------------
#   CheckBox Baustein ueberpruefen
# -------------------------------------------------------------------------

        self.Baustein = QCheckBox(self.group_zyklus1)
        self.Baustein.setObjectName(u"Baustein")
        self.Baustein.setFont(s.font7)
        self.Baustein.setStyleSheet(s.StyleCheckBox)

        self.Baustein.setTristate(False)
        self.Baustein.setText(QCoreApplication.translate("MainWindow", u"Bedingtes Bausteinende ueberpruefen", None))
        self.verticalLayout_22.addWidget(self.Baustein)

# -------------------------------------------------------------------------
#   Group - Zeitstempel 
# -------------------------------------------------------------------------

        self.group_zyklus2 = QGroupBox()
        self.group_zyklus2.setObjectName(u"group_zyklus2")
        
        self.group_zyklus2.setFont(s.font7)
        self.group_zyklus2.setStyleSheet(s.Stylegroup)

        self.group_zyklus2.setAlignment(Qt.AlignLeft)
        self.group_zyklus2.setFlat(True)
        self.group_zyklus2.setCheckable(True)

        self.group_zyklus2.setTitle(QCoreApplication.translate("MainWindow", u"Zeitstempel", None))

        self.ver_group_zyklus2 = QVBoxLayout(self.group_zyklus2)
        self.ver_group_zyklus2.setObjectName(u"ver_group_zyklus2")
        self.ver_group_zyklus2.setContentsMargins(5, 40, 5, 20)

# -------------------------------------------------------------------------
#   RadioButton_4
# -------------------------------------------------------------------------

        self.radioButton_4 = QRadioButton()
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.radioButton_4.setFont(s.font7)
        self.radioButton_4.setStyleSheet(s.StyleRadio)

        self.radioButton_4.setAutoRepeat(False)
        self.radioButton_4.setAutoExclusive(True)
        self.radioButton_4.setChecked(False)

        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", u"nur bei Signalveraenderung", None))

        self.ver_group_zyklus2.addWidget(self.radioButton_4)

# -------------------------------------------------------------------------
#   RadioButton_5
# -------------------------------------------------------------------------

        self.radioButton_5 = QRadioButton()
        self.radioButton_5.setObjectName(u"radioButton_5")

        self.radioButton_5.setFont(s.font7)
        self.radioButton_5.setStyleSheet(s.StyleRadio)

        self.radioButton_5.setAutoRepeat(False)
        self.radioButton_5.setAutoExclusive(True)
        self.radioButton_5.setChecked(True)

        self.radioButton_5.setText(QCoreApplication.translate("MainWindow", u"kontinuierlich", None))

        self.ver_group_zyklus2.addWidget(self.radioButton_5)

# -------------------------------------------------------------------------
#   Combobox Abtastinterval
# -------------------------------------------------------------------------
        
        self.label_15 = QLabel() 
        self.label_15.setFont(s.font7)
        self.label_15.setEnabled(True)
        self.label_15.setText('Abtastinterval:')
        self.label_15.setAlignment(Qt.AlignLeft)
        

        self.label_15.setStyleSheet(u"QLabel {	\n"
        "    color:rgb(255,255,255);\n"
        "}\n"
        "    QLabel: disabled{\n"
        "    color:rgb(180,180,180);\n"
        "}\n"
        "\n"
        )

        self.combo_ab = QComboBox()
     
        self.combo_ab.setFont(s.font16)
        self.combo_ab.setStyleSheet(s.StyleComboBox)
        self.combo_ab.setMinimumHeight(self.linux16)

        liste3=["minimal","100ms","200ms","500ms","1s","2s","5s","10s","30s","1m"]
        self.combo_ab.addItems(liste3)
        self.combo_ab.setEnabled(True)
        self.combo_ab.setCurrentIndex(1)

        self.ver_spacer_combo = QSpacerItem(1, 2, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.ver_group_zyklus2.addItem(self.ver_spacer_combo)
       
        self.ver_group_zyklus2.addWidget(self.label_15)
        self.ver_group_zyklus2.addWidget(self.combo_ab)
        

# -------------------------------------------------------------------------
#   Group Zyklus
# -------------------------------------------------------------------------

        self.group_zyklus = QGroupBox()
        self.group_zyklus.setObjectName(u"group_zyklus")

        self.group_zyklus.setFont(s.font7)
        self.group_zyklus.setStyleSheet(s.Stylegroup)


        self.group_zyklus.setAlignment(Qt.AlignLeft)
        self.group_zyklus.setFlat(True)
        self.group_zyklus.setCheckable(False)

        self.group_zyklus.setTitle(QCoreApplication.translate("MainWindow", u"Zyklen", None))

        self.verticalLayout_12 = QVBoxLayout(self.group_zyklus)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")

        self.horizontalSpacer_9 = QSpacerItem(10, 20, QSizePolicy.Maximum , QSizePolicy.Maximum)  #Expanding , Minimum   #40,20
        self.verticalLayout_12.addItem(self.horizontalSpacer_9)

# -------------------------------------------------------------------------
#   RadioButton Zyklus_0
# -------------------------------------------------------------------------

        self.Zyklus_0 = QRadioButton(self.group_zyklus)
        self.Zyklus_0.setObjectName(u"Zyklus_0")

        self.Zyklus_0.setFont(s.font7)
        self.Zyklus_0.setStyleSheet(s.StyleRadio)

        self.Zyklus_0.setAutoRepeat(False)
        self.Zyklus_0.setAutoExclusive(True)
        self.Zyklus_0.setChecked(True)

        self.Zyklus_0.setText(QCoreApplication.translate("MainWindow", u"Zyklus_0", None))

        self.verticalLayout_12.addWidget(self.Zyklus_0)

# -------------------------------------------------------------------------
#   RadioButton Zyklus_2
# -------------------------------------------------------------------------

        self.Zyklus_2 = QRadioButton(self.group_zyklus)
        self.Zyklus_2.setObjectName(u"Zyklus_2")
        self.Zyklus_2.setFont(s.font7)
        self.Zyklus_2.setStyleSheet(s.StyleRadio)

        self.Zyklus_2.setText(QCoreApplication.translate("MainWindow", u"Zyklus_2", None))
        self.Zyklus_2.setAutoExclusive(True)
        self.verticalLayout_12.addWidget(self.Zyklus_2)

# -------------------------------------------------------------------------
#   RadioButton Zyklus_4
# -------------------------------------------------------------------------

        self.Zyklus_4 = QRadioButton(self.group_zyklus)
        self.Zyklus_4.setObjectName(u"Zyklus_4")
        self.Zyklus_4.setFont(s.font7)
        self.Zyklus_4.setStyleSheet(s.StyleRadio)

        self.Zyklus_4.setText(QCoreApplication.translate("MainWindow", u"Zyklus_4", None))
        self.Zyklus_4.setAutoExclusive(True)
        self.verticalLayout_12.addWidget(self.Zyklus_4)

        self.horizontalSpacer_8 = QSpacerItem(10, 40, QSizePolicy.Maximum , QSizePolicy.Maximum)  #Expanding , Minimum   #40,20
        self.verticalLayout_12.addItem(self.horizontalSpacer_8)
        
# -------------------------------------------------------------------------
# Triggermodus
# -------------------------------------------------------------------------

        self.group_trigger = QGroupBox()
        self.group_trigger.setObjectName(u"group_trigger")
       
        self.group_trigger.setFont(s.font7)
        self.group_trigger.setStyleSheet(s.Stylegroup)

        self.group_trigger.setAlignment(Qt.AlignLeft)
        self.group_trigger.setFlat(True)
        self.group_trigger.setCheckable(False)
        self.group_trigger.setMinimumHeight(self.linux3)

        self.ver_group_trigger = QVBoxLayout(self.group_trigger)
        self.ver_group_trigger.setObjectName(u"ver_group_trigger")

        self.group_trigger.setTitle(QCoreApplication.translate("MainWindow", u"Trigger", None))

        self.ver_spacer_trigger = QSpacerItem(10, 20, QSizePolicy.Maximum , QSizePolicy.Maximum)  
        self.ver_group_trigger.addItem(self.ver_spacer_trigger)

# -------------------------------------------------------------------------
#   CheckBox Trigger
# -------------------------------------------------------------------------

        self.Trigger = QCheckBox(self.group_trigger)
        self.Trigger.setObjectName(u"Trigger")
        self.Trigger.setFont(s.font7)
        self.Trigger.setStyleSheet(s.StyleCheckBox)

        self.Trigger.setTristate(False)
        self.Trigger.setText(QCoreApplication.translate("MainWindow", u"Trigger aktiv", None))
        self.ver_group_trigger.addWidget(self.Trigger)

# -------------------------------------------------------------------------

        self.ver_setting_zyklus.addWidget(self.group_zyklus1)

        self.hor_setting_zyklus.addWidget(self.group_zyklus2)
        self.hor_setting_zyklus.addWidget(self.group_zyklus)

        self.ver_setting_zyklus.addLayout(self.hor_setting_zyklus)
        
        self.ver_setting_zyklus.addWidget(self.group_trigger)
        
       
        #hauptpage
        self.stackedWidget_setting.addWidget(self.page_zyklus_setting)

# -------------------------------------------------------------------------
# page sps Einstellungen
# -------------------------------------------------------------------------

        self.page_trigger_setting = QWidget()
        self.page_trigger_setting.setObjectName(u"page_trigger_setting")
        self.page_trigger_setting.setStyleSheet(u"background:rgb(91,90,90);")

        self.ver_page_trigger_setting = QVBoxLayout(self.page_trigger_setting )
        self.ver_page_trigger_setting.setObjectName(u"ver_page_trigger_setting")

# -------------------------------------------------------------------------
#   Group Ersatz
# -------------------------------------------------------------------------

        self.group_ersatz = QGroupBox()
        self.group_ersatz.setObjectName(u"group_ersatz")

        self.group_ersatz.setFont(s.font7)
        self.group_ersatz.setStyleSheet(s.Stylegroup)

        self.group_ersatz.setAlignment(Qt.AlignLeft)
        self.group_ersatz.setFlat(True)
        self.group_ersatz.setCheckable(False)
        

        self.group_ersatz.setTitle(QCoreApplication.translate("MainWindow", u"Ersatz", None))

        self.ver_group_ersatz = QVBoxLayout(self.group_ersatz)
        self.ver_group_ersatz.setObjectName(u"ver_group_ersatz")

        self.ver_spacer_ersatz = QSpacerItem(1, 2, QSizePolicy.Minimum , QSizePolicy.Maximum)  
        self.ver_group_ersatz.addItem(self.ver_spacer_ersatz)
        
        self.ver_page_trigger_setting.addWidget(self.group_ersatz)
        
        #hauptpage
        self.stackedWidget_setting.addWidget(self.page_trigger_setting)
        
# -------------------------------------------------------------------------
# page file setting
# -------------------------------------------------------------------------

        self.page_file_setting = QWidget()
        self.page_file_setting.setObjectName(u"page_file_setting")
        self.page_file_setting.setStyleSheet(u"background:rgb(91,90,90);")
        
        self.ver_page_file_setting = QVBoxLayout(self.page_file_setting)
        self.ver_page_file_setting.setSpacing(0)
        self.ver_page_file_setting.setContentsMargins(0, 0, 0, 0)
        
# -------------------------------------------------------------------------
# Button Menu Edit /Save
# -------------------------------------------------------------------------
        
        self.frame_Button_menu = QFrame(self.page_file_setting)
        self.frame_Button_menu.setObjectName(u"frame_Button_menu")
        self.frame_Button_menu.setMaximumSize(QSize(16777215, self.linux16))
        self.frame_Button_menu.setStyleSheet(u"background:rgb(91,90,90);")
        self.frame_Button_menu.setFrameShape(QFrame.NoFrame)
        self.frame_Button_menu.setFrameShadow(QFrame.Plain)

        self.hor_Button_menu= QHBoxLayout(self.frame_Button_menu)
        self.hor_Button_menu.setSpacing(0)
        self.hor_Button_menu.setObjectName(u"hor_Button_menu")
        self.hor_Button_menu.setContentsMargins(0, 0, 0, 0)

        self.frame_edit_file = QFrame(self.frame_Button_menu)
        self.frame_edit_file.setObjectName(u"frame_edit_file")
        
        self.frame_edit_file.setMaximumSize(QSize(self.linux8, self.linux16))
        self.frame_edit_file.setFrameShape(QFrame.NoFrame)
        self.frame_edit_file.setFrameShadow(QFrame.Plain)

        self.hor_edit_file = QHBoxLayout(self.frame_edit_file)
        self.hor_edit_file.setSpacing(0)
        self.hor_edit_file.setObjectName(u"hor_edit_file")
        self.hor_edit_file.setContentsMargins(0, 0, 0, 0)

        self.bn_edit_file = QPushButton(self.frame_edit_file)
        self.bn_edit_file.setObjectName(u"bn_edit_file")
        self.bn_edit_file.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_edit_file.setStyleSheet(s.StyleButton_3)
        self.bn_edit_file.setFlat(True)
        
        icon38 = QIcon()
        icon38.addFile(u"icons/1x/open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_edit_file.setIcon(icon38)
        self.bn_edit_file.setIconSize(QSize(64, 64))

        self.hor_edit_file.addWidget(self.bn_edit_file)
        self.hor_Button_menu.addWidget(self.frame_edit_file)
        
# -------------------------------------------------------------------------
# Button Save
# -------------------------------------------------------------------------
   
        self.frame_save_file = QFrame(self.frame_Button_menu)
        self.frame_save_file.setObjectName(u"frame_save_file")
        
        self.frame_save_file.setMaximumSize(QSize(self.linux8, self.linux16))
        self.frame_save_file.setFrameShape(QFrame.NoFrame)
        self.frame_save_file.setFrameShadow(QFrame.Plain)

        self.hor_save_file = QHBoxLayout(self.frame_save_file)
        self.hor_save_file.setSpacing(0)
        self.hor_save_file.setObjectName(u"hor_save_file")
        self.hor_save_file.setContentsMargins(0, 0, 0, 0)

        self.bn_save_file = QPushButton(self.frame_save_file)
        self.bn_save_file.setObjectName(u"bn_save_file")
        self.bn_save_file.setMinimumSize(QSize(self.linux8, self.linux16))
        self.bn_save_file.setStyleSheet(s.StyleButton_3)
        self.bn_save_file.setFlat(True)
        
        icon36 = QIcon()
        icon36.addFile(u"icons/1x/save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_save_file.setIcon(icon36)
        self.bn_save_file.setIconSize(QSize(64, 64))

        self.hor_save_file.addWidget(self.bn_save_file)
        self.hor_Button_menu.addWidget(self.frame_save_file)
        
        self.hor_space_file = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.hor_Button_menu.addItem(self.hor_space_file)
   
        self.ver_page_file_setting.addWidget(self.frame_Button_menu)
        
# -------------------------------------------------------------------------
#  Label + Editfeld
# -------------------------------------------------------------------------
      
        self.label_file1 = QLabel()                                            
        self.label_file1.setObjectName(u"label_file")

        self.label_file1.setFont(s.font7)
        self.label_file1.setStyleSheet(u"color:rgb(255,255,255);")

        self.label_file1.setText(QCoreApplication.translate("MainWindow", u"Messdaten speichern in :", None))

        self.ver_page_file_setting.addWidget(self.label_file1)

#--------------------------------------------------------------------------
#Editfeld Station
#--------------------------------------------------------------------------
       
        self.line_file = QTextEdit()
        self.line_file.setObjectName(u"line_file")
        self.line_file.setEnabled(False)
        self.line_file.setMaximumHeight(self.linux10)
        self.line_file.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        

        self.line_file.setAlignment(Qt.AlignCenter)

        self.line_file.setFont(s.font7)
        self.line_file.setStyleSheet(s.StyleTextEdit)

        self.line_file.setText(QCoreApplication.translate("MainWindow", Def.datei_csv, None))
      
#--------------------------------------------------------------------------
#Textedit
#--------------------------------------------------------------------------

        self.frame_textedit= QFrame()
        self.frame_textedit.setObjectName(u"frame_textedit")
        self.frame_textedit.setStyleSheet(u"background:rgb(255,255,255);")
        self.frame_textedit.setFrameShape(QFrame.NoFrame)
        self.frame_textedit.setFrameShadow(QFrame.Plain)
        
        self.vboxEdit = QVBoxLayout(self.frame_textedit)
        self.vboxEdit.setSpacing(10)
        self.vboxEdit.setContentsMargins(0, 0, 0, 0)

        self.frame_textedit_scroll= QFrame()
        self.frame_textedit_scroll.setObjectName(u"frame_textedit_scroll")
        self.frame_textedit_scroll.setStyleSheet(u"background:rgb(255,0,0);")
        self.frame_textedit_scroll.setFrameShape(QFrame.NoFrame)
        self.frame_textedit_scroll.setFrameShadow(QFrame.Plain)

        self.scrollbar_textedit = QScrollBar(self.frame_textedit_scroll)
        self.scrollbar_textedit.setOrientation(Qt.Vertical)
        self.scrollbar_textedit.setInvertedControls(True)

        self.scrollbar_textedit.setObjectName(u"scrollbar_textedit")
        self.scrollbar_textedit.setSizeIncrement(5,5)
        self.scrollbar_textedit.setStyleSheet(s.StyleScrollBar_ver)
        
#Textausgabe Daten1.csv
        self.textEdit = QTextEdit()
        self.textEdit.setMinimumWidth(16777215)
        self.textEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        #self.textEdit.setHorizontalScrollBar(self.scrollbar_textedit)
        self.textEdit.setVerticalScrollBar(self.scrollbar_textedit)
        
        self.ver_spacer_file = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.vboxEdit.addWidget(self.textEdit)
        
        self.ver_page_file_setting.addWidget(self.line_file)
        self.ver_page_file_setting.addWidget(self.frame_textedit)
        #self.ver_page_file_setting.addItem(self.ver_spacer_file)
        
        #hauptpage
        self.stackedWidget_setting.addWidget(self.page_file_setting)
        
# -------------------------------------------------------------------------
# page frei setting
# -------------------------------------------------------------------------

        self.page_frei_setting = QWidget()
        self.page_frei_setting.setObjectName(u"page_frei_setting")
        self.page_frei_setting.setStyleSheet(u"background:rgb(91,90,90);")

        self.ver_page_frei_setting = QVBoxLayout(self.page_frei_setting )
        self.ver_page_frei_setting.setObjectName(u"ver_page_frei_setting")
        
        
        #hauptpage
        self.stackedWidget_setting.addWidget(self.page_frei_setting)

# -------------------------------------------------------------------------

        self.ver_page_setting.addWidget(self.stackedWidget_setting)

        #hauptframe
        self.ver_page_setting.addWidget(self.frame_Einstellungen_menu)


        self.ver_central.addWidget(self.stackedWidget)


# -------------------------------------------------------------------------
        
        self.verticalLayout_2.addWidget(self.frame)

        self.frame_low = QFrame(self.frame_bottom_east)
        self.frame_low.setObjectName(u"frame_low")
        self.frame_low.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_low.setMinimumSize(QSize(16777215, self.linux16))
        self.frame_low.setMaximumSize(QSize(16777215, self.linux16))
        self.frame_low.setFrameShape(QFrame.NoFrame)
        self.frame_low.setFrameShadow(QFrame.Plain)
        
        self.gridlayout_11 = QGridLayout(self.frame_low)
        self.gridlayout_11.setVerticalSpacing(0)
        self.gridlayout_11.setHorizontalSpacing(0)
        
        self.gridlayout_11.setObjectName(u"gridlayout_11")
        self.gridlayout_11.setContentsMargins(0, 0, 0, 0)
        
        self.frame_error = QFrame()
        self.frame_error.setObjectName(u"frame_error")
        
        self.frame_error.setFont(s.font10)
        self.frame_error.setStyleSheet(u"background:rgb(71,71,71);")
        self.frame_error.setFrameShape(QFrame.NoFrame)  
        self.frame_error.setFrameShadow(QFrame.Plain)  
        
        self.eff_2= QGraphicsOpacityEffect()
        self.eff_2.setOpacity(0.0)
        self.frame_error.setGraphicsEffect(self.eff_2)
    	       
        self.stack_error = QStackedLayout(self.frame_error)
        self.stack_error.setObjectName(u"stack_error")
        self.stack_error.setContentsMargins(0, 0, 0, 0)
        self.lab_error = QTextEdit()
        self.lab_error.setObjectName(u"lab_error")
        self.lab_error.setFont(s.font11)
        self.lab_error.setStyleSheet(u"color:rgb(255,255,255);")

        self.lab_error.setAlignment(Qt.AlignLeft)
        
        self.stack_error.addWidget(self.lab_error)
        
# -------------------------------------------------------------------

        self.frame_tab = QFrame()
        self.frame_tab.setObjectName(u"frame_tab")
        self.frame_tab.setFont(s.font10)
        self.frame_tab.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_tab.setFrameShape(QFrame.NoFrame)  
        self.frame_tab.setFrameShadow(QFrame.Plain)  
        
        self.gridLayout_8 = QGridLayout(self.frame_tab)
        self.gridLayout_8.setSpacing(5)
        self.gridLayout_8.setHorizontalSpacing(5)
        self.gridLayout_8.setVerticalSpacing(2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)

#--------------------------------------------------------------------------
# Statusbar - lab_tab
#--------------------------------------------------------------------------

        self.lab_tab = QLabel()
        self.lab_tab.setObjectName(u"lab_tab")
        self.lab_tab.setMinimumSize(QSize(150, self.linux32))
        self.lab_tab.setMaximumSize(QSize(150, self.linux8))
        
        self.lab_tab.setFont(s.font11)
        self.lab_tab.setStyleSheet(u"color:rgb(255,255,255);")

        self.lab_tab.setAlignment(Qt.AlignLeft)
        self.lab_tab.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        self.gridLayout_8.addWidget(self.lab_tab, 0,0,1,1)

        #2te Zeile - Tab
        self.lab_tab20 = QLabel()
        self.lab_tab20.setObjectName(u"lab_tab20")
        self.lab_tab20.setMinimumSize(QSize(150, self.linux32))
        self.lab_tab20.setMaximumSize(QSize(150, self.linux8))
        
        self.lab_tab20.setFont(s.font11)
        self.lab_tab20.setStyleSheet(u"color:rgb(255,255,255);")

        self.lab_tab20.setAlignment(Qt.AlignLeft)
        self.lab_tab20.setText(QCoreApplication.translate("MainWindow", u"lab_tab20", None))
        self.gridLayout_8.addWidget(self.lab_tab20, 1,0,1,1)

        
#--------------------------------------------------------------------------
# Statusbar - lab_tab_connect
#--------------------------------------------------------------------------

        self.lab_tab_connect = QLabel()
        self.lab_tab_connect.setObjectName(u"lab_tab_connect")
        self.lab_tab_connect.setMinimumSize(QSize(150, self.linux32))
        self.lab_tab_connect.setMaximumSize(QSize(150, self.linux8))
        self.lab_tab_connect.setFont(s.font11)
        self.lab_tab_connect.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_tab_connect.setAlignment(Qt.AlignLeft)
        self.lab_tab_connect.setText(QCoreApplication.translate("MainWindow", u"plc connect=?", None))
        self.gridLayout_8.addWidget(self.lab_tab_connect, 0,1,1,1)


#--------------------------------------------------------------------------
# lab_tab_run
#--------------------------------------------------------------------------

        self.lab_tab_run = QLabel()
        self.lab_tab_run.setObjectName(u"lab_tab_run")
        self.lab_tab_run.setMinimumSize(QSize(0, self.linux32))
        self.lab_tab_run.setMaximumSize(QSize(60, self.linux8))
        self.lab_tab_run.setFont(s.font11)
        self.lab_tab_run.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_tab_run.setAlignment(Qt.AlignLeft)
        self.lab_tab_run.setText(QCoreApplication.translate("MainWindow", u"lab_tab_run", None))
        self.gridLayout_8.addWidget(self.lab_tab_run, 1,2,1,1)

#--------------------------------------------------------------------------
# Statusbar - Progressbar
#--------------------------------------------------------------------------

        self.bar = QProgressBar()
        self.bar.setMinimumSize(QSize(0, self.linux32))
        self.bar.setMaximumSize(QSize(60,self.linux8))
        self.bar.setStyleSheet(s.StyleProgress)
        self.bar.setAlignment(Qt.AlignCenter)
        self.bar.setTextVisible(False)

        self.gridLayout_8.addWidget(self.bar, 0,2,1,1)

#--------------------------------------------------------------------------
# Statusbar - lab_datetime
#--------------------------------------------------------------------------

        self.lab_datetime = QLabel()
        self.lab_datetime.setFont(s.font11)
        self.lab_datetime.setMinimumSize(QSize(0, self.linux32))
        self.lab_datetime.setMaximumSize(QSize(200, self.linux8))
        self.lab_datetime.setAlignment(Qt.AlignLeft)
        self.lab_datetime.setStyleSheet(u"color:rgb(255,255,255);")

        self.gridLayout_8.addWidget(self.lab_datetime, 1,1,1,1)

#--------------------------------------------------------------------------
# Statusbar - lab_tab1
#--------------------------------------------------------------------------

        self.lab_tab1 = QLabel()
        self.lab_tab1.setFont(s.font11)
        self.lab_tab1.setMinimumSize(QSize(0, self.linux32))
        self.lab_tab1.setMaximumSize(QSize(200, self.linux8))
        self.lab_tab1.setAlignment(Qt.AlignLeft)
        self.lab_tab1.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_tab1.setText(QCoreApplication.translate("MainWindow", u"", None))

        self.gridLayout_8.addWidget(self.lab_tab1, 1,3,1,1)

      
#--------------------------------------------------------------------------
# Statusbar - lab_tab2
#--------------------------------------------------------------------------
        self.lab_tab2 = QLabel()
        self.lab_tab2.setFont(s.font11)
        self.lab_tab2.setMinimumSize(QSize(0, self.linux32))
        self.lab_tab2.setMaximumSize(QSize(350, self.linux8))
        self.lab_tab2.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_tab2.setAlignment(Qt.AlignLeft)
        self.lab_tab2.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.gridLayout_8.addWidget(self.lab_tab2, 0,4,1,1)

#--------------------------------------------------------------------------
# Statusbar - Abtastwert
#--------------------------------------------------------------------------
        self.lab_abtast = QLabel()
        self.lab_abtast.setFont(s.font11)
        self.lab_abtast.setMinimumSize(QSize(0, self.linux32))
        self.lab_abtast.setMaximumSize(QSize(150, self.linux8))
        self.lab_abtast.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_abtast.setAlignment(Qt.AlignLeft)
        self.lab_abtast.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.gridLayout_8.addWidget(self.lab_abtast, 0,5,1,1)

#--------------------------------------------------------------------------
# Statusbar - lab_tab3
#--------------------------------------------------------------------------

        self.lab_tab3 = QLabel()
        self.lab_tab3.setFont(s.font11)
        self.lab_tab3.setMinimumSize(QSize(0, self.linux32))
        self.lab_tab3.setMaximumSize(QSize(200, self.linux8))
        self.lab_tab3.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_tab3.setAlignment(Qt.AlignLeft)
        self.lab_tab3.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.gridLayout_8.addWidget(self.lab_tab3, 0,6,1,1)

#--------------------------------------------------------------------------
# Statusbar - lab_tab4
#--------------------------------------------------------------------------

        self.lab_tab4 = QLabel()
        self.lab_tab4.setFont(s.font11)
        self.lab_tab4.setMinimumSize(QSize(0, self.linux32))
        self.lab_tab4.setMaximumSize(QSize(150, self.linux8))
        self.lab_tab4.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_tab4.setAlignment(Qt.AlignLeft)
        self.lab_tab4.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.gridLayout_8.addWidget(self.lab_tab4, 0,7,1,1)
        
#--------------------------------------------------------------------------
# Statusbar - drag - Led rot und gruen
#--------------------------------------------------------------------------

        self.frame_drag = QFrame()
        self.frame_drag.setObjectName(u"frame_drag")
        self.frame_drag.setMinimumSize(QSize(48, self.linux16))
        self.frame_drag.setMaximumSize(QSize(48, self.linux16))
        self.frame_drag.setStyleSheet(u"background:rgb(151,151,151);")  #51,51,51
        self.frame_drag.setFrameShape(QFrame.NoFrame)
        self.frame_drag.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_drag)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 4)
        #self.horizontalLayout_13.setAlignment(Qt.AlignCenter)

        self.bn_drag2 = QPushButton(self.frame_close)
        self.bn_drag2.setObjectName(u"bn_drag2")
        self.bn_drag2.setMaximumSize(QSize(16, self.linux16))
        self.bn_drag2.setStyleSheet(s.StyleButton_4)
        self.bn_drag = QPushButton(self.frame_close)
        self.bn_drag.setObjectName(u"bn_drag")
        self.bn_drag.setMaximumSize(QSize(16, self.linux16))
        self.bn_drag.setStyleSheet(s.StyleButton_4)
        self.bn_drag1 = QPushButton(self.frame_close)
        self.bn_drag1.setObjectName(u"bn_drag")
        self.bn_drag1.setMaximumSize(QSize(16, self.linux16))
        self.bn_drag1.setStyleSheet(s.StyleButton_4)

        self.bn_drag.setCheckable(True)
        self.bn_drag1.setCheckable(True)
        self.bn_drag2.setCheckable(True)
        self.bn_drag.setEnabled(True)
        self.bn_drag1.setEnabled(True)
        self.bn_drag2.setEnabled(True)

        icon35 = QIcon()
        icon35.addFile(u"icons/1x/Led_Blau_On.ico", QSize(), QIcon.Normal, QIcon.On)
        icon35.addFile(u"icons/1x/Led_Rot_Off.ico",QSize(), QIcon.Normal, QIcon.Off)
        self.bn_drag2.setIcon(icon35)
        #self.bn_drag2.setIconSize(QSize(15, 15))
        self.bn_drag2.setFlat(True)

        icon27 = QIcon()
        icon27.addFile(u"icons/1x/Led_Rot_Off.ico", QSize(), QIcon.Disabled, QIcon.Off)
        icon27.addFile(u"icons/1x/Led_Rot_On.ico", QSize(), QIcon.Normal, QIcon.On)
        icon27.addFile(u"icons/1x/Led_Rot_Off.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_drag1.setIcon(icon27)
        #self.bn_drag1.setIconSize(QSize(15, 15))
        self.bn_drag1.setFlat(True)

        icon21 = QIcon()
        icon21.addFile(u"icons/1x/Led_Gruen_Off.ico",QSize(), QIcon.Disabled, QIcon.Off)
        icon21.addFile(u"icons/1x/Led_Gruen_On.ico", QSize(), QIcon.Normal, QIcon.On)
        icon21.addFile(u"icons/1x/Led_Gruen_Off.ico",QSize(), QIcon.Normal, QIcon.Off)
        self.bn_drag.setIcon(icon21)
        #self.bn_drag.setIconSize(QSize(15, 15))
        self.bn_drag.setFlat(True)


        self.horizontalLayout_13.addWidget(self.bn_drag2)
        self.horizontalLayout_13.addWidget(self.bn_drag1)
        self.horizontalLayout_13.addWidget(self.bn_drag)
        
        self.ver_spacer_grid = QSpacerItem(2, 4, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridlayout_11.addItem(self.ver_spacer_grid, 0,2,1,1)

        self.gridlayout_11.addWidget(self.frame_drag, 1,2,1,1)
        
        self.gridlayout_11.addWidget(self.frame_tab, 1,0,1,1)
        self.frame_tab.setVisible(True)
        self.gridlayout_11.addWidget(self.frame_error, 0,0,1,1)
        self.frame_error.setVisible(False)
        
        
        self.verticalLayout_2.addWidget(self.frame_low)


        self.horizontalLayout_2.addWidget(self.frame_bottom_east)


        self.verticalLayout.addWidget(self.frame_bottom)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        #Timer fuer LED gruen
        self.timer = QTimer()
        
        #Timer fuer LED rot
        self.timer1 = QTimer()

        #Timer fuer Dial
        self.timer2 = QTimer()

        #Timer fuer live Graph Zyklusabtastung
        self.timer0 = QTimer()
        
        #Timer fuer Pydroid3 - ShowTime5 - live Graph test
        self.timer5 = QTimer()
        
        #Timer 6 fuer automatisch Fenster vergroessern
        self.timer6 = QTimer()
        
        #Timer 7 fuer sonstige (LED, plc_running, Buttons)
        self.timer7 = QTimer()
        
        #Timer 8 kein PLC Connect - Timer 1sekunde
        self.timer8 = QTimer()
        self.timer8.start(1000)
        
        #self.stackedWidget.setCurrentIndex(7)
        #self.stackedWidget_android.setCurrentIndex(2)

        self.stackedWidget.currentIndex()
        self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(4)

#--------------------------------------------------------------------------
# Reihenfolge Buttons und Frame
#--------------------------------------------------------------------------

        #home Button
        self.h_frame_home = QVBoxLayout(self.frame_home)  
        self.h_frame_home.setSpacing(0)
        self.h_frame_home.setObjectName(u"h_frame_home")
        self.h_frame_home.setContentsMargins(0, 0, 0, 0)
        self.h_frame_home.addWidget(self.bn_home)
        self.verticalLayout_3.addWidget(self.frame_home)

        #daten
        self.h_frame_daten = QHBoxLayout(self.frame_daten)  
        self.h_frame_daten.setSpacing(0)
        self.h_frame_daten.setObjectName(u"h_frame_daten")
        self.h_frame_daten.setContentsMargins(0, 0, 0, 0)
        self.h_frame_daten.addWidget(self.bn_daten)
        self.verticalLayout_3.addWidget(self.frame_daten)

        #graph live
        self.h_frame_live = QHBoxLayout(self.frame_live)
        self.h_frame_live.setSpacing(0)
        self.h_frame_live.setObjectName(u"h_frame_live")
        self.h_frame_live.setContentsMargins(0, 0, 0, 0)
        self.h_frame_live.addWidget(self.bn_live)
        self.verticalLayout_3.addWidget(self.frame_live)


        #plc
        self.h_frame_plc = QHBoxLayout(self.frame_plc)
        self.h_frame_plc.setSpacing(0)
        self.h_frame_plc.setObjectName(u"h_frame_plc")
        self.h_frame_plc.setContentsMargins(0, 0, 0, 0)
        self.h_frame_plc.addWidget(self.bn_plc)
        self.verticalLayout_3.addWidget(self.frame_plc)

        #gpanel
        self.h_frame_gpanel = QHBoxLayout(self.frame_gpanel)
        self.h_frame_gpanel.setSpacing(0)
        self.h_frame_gpanel.setObjectName(u"h_frame_gpanel")
        self.h_frame_gpanel.setContentsMargins(0, 0, 0, 0)
        self.h_frame_gpanel.addWidget(self.bn_gpanel)
        self.verticalLayout_3.addWidget(self.frame_gpanel)

        #graph
        self.h_frame_graph = QHBoxLayout(self.frame_graph)
        self.h_frame_graph.setSpacing(0)
        self.h_frame_graph.setObjectName(u"h_frame_graph")
        self.h_frame_graph.setContentsMargins(0, 0, 0, 0)
        self.h_frame_graph.addWidget(self.bn_graph)
        self.verticalLayout_3.addWidget(self.frame_graph)

        #setting
        self.h_frame_setting = QHBoxLayout(self.frame_setting)
        self.h_frame_setting.setSpacing(0)
        self.h_frame_setting.setObjectName(u"h_frame_setting")
        self.h_frame_setting.setContentsMargins(0, 0, 0, 0)
        self.h_frame_setting.addWidget(self.bn_setting)
        self.verticalLayout_3.addWidget(self.frame_setting)

        #power
        self.h_frame_power = QHBoxLayout(self.frame_power)
        self.h_frame_power.setSpacing(0)
        self.h_frame_power.setObjectName(u"h_frame_power")
        self.h_frame_power.setContentsMargins(0, 0, 0, 0)
        self.h_frame_power.addWidget(self.bn_power)
        self.verticalLayout_3.addWidget(self.frame_power)
        
        self.lab_plt=[]
        
        for x in range(0,10):
            lab_plt = QLabel()
            lab_plt.setFont(s.font11)
            
            lab_plt.setAlignment(Qt.AlignCenter)
            lab_plt.setText("lab_plt"+str(x))
            lab_plt.setStyleSheet(u"color:rgb(255,255,255);")
            self.lab_plt.append(lab_plt)
            self.verticalLayout_3.addWidget(self.lab_plt[x])
        
        
        #spacer einfuegen

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(self.verticalSpacer_7)

        self.h_frame_back = QHBoxLayout(self.frame_back)
        self.h_frame_back.setContentsMargins(0, 0, 0, 0)
        self.h_frame_back.setSpacing(0)
        self.h_frame_back.addWidget(self.bn_exit)
        self.verticalLayout_3.addWidget(self.frame_back)


# -------------------------------------------------------------------------
# stackedWidget.currentIndex() - Reihenfolge der Nummerierung
# -------------------------------------------------------------------------
        #Index Nr= 0 page_home
        self.stackedWidget.addWidget(self.page_home)

        #Index Nr=1 page_daten
        self.stackedWidget.addWidget(self.page_daten)

        #Index Nr=2 page_live
        self.stackedWidget.addWidget(self.page_live)

        #Index Nr=3 page_plc
        self.stackedWidget.addWidget(self.page_plc)

        #Index Nr=4 page_gpanel
        self.stackedWidget.addWidget(self.page_gpanel)

        #Index Nr=5 page_graph
        self.stackedWidget.addWidget(self.page_graph)

        #Index Nr=6 page_setting
        self.stackedWidget.addWidget(self.page_setting)

        self.page_plc_scroll1.setHidden(True)

        QMetaObject.connectSlotsByName(MainWindow)


    # setupUi
    
    def createSlider(self,size, group123 ,name, slider123):

        group123.setMinimumSize(QSize(5, 5))
        group123.setMaximumSize(QSize(65, 300))
        group123.setSizeIncrement(QSize(0, 0))

        font6 = QFont()
        font6.setFamily(u"Segoe UI")
        font6.setPointSize(size)

        Stylegroup = (u"QGroupBox{\n"
        "	border:5px solid rgb(51,51,51);	\n"
        "	border-radius:4px;\n"
        "	color:white;\n"
        "	background:rgb(91,90,90);\n"
        "}\n"
        "QGroupBox::indicator:unchecked {\n"
        "   border:2px solid rgb(51,51,51);\n"
        "	background:rgb(91,90,90);\n"
        "}\n"
        "\n"
        "QGroupBox::indicator:checked {\n"
        "	background-color:rgb(0,143,170);\n"
        "    border: 2px solid rgb(51,51,51);\n"
        "}\n"
        "\n"
        "")

        group123.setFont(font6)
        group123.setStyleSheet(Stylegroup)

        group123.setAlignment(Qt.AlignLeft)
        group123.setFlat(True)

        group123.setCheckable(True)  #False
        group123.setChecked(False)
        group123.setDisabled(False)

        group123.setTitle(QCoreApplication.translate("MainWindow", name, None))

        slider123.setObjectName(u"slider123")
        slider123.setStyleSheet(u"QSlider::groove:vertical {\n"
        "    background: red;\n"
        "    width:5px\n"
        "}\n"
        "\n"
        "QSlider::handle:vertical {\n"
        "    height: 10px;\n"
        "    background:rgb(0,143,170);\n"
        "	margin:0 -8px\n"
        "}\n"
        "\n"
        "QSlider::add-page:vertical {\n"
        "    background:rgb(51,51,51);\n"
        "}\n"
        "\n"
        "QSlider::sub-page:vertical {\n"
        "    background:rgb(51,51,51);\n"
        "}")

        slider123.setOrientation(Qt.Vertical)
        slider123.setTracking(True)
        slider123.setInvertedAppearance(False)   #False
        slider123.setInvertedControls(False)     #False
        slider123.setTickPosition(QSlider.NoTicks) #NoTicks
        #slider123.setMinimum(300)
        #slider123.setMaximum(300)
        #slider123.setMinimumSize(QSize(40, 300))
        #slider123.setMaximumSize(QSize(40, 300))

        vbox = QVBoxLayout()

        #vertical Spacer
        ver_Spacer1 = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        vbox.addItem(ver_Spacer1)

        vbox.addWidget(slider123)

        #vertical Spacer
        ver_Spacer2 = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        vbox.addItem(ver_Spacer2)

        vbox.addStretch(1)
        group123.setLayout(vbox)

        return group123

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))

        
# -------------------------------------------------------------------------
# ToolTip - Fenster - obere Leiste  - Button Menu, Minize, Maximize, Close
# -------------------------------------------------------------------------

#Button bn_menu - Menu
        self.bn_menu.setToolTip(QCoreApplication.translate("MainWindow", u"Menu", None))
        self.bn_menu.setText("")

#Button bn_yarak
        self.bn_yarak.setToolTip(QCoreApplication.translate("MainWindow", u"Splitter", None))
        self.bn_yarak.setText("ya")

#Button bn_oma
        self.bn_oma.setToolTip(QCoreApplication.translate("MainWindow", u"Anim1", None))
        self.bn_oma.setText("om")

#Button bn_opa
        self.bn_opa.setToolTip(QCoreApplication.translate("MainWindow", u"Anim2", None))
        self.bn_opa.setText("op")
        

#Button bn_min
        self.bn_min.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
        self.bn_min.setText("")

#Button bn_max
        self.bn_max.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
        self.bn_max.setText("")

#Button bn_close
        self.bn_close.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
        self.bn_close.setText("")

# -------------------------------------------------------------------------
# ToolTip - Hauptfenster - Button Home, Bug, Matplotlib, Android, PLC, GPanel, Graph, Setting, OnOff
# -------------------------------------------------------------------------

#Button bn_home
        self.bn_home.setToolTip(QCoreApplication.translate("MainWindow", u"Home", None))
        self.bn_home.setText(" Home")

#Button bn_daten
        self.bn_daten.setToolTip(QCoreApplication.translate("MainWindow", u"Daten", None))
        self.bn_daten.setText(" Daten")

#Button bn_live
        self.bn_live.setToolTip(QCoreApplication.translate("MainWindow", u"Live", None))
        self.bn_live.setText(" Live")

# Button bn_plc-
        self.bn_plc.setToolTip(QCoreApplication.translate("MainWindow", u"PLC", None))
        self.bn_plc.setText(" PLC")

# Button bn_gpanel
        self.bn_gpanel.setToolTip(QCoreApplication.translate("MainWindow", u"GPanel", None))
        self.bn_gpanel.setText(" GPanel")

# Button bn_graph - text graph
        self.bn_graph.setToolTip(QCoreApplication.translate("MainWindow", u"Graph", None))
        self.bn_graph.setText(" Graph")

# Button bn_Setting - text Setting
        self.bn_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.bn_setting.setText(" Setting")

# Button bn_power - text power
        self.bn_power.setToolTip(QCoreApplication.translate("MainWindow", u"Power", None))
        self.bn_power.setText(" On/Off")

# Button bn_auf - text auf
        self.bn_auf.setToolTip(QCoreApplication.translate("MainWindow", u"Aufzeichnung start/stop", None))
        self.bn_auf.setText("")
        
# Button bn_exit - text auf
        self.bn_exit.setToolTip(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.bn_exit.setText(" Exit")

# -------------------------------------------------------------------------
# ToolTip - Android - Tabs Contact, Gamepad, Clean, World, Home, Equalizer, Heart, Door
# -------------------------------------------------------------------------

#Button bn_adroid_contact
        self.bn_ip_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Zielstation", None))
        self.bn_ip_setting.setText("Zielstation")

#Button bn_adroid_game
        self.bn_android_game.setToolTip(QCoreApplication.translate("MainWindow", u"GamePad", None))
        self.bn_android_game.setText("")

#Button bn_setting_trig
        self.bn_setting_trig.setToolTip(QCoreApplication.translate("MainWindow", u"Trigger", None))
        self.bn_setting_trig.setText("")

#Button bn_s7_steuer
        self.bn_s7_steuer.setToolTip(QCoreApplication.translate("MainWindow", u"S7 Steuer", None))
        self.bn_s7_steuer.setText("")

#Button bn_aufzeichnung
        self.bn_aufzeichnung.setToolTip(QCoreApplication.translate("MainWindow", u"Aufzeichnung", None))
        self.bn_aufzeichnung.setText("")

#Button bn_plc_steuer
        self.bn_plc_steuer.setToolTip(QCoreApplication.translate("MainWindow", u"PLC Steuer", None))
        self.bn_plc_steuer.setText("")

#Button bn_S7_timer
        self.bn_S7_timer.setToolTip(QCoreApplication.translate("MainWindow", u"S7 Timer", None))
        self.bn_S7_timer.setText("")

#Button bn_auswahl 
        self.bn_auswahl.setToolTip(QCoreApplication.translate("MainWindow", u"Auswahl Graph", None))
        self.bn_auswahl.setText("")

#Button bn_dial 
        self.bn_dial.setToolTip(QCoreApplication.translate("MainWindow", u"Dialer", None))
        self.bn_dial.setText("")
        

# -------------------------------------------------------------------------
# ToolTip - Antrieb - Aus, Stop, Hand, Automatik, On, Led_Gruen, Led_Rot
# -------------------------------------------------------------------------

# Button bn_Aus
        self.bn_Aus.setToolTip(QCoreApplication.translate("MainWindow", u"Aus", None))
        self.bn_Aus.setText("")

# Button bn_Stop
        self.bn_Stop.setToolTip(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.bn_Stop.setText("")

# Button bn_Hand
        self.bn_Hand.setToolTip(QCoreApplication.translate("MainWindow", u"Hand", None))
        self.bn_Hand.setText("")

# Button bn_Auto
        self.bn_Auto.setToolTip(QCoreApplication.translate("MainWindow", u"Automatik", None))
        self.bn_Auto.setText("")

# Button bn_Prod
        self.bn_Prod.setToolTip(QCoreApplication.translate("MainWindow", u"Produktion", None))
        self.bn_Prod.setText("")

# Aufzeichnung Start - Stop und Loeschen

# Button bn_Start_Auf
        self.bn_Start_Auf.setToolTip(QCoreApplication.translate("MainWindow", u"Start Aufzeichnung", None))
        self.bn_Start_Auf.setText("")

# Button bn_Stop_Auf
        self.bn_Stop_Auf.setToolTip(QCoreApplication.translate("MainWindow", u"Stop Aufzeichnung", None))
        self.bn_Stop_Auf.setText("")

# Button bn_Laden_Auf
        self.bn_laden_Auf.setToolTip(QCoreApplication.translate("MainWindow", u"Lade Aufzeichnung", None))
        self.bn_laden_Auf.setText("")

# Button bn_On
        self.bn_On.setToolTip(QCoreApplication.translate("MainWindow", u"On Off", None))
        self.bn_On.setText("")

# Button bn_plc_start
        self.bn_plc_start.setToolTip(QCoreApplication.translate("MainWindow", u"PLC start", None))

# Button bn_plc_stop
        self.bn_plc_stop.setToolTip(QCoreApplication.translate("MainWindow", u"PLC stop", None))

# Button bn_plc_reset
        self.bn_plc_reset.setToolTip(QCoreApplication.translate("MainWindow", u"PLC Reset", None))

# Led gruen/rot
        self.bn_drag.setToolTip(QCoreApplication.translate("MainWindow", u"gruen", None))
        self.bn_drag1.setToolTip(QCoreApplication.translate("MainWindow", u"rot", None))
        

# bn_edit_file
        self.bn_edit_file.setToolTip(QCoreApplication.translate("MainWindow", u"load file", None))
        self.bn_edit_file.setText("load")
        
# bn_save_file
        self.bn_save_file.setToolTip(QCoreApplication.translate("MainWindow", u"save file", None))
        self.bn_save_file.setText("save")

    # retranslateUi

