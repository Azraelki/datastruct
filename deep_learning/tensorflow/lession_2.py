import tensorflow as tf
DATA_FILE = 'boston_housing.csv'
BATCH_SIZE = 10
NUM_FEATURES = 14
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mping
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow.contrib.layers as layers
from tensorflow.python import debug as tf_debug

mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)

def sigmaprime(x):
    """sigmod的导数"""
    return tf.multiply(tf.sigmoid(x), tf.subtract(tf.constant(1.0), tf.sigmoid(x)))

def multilayer_perception(x, weights, biases):
    h_layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['h1'])
    out_layer_1 = tf.sigmoid(h_layer_1)
    h_out = tf.matmul(out_layer_1, weights['out']) + biases['out']
    return tf.sigmoid(h_out), h_out, out_layer_1, h_layer_1

def function_1():
    """实现BPN"""
    mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)
    n_input = 784
    n_classes = 10

    # 超参数
    lr = 0.01
    max_epochs = 10000
    batch_size = 10
    seed = 0
    n_hidden = 50

    x_in = tf.placeholder(tf.float32, shape=[None, n_input])
    y = tf.placeholder(tf.float32, shape=[None, n_classes])

    # 定义权重和偏置
    weights = {
        'h1': tf.Variable(tf.random_normal(shape=[n_input, n_hidden], seed=seed)),
        'out': tf.Variable(tf.random_normal(shape=[n_hidden, n_classes], seed=seed))
    }
    biases = {
        'h1': tf.Variable(tf.random_normal(shape=[1, n_hidden], seed=seed)),
        'out': tf.Variable(tf.random_normal(shape=[1, n_classes], seed=seed))
    }
    # 正向传播
    y_hat, h_2, o_1, h_1 = multilayer_perception(x_in, weights, biases)
    # 误差
    err = y - y_hat

    # 反向传播
    delta_2 = tf.multiply(err, sigmaprime(h_2))
    delta_w_2 = tf.matmul(tf.transpose(o_1), delta_2)

    wtd_error = tf.matmul(delta_2, tf.transpose(weights['out']))
    delta_1 = tf.multiply(wtd_error, sigmaprime(h_1))
    delta_w_1 = tf.matmul(tf.transpose(x_in), delta_1)

    eta = tf.constant(lr)
    # 更新权重
    step = [
        tf.assign(weights['h1'], tf.subtract(weights['h1'], tf.multiply(eta, delta_w_1))),
        tf.assign(biases['h1'], tf.subtract(biases['h1'], tf.multiply(eta, tf.reduce_mean(delta_1, axis=[0])))),
        tf.assign(weights['out'], tf.subtract(weights['out'], tf.multiply(eta, delta_w_2))),
        tf.assign(biases['out'], tf.subtract(biases['out'], tf.multiply(eta, tf.reduce_mean(delta_2, axis=[0]))))
    ]
    # 定义精度
    acc_mat = tf.equal(tf.argmax(y_hat, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(acc_mat, tf.float32))

    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init_op)
        for epoch in range(max_epochs):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            sess.run(step, feed_dict={x_in:batch_xs, y:batch_ys})
            if epoch % 1000 == 0:
                acc_train = sess.run(accuracy, feed_dict={x_in:mnist.train.images, y:mnist.train.labels})
                acc_test = sess.run(accuracy, feed_dict={x_in:mnist.test.images, y:mnist.test.labels})
                print('epochs:{}, accuracy train%:{}, accuracy test%:{}'.format(epoch, acc_train/600, acc_test/600))


