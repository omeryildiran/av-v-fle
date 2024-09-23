        if responseKeys.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            responseKeys.frameNStart = frameN  # exact frame index
            responseKeys.tStart = t  # local t and not account for scr refresh
            responseKeys.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(responseKeys, 'tStartRefresh')  # time at next scr refresh
            responseKeys.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(responseKeys.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(responseKeys.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if responseKeys.status == STARTED and not waitOnFlip:
            theseKeys = responseKeys.getKeys(keyList=['right', 'left'], waitRelease=True)
            if len(theseKeys):
                if theseKeys[-1].name in ['right', 'left']:
                    responseKeys.keys = theseKeys[-1].name  # just the last key pressed
                    responseKeys.rt = theseKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False