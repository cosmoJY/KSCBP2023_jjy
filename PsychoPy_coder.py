# [인지및생물2023] 자극 제시 프로그램의 처리 지연에 따른 순간 제시 정확성 비교
# Copyright 2023. 정지연. All rights reserved.
# 문의: word3276@gmail.com

# PsychoPy 2022.2.4 & Python 3.8
# 절차: 입력창에 파라미터 입력 > 스크린이 켜지면 스페이스바 > 자극 제시(기본 16.7 ms) > 반복 횟수가 끝나면 자동 종료
# 프로그램 측정 데이터파일 경로: [result] 폴더
#            데이터파일 변인명: 1. ID  2. 시행번호  3. 코드: while[1]/개발자[2] 4. 지연요소: 없음[0]/키입력직후[1]/반복문[2]
#                          5. 자극 제시시간(이상ideal)  6. 자극 제시시간(프로그램)  7. 검은화면 제시시간(프로그램)

## 초기 설정
from psychopy import visual, core, event, data, gui, logging, monitors, tools, parallel #import some libraries from PsychoPy
from psychopy.hardware import keyboard
from psychopy.tools import colorspacetools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray, arctan
from numpy.random import random, randint, normal, shuffle
import random
import os #handy system and path functions
import glob # Filename globbing utility.
from PIL import Image # Get the size(demension) of an images 
logging.console.setLevel(logging.CRITICAL)  # 자잘한 경고문 숨기기
# =====================================================================================================

## 자극 파라미터 설정
screenNumber = 0;       # 모니터 스크린 번호
nrepeat = 10            # 반복 횟수

target_t = 1/60         # 자극 제시시간[기본값: 16.7 ms = 60 Hz 모니터 기준 1프레임]
mask_t = 3/60           # 검은 화면 제시시간
blank_t0 = 3/60         # 키 입력과 자극 제시 사이 시간 간격
monitor_inch = 24; distance_cm = 70; monitorX = 1920; monitorY = 1080;      # 모니터 정보

## 입력창 제시
expName = 'Input'
expInfo = {
    'ID[아무숫자]': '',
    '코드: while[1]/개발자[2]': '',
    '지연요소: 없음[0]/키입력직후[1]/반복문[2]' : '',
    'Refresh rate(Hz): 예시[60]': ''
} 
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
participant = int(expInfo['ID[아무숫자]'])
whilewhen = int(expInfo['코드: while[1]/개발자[2]'])
delay = int(expInfo['지연요소: 없음[0]/키입력직후[1]/반복문[2]'])
hz = int(expInfo['Refresh rate(Hz): 예시[60]'])

if delay != 1:
    blank_t = blank_t0
else:
    blank_t = 0
  
if whilewhen == 2 & delay == 2:
    print('개발자 코드 & 지연요소 반복문 조합은 불가능합니다.')
    core.quit()

## PsychoPy 스크린 설정 
bgColorRGB = [255,255,255]

# create a window
win = visual.Window([monitorX, monitorY], screen = screenNumber, fullscr = 'bool', units='pix', color = bgColorRGB, colorSpace = 'rgb255', multiSample = False)   # anti-aliasing (multiSample = True, numSamples = 16)  # fullscr = 'bool',
win.mouseVisible = False

centerx = 0; centery = 0; location = 2
txtloc_y = centery + 350

slack = 1/hz/2
frameTolerance = 0.001  # how close to onset before 'same' frame

waitClock = core.Clock()
key_resp = keyboard.Keyboard(backend='ptb')
blankClock = core.Clock()
ptargetClock = core.Clock()
pmaskClock = core.Clock()
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

## 자극 이미지 설정
targetName = 'stim/900x600_25_100000.jpg'

if delay != 2:
    target = visual.ImageStim(win, image = targetName, size = (900, 600), pos = (centerx, centery), units = "pix")
mask = visual.ImageStim(win, image = "stim/900x600_Black.jpg", size = (900, 600), pos = (centerx, centery), units = "pix")

