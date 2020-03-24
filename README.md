# Decentralized Deep Reinforcement Learning for a six-legged robot

This repository holds results and implementation for training a decentralized control architecture of a six-legged robot. It accompanies a submitted article: Malte Schilling, Kai Konen, Frank W. Ohl, and Timo Korthals, Decentralized Deep Reinforcement Learning for a Distributed and Adaptive Locomotion Controller of a Hexapod Robot. 

For questions, please contact: Malte Schilling, mschilli@techfak.uni-bielefeld.de

## Abstract of Article
Locomotion is a prime example for adaptive behavior in animals and biological control principles have inspired control architectures for legged robots. While machine learning has been successfully applied to many tasks in recent years, Deep Reinforcement Learning approaches still appear to struggle when applied to real world robots in continuous control tasks and in particular do not appear as robust solutions that can handle uncertainties well. Therefore, there is a new interest in incorporating biological principles into such learning architectures. While inducing a hierarchical organization as found in motor control has shown already some success, we here propose a decentralized organization as found in insect motor control for coordination of different legs. A decentralized and distributed architecture is introduced on a simulated hexapod robot and the details of the controller are learned through Deep Reinforcement Learning. We first show that such a concurrent local structure is able to learn good walking behavior. Secondly, that the simpler organization is learned faster compared to holistic approaches.

![Decentralization as an important characteristic for motor control: a) Provides an overview schematic of our motor control perspective. First, motor control is hierarchically organized, integrating different levels of neural organization as assumed in animals and complementing work on, for example, insects highlighting the importance of musculo-skeletal properties as well as the interaction with the environment. Second, there is a decentralized organization operating on different timescales. Behavior emerges as a result of decentralized and locally interacting concurrent control structures. Note that there are multiple, parallel arrows connecting different levels. Such a concurrency is well established in insects, but is also present in vertebrates. In b), this is shown for the decentralized Walknet system for the control of six-legged walking, which reflects a control architecture as found in stick insects.](2_3_CompleteHierarchy.jpg)

## Overview Repository

The repository consists of multiple parts:

