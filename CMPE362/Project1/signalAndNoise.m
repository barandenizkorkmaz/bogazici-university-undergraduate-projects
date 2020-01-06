%{
    Question 1
%}
%{ 
   Clears old variables from console and workspace to avoid some
   possible errors.
%}
clear; clc;

% Sets the title of the figure to provide better understanding.
figure('Name','Question 1');

% Creates a vector from -100 to 100.
x=-100:100

% The functions to be plotted are created below.
y1=sin(x);
y2=sin(50.*x);
y3=50.*sin(x);
y4=sin(x)+ 50;
y5=sin(x+50);
y6=50.*sin(50.*x);
y7=x.*sin(x);
y8=sin(x)./x;

%{
 This part draws plots and puts the subplots into one window with their
 titles.
%}
subplot(4,2,1);
plot(x,y1)
title('y1=sin(x)')

subplot(4,2,2);
plot(x,y2)
title('y2=sin(50x)')

subplot(4,2,3);
plot(x,y3)
title('y3=50sin(x)')

subplot(4,2,4);
plot(x,y4)
title('y4=sin(x)+50')

subplot(4,2,5);
plot(x,y5)
title('y5=sin(x+50)')

subplot(4,2,6);
plot(x,y6)
title('y6=50sin(50x)')

subplot(4,2,7);
plot(x,y7)
title('y7=xsin(x)')

subplot(4,2,8);
plot(x,y8)
title('y8=sin(x)/x')

%{
    Question 2
%}

%{ 
   Clears old variables from console and workspace to avoid some
   possible errors.
%}
clear; clc;

% Sets the title of the figure to provide better understanding.
figure('Name','Question 2');,

% Creates a vector from -20 to 20.
x=-20:20

% The functions to be plotted are created below.
y1=sin(x);
y2=sin(50.*x);
y3=50.*sin(x);
y4=sin(x)+50;
y5=sin(x+50);
y6=50.*sin(50.*x);
y7=x.*sin(x);
y8=sin(x)./x;
y9=y1+y2+y3+y4+y5+y6+y7+y8;

%{
 This part draws plots and puts the subplots into one window with their
 titles.
%}
subplot(5,2,1);
plot(x,y1)
title('y1=sin(x)')

subplot(5,2,2);
plot(x,y2)
title('y2=sin(50x)')

subplot(5,2,3);
plot(x,y3)
title('y3=50sin(x)')

subplot(5,2,4);
plot(x,y4)
title('y4=sin(x)+50')

subplot(5,2,5);
plot(x,y5)
title('y5=sin(x+50)')

subplot(5,2,6);
plot(x,y6)
title('y6=50sin(50x)')

subplot(5,2,7);
plot(x,y7)
title('y7=xsin(x)')

subplot(5,2,8);
plot(x,y8)
title('y8=sin(x)/x')

subplot(5,2,9);
plot(x,y9)
title('y9=y1+y2+y3+y4+y5+y6+y7+y8')


%{
    Question 3
%}

%{ 
   Clears old variables from console and workspace to avoid some
   possible errors.
%}
clear; clc;

% Sets the title of the figure to provide better understanding
figure('Name','Question 3');

% Creates a vector from -20 to 20
x=-20:20;

% Generates 41 Gaussian distributed random numbers.
z=randn(1,41)

% The functions to be plotted are created below.
y10=z;
y11=z+x;
y12=z+sin(x);
y13=z.*sin(x);
y14=x.*sin(z);
y15=sin(x+z);
y16=z.*sin(50.*x);
y17=sin(x+50.*z);
y18=sin(x)./z;
y19=y11+y12+y13+y14+y15+y16+y17+y18;

%{
 This part draws plots and puts the subplots into one window with their
 titles.
%}
subplot(5,2,1);
plot(x,y10)
title('y10=z')

subplot(5,2,2);
plot(x,y11)
title('y11=z+x')

subplot(5,2,3);
plot(x,y12)
title('y12=z+sin(x)')

subplot(5,2,4);
plot(x,y13)
title('y13=zsin(x)')

subplot(5,2,5);
plot(x,y14)
title('y14=xsin(z)')

subplot(5,2,6);
plot(x,y15)
title('y15=sin(x+z)')

subplot(5,2,7);
plot(x,y16)
title('y16=zsin(50x)')

subplot(5,2,8);
plot(x,y17)
title('y17=sin(x+50z)')

subplot(5,2,9);
plot(x,y18)
title('y18=sin(x)/z')

subplot(5,2,10);
plot(x,y19)
title('y19= y11+y12+y13+y14+y15+y16+y17+y18')


%{
    Question 4
%}

%{ 
   Clears old variables from console and workspace to avoid some
   possible errors.
%}
clear; clc;

% Sets the title of the figure to provide better understanding
figure('Name','Question 4');

% Creates a vector from -20 to 20
x=-20:20

% Generates 41 uniformly distributed random numbers.
z=rand(1,41);

% The functions to be plotted are created below.
y20=z;
y21=z+x;
y22=z+sin(x);
y23=z.*sin(x);
y24=x.*sin(z);
y25=sin(x+z);
y26=z.*sin(50.*x);
y27=sin(x+50.*z);
y28=sin(x)./z;
y29=y21+y22+y23+y24+y25+y26+y27+y28;

%{
 This part draws plots and puts the subplots into one window with their
 titles.
%}
subplot(5,2,1);
plot(x,y20)
title('y20=z')

subplot(5,2,2);
plot(x,y21)
title('y21=z+x')

subplot(5,2,3);
plot(x,y22)
title('y22=z+sin(x)')

subplot(5,2,4);
plot(x,y23)
title('y23=zsin(x)')

