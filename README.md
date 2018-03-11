# cs145project

As a note, I have structured my file system as follows: 



For your downloading pleasure (to be run at the root of the git project)

```
mkdir data
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2012_10.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2012_11.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2013_01.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2013_03.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2013_05.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2013_07.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2013_09.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2013_11.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2014_01.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2014_03.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2014_05.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2014_07.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2014_09.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2014_11.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2015_01.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2015_03.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2015_05.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2015_07.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2015_09.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2015_11.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_2016_01.xml.7z
wget -P ./data/ http://www.uni-weimar.de/medien/webis/corpora/corpus-wdvc-16/training/wdvc16_meta.csv.7z

```
download.sh is a script for the above. 

If you have  7za (yes, i have both wget and 7za on a windows machine shut up), then run:
```
7za e ./data/wdvc16_2012_10.xml.7z -odata
7za e ./data/wdvc16_2012_11.xml.7z -odata
7za e ./data/wdvc16_2013_01.xml.7z -odata
7za e ./data/wdvc16_2013_03.xml.7z -odata
7za e ./data/wdvc16_2013_05.xml.7z -odata
7za e ./data/wdvc16_2013_07.xml.7z -odata
7za e ./data/wdvc16_2013_09.xml.7z -odata
7za e ./data/wdvc16_2013_11.xml.7z -odata
7za e ./data/wdvc16_2014_01.xml.7z -odata
7za e ./data/wdvc16_2014_03.xml.7z -odata
7za e ./data/wdvc16_2014_05.xml.7z -odata
7za e ./data/wdvc16_2014_07.xml.7z -odata
7za e ./data/wdvc16_2014_09.xml.7z -odata
7za e ./data/wdvc16_2014_11.xml.7z -odata
7za e ./data/wdvc16_2015_01.xml.7z -odata
7za e ./data/wdvc16_2015_03.xml.7z -odata
7za e ./data/wdvc16_2015_05.xml.7z -odata
7za e ./data/wdvc16_2015_07.xml.7z -odata
7za e ./data/wdvc16_2015_09.xml.7z -odata
7za e ./data/wdvc16_2015_11.xml.7z -odata
7za e ./data/wdvc16_2016_01.xml.7z -odata
7za e ./data/wdvc16_meta.csv.7z -odata
```

If you have linux, [p7zip](http://p7zip.sourceforge.net/) seems to operate similarly. I haven't tested it.