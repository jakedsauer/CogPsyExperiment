from psychopy import visual, core, data, event, logging, gui, misc
from psychopy.visual import filters
from psychopy.tools.filetools import fromFile, toFile
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle, choice, random_integers
import numpy, time, sys, random, os, pylab, expclass, pickle, readit

try:
    import win32api
except:
    print("didn't import win32api")
    pass

try:
    file = open('data.dat', 'rb')
    experiidata = pickle.load(file)
    print("loading data...")

    # time.sleep(1)
    # print(".", end = '')
    # time.sleep(1)
    # print(".", end = '')
    # time.sleep(1)
    # print(".")
except Exception as e:
    # print(e)
    experiidata = expclass.Data()

consent = gui.Dlg(title='Consent Acknowledgement')
consent.addText('I have read the Consent Form and I am okay with participating in the study')
consent.addField(choices=['DO NOT ACCEPT', 'ACCEPT'])
consentForm = consent.show()
if consent.OK and consentForm[0] == 'ACCEPT':
    pass
else:
    core.quit()

demo = gui.Dlg(title='Demographics')
demo.addField('Age:')
demo.addText('Birthdate')
demo.addField('Day:')
demo.addField('Month:')
demo.addField('Year:')
demo.addField('Gender:', choices=['M', 'F', 'O', 'Prefer not to say'])
demo.addField('Class:', choices=['Freshman', 'Sophomore', 'Junior', 'Senior', 'Other'])
demo.addField('Ethnicity:', choices=['Hispanic or Latino', 'Not Hispanic or Latino', 'Unknown', 'Prefer not to say'])
demo.addField('Race:', choices=['American Indian / Alaska Native', 'Asian', 'Black or African American', 'More Than One Race', 'Native Hawaiian/Other Pacific Islander', 'White or European', 'Unknown', 'Other', 'Prefer not to say'])
demo.addField('First Language Learned?')
demo.addField('Are you fluent in English?', choices=['Yes', 'No', 'Prefer not to say'])
demo.addField('Have you taken any medication that could\naffect your cognitive abilities?', choices=['Yes', 'No', 'Prefer not to say'])
demo.addField('If you answered \"Yes\", please explain HOW\nthe medication may affect your participation')
demo.addField('Do you currently have any hearing problems?', choices=['Yes', 'No', 'Prefer not to say'])
demo.addText('Vision')
demo.addField('20/20', choices=['Yes', 'No', 'Prefer not to say'])
demo.addField('Glasses/Contacts', choices=['Yes', 'No', 'Prefer not to say'])
demo.addField('Color Blind', choices=['Yes', 'No', 'Prefer not to say'])
demo.addField('If you wear glasses or contacts,\nare you wearing them today?')
demoForm = demo.show()

if demo.OK:
    pass
else:
    core.quit()
med = 'Taken medication - ' + demoForm[11] + '|Medication effects - ' + demoForm[12]
vision = demoForm[13] + ',' + demoForm[14] + ',' + demoForm[15] + ',' + demoForm[16]

dlg = gui.Dlg(title='Circles and Colors Exp')
dlg.addText('Participant info')
dlg.addField('Participant Number:')
dlg.addText('Experiment Info')
dlg.addFixedField('Rundate', data.getDateStr())
ok_data = dlg.show()

if dlg.OK:
    pass
else:
    core.quit()

birthdate = demoForm[1] + '/' + demoForm[2] + '/' + demoForm[3]

demoInfo = expclass.Demographics(ok_data[0], demoForm[0], birthdate, demoForm[4], demoForm[5], demoForm[6], demoForm[7], demoForm[8], demoForm[9], med, demoForm[12], vision)
subjectInfo = expclass.Subject(ok_data[0], birthdate, demoForm[4], ok_data[1])
experii = expclass.Experiment(subjectInfo)
experiidata.add_exp(experii)
experiidata.add_demo(demoInfo)

#Stimulus locations
StimLocs = [[-124, 0],
            [0,  124],
            [124,  0]]

KEY_TERMINATE = "escape"
KEY_CONTINUE = "space"

win = visual.Window(fullscr = True, units = 'pix', allowGUI=False, color = [0, 0, 0], colorSpace = 'rgb')

