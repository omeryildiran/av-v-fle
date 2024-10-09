"""
Experiment 1 for the Project: Spatio-Temporal Correlation on Audio Visual Integration Using Flash Lag Effect

Authors: Omer Yildiran and Michael Landy, New York University(NYU)
Experiment Coded by Omer Yildiran, PhD candidate at NYU

Start Date: 09/2024
Last Update: 09/2024

Short outline of the experiment:

Experiment 1:

1- Blank screen with fixation cross(wait for space to start)
2- After a constant short delay(200ms) initiate moving bars
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
import psychopy.iohub as io
from psychopy.iohub.util import hideWindow, showWindow
from psychopy.tools.monitorunittools import deg2pix, pix2deg
from psychopy import monitors
from psychopy.hardware import keyboard
import random
from create_conditions_time_delay import TimingGenerator
import scipy.io as sio
import pandas as pd



timing_generator = TimingGenerator( trial_per_condition=10)
audioDelays, visualDelays = timing_generator.generate_audio_visual_delays()
incidentPoints = timing_generator.generate_incident_times()
initialBarSide = timing_generator.initial_bar_side()


# Set the audio library to pyo
prefs.hardware['audioLib'] = ['sounddevice']

"""          Experiment INFO Setup"""
# Store info about the experiment se ssion
psychopyVersion = '2022.2.4'
expName = 'av_v_fle' 
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
}


""" Dialog Box for Experiment Info"""
# dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
# if dlg.OK == False:
#       core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
# expInfo['expName'] = expName
# expInfo['psychopyVersion'] = psychopyVersion
# Ens ure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data\%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'],)

#setup screen properties
monitor_options = {
    "asusZenbook14": { "sizeIs": 1024,    "screen_width": 30.5,   "screen_height": 18,    "screen_distance": 60    },
    "labMon": {  "sizeIs": 1024,        "screen_width": 28,        "screen_height": 28,        "screen_distance": 60    }}
monitorSpecs=monitor_options["asusZenbook14"]
sizeIs=monitorSpecs["sizeIs"] # 1024
screen_width=monitorSpecs["screen_width"] #31 asuSs 14 # actual size of my screen in cm is 28x17
screen_height=monitorSpecs["screen_height"] #28 # 16.5 asus
screen_distance=monitorSpecs["screen_distance"] #60 # 57 asus
# define monitor
myMon=monitors.Monitor('asusMon', width=screen_width, distance=57)
#myMon.setSizePix((sizeIs, sizeIs))
selectedMon=myMon
win = visual.Window(size=(sizeIs,sizeIs),
                    fullscr=True,  monitor=myMon, units='pix',  color="black", useFBO=True, screen=1, colorSpace='rgb')
exp = data.ExperimentHandler(name="av_v_fle",version='0.1.0')


win.monitor.setWidth(screen_width)
win.monitor.setDistance(screen_distance)

refreshRate=win.getActualFrameRate()
expInfo['frameRate']=refreshRate
if expInfo['frameRate']!= None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# print(win.size)
def dva2height(dva):
    return dva_to_px(dva, h=screen_height, d=screen_distance, r=sizeIs)/win.size[1]
print(refreshRate)
print("refresh rate is", refreshRate)
frameDur=1/refreshRate
print("frame dur is", frameDur)


# Initialize components for Routine "trial"
trialClock = core.Clock()

barColor="red"
barWidth=dva_to_px(size_in_deg=0.2,h=screen_height,d=screen_distance,r=sizeIs)
barHeight=dva_to_px(size_in_deg=0.7,h=screen_height,d=screen_distance,r=sizeIs)
#barWidth=100

horizontalOffset=dva_to_px(3,h=screen_height,d=screen_distance,r=sizeIs)
movingBarYPos=-dva_to_px(0.5,screen_height,screen_distance,sizeIs)

moving_bar = visual.Rect(win=win, name='moving_bar',
    width=barWidth, height=barHeight,
    ori=0, pos=(-win.size[1]/2, movingBarYPos),
    lineWidth=0, lineColor=barColor, lineColorSpace='rgb',
    fillColor=barColor, fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True,units='pix')
burst = sound.Sound('A', secs=0.08, stereo=True, hamming=False,
    name='burst')
burst.setVolume(0.5)

flashColor="green"
flash = visual.Rect(win=win, name='flash',
    width=barWidth, height=barHeight,
    ori=0, pos=(0, 0),
    lineWidth=0, lineColor=flashColor, lineColorSpace='rgb',
    fillColor=flashColor, fillColorSpace='rgb',
    opacity=1, depth=-3.0, interpolate=True,units='pix')

# Initialize components for Routine "Response"
ResponseClock = core.Clock()
fixationSize=dva_to_px(size_in_deg=0.1,h=screen_height,d=screen_distance,r=sizeIs)
#print("fixation size is ",fixationSize)
fixation = visual.Circle(win, radius=fixationSize, fillColor=None, lineColor='white', colorSpace='rgb', units='pix',
                        pos=(0, -dva_to_px(3,screen_height,screen_distance,sizeIs)))
giveResponseText = visual.TextStim(win=win, text='Press left for flash "Lagging" or right for "Leading" responses', color=[1, 1, 1], units='pix', height=20)

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# Prepare Trial
continueRoutine = True
frameN = -1
win.setMouseVisible(False)    
trialN=0
maxTrials=3
haveRest=True
haveRestText=visual.TextStim(win, text='Press space to continue', color=[1, 1, 1], units='pix', height=20)
haveRestNum=1
space2pass=keyboard.Keyboard()
endExpNow = False  # flag for 'escape' or other condition => quit the exp
mouse = event.Mouse(win=win,visible=False)
frameTolerance = 0.001  # how close to onset before 'same' frame

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
phaseTimer = core.Clock()  # to track time remaining of each (possibly non-sl€ip) routine 

responseKeys = keyboard.Keyboard(backend='iohub')
all_responses=[]
responseTimes=[]
totalDistance=win.size[1]-horizontalOffset*2

## Save the data
incident_imes=[]
audio_delays=[]
visual_delays=[]
trial_durs=[]
audioTime=[]
flashTime=[]
incidentTimes=[]
trialNum=[]
flashPostionX=[]
bar_at_flash_X=[]
directions=[]
maxTrials=len(visualDelays-1)
#region [rgba(206, 10, 118, 0.14)]
# Start Routine "trial"
while trialN<maxTrials and not endExpNow:
    trialNum.append(trialN+1)
    _space2pass_allKeys = []
    space2pass.keys = []
    space2pass.clearEvents(eventType='keyboard')
    print(incidentPoints[trialN])
    incidentTime=incidentPoints[trialN]/1000 # ms to s
    incidentFrame=int(incidentTime*refreshRate)
    # have a rest screen
    if trialN%20==0 and trialN>0:
        haveRestText.text=f'End of {haveRestNum} trials. Press space to continue'
        haveRestNum+=1
        haveRest=True
    while haveRest:
        haveRestText.draw()
        win.flip()
        theseKeys = space2pass.getKeys(keyList=['space'])
        _space2pass_allKeys.extend(theseKeys)
        if len(_space2pass_allKeys)>0:
            haveRest=False


    win.flip(clearBuffer=True)
    continueRoutine = True
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    tStart = globalClock.getTime()
    # # wait for 0.3 second before starting the trial
    waiterTime=0
    while  waiterTime <0.3:
        waiterTime = globalClock.getTime() - tStart
        #fixation.draw()
        win.flip()

    # keep track of which components have finished
    trialComponents = [fixation, moving_bar, burst, flash]
    for thisComponent in trialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # Add a short delay before starting the trial
    #core.wait(0.1)

    # Set the initial position of the moving bar dependent on the trial
    sideBar=initialBarSide[trialN]# 1 for right, -1 for left
    directions.append(-1*sideBar)
    movingBarXPos0=sideBar*(win.size[1]/2-horizontalOffset)# if sideBar is -1, moving bar starts from the left edge of the screen vice-versa
    moving_bar.pos = [movingBarXPos0,movingBarYPos]
    flash.pos[0] = movingBarXPos0
    flash.pos[1]=dva_to_px(0.5,h=screen_height,d=screen_distance,r=sizeIs)

    # Define the speed of the bar in pixels per second
    speed = -1*sideBar*dva_to_px(0.16)  # Adjust this value as needed
    totalDur=abs(totalDistance/(speed*60))
    print("total dur",totalDur)
    #print(speed)
    clock = core.Clock()
    # Track the last frame time
    last_frame_time = clock.getTime()
    fixation.color='white'
    inicdentON=False
    """Run Trial Routine"""
    #region [rgba(10, 183, 206, 0.14)]
    # print("incident happens at frame ", incidentFrame)
    trialStart = globalClock.getTime()
    trialClock.reset()
    # print("audio delays", audioDelays[trialN])
    # print("visual delays", visualDelays[trialN])
    # print("incident time", incidentTime)
    incidentTimes.append(incidentTime)
    

    if visualDelays[trialN]<0:
        flash.pos[0] =flash.pos[0] + -1*visualDelays[trialN]*speed
    elif visualDelays[trialN]>0:
        flash.pos[0] =flash.pos[0] + -1*visualDelays[trialN]*speed
    while continueRoutine:
        t = trialClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=phaseTimer)
        frameN = frameN + 1
        



        current_time = clock.getTime() # current time in seconds
        delta_time=current_time-last_frame_time # time elapsed since the last frame
        last_frame_time = current_time # update the last frame time

        #fixation.setAutoDraw(True)   # initiate fixation cross at the center of the screen
        # initiate moving bar at the left edge of the screen
        if moving_bar.status == NOT_STARTED and t >= 0.0-frameTolerance:
            moving_bar.tStart = t # local t and not account for scr refresh
            win.timeOnFlip(moving_bar, 'tStartRefresh')  # time at next scr refresh
            moving_bar.setAutoDraw(True)

        if moving_bar.status == STARTED and t < (moving_bar.tStart + totalDur-frameTolerance):
            # moving bar moves to the right edge of the screen
            new_pos_x = moving_bar.pos[0] + speed * delta_time * 60
            moving_bar.pos = [new_pos_x, moving_bar.pos[1]]

            # if frameN <= incidentFrame+visualDelays[trialN]:
            #     flash_pos_x=flash.pos[0] + speed * delta_time * 60
            #     flash.pos = [new_pos_x, flash.pos[1]]
            # elif frameN == incidentFrame:
            #     bar_at_flash_X.append(moving_bar.pos[0])



        elif t>=totalDur-frameTolerance:#moving_bar.pos[0] >= field_size[0]/2-horizontalOffset:
            trial_durs.append(totalDur)
            continueRoutine=False

        if flash.status == NOT_STARTED and frameN <= (incidentFrame):
            flash_pos_x=flash.pos[0] + speed * delta_time * 60
            flash.pos = [flash_pos_x, flash.pos[1]]
            if frameN == incidentFrame:
                bar_at_flash_X.append(moving_bar.pos[0])

                flash.frameNStart=frameN
                flash.tStart = t
                #print("flashed at time ", flash.tStart)
                win.timeOnFlip(flash, 'tStartRefresh')
                flash.draw()
                flashTime.append(flash.tStart)
                flashPostionX.append(flash.pos[0])


        # initiate audio cue and flash when moving bar is at the center of the screen
        if burst.status == NOT_STARTED and frameN == incidentFrame+visualDelays[trialN]+audioDelays[trialN]:
            burst.tStart = t
            #print("bursted at time ", burst.tStart)
            win.timeOnFlip(burst, 'tStartRefresh')
            burst.play(when=win)  # sync with win flip
            burst.status = STARTED
            audioTime.append(burst.tStart)

        # Flip the screen to show the moving bar after all the components are drawn
        #if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            endExpNow=True
            all_responses.append(999)
            responseTimes.append(999)
            trialN-=1
            break
    # ending routine "trial"
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Update the trial number
    trialN+=1
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    phaseTimer.reset()
    win.flip()
    trialEnd = globalClock.getTime()
    print("Trial duration is ", trialEnd-trialStart)
    #endregion
    # wait for 0.2 second before starting the response phase
    #co re.wait(0.10)

    #region [rgba(88, 206, 10, 0.14)]
    # prepare to start Routine Response
    fixation.color='red'
    #fixation.draw()
    win.flip()
    # set response keys to null before starting the response phase
    responseKeys.clearEvents()

    responseClock = core.Clock()
    responseComponents = [fixation, responseKeys, giveResponseText]
    for thisComponent in responseComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    """Run Response Routine"""
    # Clear the event buffer before entering the waitResponse phase
    event.clearEvents(eventType='keyboard')
    responseKeys.keys = []
    responseKeys.rt = []

    # -- run the response routine
    waitResponse = True
    t = phaseTimer.getTime()
    tResponseStart=t

    while waitResponse and not endExpNow:
        tThisFlip = win.getFutureFlipTime(clock=phaseTimer)
        #fixation.setAutoDraw(True)
        giveResponseText.setAutoDraw(True)
        giveResponseText.pos = [0, -dva_to_px(1,h=screen_height,d=screen_distance,r=sizeIs)]
        response = responseKeys.getKeys(keyList=['up', 'down'], waitRelease=True)
        t = phaseTimer.getTime()

        if len(response)>0:
            waitResponse = False
            #all_responses.append(theseKeys[-1].name)
            
            if response[-1].name == 'up': # 1 up for leading
                all_responses.append(1)
            elif response[-1].name == 'down': # 0 down for lagging
                all_responses.append(0) # 0 for lagging, 1 for leading
            # record time of response since the start of the response phase
            tRespEnd=phaseTimer.getTime()
            responseTimes.append(tRespEnd-tResponseStart)
        else:
            waitResponse = True
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):

            endExpNow=True
            
            
        # refresh the screen
        if waitResponse:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
            
    # ending routine "Response"
    for thisComponent in responseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
                    # save the data to .mat file    
            sio.savemat(filename+".mat", {'responses':all_responses, 'responseTimes':responseTimes, 'incidentTimesAimed':incidentTimes,
                            'audioDelaysAimed':audioDelays[:trialN], 'visualDelaysAimed':visualDelays[:trialN],
                            'trialDurations':trial_durs,
                            'audioTime':audioTime, 'flashTime':flashTime, 'trialNum':trialNum,
                            'flashPostionX':flashPostionX, 'bar_at_flash_X':bar_at_flash_X, 'directions':directions})
    #fixation.setAutoDraw(False)

    # the Routine "Response" was not non-slip safe, so reset the non-slip timer
    phaseTimer.reset()
    # endregion

    #end region
    # End of Screen Space to End the experiment

while True:
    haveRestText.text='End of the Experiment'
    haveRestText.setAutoDraw(True)
    win.flip()
    if defaultKeyboard.getKeys(keyList=["space"]):
        endExpNow=True
        # # save the data
        
        
        # Zip the arrays to the shortest length
        zipped_data = list(zip(all_responses, responseTimes, incidentTimes, audioDelays[:trialN], visualDelays[:trialN], trial_durs, audioTime, flashTime, trialNum, flashPostionX, bar_at_flash_X, directions))
        # Unzip the data back into individual lists
        all_responses, responseTimes, incidentTimes, audioDelays, visualDelays, trial_durs, audioTime, flashTime, trialNum,  flashPostionX, bar_at_flash_X, directions= map(list, zip(*zipped_data))
  

        # save the data to .mat file    
        sio.savemat(filename+".mat", {'responses':all_responses, 'responseTimes':responseTimes, 'incidentTimesAimed':incidentTimes,
                            'audioDelaysAimed':audioDelays[:trialN], 'visualDelaysAimed':visualDelays[:trialN],
                            'trialDurations':trial_durs,
                            'audioTime':audioTime, 'flashTime':flashTime, 'trialNum':trialNum,
                            'flashPostionX':flashPostionX, 'bar_at_flash_X':bar_at_flash_X, 'directions':directions})
        # savemat(filename, {'responses':responses, 'responseTimes':responseTimes, 'incidentTimes':incidentTimes, 'audioDelays':audioDelays, 'visualDelays':visualDelays})
      
      

        # also create a csv file
        # first create a dataframe
        df=pd.DataFrame({'responses':all_responses, 'responseTimes':responseTimes, 'incidentTimesAimed':incidentTimes,
                           'audioDelaysAimed':audioDelays[:trialN], 'visualDelaysAimed':visualDelays[:trialN],
                            'trialDurations':trial_durs,
                            'audioTime':audioTime, 'flashTime':flashTime, 'trialNum':trialNum,
                            'flashPostionX':flashPostionX, 'bar_at_flash_X':bar_at_flash_X, 'directions':directions})
        print(df[incident_imes])
        # if the data file csv not exist, create it
        if not os.path.exists(filename+".csv"):
            # create a csv file
            with open(filename+".csv", 'w') as f:
                df.to_csv(f)

        # save the dataframe to a csv
        df.to_csv(filename+".csv")


        win.close()
        core.quit()
    #endregion

    


# end experiment
# endregion



    
    




            
            
        






