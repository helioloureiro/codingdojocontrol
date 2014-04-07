#! /usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, uic
import sys, time, os, random, re

maingui = "maingui.ui"
configui = "config.ui"

class CodingDojo(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        
        self.testDirectory = "/tmp/codingdojos"
        self.timerCountDown = "5"
        self.running = False
        
        self.main()
                
        
    def resetDisplay(self):
        self.stopAction()
        self.mainui.lcdNumber.display(self.mainui.lcdNumber.value)
        
    def updateTimer(self):
        self.mainui.lcdNumber.display(self.th_timer.counter)
        
    def startAction(self):
        if self.running: return
    
        self.running = True
        self.th_timer = CodingEngine(parent = self, opt = "count")
        self.connect(self.th_timer, 
                    QtCore.SIGNAL("updateTimer"),
                    self.updateTimer)
        self.th_timer.start()
        
        
        
        self.th_code = CodingEngine(parent = self, opt = "code")
        self.mainui.kledGreen.setState(False)
        self.mainui.kledYellow.setState(False)
        self.mainui.kledRed.setState(False)
        self.connect(self.th_code,
                     QtCore.SIGNAL("setTestStatus"),
                     self.setTestStatus)
        self.th_code.start()
        self.running = False
        
    def stopAction(self):
        self.th_timer.counter = 0
        self.th_code.shutdown = True
        self.running = False
        
    def setTestStatus(self):
        print "setTestStatus() called"
        status = self.th_code.status
        if (status == "running"):
            self.mainui.kledYellow.setState(True)
            self.mainui.kledGreen.setState(False)
            self.mainui.kledRed.setState(False)
        if (status == "failed"):
            self.mainui.kledYellow.setState(False)
            self.mainui.kledGreen.setState(False)
            self.mainui.kledRed.setState(True)
        if (status == "succeed"):
            self.mainui.kledYellow.setState(False)
            self.mainui.kledGreen.setState(True)
            self.mainui.kledRed.setState(False)
        if (status == "off"):
            self.mainui.kledYellow.setState(False)
            self.mainui.kledGreen.setState(False)
            self.mainui.kledRed.setState(False)

        
    def configureSettings(self):
        
        self.testDirectory = self.configui.testDirLineEdit.text
        self.timerCountDown = self.configui.timerLineEdit.text
        
        self.configui.close()
        
        self.mainui.lcdNumber.value = int(self.timerCountDown) * 60
        self.mainui.lcdNumber.display(self.mainui.lcdNumber.value)
            
    def chooseFile(self):
        #filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        filename = QtGui.QFileDialog.getExistingDirectory(self, 'Get directory')
        self.testDirectory = filename
        self.configui.testDirLineEdit.setText(filename)
        
    def main(self):
        self.mainui = uic.loadUi(maingui)
        self.configui = uic.loadUi(configui)
        
        self.mainui.show()
        
        ## main gui actions ##
        self.mainui.lcdNumber.value = int(self.timerCountDown) * 60
        
        self.connect(self.mainui.resetTimerButton,
                     QtCore.SIGNAL("clicked()"),
                     self.resetDisplay)
        self.connect(self.mainui.startTimerButton,
                     QtCore.SIGNAL("clicked()"),
                     self.startAction)
        self.connect(self.mainui.configureButton,
                     QtCore.SIGNAL("clicked()"),
                     self.configui.show)
        self.connect(self.configui.saveButton,
                     QtCore.SIGNAL("clicked()"),
                     self.configureSettings)
        self.connect(self.configui.chooseFileButton,
                     QtCore.SIGNAL("clicked()"),
                     self.chooseFile)
        
        self.mainui.lcdNumber.value = int(self.timerCountDown) * 60
        self.mainui.lcdNumber.display(self.mainui.lcdNumber.value)
        
        self.configui.testDirLineEdit.text = self.testDirectory

class CodingEngine(QtCore.QThread):
    def __init__(self, parent = None, opt = None):
        QtCore.QThread.__init__(self, parent)
        self.p = parent
        self.opt = opt
        
    def countDown(self):
        self.counter = self.p.mainui.lcdNumber.value
        while (self.counter):
            self.emit(QtCore.SIGNAL("updateTimer"))
            self.counter -= 1
            print self.counter
            time.sleep(1)
            
    def runCode(self):
        self.shutdown = False
        while not self.shutdown:
            self.status = "running"
            self.emit(QtCore.SIGNAL("setTestStatus"))
            total_result = 0
            print "Running files from %s" % self.p.testDirectory
            os.chdir(self.p.testDirectory)
            for filename in os.listdir("."):
                if re.search("^\.", filename):
                    continue
                print "checking file %s" % (filename)
                try:
                    result = os.system("python %s" % filename)
                except:
                    result = 100
                    
                total_result += result
                
            print "Total result:", total_result
            if (total_result != 0):
                self.status = "failed"
                self.emit(QtCore.SIGNAL("setTestStatus"))
            else:
                self.status = "succeed"
                self.emit(QtCore.SIGNAL("setTestStatus"))
            time.sleep(5)
            

            
    def run(self):
        if (self.opt == "count"):
            self.countDown()
        if (self.opt == "code"):
            self.runCode()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = CodingDojo()
    sys.exit(app.exec_())