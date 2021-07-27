# Final version of the purification template to be used in actual DNA assembly experiment
# with all the correct labware

metadata = {
    'apiLevel': '2.8',
    'protocolName': 'calibrate all labware for DNA Assembly protocols',
    'author': 'shahashka@anl.gov',
    'description': ''}


def run(protocol):
    tipracks_20 = [protocol.load_labware("opentrons_96_tiprack_20ul", 3)]

    pipette_20 = protocol.load_instrument("p20_single_gen2", mount="right", tip_racks=tipracks_20)

    well_plate = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", 6)
    tube_rack = protocol.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", 2)

    MAGDECK = protocol.load_module('magnetic module gen2', 1)
    mag_plate = MAGDECK.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")

    pipette_20.pick_up_tip()
    pipette_20.aspirate(1, tube_rack.wells_by_name()['A1'])
    pipette_20.dispense(1, well_plate.wells_by_name()['A1'])
    pipette_20.return_tip()

    pipette_20.pick_up_tip()
    pipette_20.aspirate(1, tube_rack.wells_by_name()['A1'])
    pipette_20.dispense(1, mag_plate.wells_by_name()['A1'])
    pipette_20.return_tip()