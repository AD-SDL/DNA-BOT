metadata = {
     'apiLevel': '2.8',
     'protocolName': 'CLIP_With_Thermocycler',
     'author': 'Group 4',
     'description': 'Implements linker ligation reactions using an opentrons OT-2, including the thermocycler module.'}

def run(protocol):
    tc_mod = protocol.load_module('Thermocycler Module')
    tc_mod.open_lid()
    source_plate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '2')
    destination_plate = tc_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    PIPETTE_TYPE = 'p1000_single'
    PIPETTE_MOUNT = 'left'
    tiprack_type = "opentrons_96_tiprack_1000ul"
    tiprack = protocol.load_labware(tiprack_type, '3')
    pipette = protocol.load_instrument(PIPETTE_TYPE, PIPETTE_MOUNT, tip_racks=[tiprack])
    source_wells = ['A1', 'B1', 'C1', 'D1', 'E3', 'F3', 'G3', 'H3']
    destination_wells = ['A1', 'B1', 'C1', 'D1', 'E3', 'F3', 'G3', 'H3']
    #pipette.pick_up_tip()
    #pipette.aspirate(10, source_plate['A1'])
    #pipette.dispense(10, destination_plate['A1'])
    #pipette.drop_tip()
    
    for clip_num in range(len(source_wells)):
        pipette.pick_up_tip()
        pipette.aspirate(50, source_plate[source_wells[clip_num]])
        pipette.dispense(50, destination_plate[destination_wells[clip_num]])
        pipette.drop_tip()


