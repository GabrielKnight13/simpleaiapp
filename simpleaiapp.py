#Simple Open AI Application 
#libraries
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import os
import openai
from gtts import gTTS
from audioplayer import AudioPlayer
import threading as th

#Api key and language
openai.api_key = "sk-"
language = 'en'

#Main GUI
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    #Init GUI
    def initUI(self):
        self.label_content = QtWidgets.QLabel(
            wordWrap=True,
            alignment=QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop
        )

        self.setWindowTitle("ChatGPT Interface")
        self.setGeometry(300, 300, 400, 500)

        layout = QVBoxLayout()
   
        self.text_input = QLineEdit()
        self.button_submit = QPushButton("Submit")
        self.button_listen = QPushButton("Listen")
        self.button_pause_resume = QPushButton("Pause/Resume")
        self.button_stop = QPushButton("Stop")
        self.button_exit = QPushButton("Exit")

        self.label = QLabel("Welcome!")
       
        layout.addWidget(self.text_input)
        layout.addWidget(self.button_submit)
        layout.addWidget(self.button_listen)
        layout.addWidget(self.button_pause_resume)
        layout.addWidget(self.button_stop)
        layout.addWidget(self.button_exit)

        layout.addWidget(self.label_content)
        layout.addWidget(self.label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.button_submit.clicked.connect(self.submit_pressed)   
        self.button_listen.clicked.connect(self.listen_pressed)
        self.button_pause_resume.clicked.connect(self.pause_resume_pressed)
        self.button_stop.clicked.connect(self.stop_pressed)
        self.button_exit.clicked.connect(self.exit_pressed)

        self.button_count_play = 0
        self.button_pause_resume_count = 0

    #Open AI get completion method      
    def get_completion(self, prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
          model=model,
          messages=messages,
          temperature=0
        )
        return response.choices[0].message["content"]

    #Done thread
    def done_(self):
        self.label.setText("Done.")

    #Processing thread     
    def processing_th(self):
        self.label.setText("Processing...") 

    #Submit Button Pressed
    def submit_pressed(self):
        t1 = th.Timer(0.5, self.processing_th)
        t1.start()
        t2 = th.Timer(0.5, self.main_process)
        t2.start()  

    #Main Process routed by Submit Pressed
    def main_process(self):
        self.prompt = self.text_input.text()
        self.response = self.get_completion(self.prompt)
        self.label_content.setText(self.response)

        t3 = th.Timer(0.5,self.done_)
        t3.start()

    #AI speaking thread
    def listen_th(self):
        self.label.setText("AI Speaking...") 

    #AI speaking process
    def listen_pressed(self):
        try: 
            if os.path.exists("/response.mp3"):
                self.audio = AudioPlayer("/response.mp3")
                self.audio.close()
                os.remove("/response.mp3")
          
            myobj = gTTS(text=self.response, lang=language)
            myobj.save("/response.mp3")

            self.button_count_play = 0

            if self.button_count_play == 0:
                self.audio = AudioPlayer("/response.mp3")

            self.button_count_play += 1

            if self.button_count_play >= 1:
                self.audio.play(block=False)
                t4 = th.Timer(0.3, self.listen_th)
                t4.start()

        except AttributeError:
            self.label_content.setText("Nothing to speak.")
            self.label_content.show()

    #Pause & Resume pressed method           
    def pause_resume_pressed(self):
        try:
            self.button_pause_resume_count += 1

            if self.button_pause_resume_count == 1:
                self.audio.pause()
                self.label.setText("AI Speech Paused.") 

            elif self.button_pause_resume_count == 2:
                self.audio.resume()
                self.label.setText("AI Speech Resumed.")  
                self.button_pause_resume_count = 0

        except AttributeError:
            self.label_content.setText("Nothing to pause or resume.")
            self.label_content.show()

    #Stop button pressed method
    def stop_pressed(self):
        try: 
            self.audio.stop()
            self.label.setText("AI Speech Stopped.")
        except AttributeError:
            self.label_content.setText("Nothing to stop.")
            self.label_content.show()

    #Close thread
    def close_th(self):
        if os.path.exists("/response.mp3"):
            self.audio = AudioPlayer("/response.mp3")
            self.audio.close()
            os.remove("/response.mp3") 

    #Exit button pressed method
    def exit_pressed(self, event):
        t5 = th.Timer(1, self.close_th)
        t5.start() 
        window.close()

    #Close method  
    def closeEvent(self, event):        
        t6 = th.Timer(1, self.close_th)
        t6.start()       
        window.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
