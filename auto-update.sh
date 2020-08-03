#!/bin/bash

if [[ -z $(urlwatch) ]]; then

  echo $(date -u) "Nothing changed." >> ~/covid-hyogo/updater.log 2>&1

else

  echo $(date -u)  "Something changed." >> ~/covid-hyogo/updater.log 2>&1

  cd ~/covid-hyogo

  # Update Google Spreadsheet
  python3 ~/covid-hyogo/src/updater/updateGoogleSheet.py >> ~/covid-hyogo/updater.log 2>&1

  # Update local json data
  yarn scrape >> ~/covid-hyogo/updater.log 2>&1

  # Commit and push
  git checkout master
  git pull origin master
  git add . >> ~/covid-hyogo/updater.log 2>&1 
  git commit -m "Update data $(date -u)." >> ~/covid-hyogo/updater.log 2>&1
  git push origin HEAD >> ~/covid-hyogo/updater.log 2>&1

fi
