import sys

if len(sys.argv) != 1:
     print "Usage:"
     print "python2.6 make_reweight_card.py"
     sys.exit(0)

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

#FS0
for i in range(-5,6):
     print "launch"
     print "        set anoinputs 12 0.000000e+00"
     print "        set anoinputs 1 " +str(i*0.4) + "00000e-10"

#FS1
for i in range(-5,6):
     print "launch"
     print "        set anoinputs 12 0.000000e+00"
     print "        set anoinputs 2 " +str(i/2.) + "00000e-10"

#FM0
for i in range(-5,6):
     print "launch"
     print "        set anoinputs 12 0.000000e+00"
     print "        set anoinputs 3 " +str(i/2.) + "00000e-10"

#FM1
for i in range(-5,6):
     print "launch"
     print "        set anoinputs 12 0.000000e+00"
     print "        set anoinputs 4 " +str(i/2.) + "00000e-10"

#FM6
for i in range(-5,6):
     print "launch"
     print "        set anoinputs 12 0.000000e+00"
     print "        set anoinputs 9 " +str(i*1.) + "00000e-10"

#FM7
for i in range(-5,6):
     print "launch"
     print "        set anoinputs 12 0.000000e+00"
     print "        set anoinputs 10 " +str(i*1.) + "00000e-10"     

#FT0
for i in range(-5,6):
     print "launch"
     print "        set anoinputs 12 0.000000e+00"
     print "        set anoinputs 11 " +str(i*0.5) + "00000e-11"

#FT1
for i in range(-5,6):
     print "launch"
     print "        set anoinputs 12 " +str(i*0.2) + "00000e-11"          

#FT2
for i in range(-5,6):
     print "launch"
     print "        set anoinputs 12 0.000000e+00"
     print "        set anoinputs 13 " +str(i*0.5) + "00000e-11"
