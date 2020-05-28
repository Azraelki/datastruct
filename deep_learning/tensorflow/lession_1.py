import tensorflow as tf
DATA_FILE = 'boston_housing.csv'
BATCH_SIZE = 10
NUM_FEATURES = 14
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mping
from tensorflow.examples.tutorials.mnist import input_data

def data_generator(filename):
    f_queue = tf.train.string_input_producer(filename)
    reader = tf.TextLineReader(skip_header_lines=1)
    _, value = reader.read(f_queue)

    record_defaults = [[0.0] for _ in range(NUM_FEATURES)]
    data = tf.decode_csv(value, record_defaults=record_defaults)
    features = tf.stack(tf.gather_nd(data, [[5], [10], [12]]))
    label = data[-1]

    dequeuemin_after_dequeue = 10 * BATCH_SIZE
    capacity = 20 * BATCH_SIZE

    feature_batch, label_batch = tf.train.shuffle_batch([features, label], batch_size=BATCH_SIZE,
                                                        capacity=capacity, min_after_dequeue=dequeuemin_after_dequeue)

    return feature_batch, label_batch


def generate_data(feature_batch, label_batch):
    with tf.Session() as sess:
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        for _ in range(5):
            features, labels = sess.run([feature_batch, label_batch])
            print(features, "HI")
        coord.request_stop()
        coord.join(threads)


def normalize(X):
    """归一化"""
    mean = np.mean(X)
    std = np.std(X)
    X = (X - mean) / std
    return X

def function_1():
    """
    简单线性回归
    :return:
    """
    # feature_batch, label_batch = data_generator([DATA_FILE])
    # generate_data(feature_batch, label_batch)
    boston = tf.contrib.learn.datasets.load_dataset('boston')
    x_train, y_train = boston.data[:, 5], boston.target
    x_train = normalize(x_train)
    n_sample = len(x_train)

    X = tf.placeholder(tf.float32, name='X')
    Y = tf.placeholder(tf.float32, name='y')

    w = tf.Variable(0.0)
    b = tf.Variable(0.0)

    y_hat = w * X + b

    loss = tf.square(y_hat - Y)

    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(loss)

    init_op = tf.global_variables_initializer()

    total = []

    with tf.Session() as sess:
        sess.run(init_op)
        writer = tf.summary.FileWriter('graphs', sess.graph)
        for i in range(100):
            total_loss = 0
            for x, y in zip(x_train, y_train):
                _, l = sess.run([optimizer, loss], feed_dict={X: x, Y: y})
                total_loss += l
            total.append(total_loss / n_sample)
            print('Epoch:{}, Loss:{}'.format(i, total_loss / n_sample))

        writer.close()
        b_value, w_value = sess.run([b, w])

    y_pred = x_train * w_value + b_value
    print('done')
    plt.plot(x_train, y_train, 'bo', label='real data')
    plt.plot(x_train, y_pred, 'r', label='pred data')
    plt.legend()
    plt.show()
    plt.plot(total)
    plt.show()


def append_bias_reshape(features, labels):
    m = features.shape[0]
    n = features.shape[1]
    x = np.reshape(np.c_[np.ones(m), features], (m, n+1))
    y = np.reshape(labels, (m, 1))
    return x, y


def function_2():
    """多元线性回归"""
    boston = tf.contrib.learn.datasets.load_dataset('boston')
    x_train, y_train = boston.data, boston.target
    x_train = normalize(x_train)
    x_train, y_train = append_bias_reshape(x_train, y_train)
    m = len(x_train)
    n = 13 + 1

    x = tf.placeholder(tf.float32, name='x', shape=(m, n))
    y = tf.placeholder(tf.float32, name='y')

    w = tf.Variable(tf.random_normal((n, 1)))

    y_hat = tf.matmul(x, w)

    loss = tf.reduce_mean(tf.square(y_hat-y, name='loss'))

    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(loss)

    init_op = tf.global_variables_initializer()
    total = []

    with tf.Session() as sess:
        sess.run(init_op)
        writer = tf.summary.FileWriter("graphs", sess.graph)
        for i in range(100):
            _, l = sess.run([optimizer, loss], feed_dict={x: x_train, y: y_train})
            total.append(l)
            print('epoch:{}, loss:{}'.format(i, l))
        writer.close()
        w_value = sess.run([w])
    plt.plot(total)
    plt.show()


def function_3():
    """逻辑斯蒂回归，手写数字识别"""
    mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)

    x = tf.placeholder(tf.float32, name='x', shape=(None, 784))
    y = tf.placeholder(tf.float32, name='y', shape=(None, 10))

    w = tf.Variable(tf.zeros((784, 10)), name='w')
    b = tf.Variable(tf.zeros(10), name='b')

    with tf.name_scope('wx_b') as scope:
        y_hat = tf.nn.softmax(tf.matmul(x, w) + b)
    w_h = tf.summary.histogram('weights', w)
    b_h = tf.summary.histogram('bias', b)

    with tf.name_scope('cross-entropy') as scope:
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=y_hat))
        tf.summary.scalar('loss', loss)

    with tf.name_scope('train') as scope:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(loss)
    init_op = tf.global_variables_initializer()
    merge_all_op = tf.summary.merge_all()

    with tf.Session() as sess:
        sess.run(init_op)
        summary_writer = tf.summary.FileWriter('graphs', sess.graph)
        for epoch in range(100):
            loss_avg = 0
            num_of_batch = int(mnist.train.num_examples/100)
            for i in range(num_of_batch):
                batch_xs, batch_ys = mnist.train.next_batch(100)
                _, l, summary_str = sess.run([optimizer, loss, merge_all_op], feed_dict={x: batch_xs, y: batch_ys})
                loss_avg += l
                summary_writer.add_summary(summary_str, epoch*num_of_batch+1)
            loss_avg = loss_avg/num_of_batch
            print('epoch:{}, loss:{}'.format(epoch, loss_avg))
        print('done')


if __name__ == '__main__':
    # function_2()
    function_3()