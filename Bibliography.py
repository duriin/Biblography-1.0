from tkinter import *
from tkinter.font import Font
from tkinter import colorchooser
import datetime
import pyperclip
import mechanize
import os
# import time


csl_ico = os.path.join(os.path.dirname(__file__), 'csl_logo.ico')
color_picker_png = os.path.join(os.path.dirname(__file__),'color_picker.png')

si_websites = []

def si_process_bibliography():
	#start_time = time.time()
	global si_websites, date
	url = get_text(si_txt_url)[:-1]
	br = mechanize.Browser()
	br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')]
	try:
		br.open(url)
		titre = br.title()

		date = get_text(si_txt_date)[:-1]

		if '/' in date:
			#print(date)
			date = date_slash()

		if date == '':
			date = date_consultee()

		author = get_text(si_txt_author)
		author.lower()

		if author == '\n':
			author = transl_anon

		author = author.split()

		if len(author) == 2:
			prenom, nom = author
			author = nom.upper() + ', ' + prenom.title()
		else:
			author = ' '.join(author).upper()

		if language == 'Français':
			si_websites.append(f'{author}. {titre}, [En ligne], {url} (page consultée le {date})')
		elif language == 'English':
			si_websites.append(f'{author}. {titre}, [Online], {url} (page consulted on {date})')
		elif language == 'Español':
			si_websites.append(f'{author}. {titre}, [En línea], {url} (página consultada el {date})')

		show_websites = '\n\n'.join(si_websites)
		si_txt_result.delete('1.0', END)
		si_txt_result.insert('1.0', show_websites)
		#print("si: %s seconds" % (time.time() - start_time))

	except:
		si_txt_url.insert('1.0', transl_invalid)
		si_txt_url.bind('<FocusIn>', si_dis_inva)

p_websites = []

def p_process_bibliography():
	global p_websites, date, publication
	#start_time = time.time()
	url = get_text(p_txt_url)[:-1]
	br = mechanize.Browser()
	br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')]
	try:
		br.open(url)
		titre = br.title()
		date = get_text(p_txt_date)[:-1]

		if '/' in date:
			#print(date)
			date = date_slash()

		if date == '':
			date = date_consultee()

		author = get_text(p_txt_author)
		author.lower()

		if author == '\n':
			author = transl_anon

		author = author.split()

		if len(author) == 2:
			prenom, nom = author
			author = nom.upper() + ', ' + prenom.title()

		else:
			author = ' '.join(author).upper()

		domain = url.split('www.')[-1].split('://')[-1].split('/')[0].capitalize()
		publication = get_text(p_txt_publication)[:-1]

		if '/' in publication:
			#print(publication)
			publication = publication_slash()
			
		if publication == '':
			publication = publication_consultee()

		if language == 'Français':
			p_websites.append(f'{author}. «{titre}», {domain}, {publication}, [En ligne], {url} (page consultée le {date})')
		elif language == 'English':
			p_websites.append(f'{author}. "{titre}", {domain}, {publication}, [Online], {url} (page consulted on {date})')
		elif language == 'Español':
			p_websites.append(f'{author}. «{titre}», {domain}, {publication}, [En línea], {url} (página consultada el {date})')

		show_websites = '\n\n'.join(p_websites)
		p_txt_result.delete('1.0', END)
		p_txt_result.insert('1.0', show_websites)
		#print("p: %s seconds" % (time.time() - start_time))

	except:
		p_txt_url.insert('1.0', transl_invalid)
		p_txt_url.bind('<FocusIn>', p_dis_inva)

