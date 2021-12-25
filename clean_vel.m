function [vel] = clean_vel(filename)
    %Import velocity
    data = readmatrix(filename);
    data = [data(:,1)' ; data(:,3)']';

    %Time derivative of velocity
    d_data = diff([eps; data(:,2)])./diff([eps; data(:,1)]);

    %Create spike detector array
    spike_detector = zeros(length(data));

    plot(d_data)
    hold on
    plot(data(:,1), data(:,2))
    hold off

    %Loop through d_data vectory
    for i = 2:length(data)
        %Find single peak/trough spikes
        if(xor(d_data(i-1) > 0, d_data(i) > 0)) && (abs(abs(d_data(i)) - abs(d_data(i-1))) < 0.2*abs(d_data(i)))
            spike_detector(i-1) = d_data(i-1);
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

    %Create 'cleaned' version of dataset, removing the spikes.
    cleaned_data = data;
    cleaned_data(spikes, :) = [];

    plot(cleaned_data(:,1), cleaned_data(:,2))
end