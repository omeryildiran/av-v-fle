"""
Experiment 1 for the Project: Spatio-Temporal Correlation on Audio Visual Integration Using Flash Lag Effect

Authors: Omer Yildiran and Michael Landy, New York University(NYU)
Experiment Coded by Omer Yildiran, PhD candidate at NYU

Start Date: 09/2024
Last Update: 09/2024

Short outline of the experiment:

Experiment 1:

1- Blank screen with fixation cross(wait for space to start)
2- After a constant short delay(200ms) initiate moving bar
3- Flash AudioVisual bar on upper part of screen but at exactly on same horizontal position as moving bar for 1 frame
4-turn the fixation cross color to red to indicate response phase. Which is right or left indicated flash was leading or laggin
5-repeat the trial N times and vary the horizontal position and timing of AudioVisual stimuli
6-End of the experiment

"""

# Importing Libraries
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, iohub, hardware
import os
from dva_to_pix import arcmin_to_px, dva_to_px
import numpy as np
from numpy.random import choice as randchoice
from numpy.random import random, randint, normal, shuffle, choice as randchoice
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import sys  # to get file system encoding
from psychopy import prefs
from audio_cue import create_stereo_sound, positional_audio
prefs.hardware['audioLib'] = ['pygame']
import psychopy.iohub as io
from psychopy.iohub.util import hideWindow, showWindow
from psychopy.tools.monitorunittools import deg2pix, pix2deg
from psychopy import monitors
from psychopy.hardware import keyboard
import random

"""          Experiment INFO Setup"""
# Store info about the experiment session
psychopyVersion = '2022.2.4'
expName = 'av_v_fle' 
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
}

# Experiment Dialog Box
# dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
# if dlg.OK == False:
#     core.quit()  # user pressed cancel
# expInfo['date'] = data.getDateStr()  # add a simple timestamp
# expInfo['expName'] = expName
# expInfo['psychopyVersion'] = psychopyVersion
# Ensure that relative paths start from the same directory as this script
#_thisDir = os.path.dirname(os.path.abspath(__file__))
#os.chdir(_thisDir)
# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
#filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'],)

#setup screen properties
monitor_options = {
    "asusZenbook14": { "sizeIs": 1024,    "screen_width": 15,   "screen_height": 15,    "screen_distance": 60    },
    "labMon": {  "sizeIs": 1024,        "screen_width": 28,        "screen_height": 28,        "screen_distance": 60    }}
monitorSpecs=monitor_options["asusZenbook14"]
sizeIs=monitorSpecs["sizeIs"] # 1024
screen_width=monitorSpecs["screen_width"] #31 asuSs 14 # actual size of my screen in cm is 28x17
screen_height=monitorSpecs["screen_height"] #28 # 16.5 asus
screen_distance=monitorSpecs["screen_distance"] #60 # 57 asus
# define monitor
myMon=monitors.Monitor('asusMon', width=31, distance=57)
myMon.setSizePix((sizeIs, sizeIs))
selectedMon=myMon
win = visual.Window(size=(sizeIs,sizeIs),
                    fullscr=False,  monitor=myMon, units='pix',  color=[0, 0, 0], useFBO=True, screen=1, colorSpace='rgb')

field_size=[sizeIs,sizeIs]
win.monitor.setWidth(screen_width)
win.monitor.setDistance(screen_distance)

frameRate=win.getActualFrameRate()
print(frameRate)
expInfo['frameRate']=frameRate
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

print(win.size)
def dva2height(dva):
    return dva_to_px(dva, h=screen_height, d=screen_distance, r=sizeIs)/win.size[1]



# Initialize components for Routine "trial"
trialClock = core.Clock()

barColor="black"
barWidth=dva_to_px(size_in_deg=0.15,h=screen_height,d=screen_distance,r=sizeIs)
barHeight=dva_to_px(size_in_deg=0.65,h=screen_height,d=screen_distance,r=sizeIs)
#barWidth=100
moving_bar = visual.Rect(win=win, name='moving_bar',
    width=barWidth, height=barHeight,
    ori=0, pos=(-win.size[1]/2+dva_to_px(1,h=screen_height,d=screen_distance,r=sizeIs), -dva_to_px(1,screen_height,screen_distance,sizeIs)),
    lineWidth=0, lineColor=barColor, lineColorSpace='rgb',
    fillColor=barColor, fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True,units='pix')
burst = sound.Sound('A', secs=0.08, stereo=True, hamming=False,
    name='burst')
burst.setVolume(0.5)


flash = visual.Rect(win=win, name='flash',
    width=barWidth, height=barHeight,
    ori=0, pos=(0, 0),
    lineWidth=0, lineColor=barColor, lineColorSpace='rgb',
    fillColor=barColor, fillColorSpace='rgb',
    opacity=1, depth=-3.0, interpolate=True,units='pix')

# Initialize components for Routine "Response"
ResponseClock = core.Clock()
fixationSize=dva_to_px(size_in_deg=0.1,h=screen_height,d=screen_distance,r=sizeIs)
#print("fixation size is ",fixationSize)
fixation =   visual.Circle(win, radius=fixationSize, fillColor='white',colorSpace='rgb', units='pix',pos=(0, 0))
responseKeys = keyboard.Keyboard()
giveResponseText = visual.TextStim(win=win, text='Press left for flash "Lagging" or right for "Leading" responses', color=[1, 1, 1], units='pix', height=20)

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# Prepare Trial
continueRoutine = True
frameN = -1
win.setMouseVisible(False)    
trialN=0
maxTrials=10
haveRest=False
haveRestText=visual.TextStim(win, text='Press space to continue', color=[1, 1, 1], units='pix', height=20)
haveRestNum=1
space2pass=keyboard.Keyboard()
endExpNow = False  # flag for 'escape' or other condition => quit the exp
mouse = event.Mouse(win=win,visible=False)
frameTolerance = 0.001  # how close to onset before 'same' frame

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-sl€ip) routine 