def date_consultee():
	global date

	date = datetime.datetime.now()

	if language == 'Français':
		months = {'January':'janvier', 'February':'février', 
		'March':'mars', 'April':'avril', 'May':'mai', 
		'June':'juin', 'July':'juillet', 'August':'août', 
		'September':'septembre', 'October':'octobre', 
		'November':'novembre', 'December':'décembre'}

		eng_month = date.strftime('%B')
		months = months[eng_month] 	
		return date.strftime(f"%d {months} %Y")

	elif language == 'English':
		eng_month = date.strftime('%B')
		months = eng_month
		return date.strftime(f"{months} %d, %Y")

	elif language == 'Español':
		months = {'January':'enero', 'February':'febrero', 
		'March':'marzo', 'April':'abril', 'May':'mayo', 
		'June':'junio', 'July':'julio', 'August':'agosto', 
		'September':'septiembre', 'October':'octubre', 
		'November':'noviembre', 'December':'diciembre'}

		eng_month = date.strftime('%B')
		months = months[eng_month] 
		return date.strftime(f"%d de {months} de %Y")

def publication_consultee():
	global publication

	publication = datetime.datetime.now()

	if language == 'Français':
		months = {'January':'janvier', 'February':'février', 
		'March':'mars', 'April':'avril', 'May':'mai', 
		'June':'juin', 'July':'juillet', 'August':'août', 
		'September':'septembre', 'October':'octobre', 
		'November':'novembre', 'December':'décembre'}

		eng_month = publication.strftime('%B')
		months = months[eng_month] 	
		return publication.strftime(f"%d {months} %Y")

	elif language == 'English':
		eng_month = publication.strftime('%B')
		months = eng_month
		return publication.strftime(f"{months} %d, %Y")

	elif language == 'Español':
		months = {'January':'enero', 'February':'febrero', 
		'March':'marzo', 'April':'abril', 'May':'mayo', 
		'June':'junio', 'July':'julio', 'August':'agosto', 
		'September':'septiembre', 'October':'octubre', 
		'November':'noviembre', 'December':'diciembre'}

		eng_month = publication.strftime('%B')
		months = months[eng_month] 
		return publication.strftime(f"%d de {months} de %Y")

def date_slash():
	global date
	date = date.split('/')

	day, month, year = date
	converter = {'1':'January', '01':'January', '2':'February', '02':'February', 
	'3':'March', '03':'March', '4':'April', '04':'April', '5':'May', '05':'May', 
	'6':'June', '06':'June', '7':'July', '07':'July', '8':'August', '08':'August', 
	'9':'September', '09':'September', '10':'October','11':'November', '12':'December'}
	eng_month = converter[month]

	if day[0] == '0':
		day = day[1:]

	if language == 'Français':
		months = {'January':'janvier', 'February':'février', 
		'March':'mars', 'April':'avril', 'May':'mai', 
		'June':'juin', 'July':'juillet', 'August':'août', 
		'September':'septembre', 'October':'octobre', 
		'November':'novembre', 'December':'décembre'}
		#print(eng_month)
		#print(month)
		months = months[eng_month]
		return f'{day} {months} {year}'

	elif language == 'English':
		return f'{eng_month} {day}, {year}'

	elif language == 'Español':
		months = {'January':'enero', 'February':'febrero', 
		'March':'marzo', 'April':'abril', 'May':'mayo', 
		'June':'junio', 'July':'julio', 'August':'agosto', 
		'September':'septiembre', 'October':'octubre', 
		'November':'noviembre', 'December':'diciembre'}
		months = months[eng_month]
		return f'{day} de {months} de {year}'

def publication_slash():
	global publication
	publication = publication.split('/')

	day, month, year = publication
	converter = {'1':'January', '01':'January', '2':'February', '02':'February', 
	'3':'March', '03':'March', '4':'April', '04':'April', '5':'May', '05':'May', 
	'6':'June', '06':'June', '7':'July', '07':'July', '8':'August', '08':'August', 
	'9':'September', '09':'September', '10':'October','11':'November', '12':'December'}
	eng_month = converter[month]

	if day[0] == '0':
		day = day[1:]

	if language == 'Français':
		months = {'January':'janvier', 'February':'février', 
		'March':'mars', 'April':'avril', 'May':'mai', 
		'June':'juin', 'July':'juillet', 'August':'août', 
		'September':'septembre', 'October':'octobre', 
		'November':'novembre', 'December':'décembre'}
		#print(eng_month)
		#print(month)
		months = months[eng_month]
		return f'{day} {months} {year}'

	elif language == 'English':
		return f'{eng_month} {day}, {year}'

	elif language == 'Español':
		months = {'January':'enero', 'February':'febrero', 
		'March':'marzo', 'April':'abril', 'May':'mayo', 
		'June':'junio', 'July':'julio', 'August':'agosto', 
		'September':'septiembre', 'October':'octubre', 
		'November':'noviembre', 'December':'diciembre'}
		months = months[eng_month]
		return f'{day} de {months} de {year}'

