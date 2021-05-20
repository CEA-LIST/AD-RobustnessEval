# Evaluating Robustness over High Level Driving Instruction for Autonomous Driving

This repository includes our benchmark and frozen graph of our paper accepted at IV21. Details can be found in the paper [link to paper coming soon]. 

This benchmark is an extension of the original Carla benchmark and evaluates the reaction of our agent when an inccorect driving command is provided. 
Our code is a fork of the repository [**Learning by Cheating**](https://github.com/dianchen96/LearningByCheating) from which we kept the code related to agent evaluation. 

Our benchmark adds 3 types of crossing, where one of the direction is not possible, and records the reaction of the agent when it is still told to go in that direction. 

<p align="center">
<img src="https://github.com/CEA-LIST/AD-RobustnessEval/blob/master/figs/img3.png" width="500"/>
</p>

Training and inference are performed with Carla 0.9.6


## Installation

We provide a script to install every dependencies required and run our benchmark. 

```bash

# Download Repo
git clone git@github.com:CEA-LIST/AD-RobustnessEval.git
cd AD-RobustnessEval/

# Create virtual environement 
python3.7 -m venv --system-site-packages ~/carla_env
source ~/carla_env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Download CARLA 0.9.6
wget http://carla-assets-internal.s3.amazonaws.com/Releases/Linux/CARLA_0.9.6.tar.gz
mkdir carla_0.9.6
tar -xvzf CARLA_0.9.6.tar.gz -C carla_0.9.6
cd carla_0.9.6

# Install carla client
cd PythonAPI/carla/dist
rm carla-0.9.6-py3.5-linux-x86_64.egg
wget http://www.cs.utexas.edu/~dchen/lbc_release/egg/carla-0.9.6-py3.5-linux-x86_64.egg
easy_install carla-0.9.6-py3.5-linux-x86_64.egg

```

In addition to the suites used for Carla original benchmarks, we added 3 suites, and different options available from commandline. 
The 3 suites are : `xing_left_right` (10 crossings where the only possible ways are going left or right), `xing_straight_right` (10 crossings where the only possible ways are going straight or right) and `xing_straight_left` (10 crossings where the only possible ways are going straight or left). The option `--command` is used to indicate the driving instructions. Options for `--command` are : baseline (no modification), followlane (driving command will remain followlane), or left, right or straight (driving command provided at all intersections will be left, right or straight)

To check the reaction of our driving agent when arriving at a left-right crossing while the driving command still indicates to go straigh,  run the following : 

Open up a terminal, inside the carla directory run `./CarlaUE4.sh -fps=20 -benchmark` to lauch Carla simulator.

Open another terminal and run `CUDA_VISIBLE_DEVICES="0" python benchmark_robustness.py --suite=xing_left_right --command straight --model_path ./frozen_graphs/frozen_graph.pb --logdir ./logdir/ ` . In the logdir directory you will see the video of our agent reacting to mishap. 

If you want to check that our agent drives correctly when correct command is provided, run  `CUDA_VISIBLE_DEVICES="0" python benchmark_robustness.py --suite=xing_left_right --command baseine --model_path ./frozen_graphs/frozen_graph.pb --logdir ./logdir/ `. You can also replace the suite by the original carla benchmark suites. 

## Results of our agent 

Our agent was trained with end-to-end reinforcement learning from image input. An auxiliary task, namely the prediction of semantic segmentation, was added during training to improve performance and robustness. Below is shown the results of our agent on our robustness benchmark. 

<p align="center">
<img src="https://github.com/CEA-LIST/AD-RobustnessEval/blob/master/figs/table.png" width="1000"/>
</p>

## Reference
If you find this repo to be useful in your research, please consider citing our work
```
[Paper coming soon]
```

## License
This repo is released under the MIT License (please refer to the LICENSE file for details).
Most of the code comes from the repository 
[**Learning by Cheating**](https://github.com/dianchen96/LearningByCheating)
which is under MIT license.
Part of the PythonAPI and the map rendering code is borrowed from the official 
[CARLA](https://github.com/carla-simulator/carla) repo, which is under MIT license.
