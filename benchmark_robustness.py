import sys
import glob
import os
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
 
from PIL import Image, ImageDraw, ImageFont

from pathlib import Path

from benchmark import make_suite, get_suites, ALL_SUITES

from benchmark.run_benchmark import run_benchmark

import carla
import math
import argparse
import time
import os
import numpy as np
import tensorflow as tf
import bird_view.utils.bz_utils as bzu
from PIL import Image



class TFAgent:
    """Tensorflow Agent from frozen graph"""
    def __init__(self, frozen_graph_path, save_img = False, ep_name = 'episode', big_cam=False):

        with tf.gfile.GFile(frozen_graph_path, "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        with tf.Graph().as_default() as graph:
            tf.import_graph_def(
                graph_def, input_map=None, return_elements=None, name=""
            )

        self.debug=dict()

        self.output = graph.get_tensor_by_name("model/split_2:0")
        self.x = graph.get_tensor_by_name("input/Ob:0")

        self.sess = tf.Session(graph=graph)

        self._increment = 0.05
        self.steer_cache = 0

        if big_cam : 
            self.image_cut = {
                        "top" : 220,
                        "bottom" : 420,
                        "right" : 100,
                        "left" : 700
                    }
        else : 
            self.image_cut = {
                        "top" : 70,
                        "bottom" : 134,
                        "right" : 32,
                        "left" : 224
                    }
        self.image_size = [64,192,3]
        self.save_img = save_img
        self.frame = 0
        self.ep_name = ep_name


    def run_step(self, observations, teaching=False):

        # observations is a dictionnary containing the image (rgb), the speed (velocity) and the driving command (command)

        img = observations["rgb"]  # shape = np.zeros((64,192,3))

        img = img[self.image_cut["top"]:self.image_cut["bottom"], self.image_cut["right"]:self.image_cut["left"]]
        img = np.array(Image.fromarray(img).resize((self.image_size[1], self.image_size[0]), Image.BILINEAR), dtype=np.float32)
        img /= 255.0


        speed = observations["velocity"]
        speed = 3.6 * math.sqrt(speed[0]**2 + speed[1]**2)

        info_layer = np.zeros((64, 192, 1))

        info_layer[0][0] = speed/100  # -> Speed
        info_layer[0][1] = self.steer_cache # -> wheel_angle
        info_layer[0][2] = observations["command"]

        aux_layer = np.zeros((64, 192, 5)) # zero layer to replace the auxiliary prediction in trained model
        observation = np.concatenate((img, info_layer, aux_layer), axis=2) 
        

        obs = np.expand_dims(observation, axis=0)

        action = self.sess.run(self.output, feed_dict={self.x: obs})

        self.action = action[0]


        s = action[0][0]
        tb = action[0][1]

        # Output of our model is the delta of the steering angle, hence the use of a steer cache. 
        steer_increment = self._increment * float(
            np.clip(s, -1, 1)
        ) 
        self.steer_cache += steer_increment
        self.steer_cache = float(np.clip(self.steer_cache, -1, 1))

        steer = float(np.clip(self.steer_cache, -1, 1))
        throttle = float(np.clip(tb, 0, 1))
        brake = float(np.abs(np.clip(tb, -1, 0)))

        control = carla.VehicleControl(throttle=throttle, steer=steer, brake=brake)

        return control


def agent_factory(model_path, big_cam=False):
    return lambda ep_name : TFAgent(model_path, ep_name, big_cam)



def run(model_path, config_path, log_dir, suite, big_cam, seed, autopilot, resume, client, save_img=False, max_run=200, show=False, fps=20, apply_thresh=True, threshold=[15,5], name_save_img='img', command='baseline'):
    model_path = Path(model_path)

    total_time = 0.0

    for suite_name in get_suites(suite):
        print("suite_name = ", suite_name)
        tick = time.time()

        benchmark_dir = Path(log_dir) / model_path.stem / ('%s_cmd_%s_seed%d' % (suite_name, command, seed))
        benchmark_dir.mkdir(parents=True, exist_ok=True)

        with make_suite(suite_name, big_cam=big_cam, client=client, apply_thresh=apply_thresh, threshold=threshold) as env:
           
            agent_maker = agent_factory(str(model_path), big_cam)

            run_benchmark(agent_maker, env, benchmark_dir, seed, autopilot, resume, max_run=max_run, show=show, command=command)

        elapsed = time.time() - tick
        total_time += elapsed

        print('%s: %.3f hours.' % (suite_name, elapsed / 3600))

    print('Total time: %.3f hours.' % (total_time / 3600))


# In[7]:

def main():
    """
    Runs the test
    """
    global logdir

    parser = argparse.ArgumentParser(description='benchmark')

    parser.add_argument('--suite', type=str, default="xing_left_right", help='Suite name')
    parser.add_argument('--port',type=int, help='Simulator ports', default=2000)

    parser.add_argument('--model_path', type=str, default="./frozen_graphs/frozen_graph.pb")
    parser.add_argument('--logdir', type=str, default="./logdir/")


    # driving command. Options are : baseline (no modification), followlane (driving command will remain folowlane), or left, right or straight (command given at the next intersection)
    parser.add_argument('--command', default='baseline') 


    # Allows to change the threshold of the input driving command 
    parser.add_argument('--apply_thresh',type=str, default='True')
    parser.add_argument('--thresh_before', type=int, default=15)
    parser.add_argument('--thresh_after', type=int, default=5) 

    parser.add_argument('--fps', type=int, default=20)

    parser.add_argument('--big_cam',type=str, default='False')

   
    parser.add_argument("--seed", type=int, default=2020)


    args = parser.parse_args()

    if args.apply_thresh in ['True', 'true', 't']: 
        APPLY_THRESH = True
    else:
        APPLY_THRESH = False

    if args.big_cam in ['True', 'true', 't']: 
        BIG_CAM = True
    else:
        BIG_CAM = False

    MODEL_PATH = args.model_path
    LOG_DIR = args.logdir
    CONFIG = "/tf/lbc_checkpoints/config.json"
    SUITE = args.suite

    SEED = args.seed
    AUTOPILOT = False
    RESUME = False

    THRESHOLD = [args.thresh_before, args.thresh_after]

    FPS = args.fps

    client = carla.Client('localhost', args.port)

    client.set_timeout(30.0)

    run(
        MODEL_PATH,
        CONFIG,
        LOG_DIR,
        SUITE,
        BIG_CAM,
        SEED,
        AUTOPILOT,
        RESUME,
        client, 
        max_run=200, 
        fps = FPS, 
        apply_thresh = APPLY_THRESH, 
        threshold = THRESHOLD, 
        command=args.command 

    )

if __name__ == '__main__':
    main()