myMouse = event.Mouse(win = win)

circle1 = visual.Circle(win, units = 'pix', radius = 30, lineColorSpace = 'rgb255', fillColorSpace = 'rgb255', lineWidth = 1, edges = 64)
circle2 = visual.Circle(win, units = 'pix', radius = 30, lineColorSpace = 'rgb255', fillColorSpace = 'rgb255', lineWidth = 1, edges = 64)
circle3 = visual.Circle(win, units = 'pix', radius = 30, lineColorSpace = 'rgb255', fillColorSpace = 'rgb255', lineWidth = 1, edges = 64)

circleList = [circle1, circle2, circle3]

imageName = 'circle_with_line.png'

line1 = visual.ImageStim(win, image =imageName, colorSpace = 'rgb255')
line2 = visual.ImageStim(win, image=imageName, colorSpace = 'rgb255')
# line3 = visual.ImageStim(win, image=imageName, colorSpace = 'rgb255')

lineList = [line1, line2]

RespIndic = visual.GratingStim(win, tex = 'none', mask = 'none',  size = [25,75],colorSpace = 'rgb255')

for (circle, loc) in zip(circleList, StimLocs):
    circle.setPos(loc)
for (line, i) in zip(lineList, [0,2]):
    line.setPos(StimLocs[i])


ring = visual.ElementArrayStim(win, units = 'pix', fieldPos = [0,0], fieldSize = [500,500], fieldShape = 'circle', nElements = 360,
    sizes = 60, colorSpace = 'rgb255',elementMask = 'circle', elementTex = 'none', texRes = 400, phases = 1)

def MoveMouse(x, y):
    try:
        win32api.SetCursorPos((x,y))
    except:
        pass

def setRingBlack():
    black = []

    for i in range(360):
        black.append([0,0,0])
    return numpy.array(black)

def errorCorrection(error): #corrects for close distances near degree 0
    if error >= 180.0:
        error -= 360.0
    elif error <= -180.0:
        error += 360.0
    return -error

def getCircle(radius, randomRotation, full, angles, x_centre, y_centre): # draw a cricle - for use in colour wheel and stim locations. if full = False angles must be specified
    if full == True:
        Ang = range(1 + randomRotation,361 + randomRotation) # STARTING AT 1 WHERE PYTHON INDICIES START AT 0 COULD BE A PROBLEM...
    elif full == False:
        Ang = angles
    list = []
    for i in Ang:
        x = sin((i*pi/180))*radius
        y = cos((i*pi/180))*radius
        list.append([(x+x_centre),(y+y_centre)])
    return list

def LAB2RGB(L, a, b, radius): # creates list of 360 colors for ring and stimuli in CIELab colour space with specified centre (L, a, b) and radius then converts to RGB, trimming nonsense values
    colours = []
    # create CIELab colours
    for ang in range(1, 361):
        theta = ang * pi / 180.000 # converts angle to radian
        A = a + radius*numpy.cos(theta)
        B = b + radius*numpy.sin(theta)

        # Lab to XYZ
        var_Y = (L + 16) / 115.000
        var_X = A / 500.000 + var_Y
        var_Z = var_Y - B / 200.000

        # filter X, Y, Z with threshold 0.008856
        if  var_Y**3 > 0.008856: var_Y = var_Y**3
        else: var_Y = ( var_Y - 16 / 116.000 ) / 7.787
        if var_X**3 > 0.008856: var_X = var_X**3
        else: var_X = ( var_X - 16 / 116.000 ) / 7.787
        if var_Z**3 > 0.008856: var_Z = var_Z**3
        else: var_Z = ( var_Z - 16 / 116.000 ) / 7.787

        # reference points
        ref_X =  95.047
        ref_Y = 100.000
        ref_Z = 108.883

        X = ref_X * var_X / 100.000
        Y = ref_Y * var_Y / 100.000
        Z = ref_Z * var_Z / 100.000

        # covert XYZ to RGB
        var_R = X * 3.2406 + Y * -1.5372 + Z * -0.4986
        var_G = X * -0.9689 + Y * 1.8758 + Z * 0.0415
        var_B = X * 0.0557 + Y * -0.2040 + Z * 1.0570

        # gamma correction to IEC 61966-2-1 standard
        if var_R > 0.0031308: var_R = 1.055 * ( var_R ** ( 1 / 2.400 ) ) - 0.055
        else: var_R = 12.92 * var_R
        if var_G > 0.0031308: var_G = 1.055 * ( var_G ** ( 1 / 2.400 ) ) - 0.055
        else: var_G = 12.92 * var_G
        if var_B > 0.0031308: var_B = 1.055 * ( var_B ** ( 1 / 2.400 ) ) - 0.055
        else: var_B = 12.92 * var_B

        # trim
        if (var_R*255) > 255: R = 255
        elif (var_R*255) < 0: R = 0
        else: R = round(var_R*255)

        if (var_G*255) > 255: G = 255
        elif (var_G*255) < 0: G = 0
        else: G = round(var_G*255)

        if (var_B*255) > 255: B = 255
        elif (var_B*255) < 0: B = 0
        else: B = round(var_B*255)

        colours.append([R,G,B])
    return numpy.array(colours)

