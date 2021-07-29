
# metadata
metadata = {
    'apiLevel': '2.8',
    'protocolName': 'CLIP_No_Thermocycler',
    'author': 'Group 4 & GB',
    'description': 'Implements linker ligation reactions using an opentrons OT-2. This version does not include the Thermocycler module.'}


def run(protocol):
    PIPETTE_TYPE = 'p300_multi_gen2'
    PIPETTE_MOUNT = 'left'
    tipracks = [protocol.load_labware("opentrons_96_tiprack_300ul", 2)]

    pipette = protocol.load_instrument(PIPETTE_TYPE, mount=PIPETTE_MOUNT, tip_racks=tipracks)
    deepwell = protocol.load_labware("nest_96_wellplate_2ml_deep", 1)
    pipette.pick_up_tip()
    pipette.aspirate(54, deepwell.wells_by_name()['A1'])
    pipette.dispense(54, deepwell.wells_by_name()['A2'])
    pipette.return_tip()