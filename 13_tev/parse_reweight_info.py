import copy
import sys

def parse_reweight_info(dim8_param_number,fname):

    #fname="/afs/cern.ch/work/a/anlevin/data/lhe/13_tev/wpwmjj_qed_4_qcd_0.lhe"

    f=file(fname,'r')

    line=f.readline()

    f=open(fname)

    param_values=[]
    param_values.append(-1); #in order to make the indexing consistent with the dimension 8 parameter numbers

    inside_block_anoinputs=False
    inside_rwgt=False

    line_inside_block_anoinputs=0

    #dim8_param_number=9

    oneD_grid_points = []
    histo_grid = []
    lhe_weight_index = []

    while line != '':

        line=f.readline()

        if line == "Block anoinputs \n":
            line=f.readline()
            while line != "\n":
                line_inside_block_anoinputs=line_inside_block_anoinputs+1
                param_values.append(float(line.lstrip(' ').split(' ')[1]))
                line=f.readline()

        if line == "<initrwgt>\n":
            line=f.readline()
            print line
            assert(line=="<weightgroup type='mg_reweighting'>\n");

            line=f.readline()
            i=0
            while line != "</initrwgt>\n":

                param_values_copy=copy.deepcopy(param_values)

                if line == "</weight>\n":
                    line = f.readline()
                    continue
                if line == "</weightgroup>\n":
                    line = f.readline()
                    continue

                while "set param_card anoinputs" in line:
                    param_number=int(line.split('>')[len(line.split('>')) - 1].split(' ')[3])
                    param_value=float(line.split('>')[len(line.split('>')) - 1].split(' ')[4])
                    param_values_copy[param_number]=param_value
                
                    line=f.readline()

                all_others_0 = True

                for j in range(1,21):
                    if j != dim8_param_number and param_values_copy[j] != 0.0:
                        all_others_0 = False

                found_duplicate = False

                for j in range(0,len(oneD_grid_points)):
                    if oneD_grid_points[j] == param_values_copy[dim8_param_number]:
                        found_duplicate=True

                if all_others_0 and not found_duplicate:
                    oneD_grid_points.append(param_values_copy[dim8_param_number])
                    histo_grid.append(i)
                    lhe_weight_index.append(i)

                i=i+1    

                line=f.readline()
        
    return {"oneD_grid_points": oneD_grid_points, "histo_grid" : histo_grid, "lhe_weight_index" : lhe_weight_index}
