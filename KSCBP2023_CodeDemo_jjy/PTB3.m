% [�����׻���2023] �ڱ� ���� ���α׷��� ó�� ������ ���� ���� ���� ��Ȯ�� ��
% Copyright 2023. ������. All rights reserved.
% ����: word3276@gmail.com

% MATLAB R2022b & Psychtoolbox 3.0.18
% ����: �Է�â�� �Ķ���� �Է� > ��ũ���� ������ �����̽��� > �ڱ� ����(�⺻ 16.7 ms) > �ݺ� Ƚ���� ������ �ڵ� ����
% ���α׷� ���� ���������� ���: [result] ����
%            ���������� ���θ�: 1. ID  2. �����ȣ  3. �ڵ�: while[1]/������[2] 4. �������: ����[0]/Ű�Է�����[1]/�ݺ���[2]
%                          5. �ڱ� ���ýð�(�̻�ideal)  6. �ڱ� ���ýð�(���α׷�)  7. ����ȭ�� ���ýð�(���α׷�)

%% �ʱ�ȭ
sca; 
close all;
clearvars;

%% �ڱ� �Ķ���� ����
rng('shuffle', 'twister');
screenNumber = 0;       % ����� ��ũ�� ��ȣ
issynctest = 2;         % PTB3 ��ũ�׽�Ʈ ���� [0: ����(����), 1: ���Ǻ� ����, 2: ������]            
nrepeat = 10;           % �ݺ� Ƚ��

target_t = 1/60;        % �ڱ� ���ýð�[�⺻��: 16.7 ms = 60 Hz ����� ���� 1������]
mask_t = 3/60;          % ���� ȭ�� ���ýð�
blank_t0 = 3/60;        % Ű �Է°� �ڱ� ���� ���� �ð� ����

%% �Է�â ����
prompt = {'ID[�ƹ�����]: ', '�ڵ�: while[1]/������[2]', '�������: ����[0]/Ű�Է�����[1]/�ݺ���[2]'};
dlgtitle = 'Input';
dims = [1 50];
definput = {'', '', ''};
answer = inputdlg(prompt, dlgtitle, dims, definput);

participant = str2double(answer{1, 1});
whilewhen = str2double(answer{2, 1});
delay = str2double(answer{3, 1});

if delay == 2 && whilewhen == 2
   error('������ �ڵ� & ������� �ݺ��� ������ �Ұ����մϴ�.');
end

if delay ~= 1
    blank_t = blank_t0;
else
    blank_t = 0;
end

%% PTB3 ��ũ�� ����
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

% ������ ���� --------------------------------------------------------
[win, rect]=Screen('OpenWindow', screenNumber, white, [], [], [], [], 0);
SetMouse(rect(3), rect(4));        % ���콺 Ŀ�� ������+�Ʒ��� ������ �̵�
slack = Screen('GetFlipInterval', win)/2;

%% ���α׷� ���� ���������� ����
nowtime = fix(clock);
nowdate_txt = sprintf('%4d%02d%02d_%02d%02d%02d', nowtime(1), nowtime(2), nowtime(3), nowtime(4), nowtime(5), nowtime(6));
fileName0 = strcat('result/matlab', num2str(participant), '_', num2str(whilewhen), '_', num2str(delay), '_', num2str(round(target_t*1000)), '_', nowdate_txt, '.txt');

%% �ڱ� �̹��� ����
imgloc = round(CenterRectOnPointd([0 0 900 600], rect(3)/2, rect(4)/2));
txtloc_y = imgloc(2)-50;

targetName = strcat('stim/900x600_25_100000.jpg');

if delay ~= 2
    target = imread(targetName);
    target_tex = Screen('MakeTexture', win, target);
end
mask = imread('stim/900x600_Black.jpg');
mask_tex = Screen('MakeTexture', win, mask);

%% �ڱ� ���� ����
timestamp = [];
for t = 1:nrepeat
    if whilewhen == 1 % While��
        txt = strcat('ptb(while)', num2str(round(target_t*1000)), '_', num2str(t));

        % Ű ���� ���
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

        % �� ȭ��
        blank_onset = GetSecs; % �� ȭ�� ���� ���۽���
        while GetSecs - blank_onset < blank_t - slack
            Screen('Flip', win);
        end

        % �ڱ�
        target_onset = GetSecs; % �ڱ� ���� ���۽���
        while GetSecs - target_onset < target_t - slack
            if delay == 2
                target = imread(targetName);
                target_tex = Screen('MakeTexture', win, target);
            end

            DrawFormattedText(win, txt, 'center', txtloc_y, black);
            Screen('DrawTexture', win, target_tex, [], imgloc);
            Screen('Flip', win);
        end

        % ���� ȭ��
        mask_onset = GetSecs; % �ڱ� ���� ������� = ���� ȭ�� ���۽���
        while GetSecs - mask_onset < mask_t - slack
            DrawFormattedText(win, txt, 'center', txtloc_y, black);
            Screen('DrawTexture', win, mask_tex, [], imgloc);
            Screen('Flip', win);
        end
        target_realtime = mask_onset - target_onset;

        mask_offset = GetSecs; % ���� ȭ�� �������
        mask_realtime = mask_offset - mask_onset;
        Screen('Flip',win);

    elseif whilewhen == 2 % ������ �ڵ�
        txt = strcat('ptb(when)', num2str(round(target_t*1000)), '_', num2str(t));

        % Ű ���� ���
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

        % �� ȭ��
        blank_onset = Screen('Flip', win); % �� ȭ�� ���� ���۽���

        % �ڱ�
        DrawFormattedText(win, txt, 'center', txtloc_y, black);
        if delay == 2
            target = imread(targetName);
            target_tex = Screen('MakeTexture', win, target);
        end
        Screen('DrawTexture', win, target_tex, [], imgloc);
        target_onset = Screen('Flip', win, blank_onset + blank_t - slack); % �ڱ� ���� ���۽���

        % ���� ȭ��
        DrawFormattedText(win, txt, 'center', txtloc_y, black);
        Screen('DrawTexture', win, mask_tex, [], imgloc);
        mask_onset = Screen('Flip', win, target_onset + target_t - slack); % �ڱ� ���� ������� = ���� ȭ�� ���۽���
        target_realtime = mask_onset - target_onset;

        mask_offset = Screen('Flip', win, mask_onset + mask_t - slack); % ���� ȭ�� �������
        mask_realtime = mask_offset - mask_onset;
        Screen('Flip',win);
    end
    timestamp = vertcat(timestamp, [participant t whilewhen delay target_t target_realtime mask_realtime]);
end

%% ���α׷� ���� ���������� ���� �� ����
writetable(table(timestamp), fileName0, 'Delimiter', '\t');
Screen('Close', win);