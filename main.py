import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QLineEdit, QPushButton, QProgressBar
import sys
import argparse
import glob

class OCRLabelApp(QWidget):
    def __init__(self, image_dir):
        super().__init__()
        self.title_app = "OCR Labeler"
        self.x = 300
        self.y = 300
        self.w = 800
        self.h = 450
        self.font_size = 25

        self.img_paths = [path for path in sorted(glob.glob(image_dir + "/*")) if '.txt' not in path]
        self.total_img = len(self.img_paths)
        self.current_img_index = 0

        self.layout = QGridLayout()
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle(self.title_app)
        self.setGeometry(self.x, self.y, self.w, self.h)

        # Image widget
        self.label = QLabel()
        self.update_display_img()

        # Text box widget
        self.text_box = QLineEdit()
        font = self.text_box.font()
        font.setPointSizeF(self.font_size)
        self.text_box.setFont(font)
        self.text_box.resize(280, 50)
        self.update_text_box()

        # Button
        self.next_button = QPushButton('Next Image')
        self.next_button.clicked.connect(self.handle_press_next_button)
        self.previous_button = QPushButton("Previous Image")
        self.previous_button.clicked.connect(self.hanle_press_previous_button)

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.total_img)
        self.progress_bar.setValue(self.current_img_index+1)



        # Add all widget
        self.layout.addWidget(self.label, 0, 0, 1, -1)
        self.layout.addWidget(self.text_box, 1, 0, 1, 5)
        self.layout.addWidget(self.next_button, 1, 5, 1, 1)

        self.layout.addWidget(self.previous_button, 2, 5, 1, 1)
        self.layout.addWidget(self.progress_bar, 2, 0 , 1, 5)

        self.setLayout(self.layout)
        self.show()

    def convert_size(self, old_w, old_h):
        max_w = self.w - 100
        if old_w > max_w:
            return max_w, int(old_h / old_w) * max_w
        else:
            return old_w, old_h

    def update_text_box(self):
        self.text_box.clear()
        label_text_path = self.img_paths[self.current_img_index].split(".")[0] + ".txt"
        if os.path.exists(label_text_path) and os.path.getsize(label_text_path):
            label_of_img = open(label_text_path, 'r', encoding='utf-8').read().strip()
            self.text_box.setText(label_of_img)

    def update_display_img(self):
        pixmap = QPixmap(self.img_paths[self.current_img_index])          
        new_w, new_h = self.convert_size(pixmap.width(), pixmap.height()) 
        self.label.setPixmap(pixmap.scaled(new_w, new_h))                 
        self.label.resize(new_w, new_h)                                   


    def handle_press_next_button(self):
        if self.current_img_index < self.total_img-1:

            self.save_label()
            self.current_img_index +=1
            self.update_all()
        else:
            self.save_label()

    def hanle_press_previous_button(self):
        if self.current_img_index > 0:
            self.save_label()
            self.current_img_index -=1
            self.update_all()
        else:
            self.save_label()

    def save_label(self):
        save_txt_path = self.img_paths[self.current_img_index].split(".")[0] + ".txt"
        label_text = self.text_box.text()
        with open(save_txt_path, 'w', encoding='utf-8') as f:
            f.write(label_text)

    def update_all(self):
        # update image
        self.update_display_img()

        # update text box
        self.update_text_box()

        # update progress bar
        self.progress_bar.setValue(self.current_img_index+1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_dir", type=str, default="image_dir")
    args = parser.parse_args('')
    app = QApplication(sys.argv)
    ex = OCRLabelApp(args.image_dir)
    sys.exit(app.exec_())