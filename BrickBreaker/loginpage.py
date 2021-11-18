from tkinter import *
from PIL import Image,ImageTk


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
passwordEntry = Entry(window, textvariable=password, show="*", font=20, width=210, justify='center')
passwordEntry.pack(anchor=W,ipadx=10,ipady=2,padx=30)

signupButton = Button(window, text="Sign Up")
signupButton.config(width=6, height=1)
signupButton.pack(side=LEFT, padx=(60,0), ipadx=5, ipady=5,)

signinButton = Button(window,text="Sign In")
signinButton.config(width=6,height=1)
signinButton.pack(side=RIGHT, padx=(0,60), ipadx=5, ipady=5)



if __name__ == '__main__':
	window.mainloop()