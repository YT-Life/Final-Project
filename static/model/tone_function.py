from PIL import ImageColor
import colorsys
import numpy as np

# tone in tone
def tone_in_tone(hex):
    # convert hex to rgb
    red = ImageColor.getcolor(hex, 'RGB')[0]/255 
    green = ImageColor.getcolor(hex, 'RGB')[1]/255 
    blue = ImageColor.getcolor(hex, 'RGB')[2]/255 

    # convert rgb to hsv
    hsv = colorsys.rgb_to_hsv(red, green, blue)

    # convert hsv to hex
    color_list = []
    for i in range(12):
        tmp = [(1/12)*i, hsv[1], hsv[2]]
        tmp = colorsys.hsv_to_rgb(tmp[0], tmp[1], tmp[2])
        tmp = np.uint8([i*255 for i in tmp])
        tmp = '#'+format(tmp[0], '02x')+format(tmp[1], '02x')+format(tmp[2], '02x')
        color_list.append(tmp)
        
    return color_list

# tone on tone
def tone_on_tone(hex):
    # convert hex to rgb
    red = ImageColor.getcolor(hex, 'RGB')[0]/255 
    green = ImageColor.getcolor(hex, 'RGB')[1]/255 
    blue = ImageColor.getcolor(hex, 'RGB')[2]/255 

    # convert rgb to hsv
    hls = colorsys.rgb_to_hls(red, green, blue)
    
    # convert hls to hex
    color_list = []
    for i in range(12):
        tmp = [hls[0], (1/12) * i, hls[2]]
        tmp = colorsys.hls_to_rgb(tmp[0], tmp[1], tmp[2])
        tmp = np.uint8([i*255 for i in tmp])
        tmp = '#'+format(tmp[0], '02x') + format(tmp[1], '02x') + format(tmp[2], '02x')
        color_list.append(tmp)

    return color_list