def function_2():
    """tensorflow属实现多层感知机"""
    n_hidden = 30
    n_classes = 10
    n_input = 784

    batch_size = 200
    eta = 0.001
    max_epoch = 10

    mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)

    x = tf.placeholder(tf.float32, shape=[None, n_input])
    y = tf.placeholder(tf.float32, shape=[None, n_classes])

    fc1 = layers.fully_connected(x, n_hidden, activation_fn=tf.nn.relu, scope='fc1')
    fc2 = layers.fully_connected(fc1, n_hidden, activation_fn=tf.nn.relu, scope='fc2')
    y_hat = layers.fully_connected(fc2, n_classes, activation_fn=None, scope='fc3')

    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=y_hat))
    train = tf.train.GradientDescentOptimizer(eta).minimize(loss)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        for epoch in range(max_epoch):
            epoch_loss = 0.0
            batch_steps = int(mnist.train.num_examples/batch_size)
            for i in range(batch_steps):
                batch_xs, batch_ys = mnist.train.next_batch(batch_size)
                _, l = sess.run([train, loss], feed_dict={x:batch_xs, y:batch_ys})
                epoch_loss += l/batch_steps
            print('epoch:%02d, loss:%.6f' % (epoch, epoch_loss))
        correct_predication = tf.equal(tf.argmax(y_hat, axis=1), tf.argmax(y, axis=1))
        accuracy = tf.reduce_mean(tf.cast(correct_predication, tf.float32))
        print('accuracy%:{}'.format(accuracy.eval({x:mnist.test.images, y:mnist.test.labels})))


def con2d(x, w, b, strides=1):
    x = tf.nn.conv2d(x, w, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)


def max_pool(x, k=2):
    x = tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1], padding='SAME')
    return x


def conv_net(x, weights, biases, drop_out):
    x = tf.reshape(x, shape=[-1, 28, 28, 1])
    conv1 = con2d(x, weights['wc1'], biases['wc1'])
    conv1 = max_pool(conv1)
    conv2 = con2d(conv1, weights['wc2'], biases['wc2'])
    conv2 = max_pool(conv2)

    fc1 = tf.reshape(conv2, shape=[-1, weights['wd1'].get_shape().as_list()[0]])
    fc1 = tf.add(tf.matmul(fc1, weights['wd1']), biases['wd1'])
    fc1 = tf.nn.relu(fc1)
    fc1 = tf.nn.dropout(fc1, drop_out)
    out = tf.add(tf.matmul(fc1, weights['out']), biases['out'])
    return out


def function_3():
    """卷积网络实现手写数字识别"""
    lr = 0.001
    train_iters =500
    batch_size = 128
    display_step = 10


    n_input = 784
    n_classes = 10
    drop_out = 0.85

    x = tf.placeholder(tf.float32, shape=[None, n_input])
    y = tf.placeholder(tf.float32, shape=[None, n_classes])
    keep_prob = tf.placeholder(tf.float32)

    weights = {
        'wc1': tf.Variable(tf.random_normal(shape=[5, 5, 1, 32])),
        'wc2': tf.Variable(tf.random_normal(shape=[5, 5, 32, 64])),
        'wd1': tf.Variable(tf.random_normal(shape=[7*7*64, 1024])),
        'out': tf.Variable(tf.random_normal(shape=[1024, 10]))
    }
    biases = {
        'wc1': tf.Variable(tf.random_normal([32])),
        'wc2': tf.Variable(tf.random_normal([64])),
        'wd1': tf.Variable(tf.random_normal([1024])),
        'out': tf.Variable(tf.random_normal([n_classes])),
    }

    pred = conv_net(x, weights, biases, drop_out)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=pred))
    optimizer = tf.train.GradientDescentOptimizer(lr).minimize(cost)
    correct_pred = tf.equal(tf.argmax(pred, axis=1), tf.argmax(y, axis=1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
    init = tf.global_variables_initializer()

    train_loss = []
    train_acc = []
    test_acc = []

    with tf.Session() as sess:
        sess.run(init)
        step = 1
        while step < train_iters:
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            sess.run(optimizer, feed_dict={x: batch_xs, y: batch_ys, keep_prob: drop_out})
            if step % display_step == 0:
                acc_test = sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels, keep_prob: 1.0})
                print("acc_test:{:.2f}".format(acc_test))
            step += 1



if __name__ == '__main__':
    # function_2()
    # function_1()
    function_3()