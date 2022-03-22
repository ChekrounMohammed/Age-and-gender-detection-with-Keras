import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image
from PIL import ImageTk
import numpy as np
import os
import PIL
import tensorflow as tf
import cv2
import cvlib as cv
#definition des fonctions 
filepath = None


def age():
	global filepath
	global panelA
	global window
	import tensorflow as tf
	model = tf.keras.models.load_model("C:/Users/ATLAS PRO ELECTRO/Desktop/PFE/age new/age5.h5")
	image_path = filepath
	img = cv2.imread(image_path)
	img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
	imge = cv2.resize(img, (96, 96))
	imge = np.array(imge)
	imge = np.expand_dims(imge, 0)
	cf = model.predict(imge)
	label = "age :"+str(int(cf[0]))
	face, confidence = cv.detect_face(img)
	for  f in face :
	    (startX, startY)=f[0], f[1]
	    (endX, endY)= f[2], f[3]

	    cv2.rectangle(img, (startX,startY), (endX,endY), (0,255,0), 2)
	    try :
		    face_crop = np.copy(img[startY:endY,startX:endX])
		    face_crop = cv2.resize(face_crop, (50,50))
		    face_crop = np.array(face_crop)
		    face_crop = np.expand_dims(face_crop, 0)
	    except Exception as e:
    		print(str(e))
	    
	    label = "age :"+str(int(cf[0]))
	    Y = startY - 10 if startY - 10 > 10 else startY + 10
	    cv2.putText(img, label, (startX, Y),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (0, 255, 0), 2)
	    break
	img = cv2.resize(img, (500, 500))
	img =Image.fromarray(img)
	photo = ImageTk.PhotoImage(img)   
	if panelA is None:
		panelA = Label(image=photo)    
		panelA.image = photo            
		panelA.pack(side="center", padx=10,pady=10)
	else :
		panelA.configure(image=photo)
		panelA.image = photo	





def gender():
	global filepath
	global panelA
	global window
	class_names=['male', 'female']
	model = tf.keras.models.load_model("C:/Users/ATLAS PRO ELECTRO/Desktop/PFE/gender.h5")
	image_path = filepath
	img = cv2.imread(image_path)
	img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
	img = cv2.resize(img, (512, 512))
	face, confidence = cv.detect_face(img)
	for  f in face :
	    (startX, startY)=f[0], f[1]
	    (endX, endY)= f[2], f[3]
	    if (f[2]>512 or f[3]>512):
	    	break
	    cv2.rectangle(img, (startX,startY), (endX,endY), (0,255,0), 2)
	    try :
		    face_crop = np.copy(img[startY:endY,startX:endX])
		    face_crop = cv2.resize(face_crop, (50,50))
		    face_crop = np.array(face_crop)
		    face_crop = np.expand_dims(face_crop, 0)
	    except Exception as e:
    		print(str(e))
	    cf = model.predict(face_crop)

	    score = tf.nn.sigmoid(cf[0])
	    label = class_names[np.argmax(score)]
	    idx = 100 * np.max(score)
	    label = label +" pr:"+ str(int(idx))+"%"
	    Y = startY - 10 if startY - 10 > 10 else startY + 10
	    cv2.putText(img, label, (startX, Y),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (0, 255, 0), 2)
	img =Image.fromarray(img)
	photo = ImageTk.PhotoImage(img)   
	if panelA is None:
		panelA = Label(image=photo)    
		panelA.image = photo            
		panelA.pack(side="center", padx=10,pady=10)
	else :
		panelA.configure(image=photo)
		panelA.image = photo	


#définition des fonctions
filepath = None

def open_file():
	"""Open a file for editing."""
	global filepath
	global root
	global panelA

	filepath = askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
	monimage = Image.open(filepath)
	monimage = monimage.resize((500, 500), Image.LANCZOS)
	photo = ImageTk.PhotoImage(monimage)   ## Création d'une image compatible Tkinter
	if panelA is None:
		panelA = Label(image=photo,pady=10)    
		panelA.image = photo   

		panelA.place(x=300,y=100)
	else :
		panelA.configure(image=photo,pady=10)
		panelA.image = photo
		panelA.place(x=300,y=100)	

	btngn = Button(root, text ="Gender" ,width=10 , bg='#567', fg='White' ,command=gender)
	btngn.place(x=550, y=50)
	btnag = Button(root, text ="Age" ,width=10, bg='#567', fg='White' , command=age) 
	btnag.place(x=450, y=50)









root =tk.Tk()

panelA = None


root.title("Age and Gender Estimation")
root.geometry("1080x720")


#creer un menu

menu_bar = Menu(root)

#creer un premier menu

file_menu = Menu(menu_bar, tearoff=0 )
file_menu.add_command(label='Nouveau', command=open_file)
file_menu.add_command(label='Save')
file_menu.add_command(label='Exit', command=root.quit)
menu_bar.add_cascade(label='Fichier',menu=file_menu)
root.config(menu=menu_bar)

def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo #avoid garbage collection

img = Image.open("backgroundd.jpg")
copy_of_image = img.copy()
photo = ImageTk.PhotoImage(img)
label = Label(root, image = photo)
label.bind('<Configure>', resize_image)
label.pack(fill=BOTH, expand = YES)

root.mainloop()



