%% exportdata.m
% Exports digitized and net joint moment data from the '_short.mat' files
% that save all the data generated by the MatLab code Ian created.


%%
% gather all files ending in '*_short.mat'
cd('../data/data_mat_files')
files = dir('*_short.mat');

% loop through each file and output specific data
for cnt = 1:length(files)
    % load data
    load(files(cnt).name,...
        'shoulderNJMmag_crop',...% variable for shoulder NJM magnitude
        'RF_angleForearmCROP', 'RF_mag', 'RF_mag_CROP',... % variables for reaction force angle and magnitude
        'elbow_ang_CROP', 'elb_vel_CROP', 'torso_ang_CROP', 'torso_vel_CROP'); % variables for reaction force
    
    % create table for second sheet
    tab1_out = array2table([elbow_ang_CROP, [0; elb_vel_CROP'], torso_ang_CROP, [0; torso_vel_CROP']],...
        'VariableNames', {'elbow_angle', 'elbow_angvel', 'torso_angle', 'torso_angvel'});
    % create table for second sheet
    tab2_out = array2table([shoulderNJMmag_crop, RF_angleForearmCROP, RF_mag_CROP],...
        'VariableNames', {'njm_shoulder_mag', 'rf_angle2forearm', 'rf_mag'});
    % create table for third sheet (FULL DATA!!!)
    tab3_out = array2table([RF_mag],...
        'VariableNames', {'rf_mag_full'});
    
    % create new file name
    filename = ['../subject_data/', files(cnt).name(1:length(files(cnt).name)-10), '.xlsx'];
    writetable(tab1_out, filename, 'sheet', 1)
    writetable(tab2_out, filename, 'sheet', 2)
    writetable(tab3_out, filename, 'sheet', 3)
    
    % clear vars
    clearvars -except files cnt
end