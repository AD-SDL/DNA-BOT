metadata = {
    'apiLevel': '2.8',
    'protocolName': 'Dummy Script to test camera',
    'author': 'shahashka@anl.gov',
    'description': ''}

def run(protocol):
        plate = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", 5)
        p20_tipracks = [protocol.load_labware("opentrons_96_tiprack_20ul", 1)]

        p20_pipette = protocol.load_instrument('p20_single_gen2', mount='right',
                                               tip_racks=p20_tipracks)
        source= plate.wells_by_name()['A1']

        # Show camera
        CAMERA_HEIGHT=20
        p20_pipette.pick_up_tip()
        p20_pipette.move_to(source.top(CAMERA_HEIGHT))
        p20_pipette.return_tip()