from angr import *

proj = Project('./a2.out', main_opts={'base_addr': 0x400000})

start_state = proj.factory.entry_state()

simgr = proj.factory.simgr(start_state)

simgr.explore(find = 0x401182)

if simgr.found:
    solution = simgr.found[0]
    print (solution.posix.dumps(0))
else:
    print ("No res")
