FolderName = '~/CC/Sherlock/scrape_figures\dump/full';

sp = SS_Dir(FolderName);

load(sp)

disp('Click on a point on the scatterplot to get the image number (z-coord.)')
disp('display that image by running "disp_img(z-coord,Files)"')