labColorsList = LAB2RGB(L = 50, a = 20, b = 20, radius = 60)

def screenPrompt(string = 'Trial Starting', shape = None):   #displays string on screen
                            #if string is empty, displays 'Trial Starting'
    event.Mouse(visible=False, newPos=[0,0], win=None)
    if(shape != None):
        shape.draw()
    instruction = visual.TextStim(win, text = string, color = [-1,-1,-1], colorSpace = 'rgb', height = 60, wrapWidth = 800)
    instruction.draw()
    win.flip()
    time.sleep(1)
    key = event.waitKeys(keyList = [KEY_CONTINUE, KEY_TERMINATE])
    win.flip()
    if key[0] == KEY_TERMINATE:
        file = open('data.dat', 'wb')
        pickle.dump(experiidata, file)
        file.close()
        readit.makeExcel()
        core.quit()
    time.sleep(2)

def screenWait(string = 'Trial Starting', timing = 2):      #displays string on screen
                                                            #if string is empty, displays 'Trial Starting'
    event.Mouse(visible=False, newPos=[0,0], win=None)
    instruction = visual.TextStim(win, text = string,color = [-1,-1,-1], colorSpace = 'rgb', height = 60, wrapWidth = 800)
    instruction.draw()
    win.flip()
    time.sleep(timing)

def genStimuli(sets = 1):   #sets = number of screens of stimuli needed
                            #generates an array of random integers [0, 359] 3 at a time
    stim = numpy.random.random_integers(0, high = 359, size = sets * len(circleList))
    return stim

def genProbeOrder(sets = 1): #sets = numbers of screens of stimuli that will be displayed
    order = [0,1,2]
    random.shuffle(order)
    if(sets != 1):
        for i in range(sets):
            temp = np.arange(3)
            random.shuffle(temp)
            order.append(temp)

    return order

def genStimTypeOrder(single, blockLength):   #generates a list of strings that indicate order and type of stimuli used in trial
                                        #single is a boolean for how many screens will be shown per trial
    array = []

    for i in range(blockLength):                  #controls length of blocks       Should be multiple of 4
        array.append(i)

    random.shuffle(array)

    index = 0

    if(single):
        for i in array:
            i = i % 2
            if i:
                array[index] = 'Color'
            else:
                array[index] = 'Line'
            index+=1
    else:
        for i in array:
            i = i % 4
            if i == 1:
                array[index] = 'ColCol'
            elif i == 2:
                array[index] = 'ColLin'
            elif i == 3:
                array[index] = 'LinCol'
            else:
                array[index] = 'LinLin'
            index+=1

    print(array)
    return array

STIMSHOWTIME = .3

def showColor(stim, probeIndexOrder, trialInfo):
    event.Mouse(visible = False, newPos = None, win = None)

    for (circle, color) in zip(circleList, stim):
        circle.setFillColor(labColorsList[color])
        circle.setLineColor(labColorsList[color])

    # timing = 400          #determines length stim is shown and length of blank screen
    #
    # for frameN in range(timing):
    #     if frameN < timing/2:
    for circle in circleList:
        circle.draw()
    win.flip()
    time.sleep(STIMSHOWTIME)
    win.flip()
    time.sleep(1)
        # elif timing/2 <= frameN < timing:
        #     win.flip()

    outputStim = []
    for i in probeIndexOrder:
        outputStim.append(stim[i])
    trialInfo.add_stim(outputStim)

