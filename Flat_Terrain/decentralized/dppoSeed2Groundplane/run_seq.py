import os
import sys
import time
import gym
import gym_gazebo2
import numpy as np
import multiprocessing
import tensorflow as tf

import threading

import statistics

from importlib import import_module
from baselines import bench, logger
from baselines.ppo2 import model as ppo2
from baselines.ppo2 import model as ppo
from baselines.common import set_global_seeds
from baselines.common.vec_env.dummy_vec_env import DummyVecEnv
from baselines.common.vec_env.vec_normalize import VecNormalize
from baselines.common.policies import build_policy

ncpu = multiprocessing.cpu_count()

if sys.platform == 'darwin':
    ncpu //= 2

config = tf.ConfigProto(allow_soft_placement=True,
                        intra_op_parallelism_threads=ncpu,
                        inter_op_parallelism_threads=ncpu,
                        log_device_placement=False)

config.gpu_options.allow_growth = True

tf.Session(config=config).__enter__()

def get_alg_module(alg, submodule=None):
    submodule = submodule or alg
    try:
        # first try to import the alg module from baselines
        alg_module = import_module('.'.join(['baselines', alg, submodule]))
    except ImportError:
        # then from rl_algs
        alg_module = import_module('.'.join(['rl_' + 'algs', alg, submodule]))

    return alg_module

def get_learn_function_defaults(alg, env_type):
    try:
        alg_defaults = get_alg_module(alg, 'defaults')
        kwargs = getattr(alg_defaults, env_type)()
    except (ImportError, AttributeError):
        kwargs = {}
    return kwargs

def constfn(val):
    def f(_):
        return val
    return f

def make_env():
    env = gym.make(defaults['env_name'])
    env.set_episode_size(defaults['nsteps'])
    env = bench.Monitor(env, logger.get_dir() and os.path.join(logger.get_dir()), allow_early_resets=True)

    return env

# Get dictionary from baselines/ppo2/defaults
defaults = get_learn_function_defaults('ppo2', 'phantomx_mlp')

env = gym.make('PhantomX-v0')

set_global_seeds(defaults['seed'])

alg_kwargs ={ 'num_layers': defaults['num_layers'], 'num_hidden': defaults['num_hidden'] }

nenvs = 1


nbatch = nenvs * defaults['nsteps']
nbatch_train = nbatch // defaults['nminibatches']


legs = ['lf', 'lm', 'lr', 'rf', 'rm', 'rr']
models = {}

f= open("dppoTestRun.txt","w+")

def make_leg_model(leg, env):
    leg_env = gym.make('PhantomXLeg-v0')
    leg_env.set_info(env.info)
    leg_env.leg_name = leg
    policy = build_policy(leg_env, defaults['network'], **alg_kwargs)

    model = ppo2.Model(policy=policy, ob_space=leg_env.observation_space, ac_space=leg_env.action_space, nbatch_act=nenvs,
                    nbatch_train=nbatch_train,
                    nsteps=defaults['nsteps'], ent_coef=defaults['ent_coef'], vf_coef=defaults['vf_coef'],
                    max_grad_norm=defaults['max_grad_norm'])
    model.load('' + leg + '/checkpoints/05000')
    return model

for leg in legs:
    models[leg] = make_leg_model(leg, env) #threading.Thread(target=runner, args=(leg, env))
    #models[leg].start()

loop = True
obs = leg_env.reset()
ep_reward = 0
rewards = []
episode = 0
step = 0
while loop:
    step += 1
        action, value_estimate, next_state, neglogp = model.step(obs)
        obs, reward, done, _ = leg_env.step(action[0])
        ep_reward += reward
        if done:
            leg_env.reset()
            episode += 1
            print(step)
            print(ep_reward)
            rewards.append(ep_reward)
            step = 0
            ep_reward = 0
        if episode >= 1:
            break
    f.write("Variance: " + str(np.var(rewards)))
    rewards = np.array(rewards, dtype=float)
    f.write(",Median: " + str(statistics.median(rewards)))
    f.write(",Mean: " + str(np.mean(rewards)))
    f.close()
    while True:
        time.sleep(2)
        break
      #  print("DONE")


for leg in legs:
    models[leg] = threading.Thread(target=runner, args=(leg, env))
    models[leg].start()

loop = True
while loop:
    env.info.execute_action()
    env.info.execute_reset()
    time.sleep(1/1000)

