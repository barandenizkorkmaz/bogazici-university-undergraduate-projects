%{ 
   QUESTION 1: ADVANCED PEAK FINDER
%}

%{ 
   Clears old variables from console and workspace to avoid some
   possible errors.
%}
clear;clc;
clear y Fs

%This is a string, corresponding to the filename
audioFile = 'PinkPanther30.wav';                         

%The sound has been converted into an array by audioread built-in function
[y, Fs] = audioread(audioFile);

%To check if the data has been read correctly
sound(y, Fs);

%The number of peaks of the original signal is calculated
numOfPeaksNoFilter=numel(findpeaks(y));

%Creating the cut-off frequencies array for forward-use
%0 Hz Frequency indicates the original signal to enable
%a simple notation
cutOffFrequencies = [0,1000,2000,3000,4000];

%Creating the array that will hold the number of peak values for
%corresponding frequency values
numOfPeaksForEachCutOff = zeros(1,5);

%The number of peaks of the original signal is added into the
%corresponding index which is the index number 0 which will later be
%denotes as 0 Hz Frequency in the plot.
numOfPeaksForEachCutOff(1) = numOfPeaksNoFilter;

%The loop will iterate for the indexes corresponding to the cut-off freqs
for i = 2:5
    % Defining low pass filter by designfilt method
    lowPassFilter = designfilt('lowpassiir', ...
             'PassbandFrequency', cutOffFrequencies(i), ...
             'FilterOrder',8, ...
             'PassbandRipple',0.2, ...
             'SampleRate', 22050);
         
    % Apply low pass filter by filter method
    result = filter(lowPassFilter,y);
    
    % Finding the number of peaks for the data which is the result of
    % low-pass filter
    numOfPeaksCutOff = numel(findpeaks(result));
    
    % Adding the number of peaks into the corresponding index
    numOfPeaksForEachCutOff(i) = numOfPeaksCutOff;
end

% Plotting the figure
figure;
plot(cutOffFrequencies, numOfPeaksForEachCutOff); 
title('Number Of Peaks vs Cut-Off Frequencies');