def si_dis_inva(event):
	get_inva = si_txt_url.get('1.0', END)
	if get_inva == f'{transl_invalid}\n':
		si_txt_url.delete('1.0', END)

def p_dis_inva(event):
	get_inva = p_txt_url.get('1.0', END)
	if get_inva == f'{transl_invalid}\n':
		p_txt_url.delete('1.0', END)

def si_sort_button():
	si_websites.sort()
	show_websites = '\n\n'.join(si_websites)
	si_txt_result.delete('1.0', END)
	si_txt_result.insert('1.0', show_websites)

def p_sort_button():
	p_websites.sort()
	show_websites = '\n\n'.join(p_websites)
	p_txt_result.delete('1.0', END)
	p_txt_result.insert('1.0', show_websites)

def si_copy_button():
	pyperclip.copy(si_txt_result.get('1.0', END))

def p_copy_button():
	pyperclip.copy(p_txt_result.get('1.0', END))

def si_delete_button():
	si_websites.clear()
	si_txt_result.delete('1.0', END)

def p_delete_button():
	p_websites.clear()
	p_txt_result.delete('1.0', END)

def start_screen():
	global root

	root = Tk()
	root.title('Bibliography')
	root.configure(background='#35393f')
	root.iconbitmap(csl_ico)
	root.rowconfigure([0,1], weight=1)
	root.columnconfigure([0,1], weight=1)

	big_font = Font(family = '@DengXian', size = 24)
	bigger_than_normal_font = Font(family = '@DengXian', size = 18)
	normal_font = Font(family = '@DengXian', size = 13)

	txt_font = Font(family = 'Arial', size = 10)

	clickedlang = StringVar()
	clickedlang.set('Français')

	page1 = Frame(master=root, bg='#35393f')
	page1.rowconfigure([0,1], weight=1)
	page1.columnconfigure([0,1], weight=1)

	def language_select():
		lang_drop = OptionMenu(page1, clickedlang, 'Français', 'English', 'Español')
		lang_drop.config(bg='#7289da', fg='white', bd=0, activebackground='#536fae', activeforeground='white', font=big_font)
		lang_drop["menu"].config(bg='#7289da', fg='white', bd=0, activebackground='#536fae', activeforeground='white', font=big_font)
		lang_drop.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

	def settings():
		setting_themes = Button(master=page1, text=' Color Themes ', bg='#7289da', fg='white', bd=0, activebackground='#536fae', activeforeground='white', command=select_colors, compound=LEFT, font=big_font)
		setting_themes.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

		root.mainloop()

	clickedtheme = StringVar()
	clickedtheme.set('Dark')

	def select_colors():
		global color_slct_frm, frm_colors, frm_cp

		page1.grid_forget()

		color_slct_frm = Frame(master=root, bg='#35393f')
		big_font = Font(family = '@DengXian', size = 25)
		back_btn = Button(master=color_slct_frm, text=' < ', font=big_font, bg='#7289da', fg='white', bd=0, activebackground='#536fae', activeforeground='white', command=page1_appear)
		frm_colors = Frame(master=color_slct_frm, bg='#35393f')

		theme_drop = OptionMenu(color_slct_frm, clickedtheme, 'Dark', 'Night', 'Light')
		theme_drop.config(bg='#7289da', fg='white', bd=0, activebackground='#536fae', activeforeground='white', font=big_font)
		theme_drop["menu"].config(bg='#7289da', fg='white', bd=0, activebackground='#536fae', activeforeground='white', font=big_font)
		theme_drop.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

		back_btn.grid(row=0, sticky=W, padx=10, pady=10)
		frm_colors.grid(row=1, column=0, columnspan=2)
		color_slct_frm.grid(row=0, column=1)

		btn_1 = Button(master=frm_colors, bg='#7289da', activebackground='#536fae', height=5, width=10, bd=0) #default color
		btn_2 = Button(master=frm_colors, bg='#a371d9', activebackground='#825aad', height=5, width=10, bd=0, command=purple)
		btn_3 = Button(master=frm_colors, bg='#d971d7', activebackground='#ad5aac', height=5, width=10, bd=0, command=pink) 
		btn_4 = Button(master=frm_colors, bg='#da7272', activebackground='#ad5a5a', height=5, width=10, bd=0, command=red)
		btn_5 = Button(master=frm_colors, bg='#ffb326', activebackground='#d49520', height=5, width=10, bd=0, command=orange)
		btn_6 = Button(master=frm_colors, bg='#dcc452', activebackground='#ad9b40', height=5, width=10, bd=0, command=gold)
		btn_7 = Button(master=frm_colors, bg='#b0d936', activebackground='#8dad2b', height=5, width=10, bd=0, command=lime)
		btn_8 = Button(master=frm_colors, bg='#64d936', activebackground='#50ad2b', height=5, width=10, bd=0, command=green)

		btn_1.grid(row=0, column=0, padx=10, pady=10)
		btn_2.grid(row=0, column=1, padx=10, pady=10)
		btn_3.grid(row=0, column=2, padx=10, pady=10)
		btn_4.grid(row=1, column=0, padx=10, pady=10)
		btn_5.grid(row=1, column=1, padx=10, pady=10)
		btn_6.grid(row=1, column=2, padx=10, pady=10)
		btn_7.grid(row=2, column=0, padx=10, pady=10)
		btn_8.grid(row=2, column=1, padx=10, pady=10)

		frm_cp = Frame(master=frm_colors,bg='#35393f')
		picker_dropper = PhotoImage(file=color_picker_png)
		picker_dropper = picker_dropper.subsample(5, 5) 
		btn_9 = Button(master=frm_cp, bg='#35393f', activebackground='#40444b', image=picker_dropper, bd=0, command=color_picker)

		frm_cp.grid(row=2, column=2, padx=10, pady=10)
		btn_9.grid(padx=10, pady=10)

		mainloop()

	def get_language():
		global language
		language = clickedlang.get()
		get_theme()
		sip_display()

	def get_theme():
		global theme
		theme = clickedtheme.get()

	def page1_appear():
		color_slct_frm.grid_forget()
		page1.grid(row=0, column=0, sticky='nsew')

	start_button = Button(master=page1, text='Press to start', command=get_language, bg='#7289da', fg='white', bd=0, activebackground='#536fae', activeforeground='white', font=big_font, width=15, height=2)
	start_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)
	page1.grid(row=0, column=0, sticky='nsew')

	language_select()
	settings()
	color_theme()
	root.mainloop()

