from tkinter import *
from tkinter.font import Font
from tkinter import colorchooser
import datetime
import pyperclip
import mechanize
import os
import pafy
import isbnlib
#import time

csl_ico = os.path.join(os.path.dirname(__file__), 'csl_logo.ico')
color_picker_png = os.path.join(os.path.dirname(__file__),'color_picker.png')

def search(url):
	global search_t_working

	br = mechanize.Browser()
	br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')]

	try:
		br.open(url)
		titre = br.title()
		search_t_working = True
		return titre
	except:
		search_t_working = False

def get_date(date):
	global search_d_working
	try:
		if '/' in date:
			date = date_slash(date)

		if date.strip() == '':
			date = date_consultee(date)

		search_d_working = True
		return date
	except:
		search_d_working = False

def get_publication(publication):
	global search_p_working
	try:
		if '/' in publication:
			publication = date_slash(publication)

		if publication.strip() == '':
			publication = date_consultee(publication)

		search_p_working = True
		return publication
	except:
		search_p_working = False

def get_author(author):
	author.lower()

	if author.strip() == '':
		author = transl_anon

	author = author.split()

	if len(author) == 2:
		prenom, nom = author
		author = nom.upper() + ', ' + prenom.title()
	else:
		author = ' '.join(author).upper()

	return author

def get_titre(titre):
	try:
		if '-' in titre:
			titre = titre.split('-')[0][:-1]
			return titre

		elif '|' in titre:
			titre = titre.split('|')[0][:-1]
			return titre

		else:
			return titre
	except:
		pass

si_websites = []

def si_process_bibliography():
	#start_time = time.time()
	global si_websites, show_si_websites

	url = get_text(si_txt_url)[:-1]
	date = get_text(si_txt_date)[:-1]
	date = get_date(date)
	author = get_text(si_txt_author)
	author = get_author(author)
	titre = search(url)
	titre = get_titre(titre)

	if titre != None and date != None:
		if language == 'Français':
			si_websites.append(f'{author}. {titre}, [En ligne], {url} (Page consultée le {date})')
		elif language == 'English':
			si_websites.append(f'{author}. {titre}, [Online], {url} (Page consulted on {date})')
		elif language == 'Español':
			si_websites.append(f'{author}. {titre}, [En línea], {url} (Página consultada el {date})')

		show_si_websites = '\n\n'.join(si_websites)
		si_txt_result.delete('1.0', END)
		si_txt_result.insert('1.0', show_si_websites)
		#print("si: %s seconds" % (time.time() - start_time))

	else:
		if search_d_working == False:
			si_txt_date.insert('1.0', transl_inv_date)

		if search_t_working == False:
			si_txt_url.insert('1.0', transl_invalid)

		#PUT BACK VARIABLES IN TXT BOXES, TO DO LATER

p_websites = []

def p_process_bibliography():
	global p_websites, show_p_websites
	#start_time = time.time()
	url = get_text(p_txt_url)[:-1]
	date = get_text(p_txt_date)[:-1]
	date = get_date(date)
	author = get_text(p_txt_author)
	author = get_author(author)
	titre = search(url)
	titre = get_titre(titre)
	publication = get_text(p_txt_publication)[:-1]
	publication = get_publication(publication)
	domain = url.split('www.')[-1].split('://')[-1].split('/')[0].capitalize()

	if titre != None and date != None and publication != None:
		if language == 'Français':
			p_websites.append(f'{author}. «{titre}», {domain}, {publication}, [En ligne], {url} (Page consultée le {date})')
		elif language == 'English':
			p_websites.append(f'{author}. "{titre}", {domain}, {publication}, [Online], {url} (Page consulted on {date})')
		elif language == 'Español':
			p_websites.append(f'{author}. «{titre}», {domain}, {publication}, [En línea], {url} (Página consultada el {date})')

		show_p_websites = '\n\n'.join(p_websites)
		p_txt_result.delete('1.0', END)
		p_txt_result.insert('1.0', show_p_websites)
		#print("p: %s seconds" % (time.time() - start_time))

	else:
		if search_d_working == False:
			p_txt_date.insert('1.0', transl_inv_date)

		if search_t_working == False:
			p_txt_url.insert('1.0', transl_invalid)

		if search_p_working == False:
			p_txt_publication.insert('1.0', transl_inv_date)

