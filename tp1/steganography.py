from stegano import lsb

def hide_text(img_path, text):
    # return the image with hidden text in it
    return lsb.hide(img_path, text)

def show_text(img_path):
    # return the hidding text in the image
    return lsb.reveal(img_path)

## to .save() to save the image in a path
#hide_text("inpt_img.png", "this is a hidden text, yasser!!").save('output_img.png')

#print(show_text("output_img.png"))

# print(hide_text('./tp1/a.jpg', 'hello world!').save("nigga.png"))

# print(show_text("nigga.png"))