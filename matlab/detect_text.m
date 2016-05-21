function [text_im, rp_text] = detect_text(img)

gray = rgb2gray(img);
bw = bradley(gray);
bwinv = ~bw;

% Run region props and bwlabel
rp = regionprops(bwinv,'all');
L = bwlabel(bwinv);

% Text has extent < 0.6 and area < 200
% These parameters are not reliable tho...
extent = [rp(:).Extent];
lowex = find(extent<0.6);
area = [rp(:).Area];
lowarea = find(area<200);

% Get bounding box area
for i = 1:length(rp);
    rp(i).bbarea = rp(i).BoundingBox(4)*rp(i).BoundingBox(3);
    rp(i).AR = rp(i).BoundingBox(3)/rp(i).BoundingBox(4);
end
bbarea = [rp(:).bbarea];
lowbb = find(bbarea<400);

% Aspect ratio
AR = [rp(:).AR];
tall = find(AR<1.3);

text_im = ismember(L,lowex) & ismember(L,lowbb) & ismember(L,tall);
figure; imshow(img)
figure; imshow(text_im)

myscatter3([bbarea,extent],AR,'ob')

end