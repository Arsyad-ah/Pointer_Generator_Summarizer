# -*- coding: utf-8 -*-
"""pointer_gen_train_test_eval.ipynb

Automatically generated by Colaboratory.

"""

import numpy as np
import random
import tensorflow as tf
import tensorflow.nn as nn
import time

def get_config():
  """Returns config for tf.session"""
  config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=True)
  config.gpu_options.allow_growth = True
  return config


def run_training(model, batcher, hpm, training_steps):
  with tf.train.MonitoredTrainingSession(checkpoint_dir = "/content/gdrive/My Drive/pointer_gen/checkpoints/",
                                        hooks = [tf.train.StopAtStepHook(last_step=training_steps)],
                                        save_summaries_steps = None, save_summaries_secs= None,
                                        save_checkpoint_steps=10, scaffold=tf.train.Scaffold(saver=tf.train.Saver(max_to_keep=8)),
                                        config = get_config()) as sess:
    
    model.setSession(sess)
    while not sess.should_stop():
      t0=time.time()
      batch = batcher.next_batch()
      results = model.train(batch)
      t1=time.time()

      if hpm['coverage']:
        coverage_loss= results['coverage_loss']
      else:
      	coverage_loss = None

      tf.logging.info('step : %d, seconds : %.3f, loss : %f, coverage loss: %f', results['global_step'], t1-t0, results['loss'], coverage_loss)
            
      if not np.isfinite(results['loss']):
        raise Exception('loss is not finite. Stopping!')
        
      
      
      


def restore_model(sess, hpm, model_path=None, check_path=None):
  assert  ( model_path or check_path)
  saver = tf.train.Saver()
  try:
    if model_path:
      saver.restore(sess, model_path)
      return True
    else:
      saver.restore(sess, tf.train.latest_checkpoint(check_path))
      return True
  except Exception as e:
    tf.logging.error(e)
    tf.logging.warning("Cannot restore model !!!")
    return False
    
def total_num_params():
  total_parameters = 0
  for variable in tf.trainable_variables():
    # shape is an array of tf.Dimension
    shape = variable.get_shape()
    print(variable)
    print("shape :", shape)
    variable_parameters = 1
    for dim in shape:
      variable_parameters *= dim.value
    print("parameters : ",variable_parameters)
    total_parameters += variable_parameters
  return total_parameters