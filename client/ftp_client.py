from ftplib import FTP
import tkinter as tk
from tkinter import ttk
from tkinter import *
import os
from tkinter import filedialog as fd 

# Fontların tanımlanması
NORM_FONT = ("Helvetica", 10)
LARGE_FONT = ("Helvetica", 14)
EXTRA_FONT = ("Helvetica", 18,"bold")
client_dir = os.getcwd()
server_dir = r"C:\Users\Pc\Desktop\FTP\server"


class Ftp(): # FTP sınıfının yaratılması

	def __init__(self): #constructor
		

		try :
			# bağlantının açılması
			self.ftp = FTP('')  

			self.ftp.connect('localhost',1026)
			self.ftp.login()
			self.ftp.cwd('/') 
			self.current_dir = self.ftp.pwd() 

			print("Connected to the host successfully.")
			print("Host Name: ftp.nluug.nl" )
		except Exception as e:
			print(e)


	def set_currentdir(self,directory):
		self.ftp.cwd(directory)
	def get_currentdir(self):
		return self.ftp.pwd()
	def get_files(self):
		return self.ftp.nlst()
	def download(self,selected_dir):
			self.ftp.cwd("/")

			file_to_download = selected_dir.split("/")[6]
			
			localfile = open(file_to_download, 'wb')
			try:
				print("Downloading " + file_to_download + "...")
				self.ftp.retrbinary("RETR "+ file_to_download,localfile.write,1024) # Retrieve a file in binary transfer mode.
				print("\n")
				popup = tk.Tk()
				popup.wm_title(":)")
				label = ttk.Label(popup,text = "File Downloaded Successfully.",font = NORM_FONT)
				label.pack(side="top",fill="x",pady=10)
				b1 = ttk.Button(popup,text="Okey",command=popup.destroy)
				b1.pack()
				popup.mainloop()
				try:
					localfile.close()
				except: 
					pass
			
				
			except Exception as e:
				print(e)
			
	def upload(self,selected_dir):
		self.ftp.cwd("/")
		file_to_upload = selected_dir.split("/")[6]
		ext = os.path.splitext(file_to_upload)[1]
		try:
			if ext in(".txt",".htm",".html"):
				storeCommand = "STOR %s"%file_to_upload;
				fileObject  = open(file_to_upload, 'rb');
				self.ftp.storlines(storeCommand, fileObject)
			else:

				self.ftp.storbinary("STOR "+file_to_upload,open(file_to_upload,"rb"),1024)
			popup = tk.Tk()
			popup.wm_title(":)")
			label = ttk.Label(popup,text = "File Downloaded Successfully.",font = NORM_FONT)
			label.pack(side="top",fill="x",pady=10)
			b1 = ttk.Button(popup,text="Okey",command=popup.destroy)
			b1.pack()
			popup.mainloop()
			try:
				localfile.close()
			except:
				pass

		except Exception as e :
			print(e)

	def listdirectory(self): # directory içindeki dosyalar listelenir.
		data = []
		self.ftp.dir(data.append)

		return data


	def CreateDir(self,dir_name):
		self.ftp.cwd("/")
		self.ftp.mkd(dir_name)


	def DeleteFile(self,delete_name):
		try:
			self.ftp.delete(delete_name)
			print("\n")
			print(delete_name + " deleted successfully!!")
		except Exception as e:
			print(e)

	def DeleteDir(self,delete_name):
		try:
			self.ftp.rmd(delete_name)
			print("\n")
			print(delete_name + " deleted successfully!!")
		except Exception as e:
			print(e)


class FtpApp(tk.Tk):  # app'in oluşturulması
    
    def __init__(self,*args,**kwargs):  # initializing class
        
        tk.Tk.__init__(self,*args,**kwargs)
        
        tk.Tk.wm_title(self,'FTP APP')
        
        ttk.Style().configure('TButton',relief='flat',background='#000',font=('Sans',15,'bold'))
                 
        init_btn = ttk.Style()
        
        init_btn.configure('Bold.TButton',font=('Sans','15','bold'),background='red')
        
                 
                 
        container = tk.Frame(self,borderwidth=2, relief="solid")
        container.pack(side = 'top',fill = 'both',expand = True)
        container.grid_rowconfigure(0,weight = 1) # minumum size=0, weight = 1 means priority
        container.grid_columnconfigure(0,weight = 1)
        
        menubar = tk.Menu(container)
        
        file_menu = tk.Menu(menubar,tearoff = 0)

        file_menu.add_command(label='Exit',command = self.destroy)
        
        menubar.add_cascade(label = 'File',menu = file_menu)
        
        tk.Tk.config(self,menu=menubar)
        self.frames = {}
        
        
        for F in (StartPage,PageThree):
            
            frame = F(container,self)
        
            self.frames[F] = frame
            
            frame.grid(row=0,column=0,stick='nsew')
            
            
        self.show_frame(StartPage)
        
        
    
    def show_frame(self,cont):
        
        frame = self.frames[cont]
        
        frame.tkraise()

