# /*******************************************************
#  * 
#  * Copyright (C) 2015-2016 Kyriakos Naziris <kyriakos@naziris.co.uk>
#  * This is a thesis project of University of Portsmouth.
#  *
#  * This file is part of HomeSecPi.
#  * 
#  * Feel free to use and modify the source code as long as
#  * as you give credits to the original author of the
#  * project (Kyriakos Naziris - kyriakos@naziris.co.uk).
#  *
#  *******************************************************/

#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /home/pi/HomeSecPi
while ! curl http://127.0.0.1:8068 -m1 -o/dev/null -s ; do
  sleep 0.1
  echo "Still loading"
done
sudo python startup.py
echo "Startup Initialazation done. System Ready!"
