metadata = {
     'apiLevel': '2.8'}

def run(protocol):
    source_plate = protocol.load_labware('nest_96_wellplate_2ml_deep', '8')
    destination_plate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '5')
    PIPETTE_TYPE = 'p300_multi_gen2'
    PIPETTE_MOUNT = 'right'
    tiprack_type = "opentrons_96_tiprack_300ul"
    tiprack = protocol.load_labware(tiprack_type, '11')
    pipette = protocol.load_instrument(PIPETTE_TYPE, PIPETTE_MOUNT, tip_racks=[tiprack])
    source_wells = ['A11', 'A12']
    destination_wells = ['A1', 'A12']

    for clip_num in range(len(source_wells)):
        pipette.pick_up_tip()
        pipette.aspirate(75, source_plate[source_wells[clip_num]])
        pipette.dispense(75, destination_plate[destination_wells[clip_num]])
        pipette.drop_tip()
    