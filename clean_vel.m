function [vel] = clean_vel(filename)
    %Import velocity
    data = readmatrix(filename);
    data = [data(:,1)' ; data(:,3)']';

    %Create spike detector array
    spike_detector = zeros(length(data));

    %Loop through d_data vectory
    for i = 4:length(data)-3
        %Find double trough spikes
        arr = i-3:i+3;
        arr = arr(arr ~= i);
        upper_thresh = std(data(arr, 2)) + mean(data(arr, 2));
        lower_thresh = mean(data(arr, 2)) - std(data(arr, 2));
        if(data(i, 2) > upper_thresh || data(i, 2) < lower_thresh || (data(i,2) == 0 && data(i-1) > 0))
            spike_detector(i) = 100;
        end
    end

    %This array stores spike locations
    spikes = [];
    
    %Locate spikes through the spike detector array
    for i = 1:length(data)
        if(spike_detector(i) ~= 0)
            spikes = [spikes, i];
        end
    end

    %Remove spikes
    vel = data;
    vel(spikes, :) = [];
    
    
end