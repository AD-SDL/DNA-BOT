# Final version of the purification template to be used in actual DNA assembly experiment
# with all the correct labware

metadata = {
    'apiLevel': '2.8',
    'protocolName': 'calibrate all labware for DNA Assembly protocols',
    'author': 'shahashka@anl.gov',
    'description': ''}


def run(protocol):
    tipracks_300 = [protocol.load_labware("opentrons_96_tiprack_300ul", 3)]

    pipette_300 = protocol.load_instrument("p300_multi_gen2", mount="left", tip_racks=tipracks_300)

    trough = protocol.load_labware("4ti0131_12_reservoir_21000ul", 6)
    deep_well = protocol.load_labware("nest_96_wellplate_2ml_deep", 2)

    TEMPDECK = protocol.load_module('temperature module gen2', 1)
    THERMOCYCLER = protocol.load_module('Thermocycler Module') # default 10/7/11/8 slots
    temp_plate = TEMPDECK.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")
    tc_plate = THERMOCYCLER.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")

    pipette_300.pick_up_tip()
    pipette_300.aspirate(1, deep_well.wells_by_name()['A1'])
    pipette_300.dispense(1, tc_plate.wells_by_name()['A1'])
    pipette_300.drop_tip()

    pipette_300.pick_up_tip()
    pipette_300.aspirate(1, trough.wells_by_name()['A1'])
    pipette_300.dispense(1, temp_plate.wells_by_name()['A1'])
    pipette_300.drop_tip()