class StartPage(tk.Frame):
    
    def __init__(self,parent,controller):
        
        self.ftp = ""

        def start_connection():  # bağlantının başlatılması
        	try:

        		self.ftp = Ftp ()
        		# bağlantı başarıyla başlatıldı uyarısı.

        		popup = tk.Tk()
        		popup.wm_title(":)")
        		label = ttk.Label(popup,text = "Connection Succeeded",font = NORM_FONT)
        		label.pack(side="top",fill="x",pady=10)
        		b1 = ttk.Button(popup,text="Okey",command = popup.destroy)
        		b1.pack()
        		popup.mainloop()

        	except Exception as e:
        		popup = tk.Tk()
        		popup.wm_title("WARNİNG!!")
        		label = ttk.Label(popup,text =e,font = NORM_FONT)
        		label.pack(side="top",fill="x",pady=10)
        		b1 = ttk.Button(popup,text="Okey",command=popup.destroy)
        		b1.pack()
        		popup.mainloop()

        def list_SF(frame,ftp):  # server file'ların listelenmesi

        	if(ftp == ""):
        		popup = tk.Tk()
        		popup.wm_title("WARNİNG!!")
        		label = ttk.Label(popup,text = "Please start connection first.",font = NORM_FONT)
        		label.pack(side="top",fill="x",pady=10)
        		b1 = ttk.Button(popup,text="Okey",command=popup.destroy)
        		b1.pack()
        		popup.mainloop()

        	else:
        		for widget in frame.winfo_children():
        			widget.destroy()

        		listbox = Listbox(frame,width=100,height=10,font=EXTRA_FONT)
        		listbox.pack()
        		listbox.insert(END,"ALL SERVER FİLES:")

        		data = ftp.listdirectory()

        		for d in data:
        			listbox.insert(END,d)
        def list_CF(frame,ftp):  # client file'ların listelenmesi

        	if(ftp == ""):
        		popup = tk.Tk()
        		popup.wm_title("WARNİNG!!")
        		label = ttk.Label(popup,text = "Please start connection first.",font = NORM_FONT)
        		label.pack(side="top",fill="x",pady=10)
        		b1 = ttk.Button(popup,text="Okey",command=popup.destroy)
        		b1.pack()
        		popup.mainloop()

        	else:
        		for widget in frame.winfo_children():
        			widget.destroy()

        		listbox = tk.Listbox(frame,width=100,height=10,font=EXTRA_FONT)
        		listbox.pack()
        		listbox.insert(END,"ALL CLİENT FİLES:")

        		data = [f for f in os.listdir(client_dir)]

        		for d in data:
        			listbox.insert(END,d)

        def create_dir(ftp):  # directry yaratılması
        	def getentry():  # kullanıcdan yaratılacak directory için input alma
      
        		data = entry.get()
        		ftp.CreateDir(data)
        		pop.destroy()
        	if(ftp == ""):
        		popup = tk.Tk()
        		popup.wm_title("WARNİNG!!")
        		label = ttk.Label(popup,text = "Please start connection first.",font = NORM_FONT)
        		label.pack(side="top",fill="x",pady=10)
        		b1 = ttk.Button(popup,text="Okey",command=popup.destroy)
        		b1.pack()
        		popup.mainloop()
        	else:
        		pop = tk.Tk()
        		label = ttk.Label(pop,text="Enter DIR name please:")
        		entry = tk.Entry(pop)
        		button1 = tk.Button(pop,text='Enter', command=lambda: getentry())
        		label.pack()
        		entry.pack()
        		entry.focus_set()
        		button1.pack()
        		pop.mainloop()

        def delete_dir(ftp): # directory'nin silinmesi
        	def getentry():
        		data = entry.get()
        		ftp.DeleteDir(data)
        		pop.destroy()
        	if(ftp == ""):
        		popup = tk.Tk()
        		popup.wm_title("WARNİNG!!")
        		label = ttk.Label(popup,text = "Please start connection first.",font = NORM_FONT)
        		label.pack(side="top",fill="x",pady=10)
        		b1 = ttk.Button(popup,text="Okey",command=popup.destroy)
        		b1.pack()
        		popup.mainloop()
        	else:
        		pop = tk.Tk()
        		label = ttk.Label(pop,text="Enter the fale name to be deleted:")
        		entry = tk.Entry(pop)
        		button1 = tk.Button(pop,text='Enter', command=lambda: getentry())
        		label.pack()
        		entry.pack()
        		entry.focus_set()
        		button1.pack()
        		pop.mainloop()

        def delete_file(ftp): # directory'nin silinmesi
        	def getentry():
        		data = entry.get()
        		ftp.DeleteFile(data)
        		pop.destroy()
        	if(ftp == ""):
        		popup = tk.Tk()
        		popup.wm_title("WARNİNG!!")
        		label = ttk.Label(popup,text = "Please start connection first.",font = NORM_FONT)
        		label.pack(side="top",fill="x",pady=10)
        		b1 = ttk.Button(popup,text="Okey",command=popup.destroy)
        		b1.pack()
        		popup.mainloop()
        	else:
        		pop = tk.Tk()
        		label = ttk.Label(pop,text="Please enter the file name to be deleted:")
        		entry = tk.Entry(pop)
        		button1 = tk.Button(pop,text='Enter', command=lambda: getentry())
        		label.pack()
        		entry.pack()
        		entry.focus_set()
        		button1.pack()
        		pop.mainloop()         		

        def download_file(ftp):

        	if(ftp == ""):
        		popup = tk.Tk()
        		popup.wm_title("WARNİNG!!")
        		label = ttk.Label(popup,text = "Please start connection first.",font = NORM_FONT)
        		label.pack(side="top",fill="x",pady=10)
        		b1 = ttk.Button(popup,text="Okey",command=popup.destroy)
        		b1.pack()
        		popup.mainloop()
        	else:
        		try:
	        		selected_file = fd.askopenfilename(initialdir=server_dir) # show an "Open" dialog
	        	except:
	        		selected_file = fd.askopenfilename() # without initial dir an "Open" dialog

	        	ftp.download(selected_file)


        def upload_file(ftp):

        	if(ftp == ""):
        		popup = tk.Tk()
        		popup.wm_title("WARNİNG!!")
        		label = ttk.Label(popup,text = "Please start connection first.",font = NORM_FONT)
        		label.pack(side="top",fill="x",pady=10)
        		b1 = ttk.Button(popup,text="Okey",command=popup.destroy)
        		b1.pack()
        		popup.mainloop()
        	else:

	        	selected_file = fd.askopenfilename(initialdir=client_dir) # show an "Open" dialog 
	        	ftp.upload(selected_file)


        tk.Frame.__init__(self,parent)
        
        self.frame_islemler = tk.Frame(self,borderwidth=2, relief="solid")
        self.sonuclar = tk.Frame(self,borderwidth=2, relief="solid")

        # ara yüz elemanlarının oluşturulması
        
        welcome_label = tk.Label(self.frame_islemler,text = 'Welcome to the FTP App.',font = LARGE_FONT)
        
        welcome_label.grid(pady = 10,padx = 10,row=0, column=0)


        btn_start_connection = ttk.Button(self.frame_islemler,text="Start Connection",command = lambda :start_connection())
        btn_start_connection.grid(row=1, column=0,padx=5,pady=5,sticky="we")

        btn_list_serverfiles = ttk.Button(self.frame_islemler,text="List All Server Files",command = lambda :list_SF(self.sonuclar,self.ftp))
        btn_list_serverfiles.grid(row=2, column=0,padx=5,pady=5,sticky="we")

        btn_list_clientfiles = ttk.Button(self.frame_islemler,text="List All Client Files",command = lambda :list_CF(self.sonuclar,self.ftp))
        btn_list_clientfiles.grid(row=3,column=0,padx=5,pady=5,sticky="we")

        btn_download = ttk.Button(self.frame_islemler,text="Download File",command = lambda :download_file(self.ftp))
        btn_download.grid(row=4,column=0,padx=5,pady=5,sticky="we")
        btn_upload = ttk.Button(self.frame_islemler,text="Upload File",command = lambda :upload_file(self.ftp))
        btn_upload.grid(row=5,column=0,padx=5,pady=5,sticky="we")

        btn_creatdir = ttk.Button(self.frame_islemler,text="Create Directory",command = lambda :create_dir(self.ftp))
        btn_creatdir.grid(row=6,column=0,padx=5,pady=5,sticky="we")

        btn_deletedir = ttk.Button(self.frame_islemler,text="Delete Directory",command = lambda :delete_dir(self.ftp))
        btn_deletedir.grid(row=7,column=0,padx=5,pady=5,sticky="we")

        btn_deletefile = ttk.Button(self.frame_islemler,text="Delete File",command = lambda :delete_file(self.ftp))
        btn_deletefile.grid(row=8,column=0,padx=5,pady=5,sticky="we")
        ###

        #packing
            
        self.frame_islemler.pack(side = 'left',fill = 'both',expand = True)
        
        self.sonuclar.pack(side = 'right',fill = 'both',expand = True)

        
class PageThree(tk.Frame):
    
    def __init__(self,parent,controller):
        
        tk.Frame.__init__(self,parent)


if __name__== "__main__":
	app = FtpApp()
	app.geometry('1280x720')
	app.mainloop()











