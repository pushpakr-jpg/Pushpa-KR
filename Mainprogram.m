function [pv_switch, grid_switch, central_switch] = fcn(pv_irradiance, loadcontrol_switch)
    % Initialize output variables# function [pv_switch, grid_switch, central] = fcn(pv_irradiance, loadcontrol_switch)
     % Initialize output variables
     display("pv_irradiance:")
     pv_irradiance
     pv_switch =1;
     grid_switch = 0;
     central_switch = 0;
    
     % Print the value of pv_irradiance
     % disp(['pv_irradiance: ', int2str(pv_irradiance)]);

     % Declare Python function as extrinsic
     coder.extrinsic('py.decisiontreeirradiance.predict_switches');
    
     % Call the Python function
     result = py.decisiontreeirradiance.predict_switches(pv_irradiance, loadcontrol_switch);
     % disp(pv_irradiance)
     % Convert Python results to MATLAB doubles
     pv_switch = double(result(1));
     grid_switch = double(result(2));
     central_switch = double(result(3));
 end