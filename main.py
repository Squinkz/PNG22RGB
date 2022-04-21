
#######SETUP###############################################################
#
#   Images must be named 000 upwards. So if you had 16 frames, your last
#   frame would be called 015. Then just enter the parameters into the
#   variables below.
#   Other than that, I've found it's good to really give
#   the images a huge saturation boost before running the script.
#   I'm still figuring out the pillow library so I'll get to adding that
#   eventually.

#########################BEGIN USER DEFINED VALUES#########################

frameAmount = 20
imageType = "png"
blurAmount = 0
animationLength = 90000     # in ms
isContinous = False          # If yes, the animation plays once and then loops and frametime need not be set
                            #  if false, the animation will play forward and then in reverse
frameTime = 0.02            # as a percentage of the animation length

##########################END USER DEFINED VALUES##########################

import body as bd
headerFile = open("templates/header.xml", "r")
footerFile = open("templates/footer.xml", "r")

writeFile = open("animation.cueprofile", "w")
writeStr = headerFile.read() + \
           bd.write_layer_values(frameAmount, imageType, animationLength, isContinous, frameTime, blurAmount) + \
           footerFile.read()
writeFile.write(writeStr)
headerFile.close()
footerFile.close()
writeFile.close()