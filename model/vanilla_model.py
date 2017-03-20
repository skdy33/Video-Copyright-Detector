# Code by Gunho Choi
# how to use keras pretrained models combined with tensorflow
# Required libraries keras why so many..
import numpy as np
import tensorflow as tf
import time
import matplotlib.pyplot as plt
from keras import backend as K
from keras import optimizers
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D, Convolution2D, Flatten, Reshape
start_time = time.time()

batch_size = 100
epoch = 1

# Feed data with keras image generator
# You can augment data by using this generator
# ex) rotation, zoom, flip..

datagen = image. ImageDataGenerator(featurewise_center=False,
                                    samplewise_center=False,
                                    featurewise_std_normalization=False,
                                    samplewise_std_normalization=False,
                                    zca_whitening=False,
                                    rotation_range=0.,
                                    width_shift_range=0.,
                                    height_shift_range=0.,
                                    shear_range=0.,
                                    zoom_range=0.,
                                    channel_shift_range=0.,
                                    fill_mode='nearest',
                                    cval=0.,
                                    horizontal_flip=False,
                                    vertical_flip=False,
                                    rescale=None,
                                    dim_ordering=K.image_dim_ordering())

# image generator can get a single image or get multiple images form directory
# In my opinion, Generator func. is easier to use compared to tensorflow file reader

generator = datagen.flow_from_directory(directory='/Users/gunho/Laftel/image_crawling/crawler/',
                                        target_size=(256, 256),
                                        color_mode='rgb',
                                        classes=None,
                                        class_mode="categorical",
                                        batch_size=batch_size,
                                        shuffle=False,
                                        seed=None,
                                        save_to_dir=False,
                                        save_prefix=False,
                                        save_format=False)

# create base model with pretrained weights

base_model = InceptionV3(weights='imagenet', include_top=False)

# predict with base model using images generated from generator

pretrained = base_model.predict_generator(generator, val_samples=batch_size)

# Now it's tensorflow time
# with the outputs from pretrained model and generator, do anything you want

layer1 = tf.contrib.layers.conv2d(pretrained, num_outputs=1024, kernel_size=3, stride=1,
                                  padding="VALID", activation_fn=tf.nn.relu,
                                  normalizer_fn=tf.contrib.layers.batch_norm)
layer2 = tf.contrib.layers.conv2d(layer1, num_outputs=1024, kernel_size=3, stride=1,
                                  padding="VALID", activation_fn=tf.nn.relu,
                                  normalizer_fn=tf.contrib.layers.batch_norm)
layer2 = tf.reshape(layer2, shape=[batch_size, -1])

# In order to get the tensorflow part trained, we need optimizing part
# but, I will stop here today :)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)

    for i in range(epoch):
        print(sess.run(tf.shape(layer2)))

print("--- %s seconds ---" % (time.time() - start_time))
