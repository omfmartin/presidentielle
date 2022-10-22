import tensorflow as tf

def create_model(
        input_shape: int,
        output_shape: int,
        hidden_shape: int,
        hidden_n_layers: int,
        batch_norm: bool = False,
        activation="selu",
        kernel_initializer='lecun_normal',
        optimizer="adam",
        loss=tf.keras.losses.kl_divergence):
        
    '''Create neural network model.'''

    model = tf.keras.Sequential()

    model.add(tf.keras.layers.Dense(
        input_shape,
        activation=activation,
        kernel_initializer=kernel_initializer))

    if batch_norm:
        model.add(tf.keras.layers.BatchNormalization())

    for _ in range(hidden_n_layers):
        model.add(tf.keras.layers.Dense(
            hidden_shape,
            activation=activation,
            kernel_initializer=kernel_initializer))
        if batch_norm:
            model.add(tf.keras.layers.BatchNormalization())

    model.add(tf.keras.layers.Dense(
        output_shape,
        activation="softmax",
        kernel_initializer=kernel_initializer))

    model.compile(optimizer=optimizer, loss=loss)

    return model
