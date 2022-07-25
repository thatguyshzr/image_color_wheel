import extcolors
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def resizer(input_image):
    output_width = 900 # set the output size
    img = Image.open(input_image)
    wpercent = (output_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((output_width,hsize), Image.ANTIALIAS)
    
    #save
    resize_name = 'resize_' + input_image  #the resized image name
    img.save(resize_name) #output location can be specified before resize_name
    return 0

def rgb_extractor(img):
    return extcolors.extract_from_path(img, tolerance = 12, limit = 12)

def color_to_df(colors):
    df= pd.DataFrame(columns= ['hex', 'occurence'])
    for i in range(len(colors[0])):
        df.loc[i]= ['#%02x%02x%02x' % colors[0][i][0], 
                    colors[0][i][1]] # convert rgb to hex

    return df

def make_the_wheel(data, img_name):
    list_color = list(data['hex'])
    list_percent = [int(i) for i in list(data['occurence'])]
    text_c = [c + ' ' + str(round(p*100/sum(list_percent),1)) 
                +'%' for c, p in zip(list_color, list_percent)]

    fig, ax = plt.subplots(figsize=(110,110),dpi=10)
    wedges, text = ax.pie(list_percent,
                        labels= text_c,
                        labeldistance= 1.05,
                        colors = list_color,
                        textprops={'fontsize':120, 'color':'black'}
                        )
    plt.setp(wedges, width=0.3)

    #create space in the center
    plt.setp(wedges, width=0.25)

    img = mpimg.imread(img_name)
    imagebox = OffsetImage(img, zoom=3.0)
    ab = AnnotationBbox(imagebox, (0, 0))
    ax.add_artist(ab)

    ax.set_aspect("equal")
    fig.set_facecolor('white')
    plt.savefig('wheel_'+img_name)
    return 0


input_image='cabo_de_rama_IMG20220314185556_clean.jpg'
resizer(input_image)
rgb= rgb_extractor('resize_'+input_image)
df= color_to_df(rgb)
make_the_wheel(df, 'resize_'+input_image)