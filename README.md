# Schelling Segregation Model Table Game Parser

# Train preparation

To train the model we need to first create a dataset.lknlkn

## Cell division
We can take a picture of the table and  divide  the grid
into cells. 

For example if we have a picture of a 21x25 grid we can run 

`
python Img2Game.py -i data/IMG_20221109_155318_499.jpg  -o IMG_20221109_155318_499_jpg -t -g 21x25`

where `data/IMG_20221109_155318_499.jpg` is the path to the image and `21x25` is the grid size.
the output directory will be `IMG_20221109_155318_499_jpg`

## Labelling
Then we can label  each cell in the output directory in 
5 different classes 
 - Team 1 - happy
 - Team 2 - happy
 - Team 1 - sad
 - Team 2 - sad
 - Empty cell

A simple tecnique for fast labeling is to move each cell in a directory with the name of the class.

## Train/test split
Then we need to split the picture in train and test set. We can do this by running

```splitfolders --output class_data_split --ratio .7 .2 .1 --seed 1234 -- class_data```

from the library https://github.com/jfilter/split-folders


# Contribute

## Install

```bash 
git clone git@github.com:dimitri-mar/SchellingBoardAR.git
cd SchellingBoardAR
pip install -r requirements.txt
``` 


