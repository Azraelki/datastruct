import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.examples.tutorials.mnist import input_data
from keras import applications
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten
from keras import optimizers

from keras.applications import ResNet50
from keras.applications import InceptionV3
from keras.applications import Xception
from keras.applications import VGG16
from keras.applications import VGG19
from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from matplotlib.pyplot import imshow
from PIL import Image

MODELS = {
    'vgg16':(VGG16, (224, 224)),
    'vgg19':(VGG19, (224, 224)),
    'inspection':(InceptionV3, (299, 299)),
    'xception':(Xception, (299, 299)),
    'resnet':(ResNet50, (224, 224))
}


def image_load_and_convert(image_path, model):
    """定义加载和转换图像的辅助函数"""
    pil_im = Image.open(image_path, 'r')
    imshow(np.asarray(pil_im))
    # 初始化图片的输入形状
    input_shape = MODELS[model][1]
    # 初始化预处理函数
    preprocess = imagenet_utils.preprocess_input
    image = load_img(image_path, target_size=input_shape)
    image = img_to_array(image)
    # 预训练的模型有样本数量/批大小 这一维度，我们为单张图片增加此维度，和训练时保持一致
    image = np.expand_dims(image, axis=0)
    image = preprocess(image)
    return image


def classify_image(image_path, model):
    """定义辅助函数，进行图像预测并显示前5的概率"""
    img = image_load_and_convert(image_path, model)
    Network = MODELS[model][0]
    model = Network(weights='imagenet')
    preds = model.predict(img)
    p = imagenet_utils.decode_predictions(preds)
    # 循环展示预测的前五和概率值
    for (i, (imagenetId, label, prob)) in enumerate(p[0]):
        print("{}. {}. {:.2f}%".format(i+1, label, prob*100))


def print_model(model):
    """打印模型详情"""
    print('model:',model)
    Network = MODELS[model][0]
    model = Network(weights='imagenet')
    model.summary()


def function_1():
    """抽取网络某层的特征"""
    from keras.applications.vgg16 import preprocess_input
    from keras.preprocessing import image
    from keras.models import Model
    base_model = applications.VGG16()
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('block4_pool').output)
    image = load_img('D:/work/data/train/0/cat.1.jpg', target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    features = model.predict(image)
    print(features)


if __name__ == '__main__':
    function_1()
    # for key in list(MODELS.keys())[2:]:
    #     # classify_image('D:/work/data/train/0/cat.1.jpg', key)
    #     print_model(key)
