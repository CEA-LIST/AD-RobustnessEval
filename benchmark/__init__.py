from .goal_suite import PointGoalSuite


VERSION = '096'

WEATHER_1 = [1, 3, 6, 8]
WEATHER_2 = [4, 14]
WEATHER_3 = [10, 14]
WEATHER_4 = [1, 8, 14]

_suites = dict()


def _add(suite_name, *args, **kwargs):
    assert suite_name not in _suites, '%s is already registered!' % suite_name

    town = None

    if 'Town01' in suite_name:
        town = 'Town01'
    elif 'Town02' in suite_name:
        town = 'Town02'
    else:
        raise Exception('No town specified: %s.' % suite_name)

    benchmark = 'carla100' if 'NoCrash' in suite_name else 'corl2017'
    suite = None

    if 'Turn' in suite_name:
        suite = 'turn'
    elif 'Straight' in suite_name:
        suite = 'straight'
    elif 'Full' in suite_name:
        suite = 'full'
    elif 'NoCrash' in suite_name:
        suite = 'nocrash'
    elif 'Debug' in suite_name:
        suite='debug'
    elif 'Xing' in suite_name:
        suite='xing'
    else:
        raise Exception('No suite specified: %s.' % suite_name)

    kwargs['town'] = town

    if 'left_right' in suite_name: 
        kwargs['poses_txt']='one_xing/left_right_Town01.txt'
    elif 'straight_right' in suite_name:
        kwargs['poses_txt'] = 'one_xing/straight_right_Town01.txt'
    elif 'straight_left' in suite_name:
        kwargs['poses_txt'] = 'one_xing/straight_left_Town01.txt'
    else: 
        kwargs['poses_txt'] = '%s/%s/%s_%s.txt' % (benchmark, VERSION, suite, town)
    #kwargs['col_is_failure'] = 'NoCrash' in suite_name
    kwargs['col_is_failure'] = True

    #kwargs['poses_txt'] = 'one_turn/straight_right_Town01.txt'

    _suites[suite_name] = (args, kwargs)


## ============= Register Suites ============ ##

_add('TurnTown01-v4', n_vehicles=0, weathers=[1])

_add('Town01_Xing_left_right', n_vehicles=0, weathers=[1])
_add('Town01_Xing_straight_right', n_vehicles=0, weathers=[1])
_add('Town01_Xing_straight_left', n_vehicles=0, weathers=[1])


_add('DebugTown01-v0', n_vehicles=0, weathers=WEATHER_1)
# _add('FullTown01-v0', n_vehicles=0, viz_camera=True)
# _add('FullTown02-v0', n_vehicles=0, viz_camera=True)

# data collection town; no respawn to prevent missing frames
_add('FullTown01-v0', n_vehicles=0, weathers=WEATHER_1, respawn_peds=False)
# Train town, train weathers.
_add('FullTown01-v1', n_vehicles=0, weathers=WEATHER_1)
_add('StraightTown01-v1', n_vehicles=0, weathers=WEATHER_1)
_add('TurnTown01-v1', n_vehicles=0, weathers=WEATHER_1)

# Train town, test weathers.
_add('FullTown01-v2', n_vehicles=0, weathers=WEATHER_2)
_add('StraightTown01-v2', n_vehicles=0, weathers=WEATHER_2)
_add('TurnTown01-v2', n_vehicles=0, weathers=WEATHER_2)

# Train town, more vehicles
_add('FullTown01-v3', n_vehicles=20, n_pedestrians=50, weathers=WEATHER_1)
_add('FullTown01-v4', n_vehicles=20, n_pedestrians=50, weathers=WEATHER_2)
# No ped versions
_add('FullTown01-v3-np', n_vehicles=20, n_pedestrians=0, weathers=WEATHER_1)
_add('FullTown01-v4-np', n_vehicles=20, n_pedestrians=0, weathers=WEATHER_2)

# Test town, train weathers.
_add('FullTown02-v1', n_vehicles=0, weathers=WEATHER_1)
_add('StraightTown02-v1', n_vehicles=0, weathers=WEATHER_1)
_add('TurnTown02-v1', n_vehicles=0, weathers=WEATHER_1)

# Test town, test weathers.
_add('FullTown02-v2', n_vehicles=0, weathers=WEATHER_2)
_add('StraightTown02-v2', n_vehicles=0, weathers=WEATHER_2)
_add('TurnTown02-v2', n_vehicles=0, weathers=WEATHER_2)

# Test town, more vehicles.
_add('FullTown02-v3', n_vehicles=15, n_pedestrians=50, weathers=WEATHER_1)
_add('FullTown02-v4', n_vehicles=15, n_pedestrians=50, weathers=WEATHER_2)
# No ped versions
_add('FullTown02-v3-np', n_vehicles=15, n_pedestrians=0, weathers=WEATHER_1)
_add('FullTown02-v4-np', n_vehicles=15, n_pedestrians=0, weathers=WEATHER_2)

