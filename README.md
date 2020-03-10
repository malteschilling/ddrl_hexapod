# ddrl_hexapod

## Setup Conditions

* Tested with `Ubuntu 16.04.6 LTS` and `Docker 19.03.5 build 633a0ea838`
* All commands are executed in Linux BASH
* We assume a folder `${HOME}/training` on the host machine which can be mounted into the Docker container.
* Training on the 0.10 m elevated terrain is preconfigured. We refer to `Setup Conditions->Hints->Training` if one wants to setup training on another terrain.

### Decentralized Approach

1. Run the container: `Docker run --publish-all --rm --name dppo2 --volume ${HOME}/training:/tmp -it kkonen/ros2_phantomx:master_thesis_final /bin/bash`
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

1. Run the container: `Docker run --publish-all --rm --name ppo2 --volume ${HOME}/training:/tmp -it kkonen/ros2_phantomx:master_thesis_final /bin/bash`
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
*   Hyperparameters are configured in `/root/ros2learn/algorithms/baselines/baselines/ppo2/defaults.py`
*   The hightmap used for training is stored in the Docker folder `/root/ros2learn/environments/gym-gazebo2/gym_gazebo2/worlds/parcour.world`. It needs to be overwritten by `heightmap1-0_10m.world` (standard), `heightmap1-0_15m.world`, `heightmap1-0_05m.world`, or `empty_bullet.world` (which is the flat plane) if one wants to perform training on another terrain.
