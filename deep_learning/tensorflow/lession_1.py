import tensorflow as tf
DATA_FILE = 'boston_housing.csv'
BATCH_SIZE = 10
NUM_FEATURES = 14
import numpy as np
import matplotlib.pyplot as plt

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

if __name__ == '__main__':
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
            total.append(total_loss/n_sample)
            print('Epoch:{}, Loss:{}'.format(i, total_loss/n_sample))

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
