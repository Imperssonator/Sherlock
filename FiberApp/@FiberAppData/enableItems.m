function enableItems(this)
menuItems = findobj('Type', 'uimenu', ...
    'Label', 'New Data', '-or', ...
    'Label', 'Image', '-or', ...
    'Label', 'Fiber Tracking');

toolbarItems = findobj('Type', 'uipushtool', ...
    'TooltipString', 'Zoom In (+)', '-or', ...
    'TooltipString', 'Zoom Out (-)', '-or', ...
    'TooltipString', 'Add Fiber (Space)', '-or', ...
    'TooltipString', 'Remove Fiber', '-or', ...
    'TooltipString', 'Fit Fiber (F)');

imParam = findobj('Enable', 'off', '-and', 'Parent', ...
    findobj('Type', 'uipanel', 'Tag', 'ImageParameters'));
maskParam = findobj('Enable', 'off', '-and', 'Parent', ...
    findobj('Type', 'uipanel', 'Tag', 'MaskParameters'));
fibTrackParam = findobj('Enable', 'off', '-and', 'Parent', ...
    findobj('Type', 'uipanel', 'Tag', 'FiberTrackingParameters'));
set([menuItems; toolbarItems; imParam; maskParam; fibTrackParam], ...
    'Enable', 'on');
