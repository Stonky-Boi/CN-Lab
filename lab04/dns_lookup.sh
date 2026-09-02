#!/bin/bash

# Q1
nslookup -type=A www.youtube.com > q1.txt
nslookup -type=AAAA www.youtube.com >> q1.txt

# Q2
nslookup -type=CNAME www.github.com > q2.txt

# Q3
sudo tcpdump -i en0 -nn -w q3.pcap 'udp port 53 or tcp port 53' &
PID=$!
sleep 1
nslookup -type=A www.youtube.com
nslookup -type=AAAA www.youtube.com
nslookup -type=CNAME www.github.com
sleep 1
sudo kill $PID

# Q4
sudo tcpdump -i en0 -nnvvv 'udp port 53 or tcp port 53' > q4.txt &
PID=$!
sleep 1
nslookup -type=A www.youtube.com
nslookup -type=AAAA www.youtube.com
nslookup -type=CNAME www.github.com
sleep 1
sudo kill $PID

# Q5
sudo tcpdump -i en0 -nnvvv 'udp port 53 or tcp port 53' > q5.txt &
PID=$!
sleep 1
nslookup -type=NS facebook.com
sleep 1
sudo kill $PID

# Q6
nslookup 8.8.8.8 > q6.txt
nslookup 9.9.9.9 >> q6.txt
nslookup 208.67.222.222 >> q6.txt

# Q7
echo "iteration,ttl" > q7.txt
for i in {1..10}
do
    ttl=$(nslookup -debug www.iitb.ac.in | grep "ttl =" | head -1 | awk '{print $3}')
    echo "$i,$ttl" >> q7.txt
    sleep 1
done