_add('NoCrashTown01-v1', n_vehicles=0, disable_two_wheels=True, weathers=WEATHER_1)
_add('NoCrashTown01-v2', n_vehicles=0, disable_two_wheels=True, weathers=WEATHER_3)
_add('NoCrashTown01-v3', n_vehicles=20, disable_two_wheels=True, n_pedestrians=50, weathers=WEATHER_1)
_add('NoCrashTown01-v4', n_vehicles=20, disable_two_wheels=True, n_pedestrians=50, weathers=WEATHER_3)
_add('NoCrashTown01-v5', n_vehicles=100, disable_two_wheels=True, n_pedestrians=250, weathers=WEATHER_1)
_add('NoCrashTown01-v6', n_vehicles=100, disable_two_wheels=True, n_pedestrians=250, weathers=WEATHER_3)
# No ped versions
_add('NoCrashTown01-v3-np', n_vehicles=20, disable_two_wheels=True, n_pedestrians=0, weathers=WEATHER_1)
_add('NoCrashTown01-v4-np', n_vehicles=20, disable_two_wheels=True, n_pedestrians=0, weathers=WEATHER_3)
_add('NoCrashTown01-v5-np', n_vehicles=100, disable_two_wheels=True, n_pedestrians=0, weathers=WEATHER_1)
_add('NoCrashTown01-v6-np', n_vehicles=100, disable_two_wheels=True, n_pedestrians=0, weathers=WEATHER_3)

_add('NoCrashTown02-v1', n_vehicles=0, disable_two_wheels=True, weathers=WEATHER_1)
_add('NoCrashTown02-v2', n_vehicles=0, disable_two_wheels=True, weathers=WEATHER_3)
_add('NoCrashTown02-v3', n_vehicles=15, disable_two_wheels=True, n_pedestrians=50, weathers=WEATHER_1)
_add('NoCrashTown02-v4', n_vehicles=15, disable_two_wheels=True, n_pedestrians=50, weathers=WEATHER_3)
_add('NoCrashTown02-v5', n_vehicles=70, disable_two_wheels=True, n_pedestrians=150, weathers=WEATHER_1)
_add('NoCrashTown02-v6', n_vehicles=70, disable_two_wheels=True, n_pedestrians=150, weathers=WEATHER_3)
# No ped versions
_add('NoCrashTown02-v3-np', n_vehicles=15, disable_two_wheels=True, n_pedestrians=0, weathers=WEATHER_1)
_add('NoCrashTown02-v4-np', n_vehicles=15, disable_two_wheels=True, n_pedestrians=0, weathers=WEATHER_3)
_add('NoCrashTown02-v5-np', n_vehicles=70, disable_two_wheels=True, n_pedestrians=0, weathers=WEATHER_1)
_add('NoCrashTown02-v6-np', n_vehicles=70, disable_two_wheels=True, n_pedestrians=0, weathers=WEATHER_3)

# Demo
_add('NoCrashTown01-v7', n_vehicles=100, n_pedestrians=250, weathers=WEATHER_1)
_add('NoCrashTown01-v8', n_vehicles=100, n_pedestrians=250, weathers=WEATHER_2)
_add('NoCrashTown02-v7', n_vehicles=70, n_pedestrians=150, weathers=WEATHER_1)
_add('NoCrashTown02-v8', n_vehicles=70, n_pedestrians=150, weathers=WEATHER_2)


# Weather primes.
_add('FullTown01-v5', n_vehicles=0, weathers=WEATHER_4)
_add('FullTown01-v6', n_vehicles=20, weathers=WEATHER_4)
_add('StraightTown01-v3', n_vehicles=0, weathers=WEATHER_4)
_add('TurnTown01-v3', n_vehicles=0, weathers=WEATHER_4)

_add('FullTown02-v5', n_vehicles=0, weathers=WEATHER_4)
_add('FullTown02-v6', n_vehicles=15, weathers=WEATHER_4)
_add('StraightTown02-v3', n_vehicles=0, weathers=WEATHER_4)
_add('TurnTown02-v3', n_vehicles=0, weathers=WEATHER_4)

# Random
_add('NoCrashTown01_noweather_empty', weathers=[1], n_vehicles=0)
_add('NoCrashTown01_noweather_regular', weathers=[1], n_vehicles=20, n_pedestrians=50)
_add('NoCrashTown01_noweather_dense', weathers=[1], n_vehicles=100, n_pedestrians=250)

_add('NoCrashTown02_noweather_empty', weathers=[1], n_vehicles=0)
_add('NoCrashTown02_noweather_regular', weathers=[1], n_vehicles=15, n_pedestrians=50)
_add('NoCrashTown02_noweather_dense', weathers=[1], n_vehicles=70, n_pedestrians=200)

