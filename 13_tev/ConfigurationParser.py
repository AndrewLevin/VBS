import re

def ConfigurationParser(input_filename):

    cfg = {}

    infile = open(input_filename)
    
    for line in infile:
        line = line.split('#')[0]
        line = re.sub(' ','',line)
        line = line.rstrip('\n')
        if line == "":
            continue

        assert(len(line.split('=')) == 2)        
                
        key = line.split('=')[0]        

        value = line.split('=')[1]

        assert(key == "mode" or key == "background_file" or key == "signal_file" or key == "lumi" or key == "outfile" or key == "variable" or key == "datacard_base" or key == "channel" or key == "charge" or key == "param_name" or key == "reweighted_output_fname" or key == "reweighted_file" or key == "units_conversion_exponent" or key == "block_name" or key == "data_file" or key == "atgcroostats_config_fname" or key == "ttbar_fname" or key == "fr_fname" or key == "which_selection" or key == "mc_sample_file" or key == "fake_sample_file" or key == "blind_high_mjj" or key == "data_sample_file")

        if key == "ttbar_fname":
            cfg[key] = value

        if key == "fr_fname":
            cfg[key] = value

        if key == "charge":
            cfg[key] = value
        
        if key == "mode":
            cfg[key] = value

        if key == "lumi":
            cfg[key] = float(value)

        if key == "background_file":
            if "background_file" not in cfg:
                cfg[key] = []

            assert(len(value.split(','))==3)    
            cfg[key].append(value.split(','))

        if key == "mc_sample_file":
            if "mc_sample_file" not in cfg:
                cfg[key] = []

            assert(len(value.split(','))==3)    
            cfg[key].append(value.split(','))            

        if key == "fake_sample_file":
            if "fake_sample_file" not in cfg:
                cfg[key] = []

            assert(len(value.split(','))==1)    
            cfg[key].append(value.split(','))            

        if key == "data_sample_file":
            if "data_sample_file" not in cfg:
                cfg[key] = []

            assert(len(value.split(','))==1)    
            cfg[key].append(value.split(','))            


        if key == "signal_file":
            cfg[key] = value.split(',')

        if key == "outfile":
            cfg[key] = value

        if key == "variable":
            cfg[key] = value

        if key == "datacard_base":
            cfg[key] = value

        if key == "channel":
            cfg[key] = value      

        if key == "reweighted_file":
            cfg[key] = value

        if key == "atgcroostats_config_fname":
            cfg[key] = value            

        if key == "param_name":
            cfg[key] = value

        if key == "reweighted_output_fname":
            cfg[key] = value

        if key == "units_conversion_exponent":
            cfg[key] = value                                    

        if key == "block_name":
            cfg[key] = value                                    

        if key == "data_file":
            cfg[key] = value

        if key == "which_selection":
            cfg[key] = value

        if key == "blind_high_mjj":
            assert(value == "True" or value == "False")
            if value == "True":
                cfg[key] = True
            else:
                cfg[key] = False

    if "blind_high_mjj" not in cfg:
        cfg["blind_high_mjj"] = False

    return cfg    
