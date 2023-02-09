import os
import glob
import pandas as pd
rootdir="/home/pogoda/UAM/dokt/dev/pko-ekstraklasaPL1"
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print(os.path.join(subdir, file))