all_responses=[]
responseTimes=[]
#region [rgba(206, 10, 118, 0.14)]

# Start Routine "trial"
while trialN<maxTrials and not endExpNow:
    tStart = globalClock.getTime()
    _space2pass_allKeys = []
    space2pass.keys = []
    space2pass.clearEvents(eventType='keyboard')
    
    # have a rest screen
    haveRest=True
    while haveRest:
        haveRestText.draw()
        win.flip()
        theseKeys = space2pass.getKeys(keyList=['space'])
        _space2pass_allKeys.extend(theseKeys)
        if len(_space2pass_allKeys)>0:
            haveRest=False

    # Update the trial number
    trialN+=1

    
    win.flip(clearBuffer=True)
    continueRoutine = True
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # # wait for 0.2 second before starting the trial
    waiterTime=0
    while  waiterTime <0.2:
        waiterTime = globalClock.getTime() - tStart
        fixation.draw()
        win.flip()


    # Frames of trial starts here
     # keep track of which components have finished
    trialComponents = [fixation, moving_bar, burst, flash]
    for thisComponent in trialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    t = 0
    flashPos= -win.size[0]/4+dva_to_px(random.uniform(0, 1),h=screen_height,d=screen_distance,r=sizeIs)
    flashPos=random.uniform(-win.size[0]/4,win.size[0]/4)
    """Run Trial Routine"""
    #region [rgba(10, 183, 206, 0.14)]
    while continueRoutine:
        t = trialClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1


        if fixation.status == NOT_STARTED and t >= 0.0-frameTolerance:
            fixation.frameNStart = frameN
            fixation.tStart = t
            fixation.tStartRefresh = tThisFlipGlobal
            win.timeOnFlip(fixation, 'tStartRefresh')
            fixation.setAutoDraw(True)


        # initiate moving bar at the left edge of the screen
        if moving_bar.status == NOT_STARTED and t >= 0.0-frameTolerance:
            #moving_bar.pos = [-field_size[0]/2, 0]
            moving_bar.frameNStart = frameN # exact frame index
            moving_bar.tStart = t # local t and not account for scr refresh
            moving_bar.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(moving_bar, 'tStartRefresh')  # time at next scr refresh
            moving_bar.setAutoDraw(True)

        if moving_bar.status == STARTED and moving_bar.pos[0] < field_size[0]/2:
            moving_bar.pos = [moving_bar.pos[0]+dva_to_px(0.15), moving_bar.pos[1]]
            moving_bar.draw()
            win.flip()
        elif moving_bar.status == STARTED and moving_bar.pos[0] >= field_size[0]/2:
            moving_bar.setAutoDraw(False)
            continueRoutine=False

        # initiate audio cue and flash when moving bar is at the center of the screen
        if burst.status == NOT_STARTED and moving_bar.pos[0] > flashPos and t >= 0.0-frameTolerance:
            burst.frameNStart = frameN
            burst.tStart = t
            burst.tStartRefresh = tThisFlipGlobal
            win.timeOnFlip(burst, 'tStartRefresh')
            burst.play(when=win)  # sync with win flip
            burst.status = STARTED

        # if burst.status == STARTED and frameN >= (burst.frameNStart + 1):
        #     burst.stop()

        if flash.status == NOT_STARTED and moving_bar.pos[0] >= flashPos and t >= 0.0-frameTolerance:
            flash.pos = [flashPos, dva_to_px(1,h=screen_height,d=screen_distance,r=sizeIs)]
            flash.frameNStart = frameN
            flash.tStart = t
            flash.tStartRefresh = tThisFlipGlobal
            win.timeOnFlip(flash, 'tStartRefresh')
            flash.setAutoDraw(True)

        if flash.status == STARTED and frameN >= (flash.frameNStart + 1):
            flash.setAutoDraw(False)

        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

    # ending routine "trial"
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    win.flip()

    #endregion
    
    #region [rgba(88, 206, 10, 0.14)]
    # prepare to start Routine Response
    fixation.color='red'
    fixation.draw()
    win.flip()
    continueRoutine = True

    responseClock = core.Clock()
    responseComponents = [fixation, responseKeys, giveResponseText]
    for thisComponent in responseComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    t = 0
    frameN = -1

    """Run Response Routine"""
    # -- run the response routine
    waitResponse = True
    timerResponse=core.Clock()
    t = timerResponse.getTime()
    tResponseStart=t
    while waitResponse:
        tThisFlip = win.getFutureFlipTime(clock=timerResponse)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        fixation.setAutoDraw(True)
        giveResponseText.setAutoDraw(True)
        theseKeys = responseKeys.getKeys(keyList=['left', 'right'], waitRelease=True)
        t = timerResponse.getTime()

        if len(theseKeys):
            waitResponse = False
            # record
            #all_responses.append(theseKeys[-1].name)
            if theseKeys[-1].name == 'left':
                all_responses.append(0)
            elif theseKeys[-1].name == 'right':
                all_responses.append(1) # 0 for lagging, 1 for leading
            # record time of response since the start of the response phase
            tRespEnd=timerResponse.getTime()
            responseTimes.append(tRespEnd-tResponseStart)
            
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        # refresh the screen
        if waitResponse:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
            
    # ending routine "Response"
    for thisComponent in responseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    fixation.color='white'
    # endregion


# end experiment
# endregion



    
    




            
            
        