def showLine(stim, probeIndexOrder, trialInfo):
    event.Mouse(visible = False, newPos = None, win = None)

    probeIndexOrder.remove(2)

    for (line, angle) in zip(lineList, stim):
        line.ori = angle
        line.color = (255,255,255)

    for line in lineList:
        line.draw()
    win.flip()
    time.sleep(STIMSHOWTIME)

    win.flip()
    time.sleep(1)
    outputStim = []
    for i in probeIndexOrder:
        outputStim.append(stim[i])
    trialInfo.add_stim(outputStim)
    print(outputStim)


def showStim(stim, stimType, probeIndexOrder, trialInfo):   #takes array of 3 integers and string stimtype
    trialInfo.add_stimorder(probeIndexOrder)
    if stimType == "Color":
        showColor(stim, probeIndexOrder, trialInfo)
    elif stimType == "Line":
        showLine(stim, probeIndexOrder, trialInfo)


def probeColor(stim, probeIndexOrder, trialInfo):
    event.Mouse(visible = True, newPos = None, win = None)

    for circle in circleList:
        circle.setFillColor([127,127,127])
        circle.setLineColor([255,255,255])

    responseTimes = [0,0,0]
    responses = [0,0,0]
    errors = [0,0,0]

    index = 0

    randomRot = random.choice(range(360))

    for probeIndex in probeIndexOrder:
        probeItem = circleList[probeIndex]
        probeItem.setFillColor([0,0,0])
        probeItem.setLineColor([0,0,0])

        cirLocs = getCircle(radius = 350, randomRotation = randomRot, full = True, angles = 0, x_centre = 0, y_centre = 0) # get locations for 360 circles to make up ring
        resIndLocs = getCircle(radius = 320, randomRotation = randomRot, full = True, angles = 0, x_centre = 0, y_centre = 0) # get locations for wheel indicator
        ring.setColors(labColorsList) # set ring colours
        ring.setXYs(cirLocs) # set locations
        xcoords = [x[0] for x in cirLocs]
        ycoords = [x[1] for x in cirLocs]
        minDist = 200
        event.Mouse(visible=True, newPos=[0,0], win=None)
        timer = core.MonotonicClock()
        while minDist > 100: # waits until mouse has moved x number of pixels close to an option
            win.setMouseVisible(True)
            mouse_x, mouse_y = myMouse.getPos()
            distances = sqrt((xcoords - mouse_x)**2 + (ycoords - mouse_y)**2)
            minDist = min(distances)
            probeItem.setFillColor([255,255,255])
            probeItem.setLineColor([255,255,255])
            ring.draw()
            for circle in circleList:
                circle.draw()
            win.flip()
            myMouse.clickReset()
            mouse1 = 0

        while mouse1 < 1:
            win.setMouseVisible(True)
            mouse1, mouse2, mouse3 = myMouse.getPressed()
            for key in event.getKeys():
                if key in ['escape', 'q']:
                    file = open('data.dat', 'wb')
                    pickle.dump(experiidata, file)
                    file.close()
                    readit.makeExcel()
                    core.quit()

            mouse_x, mouse_y = myMouse.getPos()
            distances = sqrt((xcoords - mouse_x)**2 + (ycoords - mouse_y)**2)
            minDist = min(distances)
            minDistIndex = numpy.argmin(distances)
            updateCol = labColorsList[minDistIndex]
            probeItem.setFillColor(updateCol)
            probeItem.setLineColor(updateCol)

            RespIndic.setPos(resIndLocs[minDistIndex])
            RespIndic.setOri(minDistIndex+randomRot)
            RespIndic.setColor(updateCol, 'rgb255')
            event.clearEvents()
            ring.draw()
            RespIndic.draw()
            for i in circleList:
                i.draw()
            win.flip()
        responseTimes[index] = timer.getTime()
        mouse1 = 0

        ResponseIndex = minDistIndex
        responses[index] = ResponseIndex
        errorDistance = stim[probeIndex] - ResponseIndex
        errors[index] = errorCorrection(errorDistance)
        index += 1

    trialInfo.add_error(errors)
    trialInfo.add_response(responses)
    trialInfo.add_responsetime(responseTimes)



