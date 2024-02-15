# The Schelling Board Augmented Reality

This app helps play the Schelling Segregation Model Board Game by using augmented reality.
It helps to play the game by using a phone or a tablet to check the happy and unhappy agents. 

This app is part of the [Transciències project](https://transciencies.wixsite.com/castellano). 
For information on how to get or play the board game, you can visit [this page](https://transciencies.wixsite.com/castellano/blank-3). 
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

## Configurations
To configure the app, you can use the `config.ini` and `.env` files 
located in the `DataApp/` folder. The `.env` file contains database 
connection information, and the variable names begin with "SCHELLING_DB_".
For instance, `SCHELLING_DB_HOST` refers to the database host. These
variables take precedence over the values in the `config.ini` file 
and will override them.

## Database

A database handles the matches and the data persistence. 
To initialize the schema you can run the following command

```bash
cd DataApp
python init_db.py
```


## Train preparation

To train the model, we need first to create a dataset.

## Cell division
We can take a picture of the board and  divide  the grid
into cells. 

For example, if we have a picture of a 21x25 grid, we can run 

`
python Img2Game.py -i data/IMG_20221109_155318_499.jpg  -o IMG_20221109_155318_499_jpg -t -g 21x25`

where `data/IMG_20221109_155318_499.jpg` is the path to the image and `21x25` is the grid size.
The output directory will be `IMG_20221109_155318_499_jpg`

### Labelling
Then we can label  each cell in the output directory in 
5 different classes 
 - Team 1 - happy
 - Team 2 - happy
 - Team 1 - sad
 - Team 2 - sad
 - Empty cell

A simple technique for fast labelling is to move each cell in a directory with the name of the class.

### Train/test split
Then, we need to split the picture into train and test sets. We can do this by running

```splitfolders --output class_data_split --ratio .7 .2 .1 --seed 1234 -- class_data```

from the library https://github.com/jfilter/split-folders


## Contribute

### Install

```bash 
git clone git@github.com:dimitri-mar/SchellingBoardAR.git
cd SchellingBoardAR
pip install -r requirements.txt
``` 

### Translation
Translations for both `stramlit_app.py` and  `streamlit_manager_app.py` are based on gettext.
Texts must be encased as `_(string)`. Take into account that f-strings are not properly implemented.
In case new texts in need of translation are added, the following steps must be taken:

- Create a .pot file with all strings for translation:

   Windows:
   ```
   python "path\pygettext.py" -d base -o DataApp\locales\base.pot DataApp\streamlit_manager_app.py DataApp\stramlit_app.py
   ```
   
   Unix:
   ```
   path/pygettext.py -d base -o DataApp/locales/base.pot DataApp/streamlit_manager_app.py DataApp/stramlit_app.py
   ```

- Update old sources with new strings
  
  Windows:
  ```
  path\msgmerge.exe locales\$language$\LC_MESSAGES\base.pot locales\base.pot -U
  ```
  
  Unix:
  ```
  msgmerge locales/$language$/LC_MESSAGES/base.pot locales/base.pot -U
  ```

- Add new translatations in base.pot file for each language.

- Create new .mo file for updated .pot file in each language

  Windows:
  ```
  "path\msgfmt.exe"-o DataApp\locales\$language$\LC_MESSAGES\base.mo DataApp\locales\$language$\LC_MESSAGES\base.pot
  ```
  
  Unix:
  ```
  msgfmt -o DataApp/locales/$language/LC_MESSAGES/base.mo DataApp/locales/$language/LC_MESSAGES/base.po
  ```
## Acknowledgments
This app is part of the [Transciències project](https://transciencies.wixsite.com/castellano). Please check the website for further information. 

<img src="https://static.wixstatic.com/media/420673_aa6887a292cc4f358d3e2cd187b027a9~mv2.jpg/v1/fill/w_332,h_210,al_c,q_80,usm_0.66_1.00_0.01,enc_auto/Copy%20of%20logo_UBICS.jpg" height="80"> <img src="https://static.wixstatic.com/media/420673_749666e941004a81a5e76e539a04f6ad~mv2.png/v1/fill/w_320,h_160,al_c,lg_1,q_85,enc_auto/Copy%20of%20logoBCNCiencia.png" height="80">  <img src="https://static.wixstatic.com/media/420673_6e692306c05b46d29f7f8da334451651~mv2.png/v1/fill/w_426,h_150,al_c,lg_1,q_85,enc_auto/descarga.png" height="80">


## License

You can redistribute "The Schelling Board Augmented Reality" and/or modify
 it under the terms of the [GNU Affero General Public](LICENSE) License as published
 by the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
All emojis are designed by [OpenMoji](https://openmoji.org/) – the open-source emoji and icon project. License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/#)