def color_theme():
	global bg_color, txt_box_color, font_color, theme
	
	bg_color = '#35393f'
	txt_box_color = '#40444b'
	font_color = 'white'
	try:
		if theme == 'Light':
			bg_color = 'white'
			txt_box_color = '#ededed'
			font_color = 'black'

		elif theme =='Night':
			bg_color = 'black'
			txt_box_color = '#121212'
	except:
		pass

btn_color = '#7289da'
btn_color_pressed = '#536fae'

def purple():
	global btn_color, btn_color_pressed
	btn_color = '#a371d9'
	btn_color_pressed = '#825aad'

def pink():
	global btn_color, btn_color_pressed
	btn_color = '#d971d7'
	btn_color_pressed = '#ad5aac'

def red():
	global btn_color, btn_color_pressed
	btn_color = '#da7272'
	btn_color_pressed = '#ad5a5a'

def orange():
	global btn_color, btn_color_pressed
	btn_color = '#ffb326'
	btn_color_pressed = '#d49520'

def gold():
	global btn_color, btn_color_pressed
	btn_color = '#dcc452'
	btn_color_pressed = '#ad9b40'

def lime():
	global btn_color, btn_color_pressed
	btn_color = '#c1db72'
	btn_color_pressed = '#9aad5a'

def green():
	global btn_color, btn_color_pressed
	btn_color = '#8edb72'
	btn_color_pressed = '#70ad5a'

