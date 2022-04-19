%{
Data Collection Test

Collect data from an accelerometer based on a voltage threshold and export
specific events as their own excel files
%}
clear
clc

%Initialize variables
arduino = arduino('COM3', 'Uno', 'AnalogReferenceMode','external','AnalogReference',3.0);
eventLog = [];
fileName = 'EVENT';
check = 100;
i = 1;
eventNum = 0;
threshold = 0.5;
cutoff = 2;
leave = 0;
%Calibrate the accelerometer by collecting values while still and creating
%an offset
[xOffset,yOffset,zOffset] = accelCalibrate(arduino);
disp('Calibration Complete!')

while (1==1)
   %Read the state of the accelerometer
   pause(0.001)
   xAccel = (readVoltage(arduino, 'A2') - xOffset)/0.300;
   yAccel = (readVoltage(arduino, 'A1') - yOffset)/0.300;
   zAccel = (readVoltage(arduino, 'A0') - zOffset)/0.300;
   
   %Is the activity threshold exceeded?
   if (abs(xAccel) > threshold || abs(yAccel) > threshold || abs(zAccel) > threshold)
       
       disp('Activity Detected')
       
       while(leave == 0)
           
       %Set exit value to 1 so that only 100 data points are recorded
       leave = 1;
       
         for j = 1:check
            
            eventLog(i,1) = xAccel;
            eventLog(i,2) = yAccel;
            eventLog(i,3) = zAccel;
            zAccel = (readVoltage(arduino, 'A0') - zOffset)/0.300;
            yAccel = (readVoltage(arduino, 'A1') - yOffset)/0.300;
            xAccel = (readVoltage(arduino, 'A2') - xOffset)/0.300;
              
            if (abs(xAccel) > threshold || abs(yAccel) > threshold || abs(zAccel) > threshold)
                %If another data point is read above threshold DURING the
                %same reading, reset the exit value so another 100 points
                %are read
                
                leave = 0;
            end
            
            pause(0.001)
            i = i + 1;
          end
     
       end
       
       %The fourth column represents the magnitude of the acceleration
       %(UNKNOWN IF IT WILL BE USED)
       eventLog(:,4) = sqrt((eventLog(:,1)).^2 + (eventLog(:,2)).^2 + (eventLog(:,3)).^2);
      
      %Create a string variable containing the date
      date = datetime;
      date = datestr(date);
      
      %Increment eventnum and append with filename so a new csv file is 
      %created for each new event 
       
      eventNum = eventNum + 1;
      add = num2str(eventNum);
      csv = '.csv';
      export = append(fileName,add,csv);
      writeMatrix(eventLog,export)
   end
end