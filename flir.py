import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from matplotlib.cm import get_cmap
import pandas as pd

def create_df():
    cam_dir = 'camera/'
    filters = os.listdir(cam_dir)

    data = pd.DataFrame(columns=['Filter', 'LED', 'Strain', 'Voltage', 'Exposure Time','Green Mean Brightness','Blue Mean Brightness'])


    for i in range(len(filters)):
         filter = filters[i]
         filter_dir = cam_dir + filter + '/'
         leds = os.listdir(filter_dir)

         for j in range(len(leds)):
             led = leds[j]
             led_dir = filter_dir + led + '/'
             strains = os.listdir(led_dir)

             for k in range(len(strains)):
                 strain = strains[k]
                 strain_dir = led_dir + strain + '/'
                 img = os.listdir(strain_dir)

                 for l in range(len(img)):
                    image = img[l]
                    img_dir = strain_dir + image
                    idx = [index for index, char in enumerate(image) if char == '_']
                    color = image[idx[1] + 1:-4]

                    if color == 'blue':
                        voltage = int(image[:idx[0] - 1])
                        exp_time = int(image[idx[0] + 1:idx[1] - 2])
                        image = cv2.imread(img_dir)
                        r, g, b = cv2.split(image)
                        entry = {'Filter': filter, 'LED': led, 'Strain': strain, 'Voltage':voltage, 'Exposure Time':exp_time, 'Green Mean Brightness':np.mean(g),'Blue Mean Brightness':np.mean(b)}
                        data = data.append(entry, ignore_index=True)
    return data

def plot_data(df,plot,variable):
    name = "Dark2"
    cmap = get_cmap(name)
    colors = cmap.colors

    if variable == '1':
        var = 'Strain'
        col1 = 'Filter'
        col2 = 'LED'
    if variable == '2':
        var = 'Filter'
        col1 = 'Strain'
        col2 = 'LED'
    if variable == '3':
        var = 'LED'
        col1 = 'Strain'
        col2 = 'Filter'

    c1 = df[col1].unique()
    for i in range(len(c1)):
        df1 = df[df[col1] == c1[i]]
        c2 = df1[col2].unique()
        for j in range(len(c2)):
            df2 = df1[df1[col2] == c2[j]]
            v = df2[var].unique()

            fig, axs = plt.subplots(1,2,figsize=(10, 5))
            max = 0
            min = 255
            for k in range(len(v)):
                df3 = df2[df2[var] == v[k]]
                if plot == '1':
                    xx = np.array(df3['Exposure Time'])
                    xxlabel = 'Exposure Time'
                else:
                    xx = np.array(df3['Voltage'])
                    xxlabel = 'Voltage'

                green_means = np.array(df3['Green Mean Brightness'])
                blue_means = np.array(df3['Blue Mean Brightness'])
                axs[0].plot(xx, green_means, 'o-', label=v[k], color=colors[k])
                axs[1].plot(xx, blue_means, 'o-', label=v[k], color=colors[k])

            axs[0].set_xlabel(xxlabel)
            axs[0].set_ylabel('Green Channel Mean Brightness')
            axs[0].legend()
            axs[0].grid()

            axs[1].set_xlabel(xxlabel)
            axs[1].set_ylabel('Blue Channel Mean Brightness')
            axs[1].legend()
            axs[1].grid()

            fig.suptitle('['+c1[i]+ ','+c2[j]+ '] Mean Brightness vs ' + xxlabel,fontsize=10)
            t = 'plots/['+c1[i]+ ','+c2[j]+ ', Variable '+ var+'] Mean Brightness vs ' + xxlabel + '.jpg'
            plt.savefig(t, format='jpeg')
            plt.show()


