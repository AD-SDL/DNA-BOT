# metadata
metadata = {
    'apiLevel': '2.8',
    'protocolName': 'Switch pipette',
    'author': 'Group 4 & GB',
    'description': 'Changing pipettes.'}


def run(protocol):
    # Thermocycler Module
    tc_mod = protocol.load_module('thermocycler module')
    tc_mod.set_lid_temperature(105)
    tc_mod.set_block_temperature(50, hold_time_minutes=45, block_max_volume=15)
    tc_mod.set_block_temperature(4, hold_time_minutes=2, block_max_volume=30)

    # Increase the hold time at 4 C if necessary
    tc_mod.set_lid_temperature(37)
    tc_mod.open_lid()