v_websites = []

def v_process_bibliography():
	#start_time = time.time()
	global v_websites, video, show_v_websites

	url = get_text(v_txt_url)[:-1]
	date = get_text(v_txt_date)[:-1]
	date = get_date(date)	
	titre = search(url)
	publication = get_text(v_txt_publication)[:-1]
	publication = get_publication(publication)

	try:
		video = pafy.new(url)
	except:
		v_txt_url.insert('1.0', transl_invalid)

	author = get_text(v_txt_author)[:-1]
	if author.strip() == '':
		author = video.author
	else:
		author = author.split()

		if len(author) == 2:
			prenom, nom = author
			author = nom.upper() + ', ' + prenom.title()
		else:
			author = ' '.join(author).upper()

	length = video.duration
	title = video.title

	length = length.split(':')

	if length[0] == '00':
		length = length[1:]

	length = ':'.join(length)

	if length[0] == '0':
		length = length[1:]

	if titre != None and date != None:
		if language == 'Français':
			v_websites.append(f'{author} (auteur). {title}, {publication}, {length}, dans YouTube, {titre}, YouTube, {url} (Page consultée le {date})')
		elif language == 'English':
			v_websites.append(f'{author} (author). {title}, {publication}, {length}, in YouTube, {titre}, YouTube, {url} (Page consulted on {date})')
		elif language == 'Español':
			v_websites.append(f'{author} (autor). {title}, {publication}, {length}, en YouTube, {titre}, YouTube, {url} (Página consultada el {date})')

		show_v_websites = '\n\n'.join(v_websites)
		v_txt_result.delete('1.0', END)
		v_txt_result.insert('1.0', show_v_websites)
		#print("v: %s seconds" % (time.time() - start_time))

	else:
		if search_d_working == False:
			v_txt_date.insert('1.0', transl_inv_date)

		if search_t_working == False:
			v_txt_url.insert('1.0', transl_invalid)

b_websites = []

def b_process_bibliography():
	#start_time = time.time()
	global b_websites, show_b_websites

	url = get_text(b_txt_url)[:-1]
	date = get_text(b_txt_date)[:-1]
	date = get_date(date)
	isbn = get_text(b_txt_isbn).strip()
	length = get_text(b_txt_length).strip()

	try:
		book = isbnlib.meta(isbn)
	except:
		b_txt_isbn.insert('1.0', transl_inv_isbn)

	year = book['Year']
	publisher = book['Publisher']
	title = book['Title']
	author = book['Authors']
	author = ''.join(author)
	author = get_author(author)

	if publisher.strip() == '':
		b_txt_isbn.insert('1.0', transl_no_publisher)

	if date != None and length.strip() != '':
		if language == 'Français':
			b_websites.append(f'{author}. {title}, {publisher}, {year}, {length}p. {url} (Page consultée le {date})')
		elif language == 'English':
			b_websites.append(f'{author}. {title}, {publisher}, {year}, {length}p. {url} (Page consulted on {date})')
		elif language == 'Español':
			b_websites.append(f'{author}. {title}, {publisher}, {year}, {length}p. {url} (Página consultada el {date})')

		show_b_websites = '\n\n'.join(b_websites)
		b_txt_result.delete('1.0', END)
		b_txt_result.insert('1.0', show_b_websites)
		#print("b: %s seconds" % (time.time() - start_time))

	else:
		if search_d_working == False:
			b_txt_date.insert('1.0', transl_inv_date)

		if length.strip() == '':
			b_txt_length.insert('1.0', transl_no_page_n)

english_months = ('January', 'February', 
	'March', 'April', 'May', 
	'June', 'July', 'August', 
	'September', 'October', 
	'November', 'December')

french_months = ('janvier', 'février', 
	'mars', 'avril', 'mai', 
	'juin', 'juillet', 'août', 
	'septembre', 'octobre', 
	'novembre', 'décembre')

spanish_months = ('enero', 'febrero', 
	'marzo', 'abril', 'mayo', 
	'junio', 'julio', 'agosto', 
	'septiembre', 'octubre', 
	'noviembre', 'diciembre')

