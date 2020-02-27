backup as compressed backupset incremental level 1 database;
backup archivelog all delete all input;
backup current controlfile;
delete noprompt expired archivelog all;
delete noprompt obsolete;
