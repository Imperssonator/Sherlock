function out = BWSpatStat(Bin,Options)

% Default parameters
defaultoptions=struct('display',0,'truncate',[0 0]);

if(~exist('Options','var')),
    Options=defaultoptions;
else
    tags = fieldnames(defaultoptions);
    for i=1:length(tags)
        if(~isfield(Options,tags{i})),  Options.(tags{i})=defaultoptions.(tags{i}); end
    end
    if(length(tags)~=length(fieldnames(Options))),
        warning('CoherenceFilter:unknownoption','unknown options found');
    end
end

T = SpatialStatsFFT(Bin,Bin,'periodic',false,'display',Options.display);
Tshift = fftshift(T);

if isequal(Options.truncate,[0 0])
    out = Tshift;
else 
    cent = ceil(size(Tshift)/2);
    frame = floor(Options.truncate/2);
    Ttrunc = Tshift(cent(1)-frame(1):cent(1)+frame(1),cent(2)-frame(2):cent(2)+frame(2));
    out = Ttrunc;
end

end



