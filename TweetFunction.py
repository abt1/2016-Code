import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from wrap_to_axes import textAxes

twitterbird = plt.imread('Twitter_logo_blue.png')
logo_position = [.92, 0.81]
pp_position = [0.05, 0.785]

fig = plt.figure(2, figsize=(8,2.5))
plt.axis([0, 1, 0, 1])
ax = plt.gca()
plt.subplots_adjust(left=.05, right=1, top=1, bottom=.05)


imagebox = OffsetImage(twitterbird, zoom = .03, resample=True)
logo = AnnotationBbox(imagebox, logo_position, xycoords='data', bboxprops={'ec':'w'})

def Tweet(name, username, profilepic, text, ID, external_font=None):
    plt.text(0.1,0.78,name,size='large', weight='demibold')
    plt.text(0.1,0.705,'@' + username,color='#8899a6',size='medium')
    if external_font:
        prop = fm.FontProperties(fname=external_font, size = 'x-large')
        textAxes(0, 0.65, text, wrap=True, verticalalignment='top', fontproperties = prop, ax=ax)
    else:
        textAxes(0, 0.65, text, wrap=True, verticalalignment='top', ax=ax, size = 'x-large')
    profile_pic = plt.imread(profilepic)
    imagebox = OffsetImage(profile_pic, zoom = .18, resample=True)
    p_pic = AnnotationBbox(imagebox, pp_position, xycoords='data', bboxprops={'ec':'w'})
    ax.add_artist(logo)
    ax.add_artist(p_pic)
    plt.axis('off')
    plt.savefig('{0}.png'.format(ID))
    plt.cla()
