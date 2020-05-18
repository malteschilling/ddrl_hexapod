#!/bin/bash

touch ppo_evaluate.txt

echo 'Flat: ' >> ppo_evaluate.txt
cp /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/empty_bullet.world /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/parcour.world
python3 run_evaluation_ppo2.py
cat ppoTestRun.txt >> ppo_evaluate.txt 
pkill gzserver

echo'' >> ppo_evaluate.txt
echo '0.05: ' >> ppo_evaluate.txt
cp /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/heightmap1-0_05m.world /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/parcour.world
python3 run_evaluation_ppo2.py
cat ppoTestRun.txt >> ppo_evaluate.txt
pkill gzserver

echo'' >> ppo_evaluate.txt
echo '0.10: ' >> ppo_evaluate.txt
cp /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/heightmap1-0_10m.world /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/parcour.world
python3 run_evaluation_ppo2.py
cat ppoTestRun.txt >> ppo_evaluate.txt
pkill gzserver

echo'' >> ppo_evaluate.txt
echo '0.15: ' >> ppo_evaluate.txt
cp /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/heightmap1-0_15m.world /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/parcour.world
python3 run_evaluation_ppo2.py
cat ppoTestRun.txt >> ppo_evaluate.txt
pkill gzserver
