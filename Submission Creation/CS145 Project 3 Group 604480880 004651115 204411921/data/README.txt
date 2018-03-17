Please have pip and Python 2.7 installed on the machine.

bash ./run.sh or ./run.sh will start the script which will download all of the data, extract it, and then run it all through the data pipeline and train our final model. The final model will be located at './data/models/final_rfc_model.bin' and can beloaded in Python with the pickle module.

Data is downloaded from http://www.wsdm-cup-2017.org/vandalism-detection.

Note that currently nothing is provided in this folder, as the base data collected totaled more than 20 gigabytes compressed. There is also an assumption that you have the capacity to decompress .7z files on the command line. For windows, the command to do so is available for download at https://sevenzip.osdn.jp/chm/cmdline/. For Linux, you may have to install it. 

Data ends up stored in the ./data folder of the folder you run the run.sh script from. 

As a note, the assumption used during the creation of this project is that data would be downloaded in the current directory of the code. The run script as it currently exists also currently does the downloading necessary to obtain this data. Since this data expanded totals more than 500 gigabytes, please be careful where you run this code. We ran this code on a Google Cloud instance.  
