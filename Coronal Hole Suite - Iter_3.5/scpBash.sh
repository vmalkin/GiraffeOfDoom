#!/bin/bash

while true; do
# Run the app to generate the data
python3 main.py

echo "Uploading file to webserver"
scp -C forecast.csv  vaughn@128.199.64.101:/var/www/html
scp  -C sun.jpg vaughn@128.199.64.101:/var/www/html
scp -C syntopic.jpg vaughn@128.199.64.101:/var/www/html
scp -C disc_full.bmp vaughn@128.199.64.101:/var/www/html
scp -C regression.php vaughn@128.199.64.101:/var/www/html
scp -C mini_4cast.csv vaughn@128.199.64.101:/var/www/html
echo " "
echo "Done uploading. Pausing..."
sleep 3600

done
