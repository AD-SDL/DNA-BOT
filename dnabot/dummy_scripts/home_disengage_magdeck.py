from opentrons import protocol_api, simulate, execute
protocol = simulate.get_protocol_api('2.8')
protocol.home()

# metadata
metadata = {
    'apiLevel': '2.8',
    'protocolName': 'Dummy Script to Disengage Magdeck',
    'author': 'Group 4 & GB',
    'description': 'Implements linker ligation reactions using an opentrons OT-2. This version does not include the Thermocycler module.'}

def run(protocol):
    PIPETTE_TYPE = 'p20_multi_gen2'
    PIPETTE_MOUNT = 'right'
    TIPRACK_TYPE = 'opentrons_96_tiprack_300ul'  # "opentrons_96_tiprack_10ul"

    MAGDECK = protocol.load_module('magnetic module gen2', '1')
    MAGDECK.engage()
    MAGDECK.disengage()

for line in protocol.commands():
    print(line)