converter = dict(zip([str(i) for i in range(1,13)], english_months))

def date_consultee(date):	
	date = datetime.datetime.now()

	if language == 'Français':
		months = dict(zip(english_months, french_months))
		eng_month = date.strftime('%B')
		months = months[eng_month]
		day = date.strftime("%d")
		if day[0] == '0':
			day = day[1:]
		return date.strftime(f"{day} {months} %Y")
	
	elif language == 'English':
		eng_month = date.strftime('%B')
		months = eng_month
		day = date.strftime("%d")
		if day[0] == '0':
			day = day[1:]
		return date.strftime(f"{months} {day}, %Y")

	elif language == 'Español':
		months = dict(zip(english_months, spanish_months))
		eng_month = date.strftime('%B')
		months = months[eng_month]
		day = date.strftime("%d")
		if day[0] == '0':
			day = day[1:] 	
		return date.strftime(f"{day} de {months} de %Y")

def date_slash(date):
	date = date.split('/')
	day, month, year = date

	if day[0] == '0':
		day = day[1:]

	if month[0] == '0':
		month = month[1:]

	eng_month = converter[month]

	if language == 'Français':
		months = dict(zip(english_months, french_months))
		months = months[eng_month]
		return f"{day} {months} {year}"

	elif language == 'English':
		return f'{eng_month} {day}, {year}'

	elif language == 'Español':
		months = dict(zip(english_months, spanish_months))
		months = months[eng_month]
		return f'{day} de {months} de {year}'

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

def v_sort_button():
	global v_sort
	v_sort = True
	v_websites.sort()
	show_websites = '\n\n'.join(v_websites)
	v_txt_result.delete('1.0', END)
	v_txt_result.insert('1.0', show_websites)

def b_sort_button():
	global b_sort
	b_sort = True
	b_websites.sort()
	show_websites = '\n\n'.join(b_websites)
	b_txt_result.delete('1.0', END)
	b_txt_result.insert('1.0', show_websites)

def si_copy_button():
	pyperclip.copy(si_txt_result.get('1.0', END))

def p_copy_button():
	pyperclip.copy(p_txt_result.get('1.0', END))

def v_copy_button():
	pyperclip.copy(v_txt_result.get('1.0', END))

def b_copy_button():
	pyperclip.copy(b_txt_result.get('1.0', END))

def si_delete_button():
	si_websites.clear()
	si_txt_result.delete('1.0', END)

def p_delete_button():
	p_websites.clear()
	p_txt_result.delete('1.0', END)

def v_delete_button():
	v_websites.clear()
	v_txt_result.delete('1.0', END)

def b_delete_button():
	b_websites.clear()
	b_txt_result.delete('1.0', END)

bg_color = '#35393f'
txt_box_color = '#40444b'
font_color = 'white'
btn_color = '#7289da'
btn_color_pressed = '#536fae'

