# sendSensorData

This programme executes system command `sensors -Aj` from a JS code to get various sensor information and then process the same and upload it using `uploadToGoogleSheets.py` programme.

## STEPS:
Run `node /path/to/sendSensorData.js` file. As in my case I have set up a cron job at every 1 minute which executes `node /home/plusx/sendSensorData/sendSensorData.js` and hence updates the google spreadsheet file.
