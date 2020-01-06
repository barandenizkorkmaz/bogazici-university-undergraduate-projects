%{
    Question 10
%}
%{ 
   Clears old variables from console and workspace to avoid some
   possible errors.
%}
clear;clc;

% Sets the file name in order to be able to read it via imread command.
path='lena.png';

% Reads the png file.
lena=imread(path);

% Converts the rgb image into the grayscale form. 
lena_gray=rgb2gray(lena);

%{ 
  The following part computes the mean, standard deviation, maximum (and location of
  maximum), minimum (and location of minimum) of the matrix obtained from
  the image.
%}
meanVal=mean2(lena_gray);
stdVal=std2(lena_gray);
maxValue = max(max(lena_gray));
[xMax,yMax]=find(lena_gray==maxValue)
minValue = min(min(lena_gray));
[xMin,yMin]=find(lena_gray==minValue)