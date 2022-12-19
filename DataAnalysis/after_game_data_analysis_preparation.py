import click
from loguru import logger

import os
from glob import glob

import hashlib
import shutil

import numpy as np
import pandas as pd
import re

from PIL import Image
from PIL.ExifTags import TAGS


@click.group()
def control():
    """ manage the image processing pipeline """
    pass


def parse_folder_name(folder_name):
    # the folder is composed by  "app_" +  md5 hash + "_" + a timestamp
    # we want to extract both the hash and the timestamp
    # the hash is 32 characters long
    # the timestamp is 14 characters long
    # the folder name is 48 characters long
    # so we can extract the hash and the timestamp by slicing the string
    # the hash is the first 32 characters
    # the timestamp is the float of 10 digits and 6 decimals
    assert len(folder_name) == 54, "folder name is not 48 characters long"
    assert re.match(r"app_[a-f0-9]{32}_[0-9]{10}\.[0-9]{6}", folder_name), "folder name does not match the pattern"

    hash = folder_name[4:36]
    timestamp = folder_name[37:]
    logger.info("processing folder: " + folder_name)
    logger.debug(f"hash: {hash}")
    logger.debug(f"timestamp: {timestamp}")




    return hash, float(timestamp)


def parse_dir_path(dir_path, deep=False, deep_deep=False):
    """Parse directory path

    Args:
        dir_path: directory path

    Returns:
        list of file paths

    """
    logger.info("parsing directory path: " + dir_path)
    if deep:
        logger.info("in mode deep")
        if deep_deep:
            logger.info("and deep_deep")

    # find all folders in dir_path
    all_files_in_team_dir = glob(os.path.join(dir_path, "*"))
    # find all folders
    # check that the folder name respect the pattern with a regular expression
    pattern = re.compile(r"app_[a-f0-9]{32}_[0-9]{10}\.[0-9]{6}")

    all_folders_in_team_dir = [f for f in all_files_in_team_dir if
                               os.path.isdir(f) and pattern.match(
                                   os.path.basename(f))]
    # if empty raise error
    if len(all_folders_in_team_dir) == 0:
        raise FileNotFoundError("No folders found in " + dir_path)


    upload_info_lst = []

    for folder in all_folders_in_team_dir:
        logger.debug("processing folder: " + folder)

        upload_info = {}
        folder_name = os.path.basename(folder)
        logger.debug("folder name length " + str(len(folder_name)))

        hash, timestamp = parse_folder_name(folder_name)

        # each folder should contain a picture and a txt file
        # the picture should have the same hash of the folder name

        all_files_in_upload_dir = glob(os.path.join(folder, "*"))

        def get_hash_of_file(x):
            with open(x, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()

        hash_all_files_in_folder = [get_hash_of_file(f) for f in
                                    all_files_in_upload_dir]

        # the hash belongs to the picture
        try:
            image_ix = hash_all_files_in_folder.index(hash)
        except ValueError:
            logger.error(f"hash {hash} not found in folder {folder}")
            raise ValueError

        image_path = all_files_in_upload_dir[image_ix]
        image_file_name = os.path.basename(image_path)

        # the txt file is called "timestamp.txt"
        with open(os.path.join(folder, "timestamp.txt")) as f:
            timestamp_from_file = float(f.read())

        assert timestamp == timestamp_from_file, "timestamp mismatch"

        upload_info["hash"] = hash
        upload_info["timestamp"] = timestamp
        upload_info["image_path"] = image_path
        upload_info["image_file_name"] = image_file_name

        if deep or deep_deep:
            image = Image.open(image_path)
            info_dict = {
                "Image Size": image.size,
                "Image Height": image.height,
                "Image Width": image.width,
                "Image Format": image.format,
                "Image Mode": image.mode,
                "Image is Animated": getattr(image, "is_animated", False),
                "Frames in Image": getattr(image, "n_frames", 1)
            }

            if deep_deep:
                exifdata = image.getexif()
                if exifdata:
                    for tag_id in exifdata:
                        # get the tag name, instead of human unreadable tag id
                        tag = TAGS.get(tag_id, tag_id)
                        data = exifdata.get(tag_id)
                        # decode bytes
                        if isinstance(data, bytes):
                            data = data.decode()

                        info_dict[tag] = data

            upload_info.update(info_dict)
        upload_info_lst.append(upload_info)


    all_files_timeseries = pd.DataFrame().from_records(upload_info_lst)
    print(all_files_timeseries.head())
    all_files_timeseries = all_files_timeseries.sort_values("timestamp")
    all_files_timeseries = all_files_timeseries.reset_index()
    all_files_timeseries["datetime"] = \
        pd.to_datetime(all_files_timeseries["timestamp"], unit="s", utc=True)\
            .dt.tz_convert(tz='Europe/Rome')

    return all_files_timeseries



@control.command()
@click.argument("team_dir", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path(exists=False))
@click.option("--team_name", type=str, default="")
@click.option("--copy_images", is_flag=True, type=bool, default=False)
@click.option("--deep", is_flag=True, help="include image properties")
@click.option("--deep_deep", is_flag=True, help="include image metadata")
def build_timeline(team_dir, output_dir, team_name, copy_images, deep, deep_deep):
    """Build timeline

    Args:
        team_dir: team directory
        output_dir: output directory

    Returns:
        None

    """
    # if output dir does not exist, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_files_timeseries = parse_dir_path(team_dir, deep=deep,
                                          deep_deep=deep_deep)

    all_files_timeseries.to_pickle(os.path.join(output_dir,
                                    f"{team_name}_all_files_timeseries.pkl"))

    all_files_timeseries.to_csv(
        os.path.join(output_dir, f"{team_name}_timeline.csv"), escapechar="\\")

    logger.info(f"Timeline saved to {output_dir}")

    if copy_images:
        for ix, row in all_files_timeseries.iterrows():
            image_path = row["image_path"]
            image_filename = row["image_file_name"]

            image_upload_time_str = row["datetime"].strftime("%Y%m%d_%H:%M.%S.%f")
            new_filename = f"{image_upload_time_str}_{image_filename}"
            shutil.copy(image_path, os.path.join(output_dir, new_filename))



if __name__ == "__main__":
    import sys

    sys.path.append("..")

    control()