* Saved models and data from the paper (currently 10 (respectively 11) seeds for each condition, we are currently running further simulations which already show significant results.
* Supplemental Material summarized in a PDF.
* Scripts that produce the provided figures for evaluation: call from the main directory using python (version 2 or 3 both should work). This requires numpy, matplotlib, pandas, and seaborn.

A description how to run training and evaluation by yourself is given below as well as links to the packaged environment.

## Setup Conditions

* Tested with `Ubuntu 16.04.6 LTS` and `Docker 19.03.5 build 633a0ea838`
* All commands are executed in Linux BASH
* We assume a folder `${HOME}/training` on the host machine which can be mounted into the Docker container.
* Training on the 0.10 m elevated terrain is preconfigured. We refer to `Setup Conditions->Hints->Training` if one wants to setup training on another terrain.

### Decentralized Approach

1. Run the container (you might have to call this as root): `docker run --publish-all --rm --name dppo2 --volume ${HOME}/training:/tmp -it kkonen/ros2_phantomx:master_thesis_final /bin/bash`
1. Start the training for 5000 epochs
    1. `cp /root/heightmap_7.png /tmp/`
    1. `cd /root/ros2learn/experiments/examples/PHANTOMX/`
    1. `python3 train_dppo2_mlp.py`
1. Evaluate the training (the scripts do not quit, but print `Done` every two seconds after finishing evaluation)
    1. `cd /tmp/ros2learn/PhantomX-v0/dppo2/*`
    1. Download the evaluation script: `wget https://raw.githubusercontent.com/malteschilling/ddrl_hexapod/master/evaluation_scripts/run_evaluation_dppo2.py`
    1. Evaluate on flat terrain
        1. `cp /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/empty_bullet.world /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/parcour.world`
        1. `python3 run_evaluation_dppo2.py dppo_flat.txt`
    1. Evaluate on 0.05 m elevated terrain
        1. `cp /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/heightmap1-0_05m.world /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/parcour.world`
        1. `python3 run_evaluation_dppo2.py dppo_005.txt`
    1. Evaluate on 0.10 m elevated terrain
        1. `cp /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/heightmap1-0_10m.world  /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/parcour.world`
        1. `python3 run_evaluation_dppo2.py dppo_010.txt`
    10. Evaluate on 0.15 m elevated terrain
        1. `cp /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/heightmap1-0_15m.world /root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/parcour.world`
        1. `python3 run_evaluation_dppo2.py dppo_015.txt`


### Centralized Approach

1. Run the container (you might have to call this as root): `docker run --publish-all --rm --name ppo2 --volume ${HOME}/training:/tmp -it kkonen/ros2_phantomx:master_thesis_final /bin/bash` 
1. Start the training for 5000 epochs
    1. `cp /root/heightmap_7.png /tmp/`
    1. `cd /root/ros2learn/experiments/examples/PHANTOMX/`
    1. `python3 train_ppo2_mlp.py`
1. Evaluate the training
    1. `cd /tmp/ros2learn/PhantomX-v0/ppo2/*`
    1. Download the evaluation scripts
        1. `wget https://raw.githubusercontent.com/malteschilling/ddrl_hexapod/master/evaluation_scripts/evaluate_ppo.sh`
        1. `wget https://raw.githubusercontent.com/malteschilling/ddrl_hexapod/master/evaluation_scripts/run_evaluation_ppo2.py`
    1. Evaluate on flat and 0.05 m, 0.10 m, 0.15 m elevated terrain: `/bin/bash evaluate_ppo.sh`

### Hints

#### Docker

*   The DDS in ROS2 causes multiple containers to have crosstalk if they are in the same network. Even if they have different IPs, the DDS discovers each other's service and causes errors. Therefore, check if every container is connected to its own Docker bridge.
*   To make the training persistent, it is recommended to mount a local folder of the host to `/tmp` inside of the container. Multiple containers may corrupt the training if they mount the same host folder.
*   The Docker network ports 8080 (gzserver) and 11345 (tensorboard) are exposed. This can cause crosstalk in ROS2 if multiple containers are exposed to the same port. Use e.g. the `-P` switch to assign ports on the host randomly.
*   The training has to report the warning `[gzserver-1] [WARN] [lf_tibia.p3d_lf_tibia_controller]: Negative update time difference detected.` periodically as a sign that the simulation is reset. ROS2 crosstalk may cause the issue, that these warnings do not occur.

#### Training

*   Check if the height map `/root/heightmap_7.png` lies inside the `/tmp` folder.
*   Scripts for training and testing are located inside the Docker folder `/root/ros2learn/experiments/examples/PHANTOMX/`, which are `train_dppo2_mlp.py` (train decentralized approach), `run_dppo2_mlp.py` (test decentralized approach), `train_ppo2_mlp.py` (train centralized approach), `run_ppo2_mlp.py` (test centralized approach), 
*   The training scripts run for 5000 epochs, while a checkpoint is stored every 10 epochs.
*   tensorboard logs, progress and checkpoints are stored in the Docker folder `/tmp/ros2learn/PhantomX-v0/ppo2` for the centralized approach and `dppo2` for the decentralized approach respectively.
*   Hyperparameters are configured in `/root/ros2learn/algorithms/baselines/baselines/ppo2/defaults.py` and `/root/ros2learn/algorithms/baselines/baselines/dppo2/defaults.py` respectively.
*   The heightmap used for training is stored in the Docker folder `/root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/parcour.world`. It needs to be overwritten by `heightmap1-0_10m.world` (standard), `heightmap1-0_15m.world`, `heightmap1-0_05m.world`, or `empty_bullet.world` (which is the flat plane) if one wants to perform training on another terrain. These are all as well in `/root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/`.
