% [인지및생물2023] 자극 제시 프로그램의 처리 지연에 따른 순간 제시 정확성 비교
% Copyright 2023. 정지연. All rights reserved.
% 문의: word3276@gmail.com

% MATLAB R2022b & Psychtoolbox 3.0.18
% 절차: 입력창에 파라미터 입력 > 스크린이 켜지면 스페이스바 > 자극 제시(기본 16.7 ms) > 반복 횟수가 끝나면 자동 종료
% 프로그램 측정 데이터파일 경로: [result] 폴더
%            데이터파일 변인명: 1. ID  2. 시행번호  3. 코드: while[1]/개발자[2] 4. 지연요소: 없음[0]/키입력직후[1]/반복문[2]
%                          5. 자극 제시시간(이상ideal)  6. 자극 제시시간(프로그램)  7. 검은화면 제시시간(프로그램)
             
%% 초기화
sca; 
close all;
clearvars;

%% 자극 파라미터 설정
rng('shuffle', 'twister');
screenNumber = 0;       % 모니터 스크린 번호
issynctest = 0;         % PTB3 싱크테스트 여부 [0: 진행(권장), 1: 조건부 진행, 2: 미진행]            
nrepeat = 10;           % 반복 횟수

target_t = 1/60;        % 자극 제시시간[기본값: 16.7 ms = 60 Hz 모니터 기준 1프레임]
mask_t = 3/60;          % 검은 화면 제시시간
blank_t0 = 3/60;        % 키 입력과 자극 제시 사이 시간 간격

%% 입력창 제시
prompt = {'ID[아무숫자]: ', '코드: while[1]/개발자[2]', '지연요소: 없음[0]/키입력직후[1]/반복문[2]'};
dlgtitle = 'Input';
dims = [1 50];
definput = {'', '', ''};
answer = inputdlg(prompt, dlgtitle, dims, definput);

participant = str2double(answer{1, 1});
whilewhen = str2double(answer{2, 1});
delay = str2double(answer{3, 1});

if delay == 2 && whilewhen == 2
   error('개발자 코드 & 지연요소 반복문 조합은 불가능합니다.');
end

if delay ~= 1
    blank_t = blank_t0;
else
    blank_t = 0;
end

%% PTB3 스크린 설정
Screen('Preference','SkipSyncTests', issynctest);
Screen('Preference','TextRenderer', 0);

% Response keys settings
KbName('UnifyKeyNames');
esc = KbName('ESCAPE');
enter = KbName('return'); space = KbName('Space');
upkey = KbName('UpArrow'); downkey = KbName('DownArrow'); rightkey = KbName('RightArrow'); leftkey = KbName('LeftArrow');
qkey = KbName('q'); okey = KbName('o');
key1 = KbName('1!'); key2 = KbName('2@'); key3 = KbName('3#'); key4 = KbName('4$'); key5 = KbName('5%');
key6 = KbName('6^'); key7 = KbName('7&'); key8 = KbName('8*'); key9 = KbName('9('); key0 = KbName('0)');

% color -------------------------------------------------------------------
black = [0 0 0]; white = [255 255 255];

% 윈도우 열기 --------------------------------------------------------
[win, rect]=Screen('OpenWindow', screenNumber, white, [], [], [], [], 0);
SetMouse(rect(3), rect(4));        % 마우스 커서 오른쪽+아래쪽 끝으로 이동
slack = Screen('GetFlipInterval', win)/2;

%% 프로그램 측정 데이터파일 설정
nowtime = fix(clock);
nowdate_txt = sprintf('%4d%02d%02d_%02d%02d%02d', nowtime(1), nowtime(2), nowtime(3), nowtime(4), nowtime(5), nowtime(6));
fileName0 = strcat('result/matlab', num2str(participant), '_', num2str(whilewhen), '_', num2str(delay), '_', num2str(round(target_t*1000)), '_', nowdate_txt, '.txt');

