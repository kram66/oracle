backup archivelog all delete all input;
backup current controlfile;
delete noprompt expired archivelog all;
delete noprompt obsolete;
