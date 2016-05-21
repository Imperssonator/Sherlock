function [] = MakeTif(IMSFile)

load(IMSFile)
Name = IMS.File;
LS = FindLastSlash(Name);
FD = FindLastDot(Name);
ActName = Name(LS+1:FD-1);
ActFolder = Name(1:LS);
TifName = [ActName '.tif'];
TifPath = [ActFolder TifName];
imwrite(IMS.IMG,TifPath)
IMS.Tif = TifPath;
save(IMSFile,'IMS')

end