def start_screen():
	global root

	try:
		window.destroy()
	except:
		pass

	root = Tk()
	root.title('Médiagraphie')
	root.configure(background=bg_color)
	root.iconbitmap(csl_ico)
	root.rowconfigure([0,1], weight=1)
	root.columnconfigure([0,1], weight=1)

	big_font = Font(family = '@DengXian', size = 24)
	bigger_than_normal_font = Font(family = '@DengXian', size = 18)
	normal_font = Font(family = '@DengXian', size = 13)
	txt_font = Font(family = 'Arial', size = 10)

	clickedlang = StringVar()
	clickedlang.set('Français')

	page1 = Frame(master=root, bg=bg_color)
	page1.rowconfigure([0,1], weight=1)
	page1.columnconfigure([0,1], weight=1)

	def language_select():
		lang_drop = OptionMenu(page1, clickedlang, 'Français', 'English', 'Español')
		lang_drop.config(bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, font=big_font)
		lang_drop["menu"].config(bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, font=big_font)
		lang_drop.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

	def settings():
		setting_themes = Button(master=page1, text='   Couleurs   ', bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=select_colors, compound=LEFT, font=big_font)
		setting_themes.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

		root.mainloop()

	clickedtheme = StringVar()
	clickedtheme.set('Sombre')

	def select_colors():
		global color_slct_frm, frm_colors, frm_cp

		page1.grid_forget()

		color_slct_frm = Frame(master=root, bg=bg_color)
		big_font = Font(family = '@DengXian', size = 25)
		back_btn = Button(master=color_slct_frm, text=' < ', font=big_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=page1_appear)
		frm_colors = Frame(master=color_slct_frm, bg=bg_color)

		theme_drop = OptionMenu(color_slct_frm, clickedtheme, 'Sombre', 'Nuit', 'Clair')
		theme_drop.config(bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, font=big_font)
		theme_drop["menu"].config(bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, font=big_font)
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

		frm_cp = Frame(master=frm_colors,bg=bg_color)
		picker_dropper = PhotoImage(file=color_picker_png)
		picker_dropper = picker_dropper.subsample(5, 5) 
		btn_9 = Button(master=frm_cp, bg=bg_color, activebackground=txt_box_color, image=picker_dropper, bd=0, command=color_picker)

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

	start_button = Button(master=page1, text='Appuyez pour démarrer', command=get_language, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, font=big_font, width=15, height=2)
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
		if theme == 'Clair':
			bg_color = 'white'
			txt_box_color = '#e3e5e8'
			font_color = 'black'

		elif theme =='Nuit':
			bg_color = 'black'
			txt_box_color = '#121212'
	except:
		pass

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

		frm_cp2 = Frame(master=frm_colors, bg=bg_color)
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
	global transl_date, transl_si, transl_p, transl_author, transl_publication, transl_process, transl_copy, transl_delete, transl_anon, transl_sort, transl_invalid, transl_online_books, transl_yt, transl_header_1, transl_header_2, transl_page_number, transl_biblio, transl_no_publisher, transl_inv_date, transl_inv_isbn, transl_no_page_n

	if language == 'Français':
		transl_si = 'Site internet'
		transl_p = 'Périodique'
		transl_online_books = "Livres en\nligne"
		transl_yt = "Vidéo\nYouTube"

		transl_date = 'Date\nconsultée'
		transl_author = '    Auteur    '
		transl_publication = 'Date de\npublication'
		transl_anon = '[ANONYME]'
		transl_invalid = 'URL invalide'
		transl_header_1 = 'Site internet / Périodique en ligne'
		transl_header_2 = 'Vidéo / Livre en ligne'
		transl_inv_date = 'date invalide'
		transl_no_page_n = "Veuillez ajouter un nombres de pages."

		transl_process = 'Traiter'
		transl_sort = 'Trier'
		transl_copy = 'Copiez'
		transl_delete = 'Supprimez'

		transl_page_number = 'Nombres\nde pages'
		transl_biblio = 'Médiagraphie'
		transl_no_publisher = "Malheureusement, vous devrez écrire la [maison d'édition] manuellement, l'ISBN n'en a trouvé aucun."
		transl_inv_isbn = 'ISBN invalide'

	elif language == 'English':
		transl_si = 'Website'
		transl_p = 'Periodic'
		transl_online_books = "Online\nbooks"
		transl_yt = "YouTube\nvideo"

		transl_date = 'Date\nconsulted'
		transl_author = '    Author    '
		transl_publication = 'Date of\npublication'
		transl_anon = '[ANONYMOUS]'
		transl_invalid = 'invalid URL'
		transl_header_1 = 'Website / Online periodic'
		transl_header_2 = 'Video / Online book'
		transl_inv_date = 'invalid date'
		transl_no_page_n = "Please add number of pages."

		transl_process = 'Process'
		transl_sort = 'Sort'
		transl_copy = 'Copy'
		transl_delete = 'Delete'

		transl_page_number = 'Number\nof pages'
		transl_biblio = 'Mediagraphy'
		transl_no_publisher = "Unfortunately, you'll have to write the [publisher] manually, the ISBN didn't find any."
		transl_inv_isbn = 'invalid ISBN'

	elif language == 'Español':
		transl_si = 'Sitio web'
		transl_p = 'Periódico'
		transl_yt = "Video de\nYoutube"
		transl_online_books = "Libros\nen linea"

		transl_date = 'Fecha de\nconsulta'
		transl_author = '     Autor     '
		transl_publication = 'Fecha de\npublicación'
		transl_anon = '[ANÓNIMO]'
		transl_invalid = 'URL invalida'
		transl_header_1 = 'Sitio web / Periódico en línea'
		transl_header_2 = 'Video / Libro en línea'
		transl_inv_date = 'fecha invalida'
		transl_no_page_n = "Por favor, poner el número de páginas."

		transl_process = 'Procesar'
		transl_sort = 'Ordenar'
		transl_copy = 'Copiar'
		transl_delete = 'Eliminar'

		transl_page_number = 'Número\nde páginas'
		transl_biblio = 'Mediagrafia'
		transl_no_publisher = "Desafortunadamente, tendrá que escribir el [editor] manualmente, el ISBN no encontró ninguno."
		transl_inv_isbn = 'ISBN invalida'

