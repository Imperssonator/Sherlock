function out = FindLastSlash(FilePath)

SlashInd = regexp(FilePath,'[\\/]');
out = SlashInd(end);

end