import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.examples.tutorials.mnist import input_data
from keras import applications
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten
from keras import optimizers




# mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)

img_width, img_height = 256, 256
batch_size = 5
epochs = 50
train_data_dir = 'D:/work/data/train'
validation_data_dir = 'D:/work/data/validation'
out_category = 1
num_train_samples = 25000
num_validation_samples = 12500


def function_1():
    """vgg_16"""
    base_model = applications.VGG16(weights='imagenet', include_top=False, input_shape=(img_width, img_height, 3))
    print(base_model.summary())
    # 冻结前15层的参数
    for layer in base_model.layers:
        layer.trainable = False
        print(layer.name)
    print('total layer:{}'.format(len(base_model.layers)))
    # 增加自定义顶层用作分类
    top_model = Sequential()
    top_model.add(Flatten(input_shape=base_model.output_shape[1:]))
    top_model.add(Dense(256, activation='relu'))
    top_model.add(Dropout(rate=0.5))
    top_model.add(Dense(out_category, activation='sigmoid'))

    # 创建新网络，组合top和base
    model = Model(inputs=base_model.input, outputs=top_model(base_model.output))
    model.compile(loss='binary_crossentropy', optimizer=optimizers.SGD(lr=0.0001, momentum=0.9), metrics=['accuracy'])

    # 重新开始训练组合模型，保持低15层冻结
    # 使用数据增强
    train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True)
    test_datagen = ImageDataGenerator(rescale=1./255)
    train_generator = train_datagen.flow_from_directory(train_data_dir, target_size=(img_width, img_height),
                                                        batch_size=batch_size, class_mode='binary')
    validation_generator = test_datagen.flow_from_directory(validation_data_dir, target_size=(img_width, img_height),
                                                            batch_size=batch_size, class_mode='binary')
    model.fit_generator(train_generator, steps_per_epoch=num_train_samples//batch_size, epochs=epochs,
                        validation_data=validation_generator, validation_steps=num_validation_samples//batch_size,
                        verbose=2, workers=4)

    score = model.evaluate(validation_generator, num_validation_samples//batch_size)
    scores = model.predict(validation_generator, num_validation_samples//batch_size)

    print(score)
    print(scores)

    pass

def show_array(a):
    a = np.uint8(np.clip(a, 0, 1)*255)
    plt.imshow(a)
    plt.show()



def function_2():
    """deep dream"""
    content_image = 'image/person.jpg'
    img_noise = np.random.uniform(size=(224, 224, 3)) + 100.0
    model_fn = 'D:/work/weights/tensorflow_inception_graph.pb'

    # 加载预训练网络
    graph = tf.Graph()
    sess = tf.InteractiveSession(graph=graph)
    with tf.gfile.FastGFile(model_fn, mode='rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    t_input = tf.placeholder(np.float32, name='input')
    imagenet_mean = 117.0
    t_preprocessed = tf.expand_dims(t_input-imagenet_mean, 0)
    tf.import_graph_def(graph_def, {'input': t_preprocessed})

def function_3():
    """情感分类器"""
    import tflearn
    from tflearn.layers.core import input_data, fully_connected, dropout
    from tflearn.layers.conv import conv_1d, global_max_pool
    from tflearn.layers.merge_ops import merge
    from tflearn.layers.estimator import regression
    from tflearn.data_utils import to_categorical, pad_sequences
    from tflearn.datasets import imdb
    # 加载稀疏向量
    train, test, _ = imdb.load_data('imdb.pkl', n_words=10000, valid_portion=0.1)
    trainX, trainY = train
    testX, testY = test
    # 填充到最大长度
    trainX = pad_sequences(trainX, maxlen=100, value=0.)
    testX = pad_sequences(testX, maxlen=100, value=0.)
    # one-hot encoding
    trainY = to_categorical(trainY, nb_classes=2)
    testY = to_categorical(testY, nb_classes=2)

    # 创建嵌入层
    net_work = input_data(shape=[None, 100], name='input')
    net_work = tflearn.embedding(net_work, input_dim=10000, output_dim=128)

    # 创建卷积网络
    branch_1 = conv_1d(net_work, nb_filter=128, filter_size=3, padding='valid', activation='relu', regularizer='L2')
    branch_2 = conv_1d(net_work, nb_filter=128, filter_size=4, padding='valid', activation='relu', regularizer='L2')
    branch_3 = conv_1d(net_work, nb_filter=128, filter_size=5, padding='valid', activation='relu', regularizer='L2')

    net_work = merge([branch_1, branch_2, branch_3], axis=1, mode='concat')
    net_work = tf.expand_dims(net_work, 2)
    net_work = global_max_pool(net_work)
    net_work = dropout(net_work, keep_prob=0.5)
    net_work = fully_connected(net_work, 2, activation='softmax')

    net_work = regression(net_work, optimizer='adam', learning_rate=0.001, name='target')

    model = tflearn.DNN(net_work, tensorboard_verbose=0)
    model.fit(trainX, trainY, n_epoch=5, shuffle=True, validation_set=(testX, testY), show_metric=True, batch_size=128)


def function_4():
    """vgg网络滤波器"""
    from vis.utils import utils
    from vis.visualization import visualize_activation
    base_model = applications.VGG16(weights='imagenet', include_top=True)
    base_model.summary()

    layer_name = 'predictions'
    layer_idx = [idx for idx, layer in enumerate(base_model.layers) if layer_name == layer.name][0]
    # 在同一层生成三个不同的图像
    vis_images = []
    # 预测层的20代表的是北斗鸟这个类别
    for idx in [20, 20, 20]:
        img = visualize_activation(base_model, layer_idx, filter_indices=idx)
        img = utils.draw_text(img, str(idx))
        vis_images.append(img)

    stitched = utils.stitch_images(vis_images)
    plt.axis('off')
    plt.imshow(stitched)
    plt.title(layer_name)
    plt.show()


if __name__ == '__main__':
    # function_2()
    # function_1()
    # function_3()
    function_4()