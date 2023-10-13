#Simple Open AI Qt Application with gTTS
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer, QThread, pyqtSignal

import os
import openai
from gtts import gTTS
from audioplayer import AudioPlayer

import threading as th
from time import sleep

#Api key and language
openai.api_key = "sk-..."
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
        button = QPushButton("Submit")
        button2 = QPushButton("Listen")
        button3 = QPushButton("Exit")

        self.label = QLabel("Welcome!")
       
        layout.addWidget(self.text_input)
        layout.addWidget(button)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(self.label_content)
        layout.addWidget(self.label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        button.clicked.connect(self.process_)
       
        button2.clicked.connect(self.listen_pressed)
        button3.clicked.connect(self.closeEvent)

        self.isplaying = False
        
    #Processing thread
    def processing_th(self):
        self.label.setText("Processing...")
        
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
    
    #Process with Submit Button Pressed
    def process_(self):
        t1 = th.Timer(0.3, self.processing_th)
        t1.start()
        #Main process activated 1 s after processing thread
        t3 = th.Timer(1, self.main_process)
        t3.start()
        
    #Main Process routed by Submit Pressed
    def main_process(self):
        self.prompt = self.text_input.text()
        self.response = self.get_completion(self.prompt)
        self.label_content.setText(self.response)    
    
        t2 = th.Timer(0.1,self.done_)
        t2.start()
        
    #Listen thread
    def listen_th(self):
        self.label.setText("AI Speaks...")
         
    #AI Speech thread with gTTS and Audio player
    def speech_ai_th(self):
        myobj = gTTS(text=self.response, lang=language)
        myobj.save("path//response.mp3")
        self.audio = AudioPlayer("path//response.mp3")
        self.audio.play(block=True)
        self.audio.close()
        os.remove("path//response.mp3") 
        self.isplaying = False

        t2 = th.Timer(0.1,self.done_)
        t2.start() 
    
    #AI speech method which is activated by listen button pressed   
    def listen_pressed(self):   
        try: 
            if not self.isplaying:
                t4 = th.Timer(1,self.listen_th)
                t4.start()
                self.isplaying = True
            if self.isplaying:
                t5 = th.Timer(1,self.speech_ai_th)
                t5.start()                    
        except AttributeError:
            self.label_content.setText("Error! Try Again with right prompt")
            self.label_content.show()
            
    #Close thread
    def close_th(self):
        self.isplaying = False 
        self.audio.close()
        
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