def color_picker():
	global color_picked, frm_cp2, new_btn9, btn_color, btn_color_pressed
	try:
		try:
			frm_cp.grid_forget()
		except:
			pass

		if not frm_cp.grid_forget():
			frm_cp.grid(row=2, column=2, padx=10, pady=10)

		frm_cp2 = Frame(master=frm_colors, bg='#35393f')
		color_picked = colorchooser.askcolor()
		btn_color_pressed = color_picked[0]
		btn_color = color_picked[1]

		r = int(btn_color_pressed[0])
		g = int(btn_color_pressed[1])
		b = int(btn_color_pressed[2])

		if r != 0:
			r -= 34
			if r < 0:
				r = 0

		if g != 0:
			g -= 34
			if g < 0:
				g = 0

		if b != 0:
			b -= 17
			if b < 0:
				b = 0

		btn_color_pressed = (r,g,b)
		btn_color_pressed = '#%02x%02x%02x' % btn_color_pressed
		frm_cp.grid_forget()

		btn_color = btn_color.replace('-', '')
		btn_color_pressed = btn_color_pressed.replace('-', '')

		new_btn9 = Button(master=frm_cp2, bg=btn_color, activebackground=btn_color_pressed, height=5, width=10, bd=0, command=color_picker)
		frm_cp2.grid(row=2, column=2)
		new_btn9.grid(padx=10, pady=10)
	except:
		pass

def translations():
	global transl_date, transl_si, transl_p, transl_author, transl_publication, transl_process, transl_copy, transl_delete, transl_anon, transl_sort, transl_invalid

	if language == 'Français':
		transl_si = 'Site internet'
		transl_p = 'Périodique'

		transl_date = 'Date\nconsultée'
		transl_author = '    Auteur    '
		transl_publication = 'Date de\npublication'
		transl_anon = '[ANONYME]'
		transl_invalid = 'URL invalide'

		transl_process = 'Traiter'
		transl_sort = 'Trier'
		transl_copy = 'Copiez'
		transl_delete = 'Supprimez'

	elif language == 'English':
		transl_si = 'Website'
		transl_p = 'Periodic'

		transl_date = 'Date\nconsulted'
		transl_author = '    Author    '
		transl_publication = 'Date of\npublication'
		transl_anon = '[ANONYMOUS]'
		transl_invalid = 'Invalid URL'

		transl_process = 'Process'
		transl_sort = 'Sort'
		transl_copy = 'Copy'
		transl_delete = 'Delete'

	elif language == 'Español':
		transl_si = 'Sitio web'
		transl_p = 'Periódico'

		transl_date = 'Fecha de\nconsulta'
		transl_author = '     Autor     '
		transl_publication = 'Fecha de\npublicación'
		transl_anon = '[ANÓNIMO]'
		transl_invalid = 'URL invalida'

		transl_process = 'Procesar'
		transl_sort = 'Ordenar'
		transl_copy = 'Copiar'
		transl_delete = 'Eliminar'

def get_text(widget):
	text = widget.get('1.0', END)
	widget.delete("1.0", END)
	return text

