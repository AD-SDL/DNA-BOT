from opentrons import protocol_api, simulate, execute
# protocol = simulate.get_protocol_api('2.8')
# protocol.home()

# metadata
metadata = {
    'apiLevel': '2.8',
    'protocolName': 'Switch pipette',
    'author': 'Group 4 & GB',
    'description': 'Changing pipettes.'}


def run(protocol):
    PIPETTE_TYPE_1 = 'p20_multi_gen2'
    PIPETTE_TYPE_2 = 'p300_multi_gen2'
    PIPETTE_MOUNT_1 = 'right'
    PIPETTE_MOUNT_2 = 'left'

    tiprack_1 = protocol.load_labware("opentrons_96_tiprack_20ul", "1")
    tiprack_2 = protocol.load_labware("opentrons_96_tiprack_300ul", "2")
    pipette_1 = protocol.load_instrument(PIPETTE_TYPE_1, mount=PIPETTE_MOUNT_1, tip_racks=[tiprack_1])
    pipette_2 = protocol.load_instrument(PIPETTE_TYPE_2, mount=PIPETTE_MOUNT_2, tip_racks=[tiprack_2])

    pipette_1.pick_up_tip()
    pipette_1.drop_tip()
    pipette_2.pick_up_tip()
    pipette_2.drop_tip()

# for line in protocol.commands():
#     print(line)