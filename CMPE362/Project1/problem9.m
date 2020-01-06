%{
    Question 9
%}
%{ 
   Clears old variables from console and workspace to avoid some
   possible errors.
%}
clear;clc;

% Sets the file name in order to be able to read it via csvread command.
file='exampleSignal.csv';

% Reads the csv file.
mySignal=csvread(file);


% Sets the title of the figure to provide better understanding. The 'off'
% option enables that the resulting title does not include the figure
% number.
figure('Name','Problem 9','NumberTitle','off');

% Plots the data.
plot(mySignal);

% Marks the peaks of the data.
findpeaks(mySignal);