subplot(5,2,5);
plot(x,y24)
title('y24=xsin(z)')

subplot(5,2,6);
plot(x,y25)
title('y25=sin(x+z)')

subplot(5,2,7);
plot(x,y26)
title('y26=zsin(50x)')

subplot(5,2,8);
plot(x,y27)
title('y27=sin(x+50z)')

subplot(5,2,9);
plot(x,y28)
title('y28=sin(x)/z')

subplot(5,2,10);
plot(x,y29)
title('y29=y21+y22+y23+y24+y25+y26+y27+y28')

%{
    Question 5
%}

%{ 
   Clears old variables from console and workspace to avoid some
   possible errors.
%}
clear; clc;

% Sets the title of the figure to provide better understanding
figure('Name','Question 5');

%{ 
  This part generates 10000 gaussian distributed random variables with given mean and
  standard deviation (recall that std deviation is the square root of the 
  variance) values.
%}
std1 = 1; 
mean = 0;
r1 = std1.*randn(10000,1) + mean;

std2 = 2; 
mean = 0;
r2 = std2.*randn(10000,1) + mean;

std3 = 4; 
mean = 0;
r3 = std3.*randn(10000,1) + mean;

std4 = 16; 
mean = 0;
r4 = std4.*randn(10000,1) + mean;


%{
 This part draws histograms and puts the subplots into one window with their
 titles.
%}
subplot(2,2,1);
hist(r1)
title('Gaussian Random Variables with Mean 0,Variance 1')

subplot(2,2,2);
hist(r2)
title('Gaussian Random Variables with Mean 0,Variance 4')

subplot(2,2,3);
hist(r3)
title('Gaussian Random Variables with Mean 0,Variance 16')

subplot(2,2,4);
hist(r4)
title('Gaussian Random Variables with Mean 0,Variance 256')

%{
    Question 6
%}

%{ 
   Clears old variables from console and workspace to avoid some
   possible errors.
%}
clear; clc;

% Sets the title of the figure to provide better understanding
figure('Name','Question 6');

%{ 
  This part generates 10000 gaussian distributed random variables with given mean and
  standard deviation (recall that std deviation is the square root of the 
  variance) values.
%}
std1 = 1; 
mean1 = 10;
r6 = std1.*randn(10000,1) + mean1;

std2 = 2; 
mean2 = 20;
r7 = std2.*randn(10000,1) + mean2;

std3 = 1; 
mean3 = -10;
r8 = std3.*randn(10000,1) + mean3;

std4 = 2; 
mean4 = -20;
r9 = std4.*randn(10000,1) + mean4;

%{
 This part draws histograms and puts the subplots into one window with their
 titles.
%}
subplot(2,2,1);
hist(r6)
title('Gaussian Random Variables with Mean 10,Variance 1')

subplot(2,2,2);
hist(r7)
title('Gaussian Random Variables with Mean 20,Variance 4')

subplot(2,2,3);
hist(r8)
title('Gaussian Random Variables with Mean -10,Variance 1')

subplot(2,2,4);
hist(r9)
title('Gaussian Random Variables with Mean -20,Variance 4')

%{
    Question 7
%}

%{ 
   Clears old variables from console and workspace to avoid some
   possible errors.
%}
clear; clc;

% Sets the title of the figure to provide better understanding
figure('Name','Question 7');

%{ 
  This part generates 10000 uniformly distributed random variables with given mean and
  standard deviation (recall that std deviation is the square root of the 
  variance) values.
%}
std1 = 1; 
mean = 0;
r11 = std1.*rand(10000,1) + mean;

std2 = 2; 
mean = 0;
r21 = std2.*rand(10000,1) + mean;

std3 = 4; 
mean = 0;
r31 = std3.*rand(10000,1) + mean;

std4 = 16; 
mean = 0;
r41 = std4.*rand(10000,1) + mean;

%{
 This part draws histograms and puts the subplots into one window with their
 titles.
%}
subplot(2,2,1);
hist(r11)
title('Uniformly Distributed Random Variables with Mean 0,Variance 1')

subplot(2,2,2);
hist(r21)
title('Uniformly Distributed Random Variables with Mean 0,Variance 4')

subplot(2,2,3);
hist(r31)
title('Uniformly Distributed Random Variables with Mean 0,Variance 16')

subplot(2,2,4);
hist(r41)
title('Uniformly Distributed Random Variables with Mean 0,Variance 256')

%{
    Question 8
%}

%{ 
   Clears old variables from console and workspace to avoid some
   possible errors.
%}
clear; clc;

% Sets the title of the figure to provide better understanding
figure('Name','Question 8');

%{ 
  This part generates 10000 uniformly distributed random variables with given mean and
  standard deviation (recall that std deviation is the square root of the 
  variance) values.
%}
std1 = 1; 
mean1 = 10;
r61 = std1.*rand(10000,1) + mean1;

std2 = 2; 
mean2 = 20;
r71 = std2.*rand(10000,1) + mean2;

std3 = 1; 
mean3 = -10;
r81 = std3.*rand(10000,1) + mean3;

std4 = 2; 
mean4 = -20;
r91 = std4.*rand(10000,1) + mean4;

%{
 This part draws histograms and puts the subplots into one window with their
 titles.
%}
subplot(2,2,1);
hist(r61)
title('Uniformly Distributed Random Variables with Mean 10,Variance 1')

subplot(2,2,2);
hist(r71)
title('Uniformly Distributed Random Variables with Mean 20,Variance 4')

subplot(2,2,3);
hist(r81)
title('Uniformly Distributed Random Variables with Mean -10,Variance 1')

subplot(2,2,4);
hist(r91)
title('Uniformly Distributed Random Variables with Mean -20,Variance 4')
