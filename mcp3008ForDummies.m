%{
Make a simple class that can read the voltage from our MCP3008 ADC

UPDATES: Created: 2/10/2022
%}

classdef mcp3008ForDummies
    properties
        raspi raspi
        channel string
        ADC raspi.internal.spidev
    end
    
    methods
        function obj = mcp3008ForDummies(rpi,chan)
            obj.raspi = rpi;
            obj.channel = chan;
            
            obj.ADC = spidev(rpi,chan);
            
        end
        
        function val = readADC(obj,chan)
            exit = 1;
            if strcmp(chan,'CH0') == 1
                bit = '10000000';
            elseif strcmp(chan,'CH1') == 1
                bit = '10010000';
            elseif strcmp(chan,'CH2') == 1
                bit = '10100000';
            else
                disp('That channel isn"t being used')
                disp('Use CH0, CH1, or CH2')
                exit = 0;
            end
            
            if exit ~= 0
                data = uint16(writeRead(obj.ADC,[1, bin2dec(bit), 0]));
                highbits = bitand(data(2), bin2dec('11'));
                val = double(bitor(bitshift(highbits, 8), data(3)));
                val = (3.3/1024) * val;
            end
        end    
    end
end
   