def probeLine(stim, probeIndexOrder, trialInfo):
    event.Mouse(visible = False, newPos = None, win = None)

    index = 0
    print(probeIndexOrder)

    responseTimes = [0,0]
    responses = [0,0]
    errors = [0,0]

    for line in lineList:
        line.ori = random.choice(range(360))
        line.color = (127,127,127)

    for probeIndex in probeIndexOrder:
        probeItem = lineList[probeIndex]
        probeItem.color = (0,0,0)

        cirLocs = getCircle(radius = 350, randomRotation = 0, full = True, angles = 0, x_centre = 0, y_centre = 0) # get locations for 360 circles to make up ring
        resIndLocs = getCircle(radius = 320, randomRotation = 0, full = True, angles = 0, x_centre = 0, y_centre = 0) # get locations for wheel indicator
        RespIndic.setColor('yellow')
        ring.setColors(setRingBlack()) # set ring colours
        ring.setXYs(cirLocs) # set locations
        xcoords = [x[0] for x in cirLocs]
        ycoords = [x[1] for x in cirLocs]
        minDist = 200
        event.Mouse(visible=True, newPos=[0,0], win=None)
        timer = core.MonotonicClock()

        while minDist > 100: # waits until mouse has moved x number of pixels close to an option
            win.setMouseVisible(True)
            mouse_x, mouse_y = myMouse.getPos()
            distances = sqrt((xcoords - mouse_x)**2 + (ycoords - mouse_y)**2)
            minDist = min(distances)
            ring.draw()
            for line in lineList:
                line.draw()
            win.flip()
            myMouse.clickReset()
            mouse1 = 0

        while mouse1 < 1:
            win.setMouseVisible(True)
            mouse1, mouse2, mouse3 = myMouse.getPressed()
            for key in event.getKeys():
                if key in ['escape', 'q']:
                    file = open('data.dat', 'wb')
                    pickle.dump(experiidata, file)
                    file.close()
                    readit.makeExcel()
                    core.quit()
            mouse_x, mouse_y = myMouse.getPos()
            distances = sqrt((xcoords - mouse_x)**2 + (ycoords - mouse_y)**2)
            minDist = min(distances)
            minDistIndex = numpy.argmin(distances)
            updateDeg = minDistIndex
            probeItem.ori = updateDeg

            RespIndic.setPos(resIndLocs[minDistIndex])
            RespIndic.setOri(minDistIndex)
            event.clearEvents()
            ring.draw()
            RespIndic.draw()
            for i in lineList:
                i.draw()
            win.flip()

        responseTimes[index] = timer.getTime()
        mouse1 = 0
        probeItem.color = (255,255,255)

        ResponseIndex = minDistIndex
        responses[index] = ResponseIndex
        errorDistance = stim[probeIndex] - ResponseIndex
        errors[index] = errorCorrection(errorDistance)
        index += 1

    trialInfo.add_response(responses)
    trialInfo.add_error(errors)
    trialInfo.add_responsetime(responseTimes)

def probe(stim, stimType, probeIndexOrder, trialInfo):

    response = [0,0,0]

    if stimType == "Color":
        response = probeColor(stim, probeIndexOrder, trialInfo)
    elif stimType == "Line":
        response = probeLine(stim, probeIndexOrder, trialInfo)

    return response

