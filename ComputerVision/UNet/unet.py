from functools import partial
from keras.models import Model, Input
from keras.layers import Conv2D, UpSampling2D, MaxPooling2D, Dropout
from keras.layers import Concatenate
from keras.optimizers import Adam


def unet(input_size=(256, 256, 1)):
   
    ## define partial
    my_Conv2D = partial(Conv2D,
                        filters=64,
                        kernel_size=3,
                        strides=1,
                        activation='relu',
                        padding='same',
                        kernel_initializer='he_normal')

    my_Pool2D = partial(MaxPooling2D,
                        pool_size=(2, 2))

    ## inputs
    inputs = Input(input_size)

    ## layer1
    conv1_1 = my_Conv2D(filters=64)(inputs)
    conv1_2 = my_Conv2D(filters=64)(conv1_1)
    pool1 = my_Pool2D()(conv1_2)

    ## layer2
    conv2_1 = my_Conv2D(filters=128)(pool1)
    conv2_2 = my_Conv2D(filters=128)(conv2_1)
    pool2 = my_Pool2D()(conv2_2)

    ## layer3
    conv3_1 = my_Conv2D(filters=256)(pool2)
    conv3_2 = my_Conv2D(filters=256)(conv3_1)
    pool3 = my_Pool2D()(conv3_2)

    ## layer4
    conv4_1 = my_Conv2D(filters=512)(pool3)
    conv4_2 = my_Conv2D(filters=512)(conv4_1)
    drop4 = Dropout(0.5)(conv4_2)
    pool4 = my_Pool2D()(drop4)

    ## layer5
    conv5_1 = my_Conv2D(filters=1024)(pool4)
    conv5_2 = my_Conv2D(filters=1024)(conv5_1)
    drop5 = Dropout(0.5)(conv5_2)

    ## layer6
    up6 = UpSampling2D(size=(2, 2))(drop5)
    conv6_1 = my_Conv2D(filters=512, kernel_size=2)(up6)
    merge6 = Concatenate(axis=3)([drop4, conv6_1])
    conv6_2 = my_Conv2D(filters=512)(merge6)
    conv6_3 = my_Conv2D(filters=512)(conv6_2)

    ## layer7
    up7 = UpSampling2D(size=(2, 2))(conv6_3)
    conv7_1 = my_Conv2D(filters=256, kernel_size=2)(up7)
    merge7 = Concatenate(axis=3)([conv3_2, conv7_1])
    conv7_2 = my_Conv2D(filters=256)(merge7)
    conv7_3 = my_Conv2D(filters=256)(conv7_2)

    ## layer8
    up8 = UpSampling2D(size=(2, 2))(conv7_3)
    conv8_1 = my_Conv2D(filters=128, kernel_size=2)(up8)
    merge8 = Concatenate(axis=3)([conv2_2, conv8_1])
    conv8_2 = my_Conv2D(filters=128)(merge8)
    conv8_3 = my_Conv2D(filters=128)(conv8_2)

    ## layer9
    up9 = UpSampling2D(size=(2, 2))(conv8_3)
    conv9_1 = my_Conv2D(filters=64, kernel_size=2)(up9)
    merge9 = Concatenate(axis=3)([conv1_2, conv9_1])
    conv9_2 = my_Conv2D(filters=64)(merge9)
    conv9_3 = my_Conv2D(filters=64)(conv9_2)
    conv9_4 = my_Conv2D(filters=2)(conv9_3)

    ## outputs
    outputs = my_Conv2D(filters=1, kernel_size=1, activation='sigmoid')(conv9_4)

    ## model
    model = Model(input=inputs, output=outputs)

    ## compile
    model.compile(optimizer=Adam(lr=1e-4),
                  loss='binary_crossentropy', metrics=['accuracy'])

    ## summary
    model.summary()
    
    return model