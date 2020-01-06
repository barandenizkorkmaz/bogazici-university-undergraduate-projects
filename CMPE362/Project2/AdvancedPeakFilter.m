%{
    Question 1
%}
%{ 
   Clears old variables from console and workspace to avoid some
   possible errors.
%}
clear;clc;

% Sets the file name in order to be able to read it via csvread command.
file='exampleSignal.csv';

% Reads the csv file. PS: csvread function caused some numerical
% anormalities, therefore in the project, the load function has been used.
mySignal=load(file);

% y1 is an alias of the signal.
y1=mySignal;

% Below are the filter coefficients for the moving average filters.
b2=[1/2 1/2];
b3=[1/3 1/3 1/3];
b4=[1/4 1/4 1/4 1/4];
b5=[1/5 1/5 1/5 1/5 1/5];
b6=[1/6 1/6 1/6 1/6 1/6 1/6];
b7=[1/7 1/7 1/7 1/7 1/7 1/7 1/7];
b8=[1/8 1/8 1/8 1/8 1/8 1/8 1/8 1/8];
b9=[1/9 1/9 1/9 1/9 1/9 1/9 1/9 1/9 1/9];
b10=[1/10 1/10 1/10 1/10 1/10 1/10 1/10 1/10 1/10 1/10];
b11=[1/11 1/11 1/11 1/11 1/11 1/11 1/11 1/11 1/11 1/11 1/11];
b12=[1/12 1/12 1/12 1/12 1/12 1/12 1/12 1/12 1/12 1/12 1/12 1/12];
b13=[1/13 1/13 1/13 1/13 1/13 1/13 1/13 1/13 1/13 1/13 1/13 1/13 1/13];
b14=[1/14 1/14 1/14 1/14 1/14 1/14 1/14 1/14 1/14 1/14 1/14 1/14 1/14 1/14];
b15=[1/15 1/15 1/15 1/15 1/15 1/15 1/15 1/15 1/15 1/15 1/15 1/15 1/15 1/15 1/15];
b16=[1/16 1/16 1/16 1/16 1/16 1/16 1/16 1/16 1/16 1/16 1/16 1/16 1/16 1/16 1/16 1/16];
b17=[1/17 1/17 1/17 1/17 1/17 1/17 1/17 1/17 1/17 1/17 1/17 1/17 1/17 1/17 1/17 1/17 1/17];
b18=[1/18 1/18 1/18 1/18 1/18 1/18 1/18 1/18 1/18 1/18 1/18 1/18 1/18 1/18 1/18 1/18 1/18 1/18];
b19=[1/19 1/19 1/19 1/19 1/19 1/19 1/19 1/19 1/19 1/19 1/19 1/19 1/19 1/19 1/19 1/19 1/19 1/19 1/19];
b20=[1/20 1/20 1/20 1/20 1/20 1/20 1/20 1/20 1/20 1/20 1/20 1/20 1/20 1/20 1/20 1/20 1/20 1/20 1/20 1/20];
b21=[1/21 1/21 1/21 1/21 1/21 1/21 1/21 1/21 1/21 1/21 1/21 1/21 1/21 1/21 1/21 1/21 1/21 1/21 1/21 1/21 1/21];
b22=[1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22 1/22];
b23=[1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23 1/23];
b24=[1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24 1/24];
b25=[1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25 1/25];
b26=[1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26 1/26];
b27=[1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27 1/27];
b28=[1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28 1/28];
b29=[1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29 1/29];
b30=[1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30 1/30];

% Below are the resulting signals after each moving average filter
% operation.
y2=conv(b2, mySignal);
y3=conv(b3, mySignal);
y4=conv(b4, mySignal);
y5=conv(b5, mySignal);
y6=conv(b6, mySignal);
y7=conv(b7, mySignal);
y8=conv(b8, mySignal);
y9=conv(b9, mySignal);
y10=conv(b10, mySignal);
y11=conv(b11, mySignal);
y12=conv(b12, mySignal);
y13=conv(b13, mySignal);
y14=conv(b14, mySignal);
y15=conv(b15, mySignal);
y16=conv(b16, mySignal);
y17=conv(b17, mySignal);
y18=conv(b18, mySignal);
y19=conv(b19, mySignal);
y20=conv(b20, mySignal);
y21=conv(b21, mySignal);
y22=conv(b22, mySignal);
y23=conv(b23, mySignal);
y24=conv(b24, mySignal);
y25=conv(b25, mySignal);
y26=conv(b26, mySignal);
y27=conv(b27, mySignal);
y28=conv(b28, mySignal);
y29=conv(b29, mySignal);
y30=conv(b30, mySignal);

%The following part calculates the number of peaks for each signal.
numOfPeaks1=numel(findpeaks(y1));
numOfPeaks2=numel(findpeaks(y2));
numOfPeaks3=numel(findpeaks(y3));
numOfPeaks4=numel(findpeaks(y4));
numOfPeaks5=numel(findpeaks(y5));
numOfPeaks6=numel(findpeaks(y6));
numOfPeaks7=numel(findpeaks(y7));
numOfPeaks8=numel(findpeaks(y8));
numOfPeaks9=numel(findpeaks(y9));
numOfPeaks10=numel(findpeaks(y10));
numOfPeaks11=numel(findpeaks(y11));
numOfPeaks12=numel(findpeaks(y12));
numOfPeaks13=numel(findpeaks(y13));
numOfPeaks14=numel(findpeaks(y14));
numOfPeaks15=numel(findpeaks(y15));
numOfPeaks16=numel(findpeaks(y16));
numOfPeaks17=numel(findpeaks(y17));
numOfPeaks18=numel(findpeaks(y18));
numOfPeaks19=numel(findpeaks(y19));
numOfPeaks20=numel(findpeaks(y20));
numOfPeaks21=numel(findpeaks(y21));
numOfPeaks22=numel(findpeaks(y22));
numOfPeaks23=numel(findpeaks(y23));
numOfPeaks24=numel(findpeaks(y24));
numOfPeaks25=numel(findpeaks(y25));
numOfPeaks26=numel(findpeaks(y26));
numOfPeaks27=numel(findpeaks(y27));
numOfPeaks28=numel(findpeaks(y28));
numOfPeaks29=numel(findpeaks(y29));
numOfPeaks30=numel(findpeaks(y30));

% The matrix a consists of the numerical values of the peaks for each
% signal.
a=[numOfPeaks1 numOfPeaks2 numOfPeaks3 numOfPeaks4 numOfPeaks5 numOfPeaks6 numOfPeaks7 numOfPeaks8 numOfPeaks9 numOfPeaks10 numOfPeaks11 numOfPeaks12 numOfPeaks13 numOfPeaks14 numOfPeaks15 numOfPeaks16 numOfPeaks17 numOfPeaks18 numOfPeaks19 numOfPeaks20 numOfPeaks21 numOfPeaks22 numOfPeaks23 numOfPeaks24 numOfPeaks25 numOfPeaks26 numOfPeaks27 numOfPeaks28 numOfPeaks29 numOfPeaks30];

% The matrix n denotes the length of the moving average filter.For example,
%  n=1 denotes the original signal.
n=[1:30]

% Plots the number of peaks for the corresponding length of the moving
% average filter.
plot(n,a);

