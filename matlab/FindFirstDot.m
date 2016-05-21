function out = FindFirstDot(FilePath)

DotInd = regexp(FilePath,'[\.]');
out = DotInd(1);

end