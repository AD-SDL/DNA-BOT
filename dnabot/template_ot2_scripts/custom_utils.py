def custom_transfer_mastermix_water(pipette, vol, source, destination_wells, new_tip='once'):
    if new_tip == 'once':
        pipette.pick_up_tip()
    for i in range(len(destination_wells)):
        if new_tip == 'always':
            pipette.pick_up_tip()
        if type(vol) == list:
            pipette.aspirate(vol[i], source)
            pipette.dispense(vol[i], destination_wells[i])
        else:
            pipette.aspirate(vol, source)
            pipette.dispense(vol, destination_wells[i])
        pipette.blow_out()
        pipette.blow_out()
        pipette.blow_out()
        if new_tip == 'always':
            pipette.drop_tip()
    if new_tip == 'once':
        pipette.drop_tip()


# Calculates which rack and tip within rack to pick up based on how many have already been picked up
# accomodates a switch from 8 channel functionality with 'transfer' and 1 channel functionality
def get_tip(index, offsets, tips):
    return tips[int(index // 96)][index % 96 - offsets[index // 96]]

# After transfering MM, water as 8 channel now direct the pipette to pick up tips from the end
# Need to set offset so that pipette correctly transitions to using next tip rack
def switch_from_8_to_1(reverse_tips, tip_at):
    # We now need to switch the reverse pick algorithm so set an offset for the current rack
    offset_by_rack = len(reverse_tips) * [0]
    current_rack = tip_at // 96
    for i in range(len(offset_by_rack)):
        if current_rack == i:
            offset_by_rack[i] = tip_at
    return offset_by_rack
