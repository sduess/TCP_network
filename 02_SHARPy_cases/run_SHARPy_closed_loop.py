import os
import aircraft as flexop
from get_settings import get_settings

def run_flexop():
        cases_route = '../../01_case_files/'
        output_route = './output/'

        case_name = 'flexop_clamped_L_10_I_10_udp_no_unsteady' #_newmark05em5_'
        

        lifting_only = True # ignore nonlifting bodies
        wing_only = False # Wing only or full configuration (wing+tail)
        dynamic = True 
        controllable = True # needed when nonlinear in closed-loop
        wake_discretisation = False 
        symmetry_condition =  False 

        client_address = '146.169.131.236' #'146.169.131.254'
        SHARPy_address ='146.169.131.236'

        flow = ['BeamLoader', 
                'AerogridLoader',
                'AerogridPlot',
                'BeamPlot',
                # 'StaticUvlm',
                # 'AeroForcesCalculator',
                'StaticCoupled',
                'AeroForcesCalculator',
                # 'StaticTrim',
                'BeamPlot',
                'AerogridPlot',
                'AeroForcesCalculator',
                'DynamicCoupled',
        ]

        # Set cruise parameter
        # trim_values = {'alpha':6.796482976011756182e-03, 
        #                 'delta':-1.784287512500099069e-03,
        #                 'thrust': 2.290077074834680371e+00
        #                 }


        trim_values = {'alpha':6.796440835038532191e-03, 
                        'delta':-1.768105934210733362e-03,
                        'thrust': 2.290049824528705091e+00
                        }


        alpha =  trim_values['alpha'] 
        u_inf =45 
        rho = 1.1336 # corresponds to an altitude of 800  m
        gravity = True
        horseshoe =  False 
        use_gust = True
        use_tcp = True
        closed_loop = True
        dynamic_cs_input =False # True
        wake_length = 10 #5
        cfl1 = not wake_discretisation
        free_flight = False # False: clamped
        cs_deflection = trim_values['delta']
        thrust = trim_values['thrust'] 

        num_chord_panels = 8

        if closed_loop:
                ailerons_type = 2
        elif dynamic_cs_input:
                ailerons_type = 1
        else:
                ailerons_type = 0

        flexop_model = flexop.FLEXOP(case_name, cases_route, output_route)
        flexop_model.clean()
        flexop_model.init_structure(sigma=0.3, 
                                n_elem_multiplier=2., 
                                n_elem_multiplier_fuselage = 1, 
                                lifting_only=lifting_only, wing_only = wing_only, 
                                symmetry_condition = symmetry_condition) 
        flexop_model.init_aero(m=num_chord_panels, cs_deflection = cs_deflection, ailerons_type = ailerons_type) 
        flexop_model.structure.set_thrust(thrust)

        # Other parameters
        CFL = 1
        dt = CFL * flexop_model.aero.chord_main_root / flexop_model.aero.m / u_inf
        # numerics
        n_step = 5
        structural_relaxation_factor = 0.6
        relaxation_factor = 0.2
        tolerance = 1e-6 
        fsi_tolerance = 1e-4 
        num_cores = 8
        newmark_damp = 0.5e-3 #5
        n_tstep = 1500


        # Gust velocity field
        gust_settings  ={'gust_shape': '1-cos',
                        'gust_length': 5.,
                        'gust_intensity': 0.1,
                        'gust_offset': 10 * dt *u_inf}

        #  Network settings for nonlinear in closed-loop simulations                       
        network_settings = {'variables_filename': '/home/sduess/Documents/Aircraft Models/demonstrator_uvlm_enhenacements/01_case_files/flexop_network_info.yml',
                                                'send_output_to_all_clients': False,
                                                'byte_ordering': 'little',
                                                'received_data_filename': './output/' + case_name + '/input.dat',
                                                'log_name': './output/' + case_name + '/sharpy_network.log',
                                                'file_log_level': 'debug',
                                                'console_log_level': 'debug',
                                                'input_network_settings': {'address': SHARPy_address,# '146.169.133.53', # '192.168.0.53', #'146.169.142.190', #146.169.128.81', #'192.168.0.53', #'146.169.132.44',
                                                                                'port': 64014,
                                                                                'destination_address': client_address, #'146.169.199.249',
                                                                                'TCP': use_tcp,
                                                                                },
                                                'output_network_settings': {'send_on_demand': False,
                                                                                'port': 59014,
                                                                                'address':SHARPy_address,#'146.169.133.53', # '192.168.0.53', #'146.169.142.190', #'146.169.128.81', #192.168.0.53', #'192.168.0.185', #'146.169.132.44',
                                                                                # 'destination_address': [client_address], #['146.169.205.28'], #142.190'], # ['146.169.203.120'] ,#['192.168.0.54'], #['146.169.191.244'],
                                                                                # 'destination_ports': [59010],
                                                                                'TCP': use_tcp,
                                                                        }
                                                        }
                        
        # Get settings dict
        settings = get_settings(flexop_model,
                                flow,
                                dt,
                                gust = use_gust,
                                gust_settings = gust_settings,
                                alpha = alpha,
                                cs_deflection = cs_deflection,
                                u_inf = u_inf,
                                rho = rho,
                                thrust = thrust,
                                wake_length = wake_length,
                                free_flight = free_flight,
                                num_cores = num_cores,
                                tolerance = tolerance,
                                fsi_tolerance = fsi_tolerance,
                                structural_relaxation_factor = structural_relaxation_factor,
                                newmark_damp = newmark_damp,
                                n_tstep = n_tstep,
                                closed_loop = closed_loop,
                                network_settings = network_settings,
                                dynamic_controllable_ailerons = dynamic_cs_input                                    
                                )

        flexop_model.generate()
        flexop_model.structure.calculate_aircraft_mass()
        flexop_model.create_settings(settings)
        flexop_model.run()


if __name__ == '__main__':
        run_flexop()