function SpatStatsFile = SS_Dir(FolderName)

% Driver
% Put the path to the folder with the images you want to analyze here, no
% final slash:

if ispc
    sep = '\';
else
    sep = '/';
end

DirectoryPath = [FolderName, sep];
ImDim = 2000;   % kind of arbitrary in this case

D = CompileImgs(DirectoryPath);
disp(D)
Files = D;  %{D(:).path}';

% For some reason this crashes Matlab beyond about 100 images.......
NumFiles = 5;
disp('Files:')
disp(NumFiles)
% return

% First find the smallest image to truncate the stats appropriately
disp('Finding spatial stats truncation size')
for i = 1:NumFiles
    imgi = imread(Files(i).path);
    Files(i).h = size(imgi,1);
    Files(i).w = size(imgi,2);
end

min_h = min([Files(:).h]);
min_w = min([Files(:).w]);

% If min_h is odd, the smallest spat stat h must be min_h, if it's even,
% min_h+1

truncate = [0 0];
if mod(min_h,2)==1
    truncate(1) = min_h;
else
    truncate(1) = min_h+1;
end
if mod(min_w,2)==1
    truncate(2) = min_w;
else
    truncate(2) = min_w+1;
end

SSMAT = zeros(NumFiles,prod(truncate));
options = struct('display',0,'truncate',truncate);

% Run spatial stats and save the truncated T matrices
for i = 1:NumFiles
    disp(i)
    disp(Files(i).path)
    imgi = imread(Files(i).path);
    grayi = rgb2gray(imgi);
    invgray = 255-grayi;
    bw = bradley(invgray);
    Ti = BWSpatStat(bw, options);
    SSMAT(i,:) = Ti(:)';
end

% save('ImgFiles2','Files')
% load('ImgFiles2')
% 
% frame = min(min([Files(:).Tm]),min([Files(:).Tn]));
% frame = floor(frame/2)-1;
% SideLen = frame*2+1;
% AreaPix = (frame*2+1)^2;
% SSMAT = zeros(NumFiles,AreaPix);
% for i = 1:NumFiles
%     Ti = Files(i).T;
%     cent = ceil(size(Ti)/2);
%     Tcut = Ti(cent(1)-frame:cent(1)+frame,cent(2)-frame:cent(2)+frame);
%     Files(i).Tcut = Tcut(:)';
%     SSMAT(i,:) = Tcut(:)';
% end

[Coef, Score] = pca(SSMAT);

save('ImgSS2')
SpatStatsFile = 'ImgSS2.mat';

hax = myscatter3([Score(:,1),Score(:,2)],(1:NumFiles));
hax.XLabel.String = 'PC1';
hax.YLabel.String = 'PC2';
hax.ZLabel.String = 'Image Number';


end



function out = CompileImgs(FolderPath)
disp(FolderPath)

ad = pwd;
% First compile any images from the folderpath
cd(FolderPath)
PNG = dir('*.png');
JPG = dir('*.jpg');
JPEG = dir('*.jpeg');
TIF = dir('*.tif');
out = [PNG; JPG; JPEG; TIF]; % Generate directory structure of images in FolderPath
cd(ad)

for i = 1:length(out)
    out(i).Folder = FolderPath;
    out(i).path = [FolderPath,out(i).name];
end
out = out;
disp(out)

end

function out = FindAllSubDirs()

% Generate a cell array of the names of all subdirectories in the current
% directory

D = dir;

Names = {D(:).name};

out = {};

for i = 1:length(Names)
    if D(i).isdir
        Name = Names{i};
        if Name(1) ~= '.'
            out = [out; Name];
        end
    end
end

end

function bw = YBSimpleSeg(gray)

%YBSeg Yanowitz-Bruckstein image segmentation with fiber unentanglement
%   SP is the structure path
%   File is the file path from current active dir
%   Dim is the image dimension in nm

edges = edge(gray,'canny');         % Apply a Canny edge finder - 1's at the edges, 0's elsewhere
grayDouble = double(gray);                     % Turn the grey image into double prec.
edgesDouble = double(edges);                     % Turn the edge image into double prec.
initThresh = grayDouble.*edgesDouble;                        % Fill in the grey values of the edge pixels in a new image file                      

threshSurf = YBiter(initThresh);                    % Perform Yanowitz-Bruckstein surface interpolation to create threshold surface from edge gray values

bw = gray>threshSurf;                          % Segment the image; pixels above threshold surface are white, if not, black

end

function Vf = YBiter(V0)

%YBiter Yanowitz/Bruckstein surface interpolation

w = 1;
[m,n] = size(V0);
InitVal = mean(V0(V0~=0)); % Start non-edges as the mean of the edges because 0's aint' working
Vupdate = V0==0;           % A logical array of pixels to update on each iteration
Vupdate(1,:) = 0;
Vupdate(:,1) = 0;
Vupdate(m,:) = 0;
Vupdate(:,n) = 0;

V0(V0==0)=InitVal;         % Put the average edge values in the non-edge cells

Vnew = zeros(m,n);         % Initialize the updated threshold surface
Vold = V0;

iter = 0;
maxiter = 40;

% tic
while iter<maxiter
    iter = iter+1;
%     disp(iter)
    
    Lap = del2(Vold);
    Vnew = Vold + Vupdate .* (w .* Lap);
    Vold = Vnew;
    
end
% toc
Vf = Vnew;

end