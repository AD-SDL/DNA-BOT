metadata = {
    'apiLevel': '2.8',
    'protocolName': 'Dummy Script to spot agar plate',
    'author': 'shahashka@anl.gov',
    'description': ''}

def run(protocol):
        agar = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", 1)
        plate = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", 2)
        p20_tipracks = [protocol.load_labware("opentrons_96_tiprack_20ul", 3)]

        p20_pipette = protocol.load_instrument('p20_single_gen2', mount='right',
                                               tip_racks=p20_tipracks)

        dead_vol=2
        spotting_dispense_rate=0.025
        stabbing_depth=10
        max_spot_vol=5
        spot_vol=5
        source= plate.wells_by_name()['A1']
        target=agar.wells_by_name()['B1']


        # Constants
        DEFAULT_HEAD_SPEED = {'x': 400, 'y': 400, 'z': 125, 'a': 125}
        SPOT_HEAD_SPEED = {'x': 400, 'y': 400, 'z': 125, 'a': 125 // 4}
        DISPENSING_HEIGHT = 0
        SAFE_HEIGHT = 15  # height avoids collision with agar tray.

        # Spot
        p20_pipette.pick_up_tip()
        p20_pipette.aspirate(spot_vol + dead_vol, source)

        p20_pipette.move_to(target.top(SAFE_HEIGHT))
        p20_pipette.move_to(target.top(DISPENSING_HEIGHT))
        p20_pipette.dispense(volume=spot_vol, rate=spotting_dispense_rate)
        protocol.max_speeds.update(SPOT_HEAD_SPEED)
        p20_pipette.move_to(target.top(-1 * stabbing_depth))
        protocol.max_speeds.update(DEFAULT_HEAD_SPEED)
        p20_pipette.move_to(target.top(SAFE_HEIGHT))
        p20_pipette.drop_tip()