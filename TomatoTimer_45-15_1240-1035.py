import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QProgressBar
from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtGui import QColor, QPainter
import win32gui

class TomatoTimer(QWidget):
    def __init__(self):
        super().__init__()
        # Set the window attributes
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool) # no window bar|always top|no icon in taskbar
        self.setAttribute(Qt.WA_TranslucentBackground) #transparent background

        # Set the layout
        layout = QHBoxLayout()
        self.work_button_label="GO"
        self.relax_button_label="O(∩_∩)O"
        self.work_progress_style=("""   
            QProgressBar {
                background-color: rgb(50, 50, 50);
                border: 1px solid black;
                border-radius: 5px;
            }                                           
            QProgressBar::chunk {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb(37, 178, 255),
                    stop:1 rgb(0, 138, 211)
                );                        
            }
        """)
        self.relax_progress_style=("""   
            QProgressBar {
                background-color: rgb(50, 50, 50);
                border: 1px solid black;
                border-radius: 5px;
            }                                           
            QProgressBar::chunk {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb(100, 200, 200),
                    stop:1 rgb(0, 100, 100)
                );                        
            }
        """)

        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setTextVisible(False) 
        self.progress.setStyleSheet(self.work_progress_style)
        layout.addWidget(self.progress)

        self.button = QPushButton(self.work_button_label)
        self.button.clicked.connect(self.start_countdown)
        self.button.setStyleSheet("background-color: rgb(78, 91, 102); color: white; font-size: 13px;")
        layout.addWidget(self.button, alignment=Qt.AlignRight)

        self.setLayout(layout)

        # Regularly check the window focus status
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_window_focus)
        self.timer.start(100)
        self.has_focus = True

        # Set the countdown time
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_progress)
        self.start_time = QTime(0, 0)
        self.elapsed_seconds = 0

        # Set the work and relax time
        self.filename=os.path.basename(sys.argv[0]).split('.')[0]
        self.work_seconds=int(self.filename.split('_')[-2].split('-')[0])*60
        self.relax_seconds=int(self.filename.split('_')[-2].split('-')[1])*60
        self.if_relax=0

    # Start the ountdown 
    def start_countdown(self):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.if_relax= 1-self.if_relax
        if QApplication.keyboardModifiers() == Qt.AltModifier:
            self.close()
            exit()

        self.elapsed_seconds = 0
        self.progress.setValue(0)
        self.progress.setStyleSheet(self.relax_progress_style if self.if_relax else self.work_progress_style)
        self.start_time = QTime(0, 0)  
        self.button.setEnabled(False)
        self.countdown_timer.start(1000)
        self.max_seconds=self.relax_seconds if self.if_relax else self.work_seconds

    # Update the progress
    def update_progress(self):
        self.elapsed_seconds += 1
        if self.elapsed_seconds <=  self.max_seconds:
            self.progress.setValue( int(self.elapsed_seconds * 100/self.max_seconds) ) 
            self.start_time = self.start_time.addSecs(1)
            self.button.setText(self.start_time.toString("mm:ss"))
        else:
            self.countdown_timer.stop()
            self.if_relax= 1- self.if_relax
            self.button.setEnabled(True)
            self.button.setText(self.relax_button_label if self.if_relax else self.work_button_label)
            
    # Check window focus
    def check_window_focus(self):
        foreground_window = win32gui.GetForegroundWindow()
        if foreground_window != self.winId():
            self.setWindowState(Qt.WindowActive)
            self.raise_()
        else:
            if not self.has_focus:
                self.setWindowState(Qt.WindowActive)
                self.raise_()
            self.has_focus = True

    # Close window
    def closeEvent(self, event):
        pass
    
    # Paint window
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 255, 255, 0))  
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TomatoTimer()
    #Set the position from filename
    x,y=int(window.filename.split('_')[-1].split('-')[0]),int(window.filename.split('_')[-1].split('-')[1])
    window.setGeometry(int(x),int(y),400,45)
    window.show()
    sys.exit(app.exec_())
