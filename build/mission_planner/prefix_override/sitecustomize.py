import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/idp/ms/src/MissionPlanner/install/mission_planner'