def executeTrial(stimType, attendType, trialInfo): #does a single trial
    print(stimType)
    stim1 = genStimuli()
    probeOrder1 = genProbeOrder()
    stim2 = genStimuli()
    probeOrder2 = genProbeOrder()

    if stimType == 'ColCol':
        showStim(stim1, 'Color', probeOrder1, trialInfo)
        showStim(stim2, 'Color', probeOrder2, trialInfo)
        if attendType == 'First':
            probe(stim1, 'Color', probeOrder1, trialInfo)
        if attendType == 'Second':
            probe(stim2, 'Color', probeOrder2, trialInfo)
        elif attendType == 'Both':
            probe(stim1, 'Color', probeOrder1, trialInfo)
            probe(stim2, 'Color', probeOrder2, trialInfo)
    elif stimType == 'ColLin':
        showStim(stim1, 'Color', probeOrder1, trialInfo)
        showStim(stim2, 'Line', probeOrder2, trialInfo)
        if attendType == 'First':
            probe(stim1, 'Color', probeOrder1, trialInfo)
        if attendType == 'Second':
            probe(stim2, 'Line', probeOrder2, trialInfo)
        elif attendType == 'Both':
            probe(stim1, 'Color', probeOrder1, trialInfo)
            probe(stim2, 'Line', probeOrder2, trialInfo)
    elif stimType == 'LinCol':
        showStim(stim1, 'Line', probeOrder1, trialInfo)
        showStim(stim2, 'Color', probeOrder2, trialInfo)
        if attendType == 'First':
            probe(stim1, 'Line', probeOrder1, trialInfo)
        elif attendType == 'Second':
            probe(stim2, 'Color', probeOrder2, trialInfo)
        elif attendType == 'Both':
            probe(stim1, 'Line', probeOrder1, trialInfo)
            probe(stim2, 'Color', probeOrder2, trialInfo)
    elif stimType == 'LinLin':
        showStim(stim1, 'Line', probeOrder1, trialInfo)
        showStim(stim2, 'Line', probeOrder2, trialInfo)
        if attendType == 'First':
            probe(stim1, 'Line', probeOrder1, trialInfo)
        elif attendType == 'Second':
            probe(stim2, 'Line', probeOrder2, trialInfo)
        elif attendType == 'Both':
            probe(stim1, 'Line', probeOrder1, trialInfo)
            probe(stim2, 'Line', probeOrder2, trialInfo)
    elif stimType == 'Color':
        showStim(stim1, 'Color', probeOrder1, trialInfo)
        probe(stim1, 'Color', probeOrder1, trialInfo)
    elif stimType == 'Line':
        showStim(stim1, 'Line', probeOrder1, trialInfo)
        probe(stim1, 'Line', probeOrder1, trialInfo)


def executeBlock(attendType, blockNumber, blockLength, practice):
    single = False
    if attendType == 'Single':
        single = True

    stimTypeOrder = genStimTypeOrder(single, blockLength)

    trialNumber = 1
    # screenPrompt("Press any key to start")

    for stim in stimTypeOrder:
        screenWait('get ready')
        trialInfo = expclass.Trial(blockNumber, trialNumber, attendType, stim, practice)
        experii.add_trial(trialInfo)
        executeTrial(stim, attendType, trialInfo)
        trialNumber +=1

def executeExample():
    INST = ["WELCOME TO THE MEMORY GAME\n\nWe appreciate your participation. \n\nIn this game, you'll be asked to remember memory items that can be either colored disks or line angles in a circle. They will look like this:\n\n(pay close attention!)",
                "It's important to stay focused on the computer screen throughout the game because as you just saw, shapes will appear and disappear really fast and if you look away, you'll miss them. \n\nResearcher press the designated key to continue",
                "You'll be told to remember either one or two groups of items:\n\t-Remember the one memory set you're shown\n\t-Remember the first memory set of two shown\n\t-Remember the second memory set of two shown\n\t-Remember both memory sets of two shown\n\nResearcher press the designated key to continue",
                "After the memory items, a ring of colors or a black ring will appear. This is how you will indicate your response.\nTo select your response for the highlighted item, move your curser to the ring and select the color, or angle of the item that was there \n\nResearcher press the designated key to continue",
                "Lets try it out, select whatever responses you'd like \n\nResearcher press the designated key to continue",
                "As you can see, the order that you are asked to give your response, is not always left to right. Give your answers for the memory item you remember being in that location.\n\nResearcher press the designated key to continue",
                "Please pay attention to the instructions before you begin each part so you know WHAT to remember \nthe 1st group, the 2nd group, or both groups. \n\nResearcher press the designated key to continue"]

    trialExample = expclass.Trial(0, 0, 'Single' ,'Color')
    index = 0
    for prompt in INST:
        screenPrompt(prompt)
        if index == 0:
            screenWait("get ready")
            trialExample = expclass.Trial(0, 0, 'Single' ,'Color')
            showStim(genStimuli(), 'Color', [0,1,2], trialExample)
            showStim(genStimuli(), 'Line', [0,1,2], trialExample)
        if index == len(INST)-3:
            probe([0,0,0], 'Color', [1,0,2], trialExample)
            probe([0,0,0], 'Line', [0,1], trialExample)
        index+=1




