function SP = InitIMS(File)

DotInd = FindLastDot(File);         % Last dot in filename before extension
SlashInd = FindLastSlash(File);     % Last slash in file name
SP = [File(1:DotInd-1) '.mat'];     % For example, '5um.tif' -> '5um'

IMS = struct();                     % Image structure
IMS.File = File;                    % Save filename in structure
IMS.Name = File(SlashInd+1:DotInd-1);        % Save image name in structure
IMS.IMG = imread(File);

save(SP,'IMS')

end
