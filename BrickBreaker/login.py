from tkinter import *
from PIL import Image,ImageTk
import mysql.connector as mysql
import brickbreaker

mydb = mysql.connect(host="localhost",user="root",password="pass",database="brickbreaker")
cursor = mydb.cursor()

def checkusername(username):
	user = username.get()
	str = "SELECT * FROM users WHERE username='"+user+"'" # defining arguments
	try:
		cursor.execute(str)
		row = cursor.fetchone()
		if row is not None:
			return True
	except mysql.Error as error:
		mydb.rollback()
		print(error)
		print('Failed to get data!')

def check(password):
	symbol = {'@', '#', '$'}
	if len(password) < 8 and len(password) > 15:
		print('Password should be in between 8 to 15')
		return False
	if not any(char.isdigit() for char in password):
		print('Password must contain digit')
		return False
	if not any(char.isupper() for char in password):
		print('Password should have at least one uppercase letter')
		return False
	if not any(char.islower() for char in password):
		print('Password should have at least one lowercase letter')
		return False
	if not any(char in symbol for char in password):
		print('Password should have at least one of the symbols $ @ #')
		return False
	return True

def insert(username,password,highscore):
	try:
		s = "INSERT INTO users VALUES ('" + username + "','" + password + "','"+highscore+"');"
		cursor.execute(s)
		mydb.commit()
		print("New user registered in the database")
	except mysql.Error as error:
		print(error)
		mydb.rollback()
		print('Failed to add data in table!')

def signup():
	user = username.get()
	pswd = password.get()
	high = '0'
	correct = False
	if not checkusername(username):
		# if check(pswd):
		insert(user, pswd, high)
		print("User registered, Sign Up successful")
		brickbreaker.opengame(user,high)
	else:
		print("User already exists!")
			
def upd(score, username):
	try:
		s = "UPDATE users SET highscore= %s WHERE username= %s"
		args = (str(score), username)
		cursor.execute(s,args)
		mydb.commit()
		print("New High Score!")
	except mysql as error:
		print(error)
		mydb.rollback()
		print('Failed to update highscore!')

def signin():
	user = username.get()
	pswd = password.get()
	str = "SELECT * FROM users WHERE username= %s AND password=%s" # defining arguments
	args = (user, pswd)
	try:
		cursor.execute(str, args)
		row = cursor.fetchone()
		if row is not None:
			print("Login successful")
			h_s=row[2]
			brickbreaker.opengame(user,h_s)
		else:
			print("Invalid Login")

	except mysql.Error as error:
		print(error)
		mydb.rollback()
		print('Failed to get login data!')


if __name__ == '__main__':
	window=Tk()
	window.geometry("300x400")
	window.minsize(300,400)
	window.maxsize(300,400)
	window.title('BrickBreaker')
	window.configure(background='#1A1C21')

	img = Image.open("images/brickbreaker.jpg")
	img=img.resize((220,120))
	image = ImageTk.PhotoImage(img)
	Label(window,image=image).pack(anchor=N,pady=15)

	label1=Label(window, text="Log In to Your Account", fg="white")
	label1.configure(background='#1A1C21')
	label1.pack(anchor=N,ipadx=5)

	usernameLabel = Label(window, text=">> User Name", fg="white")
	usernameLabel.configure(background='#1A1C21')
	usernameLabel.pack(anchor=W,ipadx=5,pady=10)
	username = StringVar()
	usernameEntry = Entry(window, textvariable=username, font=20, width=210, justify='center')
	usernameEntry.pack(anchor=W,ipadx=10,ipady=2,padx=30)

	passwordLabel = Label(window, text=">> Password", fg="white")
	passwordLabel.configure(background='#1A1C21')
	passwordLabel.pack(anchor=W,ipadx=5,pady=10)
	password = StringVar()
	passwordEntry = Entry(window, textvariable=password, font=20, width=210, justify='center')
	passwordEntry.pack(anchor=W,ipadx=10,ipady=2,padx=30)

	signupButton = Button(window, text="Sign Up", command=lambda: signup())
	signupButton.config(width=6, height=1)
	signupButton.pack(side=LEFT, padx=(60,0), ipadx=5, ipady=5,)

	signinButton = Button(window,text="Sign In", command=lambda: signin())
	signinButton.config(width=6,height=1)
	signinButton.pack(side=RIGHT, padx=(0,60), ipadx=5, ipady=5)
	window.mainloop()