def main():
    executeExample()
    # core.quit()
    screenPrompt("Now we will start a practice round.\n\nPress space to continue")
    blockNumber = 1
    trialsInBlock = 4   # For practice runs
    practice = 'True'

    shape = visual.Rect(win, lineWidth = 0, fillColor = 'yellow', fillColorSpace = 'rgb255', pos = (240,60), size = (230,100))
    screenPrompt("PRACTICE\nYou will be tested on one set of memory items\n\nPress space to start", shape)
    executeBlock("Single", blockNumber, trialsInBlock, practice)
    shape = visual.Rect(win, lineWidth = 0, fillColor = 'yellow', fillColorSpace = 'rgb255', pos = (160,30), size = (210,110))
    screenPrompt("You will be shown two sets of memory items", shape)
    shape = visual.Rect(win, lineWidth = 0, fillColor = 'yellow', fillColorSpace = 'rgb255', pos = (345,35), size = (230,110))
    screenPrompt("PRACTICE\nYou will be tested on the first set of memeory items\n(press space to start)", shape)
    blockNumber+= 1
    executeBlock("First", blockNumber, trialsInBlock, practice)
    shape = visual.Rect(win, lineWidth = 0, fillColor = 'yellow', fillColorSpace = 'rgb255', pos = (-280,-35), size = (420,110))
    screenPrompt("PRACTICE\nYou will be tested on the second set of memory items\n(press space to start)", shape)
    blockNumber+= 1
    executeBlock("Second", blockNumber, trialsInBlock, practice)
    shape = visual.Rect(win, lineWidth = 0, fillColor = 'yellow', fillColorSpace = 'rgb255', pos = (280,33), size = (250,100))
    screenPrompt("PRACTICE\nYou will be tested on both sets of memory items\n(press space to start)", shape)
    blockNumber+= 1
    executeBlock("Both", blockNumber, trialsInBlock, practice)

    screenPrompt("The real experiment will begin now\n(press space to continue)")
    practice = 'False'
    blockNumber = 1
    trialsInBlock = 10   # For real experiment // should be 40

    shape = visual.Rect(win, lineWidth = 0, fillColor = 'yellow', fillColorSpace = 'rgb255', pos = (240,60), size = (230,100))
    screenPrompt("You will be tested on one set of memory items\n(press space to start)", shape)
    executeBlock("Single", blockNumber, trialsInBlock, practice)
    shape = visual.Rect(win, lineWidth = 0, fillColor = 'yellow', fillColorSpace = 'rgb255', pos = (345,65), size = (230,110))
    screenPrompt("You will be tested on the first set of memory items\n(press space to start)", shape)
    blockNumber+= 1
    executeBlock("First", blockNumber, trialsInBlock, practice)
    shape = visual.Rect(win, lineWidth = 0, fillColor = 'yellow', fillColorSpace = 'rgb255', pos = (-280,0), size = (420,110))
    screenPrompt("You will be tested on the second set of memory items\n(press space to start)",shape)
    blockNumber+= 1
    executeBlock("Second", blockNumber, trialsInBlock, practice)
    shape = visual.Rect(win, lineWidth = 0, fillColor = 'yellow', fillColorSpace = 'rgb255', pos = (280,65), size = (250,100))
    screenPrompt("You will be tested on both sets of memory items\n(press space to start)", shape)
    blockNumber+= 1
    executeBlock("Both", blockNumber, trialsInBlock, practice)
    file = open('data.dat', 'wb')
    pickle.dump(experiidata, file)
    file.close()
    readit.makeExcel()
    screenPrompt("You're all done!")

main()
