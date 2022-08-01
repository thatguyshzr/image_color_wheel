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
    resize_name = input_image.split('.',1)[0] + '_resize.' + input_image.split('.',1)[1]  #the resized image name
    img.save(resize_name) #output location can be specified before resize_name
    return 0

def color_to_df(img):
    img_name= img.split('.',1)[0] + '_resize.' + img.split('.',1)[1]
    colors= extcolors.extract_from_path(img_name, tolerance = 12, limit = 12)
    df= pd.DataFrame(columns= ['hex', 'occurence'])
    for i in range(len(colors[0])):
        df.loc[i]= ['#%02x%02x%02x' % colors[0][i][0], 
                    colors[0][i][1]] # convert rgb to hex

    return df

def make_the_wheel(data, img):
    img_name= img.split('.',1)[0] + '_resize.' + img.split('.',1)[1]
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
    fig.set_facecolor('#e0e0e0')
    plt.tight_layout()
    plt.savefig(img_name.replace('resize','wheel'))
    return 0


input_image='assets/hotel.jpg'
resizer(input_image)
df= color_to_df(input_image)
make_the_wheel(df, input_image)
