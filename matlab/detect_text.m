function [text_im, rp_text] = detect_text(img)

img = imread('~/CC/Reverse_Plot/examples/example103.jpg');
figure; imshow(img)
gray = rgb2gray(img);
bw = YBSimple(gray);
figure; imshow(bw)
bw2 = im2bw(gray);
figure; imshow(bw2)
bw2 = bradley(gray);
figure; imshow(bw2)
bwinv = ~bw2;
figure; imshow(bwinv)
rp = regionprops(bwinv,'all');
i =1;
figure; imshow(rp(i).Image)
i=4
figure; imshow(rp(i).Image)
figure; histogram([rp(:).Extent])
figure; histogram([rp(:).Extent],50)
L = bwlabel(bwinv);
max(L(:))
whos rp
extent = [rp(:).Extent];
lowex = find(extent<0.6)
figure; imshow(ismember(L,lowex))
area = [rp(:).Area];
figure; histogram(area,50)
lowarea = find(area<200);
figure; imshow(ismember(L,lowex)&ismember(L,lowarea))
sol = [rp(:).Solidity]; figure; histogram(sol,50)
for i = 1:length(rp);
rp(i).bbarea = (rp.BoundingBox(2)-rp.BoundingBox(1))*(rp.BoundingBox(4)-rp.BoundingBox(3))
end
for i = 1:length(rp);
rp(i).bbarea = (rp(i).BoundingBox(2)-rp(i).BoundingBox(1))*(rp(i).BoundingBox(4)-rp(i).BoundingBox(3))
end
bbarea = [rp(:).bbarea];
figure; plot(bbarea,extent,'ob')
for i = 1:length(rp);
rp(i).bbarea = rp(i).BoundingBox(4)*rp(i).BoundingBox(3)
end
bbarea = [rp(:).bbarea];
figure; plot(bbarea,extent,'ob')
lowbb = find(bbarea<400);
figure; imshow(ismember(L,lowex)&ismember(L,lowbbarea))
figure; imshow(ismember(L,lowex)&ismember(L,lowbb))
AR = [rp(:).BoundingBox(3)]./[rp(:).BoundingBox(4)];
BB = [rp(:).BoundingBox];
whos BB
BB = {rp(:).BoundingBox};
whos BB
AR = cellfun(@(x) x(3)/x(4),BB);
AR{1}
AR(1)
tall = find(AR<1);
tall
final_text = ismember(L,lowex) & ismember(L,lowbb)) & ismember(L,tall);
final_text = ismember(L,lowex) & ismember(L,lowbb) & ismember(L,tall);
figure; imshow(final_text)
tall = find(AR<0.5);
final_text = ismember(L,lowex) & ismember(L,lowbb) & ismember(L,tall);
figure; imshow(final_text)
tall = find(AR<1.5);
final_text = ismember(L,lowex) & ismember(L,lowbb) & ismember(L,tall);
figure; imshow(final_text)
final_text = ismember(L,lowex) & ismember(L,lowbb) %& ismember(L,tall);
figure; imshow(final_text)
min(AR(:))
max(AR(:))
tall = find(AR<0.3);
final_text = ismember(L,lowex) & ismember(L,lowbb) & ismember(L,tall);
figure; imshow(final_text)
tall = find(AR>2);
final_text = ismember(L,lowex) & ismember(L,lowbb) & ismember(L,tall);
figure; imshow(final_text)
tall = find(AR<1.3);
final_text = ismember(L,lowex) & ismember(L,lowbb) & ismember(L,tall);
figure; imshow(final_text)
clear Tmat
clear Thor
clear T
clear sc, schor
clear schor
clear tsum
clear tsumim
tall = find(AR<1.5);
final_text = ismember(L,lowex) & ismember(L,lowbb) & ismember(L,tall);
figure; imshow(final_text)
rp
type bwlabel
figure; plot(bbarea,extent,'ob')

end