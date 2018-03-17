README:
Please have pip and Python 2.7 installed on the machine.

Also, much of the code takes advantage of multi-core processors. It is best to run
this on a machine that has at least 8 cores.

`bash ./run.sh` or `./run.sh` will start the script which will download all of the data,
extract it, and then run it all through the data pipeline and train our final model.
The final model will be located at './data/models/final_rfc_model.bin' and can be
loaded in Python with the pickle module.
