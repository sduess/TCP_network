function write_to_SHARPy(tcp_client, control_input)
%write_to_SHARPy Sends the given control input to the TCP SHARPy server 
% First, the SHARPy header (translated to REF0) is sent to SHARPy, followed
% by the control input converted to the format described in:
% Duessler et al, 2023, "LQG-based Gust Load Alleviation Systems for Very 
% Flexible Aircraft", AIAA SciTech Forum 2023, 
% doi:https://arc.aiaa.org/doi/pdf/10.2514/6.2023-2571

SHARPy_header = [82; 82; 69; 70; 48];
write(tcp_client,SHARPy_header, "uint8");

msg = single(encode_SHARPy_msg(control_input));
write(tcp_client, msg, "single");

end


function msg_encoded = encode_SHARPy_msg(input_data)
    num_values = length(input_data);
    msg = zeros(2*num_values,1);
    counter_row = 1
    for i_value=1:num_values
        msg(counter_row) = (i_value-1) * 1.4e-45;
        msg(counter_row + 1) = input_data(i_value)
        counter_row = counter_row + 2;
    end
    msg_encoded = dec2bin(single(msg))
end