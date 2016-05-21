function out = FindLastDot(FilePath)

DotInd = regexp(FilePath,'[\.]');
out = DotInd(end);

end