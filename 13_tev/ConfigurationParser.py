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

        assert(key == "mode" or key == "background_file" or key == "signal_file" or key == "lumi" or key == "outfile" or key == "variable" or key == "datacard_base" or key == "channel" or key == "charge" or key == "param_name" or key == "reweighted_output_fname" or key == "reweighted_file" or key == "units_conversion_exponent" or key == "block_name")

        if key == "charge":
            cfg[key] = value
        
        if key == "mode":
            cfg[key] = value

        if key == "lumi":
            cfg[key] = int(value)

        if key == "background_file":
            if "background_file" not in cfg:
                cfg[key] = []

            assert(len(value.split(','))==3)    
            cfg[key].append(value.split(','))

        if key == "signal_file":
            cfg[key] = value

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

        if key == "param_name":
            cfg[key] = value

        if key == "reweighted_output_fname":
            cfg[key] = value

        if key == "units_conversion_exponent":
            cfg[key] = value                                    

        if key == "block_name":
            cfg[key] = value                                    

    return cfg    
