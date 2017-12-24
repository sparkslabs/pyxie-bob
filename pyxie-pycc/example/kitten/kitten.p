sleep_time = 0
kitten_name = 0
happy_kitten = make_image(0xe,0x11,0x4,0xa,0xa)
sad_kitten = make_image(0x11,0xe,0x0,0x4,0x1b)
oh_kitten = make_image(0xe,0xa,0x4,0x1b,0xa)
confused_kitten = make_image(0x1f,0x0,0x4,0xa,0x1b)
show_image_offset(happy_kitten,0,0)
while True:
  if (get_button('A')) == True:
    kitten_name = kitten_name + 1
    if kitten_name == 0:
      show_image_offset(happy_kitten,0,0)
    elif kitten_name == 1:
      show_image_offset(sad_kitten,0,0)
    elif kitten_name == 2:
      show_image_offset(oh_kitten,0,0)
    else:
      show_image_offset(confused_kitten,0,0)
      kitten_name = -1
    while (get_button('A')) == True:
      pass
