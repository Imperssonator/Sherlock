function [] = disp_img(i,Files)

figure; imshow(imread(Files(i).path));

end