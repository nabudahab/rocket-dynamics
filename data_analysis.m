clear

%Import data
data = readmatrix('data.txt');
data = [data(:,1)' ; data(:,3)']';

%This duplicate array will be the cleaned data
d_data = diff([eps; data(:,2)])./diff([eps; data(:,1)]);

spike_detector = zeros(length(data));

plot(d_data)
hold on
plot(data(:,1), data(:,2))
hold off


for i = 2:length(data)
    if(xor(d_data(i-1) > 0, d_data(i) > 0)) && (abs(abs(d_data(i)) - abs(d_data(i-1))) < 0.2*abs(d_data(i)))
        spike_detector(i-1) = d_data(i-1);
    end
end

spikes = [];

for i = 1:length(data)
    if(spike_detector(i) ~= 0)
        spikes = [spikes, i];
    end
end

