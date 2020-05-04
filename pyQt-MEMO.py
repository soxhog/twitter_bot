import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sip
import unicodedata
import sqlite3

dbname = "tweet-db.db"
tablename = "tweettable"
imagefolder = "画像/"

# グローバル変数の宣言
textbuff = ""
imgpathbuff = ""
textidbuff = 1

class MainWindow(QWidget):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		# ウィンドウの設定
		self.setGeometry(600, 200, 700, 600)	# ウィンドウの初期位置とサイズを指定
		self.setFixedSize(700, 600)				# ウィンドウのサイズを固定
		self.setWindowTitle('MEMOapl')			# ウィンドウのタイトルの設定

		# Textbox1（登録済み編集用）設定
		self.textbox1 = QTextEdit(self)
		self.textbox1.move(220, 20)
		self.textbox1.resize(460, 200)

		self.textbox1.textChanged.connect(self.textconut1)		# テキストが変化したときに残り文字をリストに表示する
		self.textbox1.setReadOnly(True)

		# Textbox2（新規登録用）設定
		self.textbox2 = QTextEdit(self)
		self.textbox2.move(220, 300)
		self.textbox2.resize(460, 200)
		self.textbox2.textChanged.connect(self.textconut2)		# テキストが変化したときに残り文字をリストに表示する

		# 画像のパス用のTextline1(登録済み編集用)設定
		self.textline1 = QLineEdit(self)
		self.textline1.move(220, 225)
		self.textline1.resize(400, 20)
		self.textline1.setReadOnly(True)

		# 画像のパス用のTextline2(登録済み編集用)設定
		self.textline2 = QLineEdit(self)
		self.textline2.move(220, 505)
		self.textline2.resize(400, 20)

		# Listbox設定
		self.listbox = QListWidget(self)
		self.listbox.move(20, 20)
		self.listbox.resize(180, 505)
		list_title = list_from_db()				# データベースからタイトルリストを取得
		self.listbox.addItems(list_title)		# Listboxにタイトルリストを追加
		self.listbox.itemClicked.connect(self.list2textedit)

		# Textbox1の残り文字数を表示するlabel1を設定
		self.label1 = QLabel(self)
		self.label1.move(225, 250)
		self.label1.setText("残り:140.0文字")
		self.label1.resize(200, 20)

		# Textbox2の残り文字数を表示するlabel2を設定
		self.label2 = QLabel(self)
		self.label2.move(225, 530)
		self.label2.setText("残り:140.0文字")
		self.label2.resize(200, 20)

		# 登録したテキストの数を表示するlabel3を設定
		self.label3 = QLabel(self)
		self.label3.move(25, 530)
		self.label3.resize(180, 20)
		self.label3.setText("ツイート登録数:{0}".format(len(list_title)))

		# 変更時のSQLiteのエラーを表示するlabel4を設定
		self.label4 = QLabel(self)
		self.label4.move(225, 275)
		self.label4.resize(460, 20)

		# 登録時のSQLiteのエラーを表示するlabel5を設定
		self.label5 = QLabel(self)
		self.label5.move(225, 275)
		self.label5.resize(460, 20)

		# 変更ボタンの設定
		self.btnConv1 = QPushButton(self)
		self.btnConv1.move(625, 245)
		self.btnConv1.resize(60, 25)
		self.btnConv1.setText("変更")
		self.btnConv1.setDisabled(True)

		# 取消ボタンの設定
		self.btnConv2 = QPushButton(self)
		self.btnConv2.move(575, 245)
		self.btnConv2.resize(60, 25)
		self.btnConv2.setText("取消")
		self.btnConv2.setDisabled(True)

		# 編集ボタンの設定
		self.btnConv3 = QPushButton(self)
		self.btnConv3.move(525, 245)
		self.btnConv3.resize(60, 25)
		self.btnConv3.setText("編集")
		self.btnConv3.setDisabled(True)

		# 登録ボタンの設定
		self.btnConv4 = QPushButton(self)
		self.btnConv4.move(625, 545)
		self.btnConv4.resize(60, 25)
		self.btnConv4.setText("登録")

		# 削除ボタンの設定
		self.btnConv5 = QPushButton(self)
		self.btnConv5.move(4755, 245)
		self.btnConv5.resize(60, 25)
		self.btnConv5.setText("削除")
		self.btnConv5.setDisabled(True)

		# 挿入ボタンの設定
		self.btnConv6 = QPushButton(self)
		self.btnConv6.move(575, 525)
		self.btnConv6.resize(60, 25)
		self.btnConv6.setText("挿入")
		self.btnConv6.setDisabled(True)

		# 画像ファイルのファイルダイアログ参照ボタン(変更用)の設定
		self.btnConv7 = QPushButton(self)
		self.btnConv7.move(620, 220)
		self.btnConv7.resize(60, 25)
		self.btnConv7.setText("参照")
		self.btnConv7.setDisabled(True)

		# 画像ファイルのファイルダイアログ参照ボタン(登録用)の設定
		self.btnConv8 = QPushButton(self)
		self.btnConv8.move(620, 500)
		self.btnConv8.resize(60, 25)
		self.btnConv8.setText("参照")

		self.btnConv1.clicked.connect(self.doRewrite)
		self.btnConv2.clicked.connect(self.doCancel)
		self.btnConv3.clicked.connect(self.enableEdit)
		self.btnConv4.clicked.connect(self.doWrite)
		self.btnConv5.clicked.connect(self.doDelete)
		self.btnConv6.clicked.connect(self.doInsert)
		self.btnConv7.clicked.connect(self.showDialog1)
		self.btnConv8.clicked.connect(self.showDialog2)

	# Textbox1に変更があった場合にlabel1に残り文字数を表示
	def textconut1(self):
		s = self.textbox1.toPlainText()		# Textbox1の内容を取得
		count_s = 140 - get_east_asian_width_count(s)
		self.label1.setText("残り:{0}文字".format(count_s))

	# Textbox2に変更があった場合にlabel1に残り文字数を表示
	def textconut2(self):
		s = self.textbox2.toPlainText()		# Textbox2の内容を取得
		count_s = 140 - get_east_asian_width_count(s)
		self.label2.setText("残り:{0}文字".format(count_s))

	# リストで選択したタイトルのテキストをTextbox1に表示する
	def list2textedit(self, item):
		global textidbuff

		self.btnConv3.setDisabled(False)		# 編集ボタンをアクティブにする
		self.btnConv5.setDisabled(False)		# 削除ボタンをアクティブにする
		self.btnConv6.setDisabled(False)		# 挿入ボタンをアクティブにする
		text1, imgpath1, textid = text_from_db(item.text())
		textidbuff = textid						# 選択したテキストのIDを保存しておく
		self.textbox1.setText(text1)
		self.textline1.setText(imgpath1)

	# 変更ボタンを押した時の動作
	def doRewrite(self):
		global textidbuff

		self.label4.clear()
		text = self.textbox1.toPlainText()		# Textbox1の内容を取得
		imgpath = self.textline1.text()
		try:
			text_update_db(textidbuff, text, imgpath)
		except sqlite3.Error:
			self.label4.setText('<p><font size="3" color="#ff0000">変更できませんでした</font></p>')	#変更できなかったときに警告する
		self.textbox1.setReadOnly(True)			# Textbox1を非アクティブにする
		self.textline1.setReadOnly(True)		# Textline1を非アクティブにする
		self.listbox.setReadOnly(False)			# listboxをアクティブに戻す
		self.btnConv1.setReadOnly(True)			# 変更ボタンを非アクティブにする
		self.btnConv2.setReadOnly(True)			# 取消ボタンを非アクティブにする
		self.btnConv3.setReadOnly(False)		# 編集ボタンをアクティブに戻す
		self.btnConv4.setReadOnly(False)		# 登録ボタンをアクティブに戻す
		self.btnConv5.setReadOnly(False)		# 削除ボタンをアクティブに戻す
		self.btnConv6.setReadOnly(False)		# 挿入ボタンをアクティブに戻す
		self.btnConv7.setReadOnly(True)			# 参照ボタン2を非アクティブにする
		self.listbox.clear()
		list_title = list_from_db()
		self.listbox.addItems(list_title)		# listboxを更新
		self.label3.setText("ツイート登録数:{0}".format(len(list_title)))
		self.btnConv6.setDisabled(True)			# 挿入ボタンを非アクティブにする

	# 取消ボタンを押した時の動作
	def doCancel(self):
		global textbuff
		global imgpathbuff

		self.label4.clear()
		self.textbox1.setText(textbuff)			# Textbox1の内容を編集前に戻す
		self.textline1.setText(imgpathbuff)
		self.textbox1.setReadOnly(True)			# Textbox1を非アクティブにする
		self.textline1.setReadOnly(True)		# Textline1を非アクティブにする
		self.listbox.setReadOnly(False)			# listboxをアクティブに戻す
		self.btnConv1.setReadOnly(True)			# 変更ボタンを非アクティブにする
		self.btnConv2.setReadOnly(True)			# 取消ボタンを非アクティブにする
		self.btnConv3.setReadOnly(False)		# 編集ボタンをアクティブに戻す
		self.btnConv4.setReadOnly(False)		# 登録ボタンをアクティブに戻す
		self.btnConv5.setReadOnly(False)		# 削除ボタンをアクティブに戻す
		self.btnConv6.setReadOnly(False)		# 挿入ボタンをアクティブに戻す
		self.btnConv7.setReadOnly(True)			# 参照ボタン2を非アクティブにする

	# 編集ボタンを押した時の動作
	def enableEdit(self):
		global textbuff:
		global imgpathbuff

		self.label4.clear()
		textbuff = self.textbox1.toPlainText()	# textbuffに編集前の内容を保存
		imgpathbuff = self.textline1.text()		# imgpathbuffに編集前の画像のパスを保存
		self.textbox1.setReadOnly(False)		# Textbox1をアクティブに戻す
		self.textline1.setReadOnly(False)		# Textline1をアクティブに戻す
		self.listbox.setReadOnly(True)			# listboxを非アクティブにする
		self.btnConv1.setReadOnly(False)		# 変更ボタンをアクティブに戻す
		self.btnConv2.setReadOnly(False)		# 取消ボタンをアクティブに戻す
		self.btnConv3.setReadOnly(True)			# 編集ボタンを非アクティブにする
		self.btnConv4.setReadOnly(True)			# 登録ボタンを非アクティブにする
		self.btnConv5.setReadOnly(True)			# 削除ボタンを非アクティブにする
		self.btnConv6.setReadOnly(True)			# 挿入ボタンを非アクティブにする
		self.btnConv7.setReadOnly(False)		# 参照ボタン2をアクティブに戻す


	# ボタンをクリック時の動作
	def showDialog(self):
		imagefolder = "画像/"
		fname = QFileDialog.getOpenFileName(self, 'Open file', imagefolder)

		#ファイルを選択した時の動作
		if fname[0]:
			imgpath = fname[0].split("/")
			# 相対パスへの変換
			self.label.setText(imgpath[-3] + "/" + imgpath[-2] + "/" + imgpath[-1])

