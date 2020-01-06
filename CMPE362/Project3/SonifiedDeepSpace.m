%{
   QUESTION 2: CONVERTING A HUBBLE DEEP SPACE IMAGE INTO SPACE SOUND
%}

%{ 
   Clears old variables from console and workspace to avoid some
   possible errors.
%}
clear;clc;
% Sets the file name in order to be able to read it via imread command.
path='Hubble-Massive-Panorama.png';

% Reads the png file.
hubble=imread(path);

% Converts the rgb image into the grayscale form. 
hubblegray=rgb2gray(hubble);

% Converts the rgb image into the black-white form. The default threshold
% value is 0.5.
hubbleBW=imbinarize(hubblegray);

% The sound array that will hold the concatenated sounds with duration of 
% 1-sec 
soundArray=0;

% The duration has been specified.
duration=1;

% The sampling rate has been specified. The sampling rate is selected
% according to the Nyquist Rate.
Fs=2000;

% The array that will be used in the creation of the sound which holds
% values from 0 to duration (1) with an interval of 1/Sampling Rate.
t=0:1/Fs:duration;

% The 900*1024 array will be processed inside the nested loops.
for i = 1:1024 % The number of columns is indicated by i which is 1024.
    myWave=0; % The wave of the column processed has been initialized.
    for j = 900:-1:1 % The number of rows is indicated by j which is 900
        Amplitude=0; % The amplitude of the wave has been initialized.
        
        %{
            If the current cell is marked as white, Then the amplitude
            according to the number of the pixel will be assigned and
            the wave created by the pixel will be added into the myWave
            variable which holds the overall signal for a given column.
        %}
        if hubbleBW(j,i)==1
            if j>=1 && j<=90
                Amplitude=10;
                myWave=myWave+Amplitude*sin(2*pi*j*t);
            end
            if j>=91 && j<=180
                Amplitude=9;
                myWave=myWave+Amplitude*sin(2*pi*j*t);
            end
            if j>=181 && j<=270
                Amplitude=8;
                myWave=myWave+Amplitude*sin(2*pi*j*t);
            end
            if j>=271 && j<=360
                Amplitude=7;
                myWave=myWave+Amplitude*sin(2*pi*j*t);
            end
            if j>=361 && j<=450
                Amplitude=6;
                myWave=myWave+Amplitude*sin(2*pi*j*t);
            end
            if j>=451 && j<=540
                Amplitude=5;
                myWave=myWave+Amplitude*sin(2*pi*j*t);
            end
            if j>=541 && j<=630
                Amplitude=4;
                myWave=myWave+Amplitude*sin(2*pi*j*t);
            end
            if j>=631 && j<=720
                Amplitude=3;
                myWave=myWave+Amplitude*sin(2*pi*j*t);
            end
            if j>=721 && j<=810
                Amplitude=2;
                myWave=myWave+Amplitude*sin(2*pi*j*t);
            end
            if j>=811 && j<=900
                Amplitude=1;
                myWave=myWave+Amplitude*sin(2*pi*j*t);
            end
        end
    end
    %Before a new column has been processed, the overall wave of the
    %current column will be concatenated into the soundArray which holds
    %the sounds created by each column.
    soundArray=cat(2,soundArray,myWave);
end

% The wav file has been created.
audiowrite("SonifiedDeepSpace.wav",soundArray,2000);
% The wav file has been read to enable sound function.
[y,Fs]=audioread("SonifiedDeepSpace.wav");
% Plays the created sound.
sound(y,Fs);
