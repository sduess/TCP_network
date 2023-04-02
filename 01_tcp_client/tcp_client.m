% matlab works as client, while Python works as server

% open_system('tcp_client_simulink');
% % start simulation and pause simulation, waiting for signal from python
% set_param(gcs,'SimulationCommand','start','SimulationCommand','pause');
ip_address_server = '192.168.0.53' %'146.169.133.53'

% open a client for  SHARPy's output network
t_receive = tcpclient(ip_address_server,59011);
all_data_2 = [];
count = 0;
control_input = zeros(1,8);

% open a client for  SHARPy's input network
t_send = tcpclient(ip_address_server,64011);
all_data = [];
count = 0;



data_recv = [];
while count<120 % just run for 120 steps for demo
    % TCP sending
    write_to_SHARPy(t_send,control_input)
    
    % TCP receiving
    while(1) % loop, until getting some data
        nBytes = get(t_receive,'BytesAvailable');
        if nBytes > 0
            break;
        end
    end
    command_rev = read(t_receive,nBytes); % read() will read binary as str
    data = str2num(char(command_rev)); % transform str into numerical matrix
    all_data = [all_data;data]; % store history data
    if isempty(data)
        data = [0,0,0,0];
    end
    
end