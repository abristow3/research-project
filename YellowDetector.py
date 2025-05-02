import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def prepare_data(train_dir, val_dir):
    # Define ImageDataGenerator for data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,  # Normalize pixel values to [0, 1]
        rotation_range=30,  # Random rotations
        width_shift_range=0.2,  # Random horizontal shifts
        height_shift_range=0.2,  # Random vertical shifts
        shear_range=0.2,  # Random shear transformations
        zoom_range=0.2,  # Random zoom
        horizontal_flip=True,  # Random horizontal flip
        fill_mode='nearest'  # Fill missing pixels after transformations
    )

    val_datagen = ImageDataGenerator(rescale=1. / 255)  # Only rescale for validation

    # Load and batch images from the directories
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(224, 224),  # Resize images to fit MobileNetV2 input size
        batch_size=32,
        class_mode='binary'  # Binary classification: yellowing or healthy
    )

    validation_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(224, 224),
        batch_size=32,
        class_mode='binary'
    )

    return train_generator, validation_generator


def create_model():
    # Load MobileNetV2 pre-trained on ImageNet, excluding the top (classification) layers
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,  # We will add custom classification layers
        weights='imagenet'  # Pre-trained weights
    )

    # Freeze the layers of the base model so they don’t get updated during training
    base_model.trainable = False

    # Add custom layers for binary classification (yellowing vs healthy)
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),  # Pooling layer to reduce the size
        tf.keras.layers.Dense(1, activation='sigmoid')  # Output layer: sigmoid for binary classification
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model


def train_model(model, train_generator, validation_generator, epochs=10):
    # Train the model using the training and validation generators
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // train_generator.batch_size,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // validation_generator.batch_size
    )
    return model


def predict_yellowing(model, image_path):
    # Load and preprocess the image
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = tf.expand_dims(image_array, axis=0)  # Add batch dimension
    image_array = image_array / 255.0  # Normalize the image

    # Make a prediction
    prediction = model.predict(image_array)

    # If prediction > 0.5, it's yellowing; else, it's healthy
    if prediction > 0.5:
        print("The plant has yellowing on its leaves.")
        return True
    else:
        print("The plant does not have yellowing on its leaves.")
        return False


class YellowDetector:
    def __init__(self, model=None):
        self.model = model or self.create_model()

    def create_model(self):
        base_model = tf.keras.applications.MobileNetV2(
            input_shape=(224, 224, 3),
            include_top=False,
            weights='imagenet'
        )
        base_model.trainable = False
        model = tf.keras.Sequential([
            base_model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def train(self, train_generator, validation_generator, epochs=10):
        self.model = train_model(self.model, train_generator, validation_generator, epochs)

    def predict_yellowing(self, image_path):
        return predict_yellowing(self.model, image_path)


train_dir = 'path_to_train_data'
val_dir = 'path_to_validation_data'

# Prepare data
train_generator, val_generator = prepare_data(train_dir, val_dir)

# Create the YellowDetector object
detector = YellowDetector()

# Train the model
detector.train(train_generator, val_generator, epochs=10)

# Check if an image has yellowing
image_path = 'path_to_new_plant_image.jpg'
detector.predict_yellowing(image_path)
