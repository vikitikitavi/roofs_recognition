#from __future__ import absolute_import
#from __future__ import division
#from __future__ import print_function
from importFiles import create_roofs_arrays
from importFiles import LEARN
from importFiles import TEST

# Imports
import numpy as np
import tensorflow as tf
flags = tf.app.flags
FLAGS = flags.FLAGS

from tensorflow.contrib import learn
from tensorflow.contrib.learn.python.learn.estimators import model_fn as model_fn_lib

config=tf.ConfigProto()
config.gpu_options.allow_growth=True
config.gpu_options.per_process_gpu_memory_fraction = 0.7


tf.logging.set_verbosity(tf.logging.INFO)

# Our application logic will be added here
def cnn_model_fn(features, labels, mode):
  """Model function for CNN."""
  # Input Layer
  input_layer = tf.reshape(features, [-1, 28, 28, 1])

  # Convolutional Layer #1
  conv1 = tf.layers.conv2d(
      inputs=input_layer,
      filters=32,
      kernel_size=[5, 5],
      padding="same",
      activation=tf.nn.relu)

  # Pooling Layer #1
  pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=1)

  # Convolutional Layer #2 and Pooling Layer #2
  conv2 = tf.layers.conv2d(
      inputs=pool1,
      filters=64,
      kernel_size=[5, 5],
      padding="same",
      activation=tf.nn.relu)
  pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=1)

  # Convolutional Layer #2 and Pooling Layer #3
  conv3 = tf.layers.conv2d(
      inputs=pool2,
      filters=32,
      kernel_size=[3, 3],
      padding="same",
      activation=tf.nn.relu)
  pool3 = tf.layers.max_pooling2d(inputs=conv3, pool_size=[2, 2], strides=1)


  # Dense Layer
  pool3Shape = pool3.get_shape().as_list()
  pool3_flat = tf.reshape(pool3, [-1, pool3Shape[1]*pool3Shape[2]*pool3Shape[3]])
  dense = tf.layers.dense(inputs=pool3_flat, units= pool3Shape[1]*pool3Shape[2]*pool3Shape[3], activation=tf.nn.relu)
  dropout = tf.layers.dropout(
      inputs=dense, rate=0.4, training=mode == learn.ModeKeys.TRAIN)
  # Logits Layer
  logits = tf.layers.dense(inputs=dropout, units=3)

  loss = None
  train_op = None

  # Calculate Loss (for both TRAIN and EVAL modes)
  if mode != learn.ModeKeys.INFER:
    onehot_labels = tf.one_hot(indices=tf.cast(labels, tf.int32), depth=3)
    loss = tf.losses.softmax_cross_entropy(
        onehot_labels=onehot_labels, logits=logits)

  # Configure the Training Op (for TRAIN mode)
  if mode == learn.ModeKeys.TRAIN:
    train_op = tf.contrib.layers.optimize_loss(
        loss=loss,
        global_step=tf.contrib.framework.get_global_step(),
        learning_rate=0.001,
        optimizer="SGD")

  # Generate Predictions
  predictions = {
      "classes": tf.argmax(
          input=logits, axis=1),
      "probabilities": tf.nn.softmax(
          logits, name="softmax_tensor")
  }

  # Return a ModelFnOps object
  return model_fn_lib.ModelFnOps(
      mode=mode, predictions=predictions, loss=loss, train_op=train_op)

def main(unused_argv):
  # Load training and eval data
  flags.DEFINE_string('name', 'main', 'main')

  train_data, train_labels = create_roofs_arrays(LEARN)
  eval_data, eval_labels = create_roofs_arrays(TEST)

  print(train_data.shape)

  metrics = {
      "accuracy":
          learn.MetricSpec(
              metric_fn=tf.metrics.accuracy, prediction_key="classes"),
  }


  validation_monitor = tf.contrib.learn.monitors.ValidationMonitor(
      eval_data,
      eval_labels,
      every_n_steps=2,
      metrics = metrics)

  # Create the Estimator
  classifier = learn.Estimator(
      model_fn=cnn_model_fn,
      model_dir="model4")

  # Set up logging for predictions
  tensors_to_log = {"probabilities": "softmax_tensor"}
  logging_hook = tf.train.LoggingTensorHook(
      tensors=tensors_to_log, every_n_iter=100)



  # Train the model
  classifier.fit(
      x=train_data,
      y=train_labels,
      batch_size=100,
      steps=1000,
      monitors=[ validation_monitor])

  # Configure the accuracy metric for evaluation

  # Evaluate the model and print results
  eval_results = classifier.evaluate(
      x=eval_data, y=eval_labels, metrics=metrics)
  print(eval_results)
  print('a')

if __name__ == "__main__":
  tf.app.run()
