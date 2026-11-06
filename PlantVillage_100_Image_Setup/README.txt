# PlantVillage 100-image setup pack

This ZIP is a small setup pack, **not the 100 photo files themselves**.
It contains a script that downloads the public PlantVillage dataset and
copies exactly 20 images from each of 5 tomato classes into `dataset/`
(100 real images total).

## Use in VS Code

1. Extract this ZIP inside your crop disease project folder.
2. Open the extracted folder in VS Code.
3. Open Terminal and run:

   `pip install tensorflow-datasets pillow`

4. Run:

   `python create_100_dataset.py`

5. After it finishes, the `dataset/` folder will contain five class folders,
   each with 20 JPG images.

## Important

- Internet is required for the first run.
- TensorFlow Datasets downloads the full source dataset before selecting
  the 100 images, so the initial download can be large.
- Your project's `ml_model/train_model.py` must use these exact class-folder
  names or its dataset path/class handling may need a small adjustment.
- 100 images is only a tiny demo/training subset. It is not enough for a
  reliable real-world disease prediction model.
- PlantVillage dataset source: https://github.com/spMohanty/PlantVillage-Dataset