## 자극 제시 시작
timestamp = np.empty((0, 7), int)
for t in range(0, nrepeat):
    tcurrent = t
    if whilewhen == 1: # while문
        text = visual.TextStim(win, text= 'psychopy(while)' +  str(round(target_t*1000)) + '_' + str(t), pos = (centerx, txtloc_y), units = 'pix', height = 30, color = 'black', bold = False)
        win.flip()
        # 키 응답 대기
        kb = keyboard.Keyboard(backend='ptb')
        kb.waitKeys(waitRelease=False)
        # 빈 화면
        clock_b = core.Clock() # 빈 화면 제시 시작시점
        while clock_b.getTime() < blank_t - slack:
            win.flip()
        # 자극
        clock = core.Clock() # 자극 제시 시작시점
        while clock.getTime() < target_t - slack:
            if delay == 2:
                target = visual.ImageStim(win, image = targetName, size = (900, 600), pos = (centerx, centery), units = "pix")
            target.draw(); text.draw()
            win.flip()
        target_realtime = clock.getTime()
        # 검은 화면
        clock_m = core.Clock() # 자극 제시 종료시점 = 검은 화면 시작시점
        while clock_m.getTime() < mask_t - slack:
            mask.draw(); text.draw()
            win.flip()
        mask_realtime = clock_m.getTime()
    if whilewhen == 2: # 개발자 코드(Builder에서 발췌)
        text = visual.TextStim(win, text= 'psychopy(when)' + str(round(target_t*1000)) + '_' + str(tcurrent), pos = (centerx, txtloc_y), units = 'pix', height = 30, color = 'black', bold = False)
        # 키 응답 대기 
        # ------Prepare to start Routine "wait"-------
        continueRoutine = True
        # update component parameters for each repeat
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # keep track of which components have finished
        waitComponents = [key_resp]
        for thisComponent in waitComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        ttime = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        waitClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        # -------Run Routine "wait"-------
        while continueRoutine:
            # get current time
            t = waitClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=waitClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # *key_resp* updates
            waitOnFlip = False
            if key_resp.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                key_resp.frameNStart = frameN  # exact frame index
                key_resp.tStart = ttime  # local t and not account for scr refresh
                key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp.status == STARTED and not waitOnFlip:
                theseKeys = key_resp.getKeys(keyList=['space'], waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                    key_resp.rt = _key_resp_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in waitComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        # -------Ending Routine "wait"-------
        for thisComponent in waitComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "wait" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # 빈 화면 
        # ------Prepare to start Routine "blank"-------
        continueRoutine = True
        routineTimer.add(blank_t)
        # reset timers
        ttime = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        blankClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        # -------Run Routine "blank"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            ttime = blankClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=blankClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # -------Ending Routine "blank"-------
        routineTimer.reset()
        
        # 자극
        # ------Prepare to start Routine "ptarget"-------
        continueRoutine = True
        # update component parameters for each repeat
            # keep track of which components have finished
        ptargetComponents = [target, text]
        for thisComponent in ptargetComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        ttime = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        ptargetClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        # -------Run Routine "ptarget"-------
        while continueRoutine:
            # get current time
            ttime = ptargetClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=ptargetClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *target* updates
            if target.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                target.frameNStart = frameN  # exact frame index
                target.tStart = ttime  # local t and not account for scr refresh
                target.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(target, 'tStartRefresh')  # time at next scr refresh
                target.setAutoDraw(True)
            if target.status == STARTED:
                if tThisFlipGlobal > target.tStartRefresh + target_t-frameTolerance:
                    # keep track of stop time/frame for later
                    target.tStop = ttime  # not accounting for scr refresh
                    target.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(target, 'tStopRefresh')  # time at next scr refresh
                    target.setAutoDraw(False) 
                     
            # *text* updates
            if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text.frameNStart = frameN  # exact frame index
                text.tStart = ttime  # local t and not account for scr refresh
                text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
                text.setAutoDraw(True)
            if text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > text.tStartRefresh + target_t-frameTolerance:
                    # keep track of stop time/frame for later
                    text.tStop = ttime  # not accounting for scr refresh
                    text.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(text, 'tStopRefresh')  # time at next scr refresh
                    text.setAutoDraw(False)
                    
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in ptargetComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        # -------Ending Routine "ptarget"-------
        for thisComponent in ptargetComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        target_realtime = tThisFlipGlobal - target.tStartRefresh # ptargetClock.getTime()
        # the Routine "ptarget" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # 검은 화면 
        # ------Prepare to start Routine "pmask"-------
        continueRoutine = True
        routineTimer.add(mask_t)
        text_2 = text
        # keep track of which components have finished
        pmaskComponents = [mask, text_2]
        for thisComponent in pmaskComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        ttime = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        pmaskClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        # -------Run Routine "pmask"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            ttime = pmaskClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=pmaskClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # *mask* updates
            if mask.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                mask.frameNStart = frameN  # exact frame index
                mask.tStart = ttime  # local t and not account for scr refresh
                mask.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(mask, 'tStartRefresh')  # time at next scr refresh
                mask.setAutoDraw(True)
            if mask.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > mask.tStartRefresh + mask_t-frameTolerance:
                    # keep track of stop time/frame for later
                    mask.tStop = ttime  # not accounting for scr refresh
                    mask.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(mask, 'tStopRefresh')  # time at next scr refresh
                    mask.setAutoDraw(False)
            # *text_2* updates
            if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text_2.frameNStart = frameN  # exact frame index
                text_2.tStart = ttime  # local t and not account for scr refresh
                text_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
                text_2.setAutoDraw(True)
            if text_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > text_2.tStartRefresh + mask_t-frameTolerance:
                    # keep track of stop time/frame for later
                    text_2.tStop = ttime  # not accounting for scr refresh
                    text_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(text_2, 'tStopRefresh')  # time at next scr refresh
                    text_2.setAutoDraw(False)
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in pmaskComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        # -------Ending Routine "pmask"-------
        for thisComponent in pmaskComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        mask_realtime = tThisFlipGlobal - mask.tStartRefresh  #pmaskClock.getTime()
    timestamp  = np.append(timestamp, np.array([[participant, tcurrent, whilewhen, delay, target_t, target_realtime, mask_realtime]]), axis = 0);  # 행 추가

## 프로그램 측정 데이터파일 저장 후 종료
dataFileName='result' + os.path.sep + 'PsychoPy(Coder)_' + str(participant) + '_' + str(whilewhen) + '_' + str(delay) + '_' + str(round(target_t*1000)) + '_' + data.getDateStr() + '.txt'
np.savetxt(dataFileName, timestamp, delimiter='\t', fmt='%f')
core.quit()
