# Light Painting

## Install

    sudo apt install python3-gpiozero python3-pip libboost-all-dev
    pip3 install -r requirements.txt

If you are on raspberry pi, installing the rtde module will likely fail.  Build it from source

## Usage

    python3 light_painter.py [-h] [--IP IP] [--Image IMAGE] [--Width WIDTH] [--Height HEIGHT] [--Spacing SPACING] [--Rate RATE] [--Speed SPEED] [--Distance DISTANCE] [--Overhang OVERHANG]

    optional arguments:
      -h, --help           show this help message and exit
      --IP IP              IP of the robot
      --Image IMAGE        URI of the image file
      --Width WIDTH        Width of the path (m)
      --Height HEIGHT      Height of the path (m)
      --Spacing SPACING    Spacing between parallel passes (m)
      --Rate RATE          Poling rate (Hz)
      --Speed SPEED        Movement speed (m/s)
      --Distance DISTANCE  Distance from robot world (m)
      --Overhang OVERHANG  Overhang out the sides of the path (m)
