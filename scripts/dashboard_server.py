#!/usr/bin/python3

import rospy
# exit(1)
from voice_commands.srv import Dashboard, DashboardResponse
import datetime

def callback_dashboard(req):

        rospy.loginfo(req.goal)

        if 'unload_tool' in req.goal:
            rospy.loginfo('unloading tool ...')
            # unload_tools(dummy=True)

        elif 'load_tool' in req.goal:
            rospy.loginfo('loading tool ...')
            selected_tool = req.goal.split(',')[-1]
            if selected_tool == 'paint':
                # select_tool(2)
                rospy.loginfo("Loading " + str(selected_tool) + "ing tool...")
                pass
            if selected_tool == 'debur':
                # select_tool(1)
                rospy.loginfo("Loading " + str(selected_tool) + "ing tool...")
                pass
            if selected_tool == 'drill':
                # select_tool(0)
                rospy.loginfo("Loading " + str(selected_tool) + "ing tool...")
                pass

        if 'calibrate' in req.goal:
            a = req.goal.split(',')[-1]
            # password match
            if a == "123":
                rospy.logwarn("Calibration Starting")
                # if not running:
                #     queueCalibration = True
                #     step = 0
                # else:
                    # rospy.logwarn("Cannot perform calibration while a job is running!")
            else:
                rospy.logwarn("Not Authorised! Calibration will not run.")

        if 'new' == req.goal:

            rospy.loginfo('Creating a New Job')
            now = datetime.datetime.now()
            filename = 'WO{0}.json'.format(now.strftime('%Y%m%d%H')[2:])

            # fromPath = os.path.join(cd(1), 'config', 'template.json') # For Spar
            # fromPath = os.path.join(cd(1), 'config', 'template-WO.json') # For Coupons

            # toPath = os.path.join(cd(1), 'config', filename)
            # copyfile(fromPath, toPath)
            rospy.loginfo('Created {} '.format(filename))
            return

        if 'retract_end_effector' in req.goal:
            rospy.loginfo('Retracting ...')
            # H = compound_transforms([get_transform_matrix('base', 'pressurefoot_debur'),
            #                                             conv([0, 0, -70, 0, 0, 0]),
            #                                             get_transform_matrix('pressurefoot_debur', 'tool0')])

            # robby.movel(tpose=Transform(H), acc=0.1, vel=0.005, wait=True, threshold=0.001)
                        
        if 'reset' in req.goal:
            rospy.loginfo('Resetting job ...')
            # ledgerName = "DAS.json" #"DAS.json"
            # with open(os.path.join(cd(1), 'config', ledgerName), 'r') as f:
            #     fixture = json.load(f, object_pairs_hook=OrderedDict)
            # reset_fixture()
            # fixture_copy = copy.deepcopy(fixture)
            # if not bool(fixture_copy):
            #     reset_fixture()
            # else:
            #     fixture = copy.deepcopy(fixture_copy)
            #     update_indicators()

        if 'start' in req.goal:
            # rospy.loginfo(req.goal)
            # perform_drill_b = True
            # perform_debur_b = True
            # loop = True #True
            ledgerName = "DAS.json" #"DAS.json"
            
            if 'drill' in req.goal.split(',')[1]:
                perform_drill_b = True
                rospy.loginfo('Starting ' + req.goal.split(',')[1] + 'ing operation ...')
            if 'debur' in req.goal.split(',')[1]:
                perform_debur_b = True
                rospy.loginfo('Starting ' + req.goal.split(',')[1] + 'ing operation ...')
            if 'paint' in req.goal.split(',')[1]:
                perform_paint_b = True
                rospy.loginfo('Starting ' + req.goal.split(',')[1] + 'ing operation ...')
            # if 'loop' in req.goal.split(',')[1]:
            #     loop = True
            

            # ledgerName = req.goal.split(',')[-1]
            rospy.logwarn('Starting Selected job - {}'.format(ledgerName))
            # with open(os.path.join(cd(1), 'config', ledgerName), 'r') as f:
            #     fixture = json.load(f, object_pairs_hook=OrderedDict)

            # Expand Blacklist
            # blacklist = []
            # for item in fixture['Blacklist']:
            #     if '_' in item:
            #         name, range = item.split('-')
            #         range = np.asarray(range.split('_')).astype(int)
            #         for num in np.arange(range[0], range[1] + 1):
            #             blacklist.append('{0}-{1}'.format(name, num))
            #     else:
            #         blacklist.append(item)

            # # Expand Whitelist

            # whitelist = []
            # for item in fixture['Whitelist']:
            #     if '_' in item:
            #         name, range = item.split('-')
            #         range = np.asarray(range.split('_')).astype(int)
            #         for num in np.arange(range[0], range[1] + 1):
            #             whitelist.append('{0}-{1}'.format(name, num))
            #     else:
            #         whitelist.append(item)

            # fixture['Whitelist'] = whitelist

            # # Remove items from Blacklist

            # for item in fixture['Whitelist']:
            #     if item in blacklist:
            #         blacklist.remove(item)

            # fixture['Blacklist'] = blacklist

            # # Reset all visual updates
            # # reset_fixture()

            # if not bool(fixture_copy):
            #     fixture_copy = copy.deepcopy(fixture)

            # # rospy.logwarn('moving base home ....')
            # # move_base_home()
            running = True

        if 'stop' == req.goal:

            # srv_ur_setio(fun=1, pin=PINS.OUT_DRILL, state=False)
            # robby.stopj(0.5)

            # pub = rospy.Publisher('/move_base/cancel', GoalID, queue_size=10)
            # pub.publish(GoalID())

            # pub = rospy.Publisher('/move_base_drifter/cancel', GoalID, queue_size=10)
            # pub.publish(GoalID())

            # running = False

            rospy.logwarn('Stopping!')
            # updateCoreState('stopped')
        
        if 'resume' in req.goal:
            # running = True
            rospy.loginfo('Resuming Operation ...')
            # updateCoreState('resuming')

        if 'home' in req.goal:
            # a = req.goal.split(',')[-1]
            a = 'robot' #TODO

            if a == 'robot':
                rospy.logwarn('Homing Robot Arm')
                # move_robot_home()

            if a == 'base':

                rospy.logwarn('Moving to Dock')
                # move_base_home()

                # running = True
                # success, _dict = perform_drill()
                # if success:
                #     move_robot(tool='pressurefoot', relative=[0, 0, -Standoffs.pressurefoot, 0, 0, 0])
                # running = False

                # queueCalibration = True
                # step = 0

        # if 'init' in req.goal:
        #     rospy.loginfo('Initialising Base...')
        #     rospy.loginfo("Init Base Called")
        #     # prepare initial pose

        #     pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, latch=True, queue_size=1)

        #     now = rospy.Time.now()
        #     targetFrame = 'map'
        #     sourceFrame = 'Dock'
        #     tl.waitForTransform(targetFrame, sourceFrame, now, rospy.Duration(1.0))
        #     translation, rotation = tl.lookupTransform(targetFrame, sourceFrame, now)

        #     p=PoseWithCovarianceStamped()
        #     p.header.frame_id = 'map'
        #     p.pose.pose.position.x = translation[0]
        #     p.pose.pose.position.y = translation[1]
        #     p.pose.pose.position.z = translation[2]

        #     p.pose.pose.orientation.x = rotation[0]
        #     p.pose.pose.orientation.y = rotation[1]
        #     p.pose.pose.orientation.z = rotation[2]
        #     p.pose.pose.orientation.w = rotation[3]

        #     p.pose.covariance = np.dot(0.1,[10.788237988127957, -1.7035538156851895, 0.0, 0.0, 0.0, 0.0,
        #                          -1.7035538156851904, 16.7268275003162, 0.0, 0.0, 0.0, 0.0,
        #                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        #                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        #                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        #                          0.0, 0.0, 0.0, 0.0, 0.0, 9.245442313197612])

        #     pub.publish(p)

        if 'getWorkOrders' in req.goal:
            rospy.loginfo('Getting work orders')
            # import glob
            # jobs = []
            # files = glob.glob(os.path.join(cd(1), 'config', "WO*.json"))
            # for file in files:
            #     jobs.append(file.split('/')[-1])
            # response = json.dumps(sorted(jobs,reverse=True))
            # return response

        if 'getBoundAddress' in req.goal:
            rospy.loginfo("getBoundAddress")
        
        response = DashboardResponse()
        rospy.loginfo(response)
        return response

    
if __name__ == "__main__":
    rospy.init_node('dashboard_node')
    rospy.Service('dashboard', Dashboard, callback_dashboard)

    rospy.loginfo("Dashboard Server.")
    rospy.spin()
