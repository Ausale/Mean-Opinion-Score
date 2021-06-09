# Mean Opinion Score (MOS)

This python script uses ICMP (ping) to calculate 'Mean Opinion Score' (MOS). 
I am aware that ICMP does not produce accurate data on which to calculate MOS. 
This script was created purely for my own learning. 
Tested on Windows, Linux and Mac platforms. 
Any advice on how to improve the code would be very welcome.


# The script does the following:

1. Pings a host x amount of times (64 bytes per ping)
2. Extracts and calculates jitter, avg latency and packet loss from the output
3. Calculates MOS based on jitter, avg latency, packet loss and an arbitrary codec delay value
4. Returns MOS


# How to run the script:

in CMD/terminal, run:
python mos.py <ip address> <ping count>
  
