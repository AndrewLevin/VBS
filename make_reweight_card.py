import sys

if len(sys.argv) != 2:
     print "Usage:"
     print "python2.6 make_reweight_card.py model"
     print "possible models: SM_LT012_UFO, SM_LM0123_UFO, or SM_LS0_LS1_UFO"
     sys.exit(0)

model=sys.argv[1]

print "#******************************************************************"
print "#                       Reweight Module                           *"
print "#******************************************************************"
print "# launch"
print "#* Use the set command to specify the new set of parameter"
print "#* Or specify a path to a valid param_card/banner"
print "#* Example of valid command:"
print "#*     set aewm1 137"
print "#*     ~/param_card.dat"
print "#*"
print "#* Note:"
print "#*   1) the value of alphas will be used from the event"
print "#*      so the value of the param_card is not taken into account."
print "#*   2) It is dangerous to change a mass of any particle."
print ""
print ""
print "#* If you want to compute the weight for more than one hyppothesis"
print "#* you need first to uncomment the following line:"
print "# launch"
print "# and then use the set command to specify your parameter."
print "# All modification will start from the ORIGINAL card not from the"
print "# last define one."
print "#* You can have as many weight as you want."

if model == "SM_LS0_LS1_UFO":
    for i in range(-5,6):
        for j in range(-5,6):
            if i == 0 and j == 0:
                continue
            print ""
            print "launch"
            print "        set anoinputs 1 " +str(i/2.) + "00000e-10"
            print "        set anoinputs 2 " + str(j/2.)+ "00000e-9"
elif model=="SM_LT012_UFO":
    for param_num1 in range(11,14):
        for param_num2 in range (param_num1+1,14):
            for i in range(-5,6):
                for j in range(-5,6):
                    if i == 0 and j == 0:
                        continue
                    print ""
                    print "launch"
                    print "        set anoinputs "+str(param_num1)+" " +str(i*2.) + "00000e-11"
                    print "        set anoinputs "+str(param_num2)+" "+str(j*2.)+ "00000e-11"
if model == "SM_LM0123_UFO":
    for i in range(-5,6):
        for j in range(-7,8):
            if i == 0 and j == 0:
                continue
            print ""
            print "launch"
            print "        set anoinputs 3 " +str(i/2.) + "00000e-10"
            print "        set anoinputs 4 " + str(j/2.)+ "00000e-10"
else:                    
    print "unknown model, exiting"
    
