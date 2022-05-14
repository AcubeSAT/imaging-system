# Logbook

# *Camera testing 14/5/2022*

## **Operations**

| ID | Step Description | Remarks |
| :---: | ---------------- | ------ |
| 010 | Setup the camera | 
| 020 | Receive images from camera | Cover the lens of the camera so the image is dark
| 030 | Replace the cable with the unused one |
| 040 | Receive images | Cover the lens of the camera so the image is dark
| 050 | Enable sensor defects correction |
| 060 | Receive images |  Cover the lens of the camera so the image is dark
| 070 | Enable Flat Field correction |
| 080 | Receive images |  Cover the lens of the camera so the image is dark
| 090 | Gradually approach the lens with the light source (phone torchlight) until the transition to a green hue takes place and move it back untill the feed is normal |
| 100 | Extract the camera settings |
| 110 | Bring the light source closer for the green hue to appear in the camera feed |
| 120 | Extract the camera settings |



## **Results**

|   ID   |       Result      | Status |
| :----: | ----------------- | :------: |
|  010  | Bad connection between the cable (USB) and the laptop, the camera connection is not stable, leads to deviation 011 | ![deviation]
|  020  | [Image](./assets/old-cable.tif) shows stuck pixels, satisfied with the results, decided to stop the procedure  | ![complete]

## **Deviations**

# ID-010
|   ID   |       Step Description      | Status |
| :----: | --------------------------- | ------ |
|  011  | Try diffrent USB ports and securing the cable to the camera, problem not solved | ![anomaly]
|  012  | Replace the cable with the unused one, The POWER display turns on, and the STATUS 1 display keeps blinking, problem not solved  | ![anomaly]
|  013  | Try on a diffrent computer, problem not solved  | ![anomaly]
| 014 | Change settings on computer (see "Extra"), problem not solved | ![anomaly]
| 015 | Shut down XiCOP (through task manager), restart it and start it as admin, problem not solved | ![anomaly]
| 016 | Uninstall and intall XIMEA Windows Software Package and reinstall the latest version, problem not solved | ![anomaly]
| 017 | Install the program on a diffrent computer and connect the camera, receiving feed normally | ![successful]
| 018 | receive [image](./assets/new-cable.tif) with new cable, image shows no stuck pixels | ![successful]
| 019 | replace the cable with the old one, move to step 020 | ![successful]


# Extra
- Temperature in the cleanroom is 21.7°C
- The steps while adjusting the program settings (for deviation 014) more spesifically are: 
   - While using the new unused cable the POWER display on the camera turns on, and the STATUS 1 display keeps blinking
   - CamTool doesn't detect the device
   - XiCOP says the Firmware (CPU/Flash) is corrupted
   - Attempt to update the firmware through XiCOP
   - Because it detected the firmware as corrupted, it requires the model number
   - No option in the dropdown to select the device
   - "Do you want to fix the camera flash file system?" yes
   - Failed because it doesn't support the serial number
   - Retry, now the models are shown in the dropdown and the correct one was selected
   - Error on "updating firmware cannot open usb3 device using ximea driver"
   - New error that says again that no firmware is supported for the camera appears



[complete]: <./assets/markdown_complete.png>
[successful]: <./assets/markdown_successful.png>
[deviation]: <./assets/markdown_deviation.png>
[anomaly]: <./assets/markdown_anomaly.png>