%% 자극 이미지 설정
imgloc = round(CenterRectOnPointd([0 0 900 600], rect(3)/2, rect(4)/2));
txtloc_y = imgloc(2)-50;

targetName = strcat('stim/900x600_25_100000.jpg');

if delay ~= 2
    target = imread(targetName);
    target_tex = Screen('MakeTexture', win, target);
end
mask = imread('stim/900x600_Black.jpg');
mask_tex = Screen('MakeTexture', win, mask);

%% 자극 제시 시작
timestamp = [];
for t = 1:nrepeat
    if whilewhen == 1 % While문
        txt = strcat('ptb(while)', num2str(round(target_t*1000)), '_', num2str(t));

        % 키 응답 대기
        KbQueueCreate;
        KbQueueStart;
        while true
            [pressed, firstPress, firstRelease, lastPress, lastRelease] = KbQueueCheck; 
            if pressed
                if firstPress(esc)
                    Screen('Close', win);
                elseif firstPress(space)
                    break;
                end
            end
        end
        KbQueueStop;
        KbQueueRelease;

        % 빈 화면
        blank_onset = GetSecs; % 빈 화면 제시 시작시점
        while GetSecs - blank_onset < blank_t - slack
            Screen('Flip', win);
        end

        % 자극
        target_onset = GetSecs; % 자극 제시 시작시점
        while GetSecs - target_onset < target_t - slack
            if delay == 2
                target = imread(targetName);
                target_tex = Screen('MakeTexture', win, target);
            end

            DrawFormattedText(win, txt, 'center', txtloc_y, black);
            Screen('DrawTexture', win, target_tex, [], imgloc);
            Screen('Flip', win);
        end

        % 검은 화면
        mask_onset = GetSecs; % 자극 제시 종료시점 = 검은 화면 시작시점
        while GetSecs - mask_onset < mask_t - slack
            DrawFormattedText(win, txt, 'center', txtloc_y, black);
            Screen('DrawTexture', win, mask_tex, [], imgloc);
            Screen('Flip', win);
        end
        target_realtime = mask_onset - target_onset;

        mask_offset = GetSecs; % 검은 화면 종료시점
        mask_realtime = mask_offset - mask_onset;
        Screen('Flip',win);

    elseif whilewhen == 2 % 개발자 코드
        txt = strcat('ptb(when)', num2str(round(target_t*1000)), '_', num2str(t));

        % 키 응답 대기
        KbQueueCreate;
        KbQueueStart;
        while true
            [pressed, firstPress, firstRelease, lastPress, lastRelease] = KbQueueCheck; 
            if pressed
                if firstPress(esc)
                    Screen('Close', win);
                elseif firstPress(space)
                    break;
                end
            end
        end
        KbQueueStop;
        KbQueueRelease;

        % 빈 화면
        blank_onset = Screen('Flip', win); % 빈 화면 제시 시작시점

        % 자극
        DrawFormattedText(win, txt, 'center', txtloc_y, black);
        if delay == 2
            target = imread(targetName);
            target_tex = Screen('MakeTexture', win, target);
        end
        Screen('DrawTexture', win, target_tex, [], imgloc);
        target_onset = Screen('Flip', win, blank_onset + blank_t - slack); % 자극 제시 시작시점

        % 검은 화면
        DrawFormattedText(win, txt, 'center', txtloc_y, black);
        Screen('DrawTexture', win, mask_tex, [], imgloc);
        mask_onset = Screen('Flip', win, target_onset + target_t - slack); % 자극 제시 종료시점 = 검은 화면 시작시점
        target_realtime = mask_onset - target_onset;

        mask_offset = Screen('Flip', win, mask_onset + mask_t - slack); % 검은 화면 종료시점
        mask_realtime = mask_offset - mask_onset;
        Screen('Flip',win);
    end
    timestamp = vertcat(timestamp, [participant t whilewhen delay target_t target_realtime mask_realtime]);
end

%% 프로그램 측정 데이터파일 저장 후 종료
writetable(table(timestamp), fileName0, 'Delimiter', '\t');
Screen('Close', win);
