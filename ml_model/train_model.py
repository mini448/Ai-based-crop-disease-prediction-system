import os
import json
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATASET = os.path.join(PROJECT_ROOT, 'dataset')
SAVED_MODEL_DIR = os.path.join(PROJECT_ROOT, 'ml_model', 'saved_model')

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

class ModelTrainer:
    def __init__(self, dataset_dir=None, img_size=(224, 224), batch_size=16):
        self.dataset_dir = dataset_dir or DEFAULT_DATASET
        self.img_size = img_size
        self.batch_size = batch_size
        self.model = None
        self.class_indices = None
        self.num_classes = None
        os.makedirs(SAVED_MODEL_DIR, exist_ok=True)

    def _dataset_info(self):
        info = {'classes': {}, 'total': 0, 'demo_files': 0}
        if not os.path.isdir(self.dataset_dir):
            return info
        for name in sorted(os.listdir(self.dataset_dir)):
            d = os.path.join(self.dataset_dir, name)
            if not os.path.isdir(d):
                continue
            files = [f for f in os.listdir(d) if f.lower().endswith(('.jpg','.jpeg','.png'))]
            demo = [f for f in files if '_demo' in f.lower()]
            info['classes'][name] = len(files)
            info['total'] += len(files)
            info['demo_files'] += len(demo)
        info['is_demo_dataset'] = info['total'] > 0 and info['demo_files'] == info['total']
        return info
        
    def prepare_data_generators(self):
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=25,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest',
            validation_split=0.2
        )
        self.train_generator = train_datagen.flow_from_directory(
            self.dataset_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        self.validation_generator = train_datagen.flow_from_directory(
            self.dataset_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )
        self.class_indices = self.train_generator.class_indices
        self.num_classes = len(self.class_indices)
        print(f'Number of classes: {self.num_classes}')
        print(f'Class indices: {self.class_indices}')
        ds = self._dataset_info()
        if ds.get('is_demo_dataset'):
            print('\nWARNING: Dataset contains only *_demo* placeholder images. The trained model will NOT reliably detect real diseases. Run PlantVillage_100_Image_Setup/create_100_dataset.py to generate real images, then retrain.\n')
        return self.train_generator, self.validation_generator
    
    def build_model(self):
        base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(*self.img_size, 3))
        for layer in base_model.layers:
            layer.trainable = False
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dropout(0.4)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.3)(x)
        predictions = Dense(self.num_classes, activation='softmax')(x)
        self.model = Model(inputs=base_model.input, outputs=predictions)
        self.model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.summary()
        return self.model
    
    def train(self, epochs=20):
        model_path = os.path.join(SAVED_MODEL_DIR, 'crop_disease_model.h5')
        history = self.model.fit(
            self.train_generator,
            epochs=epochs,
            validation_data=self.validation_generator,
            callbacks=[
                ModelCheckpoint(model_path, monitor='val_accuracy', save_best_only=True, mode='max', verbose=1),
                EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True, verbose=1),
                ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=4, min_lr=1e-6, verbose=1),
            ],
            verbose=1
        )
        with open(os.path.join(SAVED_MODEL_DIR, 'class_indices.json'), 'w') as f:
            json.dump(self.class_indices, f, indent=2)
        ds = self._dataset_info()
        meta = {
            'dataset_dir': self.dataset_dir,
            'num_classes': self.num_classes,
            'class_indices': self.class_indices,
            'is_demo_dataset': ds.get('is_demo_dataset', False),
            'total_images': ds.get('total', 0),
            'demo_files': ds.get('demo_files', 0),
            'note': 'Demo dataset: predictions are not reliable for real leaf images.' if ds.get('is_demo_dataset') else 'Trained on dataset images present at training time.',
        }
        with open(os.path.join(SAVED_MODEL_DIR, 'model_metadata.json'), 'w') as f:
            json.dump(meta, f, indent=2)
        print('Model, class indices, and metadata saved')
        return history
    
    def evaluate(self):
        test_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
        test_generator = test_datagen.flow_from_directory(
            self.dataset_dir, target_size=self.img_size, batch_size=self.batch_size,
            class_mode='categorical', subset='validation', shuffle=False
        )
        if self.model is None:
            self.model = tf.keras.models.load_model(os.path.join(SAVED_MODEL_DIR, 'crop_disease_model.h5'))
        predictions = self.model.predict(test_generator, verbose=0)
        y_pred = np.argmax(predictions, axis=1)
        y_true = test_generator.classes
        labels = list(test_generator.class_indices.keys())
        print('\\n=== CLASSIFICATION REPORT ===')
        print(classification_report(y_true, y_pred, target_names=labels, zero_division=0))
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
        plt.title('Confusion Matrix'); plt.ylabel('True Label'); plt.xlabel('Predicted Label')
        plt.xticks(rotation=45, ha='right'); plt.tight_layout()
        plt.savefig(os.path.join(SAVED_MODEL_DIR, 'confusion_matrix.png')); plt.close()
        print('Confusion matrix saved')

if __name__ == '__main__':
    trainer = ModelTrainer()
    trainer.prepare_data_generators()
    trainer.build_model()
    trainer.train(epochs=20)
    trainer.evaluate()
