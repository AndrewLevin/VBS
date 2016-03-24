import copy
import sys

def parse_reweight_info(param_num,initrwgt_header,slha_header,block_name):

    param_values=[]
    param_values.append(-1); #in order to make the indexing consistent with the dimension 8 parameter numbers

    inside_block_anoinputs=False
    inside_rwgt=False

    line_inside_block_anoinputs=0

    #dim8_param_number=9

    oneD_grid_points = []
    histo_grid = []
    lhe_weight_index = []

    i=0

    while i < len(slha_header):

        line=str(slha_header[i])

        if line == "Block "+block_name+" \n":
            
            i=i+1
            line=slha_header[i]
            while line != "\n":
                line_inside_block_anoinputs=line_inside_block_anoinputs+1
                param_values.append(float(line.lstrip(' ').split(' ')[1]))
                i=i+1
                line=slha_header[i]

        i=i+1        

    in_mg_reweighting_header = False

    i=0
    while i < len(initrwgt_header):

        line = str(initrwgt_header[i])

        param_values_copy=copy.deepcopy(param_values)

        if "<weightgroup type=\'mg_reweighting\'>" in line or "<weightgroup type=\"mg_reweighting\">" in line:
            in_mg_reweighting_header = True
            i=i+1
            continue

        if not in_mg_reweighting_header:
            i=i+1
            continue

        if "</weightgroup>" in line:
            i=i+1
            in_mg_reweighting_header = False
            continue

        if line == "</weight>\n":
            i=i+1
            continue

        assert("weight id" in line)

        end_of_line=line.split("<weight id=\"mg_reweight_")[len(line.split("<weight id=\"mg_reweight_")) - 1]

        weight_id=int(end_of_line.split('\">')[0])

        while "set param_card "+block_name in line:
            param_number=int(line.split('>')[len(line.split('>')) - 1].split(' ')[3])
            param_value=float(line.split('>')[len(line.split('>')) - 1].split(' ')[4])
            param_values_copy[param_number]=param_value
            i=i+1
            line = str(initrwgt_header[i])

        all_others_0 = True

        for j in range(1,len(param_values)):
            if j != param_num and param_values_copy[j] != 0.0:
                all_others_0 = False
                
        found_duplicate = False

        for j in range(0,len(oneD_grid_points)):
            if oneD_grid_points[j] == param_values_copy[param_num]:
                found_duplicate=True

        if all_others_0 and not found_duplicate:
            oneD_grid_points.append(param_values_copy[param_num])
            histo_grid.append(weight_id-1)
            lhe_weight_index.append(weight_id-1)

        i=i+1    

    return {"oneD_grid_points": oneD_grid_points, "histo_grid" : histo_grid, "lhe_weight_index" : lhe_weight_index}
