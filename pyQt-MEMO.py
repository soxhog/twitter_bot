import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sip

class MainWindow(QWidget):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.setGeometry(600, 200, 700, 600)	# ウィンドウの初期位置とサイズを指定
		self.setFixedSize(700, 600)				# ウィンドウのサイズを固定
		self.setWindowTitle('MEMOapl')			# ウィンドウのタイトルの設定

		# テキストボックス
		self.textbox = QTextEdit(self)
		self.textbox.move(220, 20)
		self.textbox.resize(460, 200)
		self.textbox.setText("テキストボックス")

		# 1行テキストボックス
		self.textline = QLineEdit(self)
		self.textline.move(220, 225)
		self.textline.resize(400, 20)
		self.textline.setText("1行テキストボックス")

		# ボタン
		self.btnConv = QPushButton(self)
		self.btnConv.move(625, 245)
		self.btnConv.resize(60, 25)
		self.btnConv.setText("ボタン")

		# ラベル
		self.label = QLabel(self)
		self.label.move(225, 250)
		self.label.resize(200, 20)
		self.label.setText("ラベル")

		self.btnConv.clicked.connect(self.showDialog)	# ボタンをクリック時にファイルダイアログを開く

	# ボタンをクリック時の動作
	def showDialog(self):
		imagefolder = "画像/"
		fname = QFileDialog.getOpenFileName(self, 'Open file', imagefolder)

		#ファイルを選択した時の動作
		if fname[0]:
			imgpath = fname[0].split("/")
			# 相対パスへの変換
			self.label.setText(imgpath[-3] + "/" + imgpath[-2] + "/" + imgpath[-1])

def main():
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
