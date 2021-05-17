from PIL import Image, ImageFont, ImageDraw

def add_caption(meme_type, title_text):
	title_text = title_text.replace(" ; ","\n").replace(" ;", "")
	if meme_type == 'Surprised-Pikachu':
		box_length = 40
		box_x = 15
		box_y = 15
		text_size = 100
		image_link = "Surprised-Pikachu.jpeg"

		write(box_length, box_x, box_y, text_size, image_link, title_text)
		
	elif meme_type == 'Change-My-Mind':
		box_length = 30
		box_x = 300
		box_y = 550
		text_size = 40 
		image_link = "Change-My-Mind.jpeg"

		write(box_length, box_x, box_y, text_size, image_link, title_text)

	elif meme_type == 'Imma-Head-Out':
		box_length = 35
		box_x = 10
		box_y = 10
		text_size = 50
		image_link = "Imma-Head-Out.jpeg"

		write(box_length, box_x, box_y, text_size, image_link, title_text)
		
	elif meme_type == 'Tuxedo-Winnie-The-Pooh': #no worky
		two_captions = title_text.split('\n', 1)

		box_length = 20
		box_x = 350
		box_y = 10
		text_size = 50
		image_link = "Tuxedo-Winnie-The-Pooh.jpeg"
		title_text = two_captions[0]

		box_x2 = 350
		box_y2 = 300
		title_text2 = two_captions[1]

		write2(box_length, box_x, box_y, text_size, image_link, title_text, box_x2, box_y2, title_text2)

	elif meme_type =='Sleeping-Shaq':  
		two_captions = title_text.split('\n', 1)

		box_length = 19
		box_x = 10
		box_y = 10
		text_size = 35
		box_x2 = 350
		box_y2 = 10
		image_link = "Sleeping-Shaq.jpeg"
		title_text = two_captions[0]
		title_text2 = two_captions[1]

		write2(box_length, box_x, box_y, text_size, image_link, title_text, box_x2, box_y2, title_text2)


	elif meme_type == 'Laughing-Leo':
		box_length = 30
		box_x = 300
		box_y = 10
		text_size = 35
		image_link = "Laughing-Leo.jpeg"
		color = 255

		write(box_length, box_x, box_y, text_size, image_link, title_text, color)
		
	elif meme_type == 'One-Does-Not-Simply':
		two_captions = title_text.split('\n', 1)

		box_length = 35
		box_x = 5
		box_y = 10
		box_x2 = 200
		box_y2= 10
		text_size = 35
		image_link = "One-Does-Not-Simply.jpeg"
		title_text = two_captions[0]
		title_text2 = two_captions[1]
		color = 255

		write2(box_length, box_x, box_y, text_size, image_link, title_text, box_x2, box_y2, title_text2)
		
	else:
		print('ok')

def write(box_length, box_x, box_y, text_size, image_link, title_text, color = 1):
	my_image = Image.open(image_link)
	image_editable = ImageDraw.Draw(my_image)
	title_font = ImageFont.truetype('impact.ttf', text_size)

	count = 0
	last = 0
	lines = []
	for element in range(0, len(title_text)):
		if title_text[element] == "\n":
			count = 0
		else:
			count += 1
		if count > box_length:
			lines.append(title_text[last:element])
			count = 0
			last = element

	lines.append(title_text[last:element + 1])
	title_text = '\n'.join(lines)		

	image_editable.text((box_y,box_x), title_text, (color, color, color), font=title_font)
	my_image.save("result.jpg")

def write2(box_length1, box_x1, box_y1, text_size1, image_link1, title_text1, box_x2, box_y2, title_text2, color = 1):
	my_image = Image.open(image_link1)
	image_editable = ImageDraw.Draw(my_image)
	title_font = ImageFont.truetype('impact.ttf', text_size1)

	count = 0
	last = 0
	lines = []
	for element in range(0, len(title_text1)):
		if title_text1[element] == "\n":
			count = 0
		else:
			count += 1
		if count > box_length1:
			lines.append(title_text1[last:element])
			count = 0
			last = element

	lines.append(title_text1[last:element + 1])
	title_text1 = '\n'.join(lines)		

	image_editable.text((box_y1,box_x1), title_text1, (color, color, color), font=title_font)

	count = 0
	last = 0
	lines = []
	for element in range(0, len(title_text2)):
		if title_text2[element] == "\n":
			count = 0
		else:
			count += 1
		if count > box_length1:
			lines.append(title_text2[last:element])
			count = 0
			last = element

	lines.append(title_text2[last:element + 1])
	title_text2 = '\n'.join(lines)		

	image_editable.text((box_y2,box_x2), title_text2, (color, color, color), font=title_font)

	my_image.save("result.jpg")

add_caption("Laughing-Leo", "knows about corona virus ; pikachu oh my god ; ash dont look when pikachu knows about corona virus ;")
