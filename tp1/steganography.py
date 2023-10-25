from stegano import lsb

def hide_text(img_path, text):
    # return the image with hidden text in it
    return lsb.hide(img_path, text)

def show_text(img_path):
    # return the hidding text in the image
    return lsb.reveal(img_path)