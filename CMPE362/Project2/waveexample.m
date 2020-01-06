%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   CMPE 362 Homework II-b   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%

                                                % Fs is the frequency = number of samples per second
                                                % y is the actual sound data 
hfile = 'laughter.wav';                         % This is a string, corresponding to the filename
clear y Fs                                      % Clear unneded variables

%% PLAYING A WAVE FILE

[y, Fs] = audioread(hfile);      % Read the data back into MATLAB, and listen to audio.
                                                % nbits is number of bits per sample
sound(y, Fs);                                   % Play the sound & wait until it finishes

duration = numel(y) / Fs;                       % Calculate the duration
pause(duration + 2)                             % Wait that much + 2 seconds

%% CHANGE THE PITCH

yChanged=y(1:2:end);
sound(yChanged, Fs);                          % Get rid of even numbered samples and play the file
pause(duration + 2)

%% EXERCISE I
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Re-arrange the data so that   %
%   the frequency is quadrupled and play the file   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% In order to be able to quadruple the frequency that is getting a
% frequenct multiplied by four, the following code piece simply changes the
% pitch. Then the duration of the pause should be determined by the
% one-forth of the duration of the normal signal since the frequency is
% quadrupled.
yQuadrupled=y(1:4:end);
sound(yQuadrupled, Fs);
pause(duration/4+2)
                                                
                              
%% EXERCISE II
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Re-arrange the data so that   %
%   the frequency is halved and play the file  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%In order to halve the frequency, the following desing enables us to expand
%the signal in a way that the frequency becomes half of the old value. The
%design simply creates a new vector of size of the double of the length of
%the signal, and it puts the first index value of the signal into the first
%two index of the new signal. The process goes on until the all n elements
%are distributed into 2n indexes of the new signal. The new signal is a
%good model for the signal with a frequency that is halved. Since the
%frequency is halved, the pause duration will be determined by the double
%of the old duration.

col=2*size(y,1);
yHalved = ones(col,1);

for index = 1 : size(y, 1)
    yHalved(2 * index) = y(index);
    yHalved(2 * index - 1) = y(index);
end

sound(yHalved, Fs);
pause(2*duration + 2)
                                                
%% EXERCISE III 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Double Fs and play the sound  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%The following code piece multiplies Fs by 2 and sounds it. The duration is
%arranged to adapt into the new frequency.
FsDoubled=Fs*2;
sound(y,FsDoubled);
pause(duration/2 + 2)

%% EXERCISE IV
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Divide Fs by two and play the sound  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%The following code piece divides Fs by 2 and sounds it. The duration is
%arranged to adapt into the new frequency.
FsHalved=Fs/2;
sound(y,FsHalved);



