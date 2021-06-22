from opentrons import protocol_api, simulate, execute
protocol = simulate.get_protocol_api('2.8')
protocol.home()

# metadata
metadata = {
    'apiLevel': '2.8',
    'protocolName': 'CLIP_No_Thermocycler',
    'author': 'Group 4 & GB',
    'description': 'Implements linker ligation reactions using an opentrons OT-2. This version does not include the Thermocycler module.'}


def run(protocol):
    PIPETTE_TYPE = 'p20_multi_gen2'
    PIPETTE_MOUNT = 'right'
    TIPRACK_TYPE = 'opentrons_96_tiprack_300ul'  # "opentrons_96_tiprack_10ul"

    tipracks = None
    pipette = protocol.load_instrument(PIPETTE_TYPE, mount=PIPETTE_MOUNT, tip_racks=None)

    if pipette.has_tip:
        pipette.drop_tip()
    else:
        print("Pipette does not recognize the tip, manually remove it.")

for line in protocol.commands():
    print(line)