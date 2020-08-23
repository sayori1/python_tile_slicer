
from PIL import Image
import sys
if(len(sys.argv) == 1):
    print("destinate path to image");
image = Image.open(sys.argv[1]);
step = 1;
if(len(sys.argv) < 3 or sys.argv[2] == "-low"):
    step = 1;
elif(sys.argv[2] == "-fast"):
    step = 5;

alpha = 61
tiles = []

def has_tile(square):
    for tile in tiles:
        if tile == square:
            return True;
    return False;

def split_by_alpha():
    for y in range(0, image.height, step):
        for x in range(0, image.width, step):
            if(image.getpixel((x,y)) != alpha):  #if we find not transparent pixel
                square = process(x,y);
                if(has_tile(square)):
                    continue;
                tiles.append(square)
                
def split():
    index=0;
    for tile in tiles:
        img = image.crop(tile);
        img.save("tile"+str(index)+".png");
        index+=1;
def process(x, y):
    square = (x, y, x+1, y+1);
    while True:
        result = check(square[0], square[1], square[2], square[3]);
        if(result == "up"):
            square = (square[0], square[1] - 1, square[2], square[3])
        elif(result == "left"):
            square = (square[0]-1, square[1], square[2], square[3])
        elif(result == "right"):
            square = (square[0], square[1], square[2]+1, square[3])
        elif(result == "down"):
            square = (square[0], square[1], square[2], square[3]+1)
        elif(result == "none"):
            break;
        elif(result == "out of image"):
            break;
    if(square[2] > image.width):
        square[2] = image.width;
    if(square[3] > image.height):
        square[3] = image.height;
    return square
def check(x, y, x1, y1):
    if(x1 >= image.width or y1 >= image.height):
        return "out of image";
    for i in range(x,x1):
        if(image.getpixel((i, y)) != alpha):
            return "up"
        if(image.getpixel((i, y1)) != alpha):
            return "down"
    for i in range(y, y1):
        if(image.getpixel((x, i)) != alpha):
            return "left"
        if(image.getpixel((x1, i)) != alpha):
            return "right"
    return "none"
        
split_by_alpha();
split();