_add('StraightTown01-noweather', n_vehicles=0, weathers=[1])
_add('TurnTown01-noweather', n_vehicles=0, weathers=[1])
_add('FullTown01-noweather-nav', n_vehicles=0, weathers=[1])
_add('FullTown01-noweather', n_vehicles=20, weathers=[1])

_add('StraightTown02-noweather', n_vehicles=0, weathers=[1])
_add('TurnTown02-noweather', n_vehicles=0, weathers=[1])
_add('FullTown02-noweather-nav', n_vehicles=0, weathers=[1])
_add('FullTown02-noweather', n_vehicles=15, weathers=[1])


_aliases = {
        'debug' : ['DebugTown01-v0'],
        'town1': [
            'FullTown01-v1', 'FullTown01-v2', 'FullTown01-v3', 'FullTown01-v4',
            'StraightTown01-v1', 'StraightTown01-v2',
            'TurnTown01-v1', 'TurnTown01-v2'],
        'town1_s': [
            'StraightTown01-v1', 'StraightTown01-v2'
            ],
        'town1_turn1': [
            'TurnTown01-v4'],
        'xing_left_right':['Town01_Xing_left_right'], 
        'xing_straight_right':['Town01_Xing_straight_right'],
        'xing_straight_left':['Town01_Xing_straight_left'],
        'town1_t': [
            'TurnTown01-v1', 'TurnTown01-v2'],
        'town1_fnp': [
            'FullTown01-v1', 'FullTown01-v2'],
        'town1_f': [
            'FullTown01-v1', 'FullTown01-v2', 'FullTown01-v3', 'FullTown01-v4'],
        'town2': [
            'FullTown02-v1', 'FullTown02-v2', 'FullTown02-v3', 'FullTown02-v4',
            'StraightTown02-v1', 'StraightTown02-v2',
            'TurnTown02-v1', 'TurnTown02-v2'],
        'town2_s': [
            'StraightTown02-v1', 'StraightTown02-v2'],
        'town2_t': [
           'TurnTown02-v1', 'TurnTown02-v2'],
        'town2_f': [
            'FullTown02-v1', 'FullTown02-v2', 'FullTown02-v3', 'FullTown02-v4'],
        'town2_fwp': [
            'FullTown02-v3', 'FullTown02-v4'],
        'town2_fnp': [
            'FullTown02-v1', 'FullTown02-v2'],
        'town1p': [
            'FullTown01-v5', 'FullTown01-v6',
            'StraightTown01-v3', 'TurnTown01-v3',
            'FullTown01-v5', 'FullTown01-v6',
            ],
        'town2p': [
            'FullTown02-v5', 'FullTown02-v6',
            'StraightTown02-v3', 'TurnTown02-v3',
            'FullTown02-v5', 'FullTown02-v6',
            ],
        'ntown1p': [
            'NoCrashTown01-v7', 'NoCrashTown01-v8', 'NoCrashTown01-v9',
            ],

        'ntown2p': [
            'NoCrashTown02-v7', 'NoCrashTown02-v8', 'NoCrashTown02-v9',
            ],
        'empty': [
            'NoCrashTown01-v1', 'NoCrashTown01-v2',
            'NoCrashTown02-v1', 'NoCrashTown02-v2',
            ],
        'regular': [
            'NoCrashTown01-v3', 'NoCrashTown01-v4',
            'NoCrashTown02-v3', 'NoCrashTown02-v4',
            ],
        'regular-np': [
            'NoCrashTown01-v3-np', 'NoCrashTown01-v4-np',
            'NoCrashTown02-v3-np', 'NoCrashTown02-v4-np',
            ],
        'dense': [
            'NoCrashTown01-v5', 'NoCrashTown01-v6',
            'NoCrashTown02-v5', 'NoCrashTown02-v6',
            ],
        'dense-np': [
            'NoCrashTown01-v5-np', 'NoCrashTown01-v6-np',
            'NoCrashTown02-v5-np', 'NoCrashTown02-v6-np',
            ]
        }

_aliases['all'] = _aliases['town1'] + _aliases['town2']

ALL_SUITES = list(_suites.keys()) + list(_aliases.keys())


def make_suite(suite_name, port=2000, big_cam=False, planner='new', client=None, apply_thresh=True, threshold=[15,5]):
    assert suite_name in _suites, '%s is not registered!'%suite_name

    args, kwargs = _suites[suite_name]
    kwargs['port'] = port
    kwargs['big_cam'] = big_cam
    kwargs['planner'] = planner
    kwargs['client'] = client
    kwargs['apply_thresh']=apply_thresh
    kwargs['threshold']=threshold

    return PointGoalSuite(*args, **kwargs)


def get_suites(suite_name):
    if suite_name.lower() in _aliases:
        return _aliases[suite_name]

    return [suite_name]
