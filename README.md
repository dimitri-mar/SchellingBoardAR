# The Schelling Board Augmented Reality

This app helps to play Schelling Segregation Model Table Game by using Augmented Reality.
It helps to play the game by using a phone or a tablet to check the happy and unhappy agents. 


## Launch app

You can launch the app using docker. 

```bash
docker build -t schellingar_st_1_20_0 . 
docker run -d --restart unless-stopped -p 8501:8501 \ 
        -v ./data:/app/DataApp/data --name schellingar \
        schellingar_st_1_20_0 
```
where the `data` folder helps to keep the data persistent on the disk. 

You can then access the app at http://localhost:8501



## Train preparation

To train the model we need to first create a dataset.lknlkn

## Cell division
We can take a picture of the table and  divide  the grid
into cells. 

For example if we have a picture of a 21x25 grid we can run 

`
python Img2Game.py -i data/IMG_20221109_155318_499.jpg  -o IMG_20221109_155318_499_jpg -t -g 21x25`

where `data/IMG_20221109_155318_499.jpg` is the path to the image and `21x25` is the grid size.
the output directory will be `IMG_20221109_155318_499_jpg`

### Labelling
Then we can label  each cell in the output directory in 
5 different classes 
 - Team 1 - happy
 - Team 2 - happy
 - Team 1 - sad
 - Team 2 - sad
 - Empty cell

A simple tecnique for fast labeling is to move each cell in a directory with the name of the class.

### Train/test split
Then we need to split the picture in train and test set. We can do this by running

```splitfolders --output class_data_split --ratio .7 .2 .1 --seed 1234 -- class_data```

from the library https://github.com/jfilter/split-folders


## Contribute

### Install

```bash 
git clone git@github.com:dimitri-mar/SchellingBoardAR.git
cd SchellingBoardAR
pip install -r requirements.txt
``` 


## License

You can redistribute "The Schelling Board Augmented Reality" and/or modify
 it under the terms of the [GNU Affero General Public](LICENSE) License as published
 by the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
All emojis designed by [OpenMoji](https://openmoji.org/) – the open-source emoji and icon project. License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/#)