# 全角文字を1、半角文字を0.5として文字数をカウントする関数
def get_east_asian_width_count(text):
	count = 0.0
	for c in text:
		if unicodedata.east_asian_width(c) in 'FWA':
			count += 1.0
		else:
			count += 0.5
	return count

# データベースからタイトルのリストを取り出す
def list_from_db():
	conn = sqlite3.connect(dbname)
	cur = conn.cursor()
	cur.execute(u"select title from {0} order by id asc".format(tablename))		# タイトルのカラムを抜き出しID昇順でソート
	tuplelist = cur.fetchall()
	title_list = [i[0] for i in tuplelist]
	conn.close()
	return title_list

# データベースから選んだタイトルのテキストを取り出す
def text_from_db(listword):
	conn = sqlite3.connect(dbname)
	cur = conn.cursor()
	listword = text2SQL(listword)
	cur.execute(u"select * from {0} where title = {1}".format(tablename, listword))		# タイトルが一致する行のテキストを選ぶ
	tupletext = cur.fetchone()
	text = tupletext[2]
	imgpath = tupletext[3]
	textid = tupletext[0]
	conn.close()
	return text, imgpath, textid

# 文字列をSQLite仕様に変換する関数
def text2SQL(text):
	if text == "":
		text = "NULL"
	else:
		text = text.replace("'", "''")		# シングルコーテーションをエスケープ処理
		text = "'{}'".format(text)
	return text

# データベースのテキストを更新する
def text_update_db(textid, text, imgpath):
	erroralert = False					# エラーフラグ
	conn = sqlite3.connect(dbname)
	cur = conn.cursor()
	imgpath = text2SQL(imgpath)
	title = text.splitlines()
	if len(title) == 0: title.append("")
	title[0] = text2SQL(title[0])
	text = text2SQL(text)
	try:
		cur.execute(u"update '{0}' set text = {1}, title = {2}, image = {3} where id = '{4}'".format(tablename, text, title[0], imgpath, textid))		# 指定したIDのテキストと画像のパスを更新、1行目をタイトルとして登録
	except sqlite3.Error:
		erroralert = True				# エラ〜フラグを立てる
		pass							# 一旦エラーをパス
	finally:
		conn.commit()
		conn.close()
	if erroralert: raise sqlite3.Error	# エラーフラグが立っていたら改めてエラーを出す

def main():
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