def sip_display():
	global si_txt_url, si_txt_result, window

	translations()
	color_theme()

	root.destroy()
	window = Tk()
	window.title('Bibliography')
	window.iconbitmap(csl_ico)
	window.config(bg=bg_color)

	window.rowconfigure([0,1], weight=1)
	window.columnconfigure([0,1], weight=1)

	big_font = Font(family = '@DengXian', size = 24)

	def website():
		global si_txt_url, si_txt_result, si_txt_date, si_txt_author

		big_font = Font(family = '@DengXian', size = 24)
		bigger_than_normal_font = Font(family = '@DengXian', size = 18)
		normal_font = Font(family = '@DengXian', size = 13)
		txt_font = Font(family = 'Arial', size = 10)

		frm_si = Frame(master=window, highlightthickness=5, bg=bg_color)
		frm_si.config(highlightbackground = btn_color, highlightcolor=btn_color)
		frm_si.rowconfigure(0, weight=1)
		frm_si.columnconfigure([0,1,2], weight=1)
		frm_si.grid(row=0, padx=10, pady=10, sticky='nsew')

		si_frm_left = Frame(master=frm_si, bg=bg_color)
		si_frm_left.rowconfigure([0,1,2], weight=1)
		si_frm_left.columnconfigure([0,1], weight=1)

		si_frm_middle = Frame(master=frm_si, bg=bg_color)
		si_frm_middle.rowconfigure([0,1,2], weight=1)
		si_frm_middle.columnconfigure(0, weight=1)

		si_frm_right = Frame(master=frm_si, bg=bg_color)
		si_frm_right.rowconfigure([0,1], weight=1)
		si_frm_right.columnconfigure(0, weight=1)

		#LEFT FRAME

		si_lbl_url = Label(master=si_frm_left, text='URL', font=normal_font, bg=bg_color, fg=font_color)
		si_lbl_author = Label(master=si_frm_left, text=transl_author, font=normal_font, bg=bg_color, fg=font_color)
		si_lbl_date = Label(master=si_frm_left, text=transl_date, font=normal_font, bg=bg_color, fg=font_color)

		si_lbl_url.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
		si_lbl_author.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
		si_lbl_date.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

		si_txt_url = Text(master=si_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)
		si_txt_date = Text(master=si_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)
		si_txt_author = Text(master=si_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)

		si_txt_url.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
		si_txt_author.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
		si_txt_date.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')

		#MIDDLE FRAME

		si_lbl_title = Label(master=si_frm_middle, text=transl_si, height=1, width=10, font=big_font, bg=bg_color, fg=font_color)
		si_btn_process = Button(master=si_frm_middle, text=transl_process, height=1, width=5, font=bigger_than_normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=si_process_bibliography)
		si_lbl_blank1 = Label(master=si_frm_middle, height=4, bg=bg_color)

		si_lbl_title.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
		si_btn_process.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
		si_lbl_blank1.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

		#RIGHT FRAME

		scroll = Scrollbar(master=si_frm_right)		
		scroll.grid(row=0, column=1, sticky='nsew')

		si_txt_result = Text(master=si_frm_right, yscrollcommand=scroll.set, height=15, width=20, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)
		scroll.config(command=si_txt_result.yview)

		si_frm_right_buttons = Frame(master=si_frm_right, bg=bg_color)
		si_frm_right_buttons.columnconfigure([0,1,2], weight=1)
		si_frm_right_buttons.rowconfigure(0, weight=1)

		si_txt_result.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
		si_frm_right_buttons.grid(row=1, column=0, sticky='nsew')

		btn_sort = Button(master=si_frm_right_buttons, text=transl_sort, height=1, width=15, font=normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=si_sort_button)
		btn_copy = Button(master=si_frm_right_buttons, text=transl_copy, height=1, width=15, font=normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=si_copy_button)
		btn_delete = Button(master=si_frm_right_buttons, text=transl_delete, height=1, width=15, font=normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=si_delete_button)

		btn_sort.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
		btn_copy.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
		btn_delete.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

		si_frm_left.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
		si_frm_middle.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
		si_frm_right.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)


	def periodic():
		global p_txt_url, p_txt_result, p_txt_date, p_txt_author, p_txt_publication
		
		big_font = Font(family = '@DengXian', size = 24)
		bigger_than_normal_font = Font(family = '@DengXian', size = 18)
		normal_font = Font(family = '@DengXian', size = 13)
		txt_font = Font(family = 'Arial', size = 10)

		frm_p = Frame(master=window, highlightthickness=5, bg=bg_color)
		frm_p.config(highlightbackground =btn_color, highlightcolor= btn_color)
		frm_p.rowconfigure(0, weight=1)
		frm_p.columnconfigure([0,1,2], weight=1)
		frm_p.grid(row=1, padx=10, pady=10, sticky='nsew')

		p_frm_left = Frame(master=frm_p, bg=bg_color)
		p_frm_left.rowconfigure([0,1,2,3], weight=1)
		p_frm_left.columnconfigure([0,1], weight=1)

		p_frm_middle = Frame(master=frm_p, bg=bg_color)
		p_frm_middle.rowconfigure([0,1,2], weight=1)
		p_frm_middle.columnconfigure(0, weight=1)

		p_frm_right = Frame(master=frm_p, bg=bg_color)
		p_frm_right.rowconfigure([0,1], weight=1)
		p_frm_right.columnconfigure(0, weight=1)

		#LEFT FRAME

		p_lbl_url = Label(master=p_frm_left, text='URL', font=normal_font, bg=bg_color, fg=font_color)
		p_lbl_author = Label(master=p_frm_left, text=transl_author, font=normal_font, bg=bg_color, fg=font_color)
		p_lbl_date = Label(master=p_frm_left, text=transl_date, font=normal_font, bg=bg_color, fg=font_color)
		p_lbl_publication = Label(master=p_frm_left, text=transl_publication, font=normal_font, bg=bg_color, fg=font_color)

		p_lbl_url.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
		p_lbl_author.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
		p_lbl_date.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
		p_lbl_publication.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

		p_txt_url = Text(master=p_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)
		p_txt_author = Text(master=p_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)		
		p_txt_date = Text(master=p_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)

		p_txt_publication = Text(master=p_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)

		p_txt_url.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
		p_txt_author.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
		p_txt_date.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')
		p_txt_publication.grid(row=3, column=1, padx=5, pady=5, sticky='nsew')

		#MIDDLE FRAME

		p_lbl_title = Label(master=p_frm_middle, text=transl_p, height=1, width=10, font=big_font, bg=bg_color, fg=font_color)
		p_btn_process = Button(master=p_frm_middle, text=transl_process, height=1, width=5, font=bigger_than_normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=p_process_bibliography)
		p_lbl_blank1 = Label(master=p_frm_middle, height=6, bg=bg_color)

		p_lbl_title.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
		p_btn_process.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
		p_lbl_blank1.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

		#RIGHT FRAME

		scroll = Scrollbar(master=p_frm_right)		
		scroll.grid(row=0, column=1, sticky='nsew')

		p_txt_result = Text(master=p_frm_right, yscrollcommand=scroll.set, height=15, width=20, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)
		scroll.config(command=p_txt_result.yview)

		p_frm_right_buttons = Frame(master=p_frm_right, bg=bg_color)
		p_frm_right_buttons.columnconfigure([0,1,2], weight=1)
		p_frm_right_buttons.rowconfigure(0, weight=1)

		p_txt_result.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
		p_frm_right_buttons.grid(row=1, column=0, sticky='nsew')

		btn_sort = Button(master=p_frm_right_buttons, text=transl_sort, height=1, width=15, font=normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=p_sort_button)
		btn_copy = Button(master=p_frm_right_buttons, text=transl_copy, height=1, width=15, font=normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=p_copy_button)
		btn_delete = Button(master=p_frm_right_buttons, text=transl_delete, height=1, width=15, font=normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=p_delete_button)

		btn_sort.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
		btn_copy.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
		btn_delete.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

		#FRAMES

		p_frm_left.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
		p_frm_middle.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
		p_frm_right.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)

	website()
	periodic()

if __name__ == '__main__':
	start_screen()