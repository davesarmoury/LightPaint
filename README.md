# Light Painting

## Install

    sudo apt install python3-gpiozero
    pip3 install -r requirements.txt

## Usage

    python3 light_painter.py [-h] [--IP IP] [--Image IMAGE] [--Width WIDTH]
                        [--Height HEIGHT] [--Spacing SPACING] [--Rate RATE]
                        [--Speed SPEED] [--Distance DISTANCE]
                        [--Overhang OVERHANG]

    optional arguments:
      -h, --help           show this help message and exit
      --IP IP              IP of the robot
      --Image IMAGE        URI of the image file
      --Width WIDTH        Width of the path (mm)
      --Height HEIGHT      Height of the path (mm)
      --Spacing SPACING    Spacing between parallel passes (mm)
      --Rate RATE          Poling rate (Hz)
      --Speed SPEED        Movement speed (m/s)
      --Distance DISTANCE  Distance from robot world (mm)
      --Overhang OVERHANG  Overhang out the sides of the path (mm)
