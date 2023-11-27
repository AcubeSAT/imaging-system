import flir

camera = input("Choose Camera\n"
               "1. FLIR\n"
               "2. Dinolite\n")

plot = input("Choose Plot\n"
             "1. Brightness vs Exposure Time\n"
             "2. Brightness vs Voltage\n")

variable = input("Choose Variable\n"
                 "1. Strains\n"
                 "2. Filter\n"
                 "3. LED\n")

if camera == '1':
    data = flir.create_df()
    flir.plot_data(data,plot,variable)

breakpoint()