def get_text(widget):
	text = widget.get('1.0', END)
	widget.delete("1.0", END)
	return text

def sip_display():
	global window, page4

	translations()
	color_theme()

	root.destroy()
	window = Tk()
	window.title(transl_biblio)
	window.iconbitmap(csl_ico)
	window.config(bg=bg_color)

	big_font = Font(family = '@DengXian', size = 24)
	bigger_than_normal_font = Font(family = '@DengXian', size = 18)
	bigger_bigger_than_normal_font = Font(family = '@DengXian', size = 22)
	normal_font = Font(family = '@DengXian', size = 13)
	small_font = Font(family = '@DengXian', size = 11)
	txt_font = Font(family = 'Arial', size = 10)
	
	window.rowconfigure([0,1], weight=1)
	window.columnconfigure([0,1], weight=1)

	head = Frame(master=window, bg=bg_color)
	head.rowconfigure([0], weight=1)
	head.columnconfigure([0], weight=1, minsize=50)
	head.columnconfigure([1,2], weight=1,minsize=500)

	page3 = Frame(master=window, bg=bg_color)
	page3.rowconfigure([0,1], weight=1)
	page3.columnconfigure([0,1], weight=1)

	page4 = Frame(master=window, bg=bg_color)
	page4.rowconfigure([0,1], weight=1)
	page4.columnconfigure([0,1], weight=1)

	si_websites.clear()
	p_websites.clear()
	v_websites.clear()
	b_websites.clear()
	show_v_websites = None
	show_b_websites = None

	def header():
		p3_back_btn = Button(master=head, text='<', bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, font=bigger_than_normal_font, width=1, command=start_screen)
		tab_sip = Button(master=head, text=transl_header_1, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, font=bigger_than_normal_font, width=5, command=page3_appear)
		tab_vb = Button(master=head, text=transl_header_2, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, font=bigger_than_normal_font, width=5, command=page_vb)

		p3_back_btn.grid(row=0, column=0, padx=(10,0), pady=(10,0), sticky='nsew')
		tab_sip.grid(row=0, column=1, padx=10, pady=(10,0), sticky='nsew')
		tab_vb.grid(row=0, column=2, padx=(0,10), pady=(10,0), sticky='nsew')
	
	def page3_appear():
		try:
			page4.grid_forget()		
			head.grid(row=0, column=0, sticky='nsew')
			page3.grid(row=1, column=0, sticky='nsew')
		except:
			pass

	def page_sip():

		def website():
			global si_txt_url, si_txt_result, si_txt_date, si_txt_author

			frm_si = Frame(master=page3, highlightthickness=5, bg=bg_color)
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

			frm_p = Frame(master=page3, highlightthickness=5, bg=bg_color)
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
	
	def page_vb():
		page3.grid_forget()
		head.grid(row=0, column=0, sticky='nsew')
		page4.grid(row=1, column=0, sticky='nsew')

		def video():
			global v_txt_url, v_txt_date, v_txt_publication, v_txt_author, v_txt_result

			frm_v = Frame(master=page4, highlightthickness=5, bg=bg_color)
			frm_v.config(highlightbackground = btn_color, highlightcolor=btn_color)
			frm_v.rowconfigure(0, weight=1)
			frm_v.columnconfigure([0,1,2], weight=1)
			frm_v.grid(row=0, padx=10, pady=10, sticky='nsew')

			v_frm_left = Frame(master=frm_v, bg=bg_color)
			v_frm_left.rowconfigure([0,1,2,3], weight=1)
			v_frm_left.columnconfigure([0,1], weight=1)

			v_frm_middle = Frame(master=frm_v, bg=bg_color)
			v_frm_middle.rowconfigure([0,1,2], weight=1)
			v_frm_middle.columnconfigure(0, weight=1)

			v_frm_right = Frame(master=frm_v, bg=bg_color)
			v_frm_right.rowconfigure([0,1], weight=1)
			v_frm_right.columnconfigure(0, weight=1)

			#LEFT FRAME

			v_lbl_url = Label(master=v_frm_left, text='URL', font=normal_font, bg=bg_color, fg=font_color)
			v_lbl_author = Label(master=v_frm_left, text=transl_author, font=normal_font, bg=bg_color, fg=font_color)
			v_lbl_date = Label(master=v_frm_left, text=transl_date, font=normal_font, bg=bg_color, fg=font_color)
			v_lbl_publication = Label(master=v_frm_left, text=transl_publication, font=normal_font, bg=bg_color, fg=font_color)

			v_lbl_url.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
			v_lbl_author.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
			v_lbl_date.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
			v_lbl_publication.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

			v_txt_url = Text(master=v_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)
			v_txt_author = Text(master=v_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)
			v_txt_date = Text(master=v_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)
			v_txt_publication = Text(master=v_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)

			v_txt_url.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
			v_txt_author.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
			v_txt_date.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')
			v_txt_publication.grid(row=3, column=1, padx=5, pady=5, sticky='nsew')

			#MIDDLE FRAME

			v_lbl_title = Label(master=v_frm_middle, text=transl_yt, height=1, width=10, font=big_font, bg=bg_color, fg=font_color)
			v_btn_process = Button(master=v_frm_middle, text=transl_process, height=1, width=5, font=bigger_than_normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=v_process_bibliography)
			v_lbl_blank1 = Label(master=v_frm_middle, height=4, bg=bg_color)

			v_lbl_title.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
			v_btn_process.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
			v_lbl_blank1.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

			#RIGHT FRAME

			scroll = Scrollbar(master=v_frm_right)		
			scroll.grid(row=0, column=1, sticky='nsew')

			v_txt_result = Text(master=v_frm_right, yscrollcommand=scroll.set, height=15, width=20, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)
			scroll.config(command=v_txt_result.yview)

			v_frm_right_buttons = Frame(master=v_frm_right, bg=bg_color)
			v_frm_right_buttons.columnconfigure([0,1,2], weight=1)
			v_frm_right_buttons.rowconfigure(0, weight=1)

			v_txt_result.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
			v_frm_right_buttons.grid(row=1, column=0, sticky='nsew')

			try:
				if v_sort == True:
					v_websites.sort()
					show_websites = '\n\n'.join(v_websites)
					v_txt_result.delete('1.0', END)
					v_txt_result.insert('1.0', show_websites)
			except:
				try:
					v_txt_result.insert('1.0', show_v_websites)
				except:
					pass

			btn_sort = Button(master=v_frm_right_buttons, text=transl_sort, height=1, width=15, font=normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=v_sort_button)
			btn_copy = Button(master=v_frm_right_buttons, text=transl_copy, height=1, width=15, font=normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=v_copy_button)
			btn_delete = Button(master=v_frm_right_buttons, text=transl_delete, height=1, width=15, font=normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=v_delete_button)

			btn_sort.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
			btn_copy.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
			btn_delete.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

			v_frm_left.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
			v_frm_middle.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
			v_frm_right.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)
		
		def book():
			global b_txt_url, b_txt_date, b_txt_isbn, b_txt_length, b_txt_result
			
			frm_b = Frame(master=page4, highlightthickness=5, bg=bg_color)
			frm_b.config(highlightbackground = btn_color, highlightcolor=btn_color)
			frm_b.rowconfigure(0, weight=1)
			frm_b.columnconfigure([0,1,2], weight=1)
			frm_b.grid(row=1, padx=10, pady=10, sticky='nsew')

			b_frm_left = Frame(master=frm_b, bg=bg_color)
			b_frm_left.rowconfigure([0,1,2,3], weight=1)
			b_frm_left.columnconfigure([0,1], weight=1)

			b_frm_middle = Frame(master=frm_b, bg=bg_color)
			b_frm_middle.rowconfigure([0,1,2], weight=1)
			b_frm_middle.columnconfigure(0, weight=1)

			b_frm_right = Frame(master=frm_b, bg=bg_color)
			b_frm_right.rowconfigure([0,1], weight=1)
			b_frm_right.columnconfigure(0, weight=1)

			#LEFT FRAME

			b_lbl_url = Label(master=b_frm_left, text='URL', font=normal_font, bg=bg_color, fg=font_color)
			b_lbl_isbn = Label(master=b_frm_left, text='      ISBN     ', font=normal_font, bg=bg_color, fg=font_color)
			b_lbl_date = Label(master=b_frm_left, text=transl_date, font=normal_font, bg=bg_color, fg=font_color)
			b_lbl_length = Label(master=b_frm_left, text=transl_page_number, font=normal_font, bg=bg_color, fg=font_color)

			b_lbl_url.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
			b_lbl_isbn.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
			b_lbl_date.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
			b_lbl_length.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

			b_txt_url = Text(master=b_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)
			b_txt_date = Text(master=b_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)
			b_txt_isbn = Text(master=b_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)
			b_txt_length = Text(master=b_frm_left, height=1, width=30, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)

			b_txt_url.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
			b_txt_isbn.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
			b_txt_date.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')
			b_txt_length.grid(row=3, column=1, padx=5, pady=5, sticky='nsew')

			#MIDDLE FRAME

			b_lbl_title = Label(master=b_frm_middle, text=transl_online_books, height=1, width=10, font=big_font, bg=bg_color, fg=font_color)
			b_btn_process = Button(master=b_frm_middle, text=transl_process, height=1, width=5, font=bigger_than_normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=b_process_bibliography)
			b_lbl_blank1 = Label(master=b_frm_middle, height=4, font=small_font, bg=bg_color, fg=font_color)

			b_lbl_title.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
			b_btn_process.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
			b_lbl_blank1.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

			#RIGHT FRAME

			scroll = Scrollbar(master=b_frm_right)		
			scroll.grid(row=0, column=1, sticky='nsew')

			b_txt_result = Text(master=b_frm_right, yscrollcommand=scroll.set, height=15, width=15, font=txt_font, bg=txt_box_color, bd=0, fg=font_color)
			scroll.config(command=b_txt_result.yview)

			b_frm_right_buttons = Frame(master=b_frm_right, bg=bg_color)
			b_frm_right_buttons.columnconfigure([0,1,2], weight=1)
			b_frm_right_buttons.rowconfigure(0, weight=1)

			b_txt_result.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
			b_frm_right_buttons.grid(row=1, column=0, sticky='nsew')
			
			try:
				if b_sort == True:
					b_websites.sort()
					show_websites = '\n\n'.join(b_websites)
					b_txt_result.delete('1.0', END)
					b_txt_result.insert('1.0', show_websites)
			except:
				try:
					b_txt_result.insert('1.0', show_b_websites)
				except:
					pass

			btn_sort = Button(master=b_frm_right_buttons, text=transl_sort, height=1, width=15, font=normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=b_sort_button)
			btn_copy = Button(master=b_frm_right_buttons, text=transl_copy, height=1, width=15, font=normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=b_copy_button)
			btn_delete = Button(master=b_frm_right_buttons, text=transl_delete, height=1, width=15, font=normal_font, bg=btn_color, fg=font_color, bd=0, activebackground=btn_color_pressed, activeforeground=font_color, command=b_delete_button)

			btn_sort.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
			btn_copy.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
			btn_delete.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

			b_frm_left.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
			b_frm_middle.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
			b_frm_right.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)

		video()
		book()
	
	page3_appear()
	header()
	page_sip()

if __name__ == '__main__':
	start_screen()
