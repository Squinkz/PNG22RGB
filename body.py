def layer_header(_value, _keyName, _animLen):
    import idlist as idl
    idList = idl.idList
    writeStr = "<value" + str(_value) + ">\n"
    writeStr += "\t<polymorphic_id>" + idList[_value][0] + "</polymorphic_id>\n"
    writeStr += "\t<ptr_wrapper>\n"
    writeStr += "\t\t<id>" + idList[_value][1] + "</id>\n"
    writeStr += "\t\t<data>\n"
    writeStr += "\t\t\t<base>\n"
    writeStr += "\t\t\t\t<name>" + _keyName + " frames</name>\n"
    writeStr += "\t\t\t\t\t<keys size=\"dynamic\">\n"
    writeStr += "\t\t\t\t\t\t<value0>" + _keyName + "</value0>\n"
    writeStr += "\t\t\t\t\t</keys>\n"
    writeStr += "\t\t\t\t\t<enabled>true</enabled>\n"
    writeStr += "\t\t\t\t\t<executionHints>\n"
    writeStr += "\t\t\t\t\t\t<startOnKeyPress>false</startOnKeyPress>\n"
    writeStr += "\t\t\t\t\t\t<startWithProfile>true</startWithProfile>\n"
    writeStr += "\t\t\t\t\t\t<stopOnKeyPress>false</stopOnKeyPress>\n"
    writeStr += "\t\t\t\t\t\t<stopOnKeyRelease>false</stopOnKeyRelease>\n"
    writeStr += "\t\t\t\t\t\t<stopAfterTimes>-1</stopAfterTimes>\n"
    writeStr += "\t\t\t\t\t\t<playOption>Standard</playOption>\n"
    writeStr += "\t\t\t\t\t</executionHints>\n"
    writeStr += "\t\t\t\t<option>ConcreteLeds</option>\n"
    writeStr += "\t\t\t</base>\n"
    writeStr += "\t\t\t<lighting>\n"
    writeStr += "\t\t\t\t<polymorphic_id>" + idList[_value][2] + "</polymorphic_id>\n"
    if (_value == 0):
        writeStr += "\t\t\t\t<polymorphic_name>GradientLighting</polymorphic_name>\n"
    writeStr += "\t\t\t\t<ptr_wrapper>\n"
    writeStr += "\t\t\t\t\t<id>" + idList[_value][3] + "</id>\n"
    writeStr += "\t\t\t\t\t<data>\n"
    if (_value == 0):
        writeStr += "\t\t\t\t\t\t<cereal_class_version>300</cereal_class_version>\n"
    writeStr += "\t\t\t\t\t\t<base>\n"
    if (_value == 0):
        writeStr += "\t\t\t\t\t\t\t<cereal_class_version>201</cereal_class_version>\n"
    writeStr += "\t\t\t\t\t\t\t<base>\n"
    writeStr += "\t\t\t\t\t\t\t\t<name>" + _keyName + "</name>\n"
    writeStr += "\t\t\t\t\t\t\t\t<id>" + idList[_value][4] + "</id>\n"
    writeStr += "\t\t\t\t\t\t\t\t<duration>" + str(_animLen) + "</duration>\n"
    writeStr += "\t\t\t\t\t\t\t\t<brightness>10</brightness>\n"
    writeStr += "\t\t\t\t\t\t\t</base>\n"
    return writeStr

def layer_footer(_value):
    writeStr =	"\t\t\t\t\t\t</base>\n"
    writeStr +=	"\t\t\t\t\t</data>\n"
    writeStr +=	"\t\t\t\t</ptr_wrapper>\n"
    writeStr +=	"\t\t\t</lighting>\n"
    writeStr +=	"\t\t</data>\n"
    writeStr += "\t</ptr_wrapper>\n"
    writeStr += "</value" + str(_value) + ">\n"
    return writeStr

def make_black_alpha(_rgbColor):
    if (int(_rgbColor[0]) + int(_rgbColor[1]) + int(_rgbColor[2]) == 0):
        return "00"

def write_layer_values(_imgAmt, _imgType, _animLen, _continous, _timeInc, _blurFactor):
    from PIL import Image, ImageFilter, ImageEnhance
    import keymap as kl

    keyMap = kl.keyList
    finalHex = ""
    writeStr = ""
    if (_continous):
        _timeInc = 1 / _imgAmt
    timeRemainder = (1 - (_timeInc * (_imgAmt - 1) * 2)) * 0.5

    imgList = []
    for i in range(_imgAmt):
        tempImg = Image.open(str(i).rjust(3, "0") + "." + _imgType)
        tempImg.filter(ImageFilter.GaussianBlur(_blurFactor))
        #tempImg.filter(ImageEnhance.Color(2))
        imgList.append(tempImg)

    for key in range(len(keyMap)):
        if not _continous and ((_timeInc * (_imgAmt - 1) * 2) > 1):
            print("Frametime too long!")
            break
        time = 0.0
        forward = False
        writeStr += layer_header(key, keyMap[key][0], _animLen)
        writeStr += "\t\t\t\t\t\t\t<transitions size=\"dynamic\">\n"

        frameAmt = _imgAmt * ((not _continous) + 1)
        for i in range(frameAmt):
            if forward:
                img = imgList[i - _imgAmt]
            else:
                img = imgList[_imgAmt - 1 - i]

            sampleCoordsNorm = [keyMap[key][1], keyMap[key][2]]
            imgSize = img.size
            sampleCoordsPixel = [imgSize[0] * sampleCoordsNorm[0], imgSize[1] * sampleCoordsNorm[1]]

            sampledRGB = img.getpixel((int(sampleCoordsPixel[0]), int(sampleCoordsPixel[1])))
            sampledHex = [hex(sampledRGB[0])[2:], hex(sampledRGB[1])[2:], hex(sampledRGB[2])[2:]]

            hexStr = "ff" + \
                     str(sampledHex[0]).rjust(2, "0") + \
                     str(sampledHex[1]).rjust(2, "0") + \
                     str(sampledHex[2]).rjust(2, "0")

            writeStr += ("\t\t\t\t\t\t\t\t<value" + str(i) + ">\n")
            if (i == 0 and key == 0):
                writeStr += "\t\t\t\t\t\t\t\t\t<cereal_class_version>200</cereal_class_version>\n"
            writeStr += ("\t\t\t\t\t\t\t\t\t<time>" + str(time) + "</time>\n")
            writeStr += ("\t\t\t\t\t\t\t\t\t<color>#" + str(hexStr) + "</color>\n")
            writeStr += ("\t\t\t\t\t\t\t\t</value" + str(i) + ">\n")

            if (i  == _imgAmt - 1):
                time = round(time + timeRemainder, 3)
                forward = True
            else:
                time = round(time + _timeInc, 3)

            if (i == frameAmt - 1):
                finalHex = hexStr

            print (".", end="")

        writeStr += ("\t\t\t\t\t\t\t\t<value" + str(frameAmt) + ">\n")
        writeStr += ("\t\t\t\t\t\t\t\t\t<time>" + "1" + "</time>\n")
        writeStr += ("\t\t\t\t\t\t\t\t\t<color>#" + finalHex + "</color>\n")
        writeStr += ("\t\t\t\t\t\t\t\t</value" + str(frameAmt) + ">\n")

        writeStr += "\t\t\t\t\t\t\t</transitions>\n"
        writeStr += layer_footer(key)

        print("\nFinished sampling for " + keyMap[key][0])

    for i in range(_imgAmt):
        imgList[i].close()

    return writeStr