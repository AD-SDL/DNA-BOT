from opentrons import simulate, protocol_api
import numpy as np
import sys
sys.path.append(".")
from . import custom_utils
# metadata
metadata = {
'protocolName': 'My Protocol',
'author': 'Name <email@address.com>',
'description': 'Simple protocol to get started using OT2',
'apiLevel': '2.7'
}
#protocol = simulate.get_protocol_api('2.7')
# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
# where to look for autocomplete suggestions

final_assembly_dict={"A1": ["A7", "G7", "H7", "B8", "E8"], "B1": ["A7", "G7", "H7", "B8", "G8"], "C1": ["A7", "G7", "H7", "A9", "E8"], "D1": ["A7", "G7", "H7", "A9", "G8"], "E1": ["A7", "D9", "B8", "E9", "G9"], "F1": ["A7", "D9", "B8", "A10", "G9"], "G1": ["A7", "D9", "A9", "E9", "G9"], "H1": ["A7", "D9", "A9", "A10", "G9"], "A2": ["A7", "G7", "C10", "B8", "E8"], "B2": ["A7", "G7", "C10", "B8", "G8"], "C2": ["A7", "G7", "C10", "A9", "E8"], "D2": ["A7", "G7", "C10", "A9", "G8"], "E2": ["A7", "D9", "B8", "E9", "E10"], "F2": ["A7", "D9", "B8", "A10", "E10"], "G2": ["A7", "D9", "A9", "E9", "E10"], "H2": ["B7", "D9", "A9", "A10", "E10"], "A3": ["B7", "G10", "H10", "B8", "E8"], "B3": ["B7", "G10", "H10", "B8", "G8"], "C3": ["B7", "G10", "H10", "A9", "E8"], "D3": ["B7", "G10", "H10", "A9", "G8"], "E3": ["B7", "A11", "B8", "E9", "B11"], "F3": ["B7", "A11", "B8", "A10", "B11"], "G3": ["B7", "A11", "A9", "E9", "B11"], "H3": ["B7", "A11", "A9", "A10", "B11"], "A4": ["B7", "G10", "H7", "B8", "E8"], "B4": ["B7", "G10", "H7", "B8", "G8"], "C4": ["B7", "G10", "H7", "A9", "E8"], "D4": ["B7", "G10", "H7", "A9", "G8"], "E4": ["B7", "A11", "B8", "E9", "G9"], "F4": ["B7", "A11", "C8", "A10", "G9"], "G4": ["C7", "A11", "A9", "E9", "G9"], "H4": ["C7", "A11", "B9", "A10", "G9"], "A5": ["C7", "G10", "C10", "C8", "E8"], "B5": ["C7", "G10", "C10", "C8", "G8"], "C5": ["C7", "G10", "C10", "B9", "E8"], "D5": ["C7", "G10", "C10", "B9", "G8"], "E5": ["C7", "A11", "C8", "E9", "E10"], "F5": ["C7", "A11", "C8", "A10", "E10"], "G5": ["C7", "A11", "B9", "E9", "E10"], "H5": ["C7", "A11", "B9", "A10", "E10"], "A6": ["C7", "C11", "H10", "C8", "E8"], "B6": ["C7", "C11", "H10", "C8", "G8"], "C6": ["C7", "C11", "H10", "B9", "E8"], "D6": ["C7", "C11", "H10", "B9", "G8"], "E6": ["C7", "D11", "C8", "E9", "B11"], "F6": ["D7", "D11", "C8", "A10", "B11"], "G6": ["D7", "D11", "B9", "E9", "B11"], "H6": ["D7", "D11", "B9", "A10", "B11"], "A7": ["D7", "C11", "H7", "C8", "E8"], "B7": ["D7", "C11", "H7", "C8", "G8"], "C7": ["D7", "C11", "H7", "B9", "E8"], "D7": ["D7", "C11", "H7", "B9", "G8"], "E7": ["D7", "D11", "C8", "E9", "G9"], "F7": ["D7", "D11", "C8", "A10", "G9"], "G7": ["D7", "D11", "B9", "E9", "G9"], "H7": ["D7", "D11", "B9", "A10", "G9"], "A8": ["D7", "C11", "C10", "C8", "E8"], "B8": ["D7", "C11", "C10", "C8", "G8"], "C8": ["D7", "C11", "C10", "B9", "F8"], "D8": ["D7", "C11", "C10", "B9", "H8"], "E8": ["E7", "D11", "D8", "E9", "E10"], "F8": ["E7", "D11", "D8", "A10", "E10"], "G8": ["E7", "D11", "C9", "F9", "E10"], "H8": ["E7", "D11", "C9", "B10", "E10"], "A9": ["E7", "E11", "H10", "D8", "F8"], "B9": ["E7", "E11", "H10", "D8", "H8"], "C9": ["E7", "E11", "H10", "C9", "F8"], "D9": ["E7", "E11", "H10", "C9", "H8"], "E9": ["E7", "F11", "D8", "F9", "B11"], "F9": ["E7", "F11", "D8", "B10", "B11"], "G9": ["E7", "F11", "C9", "F9", "B11"], "H9": ["E7", "F11", "C9", "B10", "B11"], "A10": ["E7", "E11", "H7", "D8", "F8"], "B10": ["E7", "E11", "H7", "D8", "H8"], "C10": ["E7", "E11", "H7", "C9", "F8"], "D10": ["F7", "E11", "A8", "C9", "H8"], "E10": ["F7", "F11", "D8", "F9", "G9"], "F10": ["F7", "F11", "D8", "B10", "G9"], "G10": ["F7", "F11", "C9", "F9", "G9"], "H10": ["F7", "F11", "C9", "B10", "H9"], "A11": ["F7", "E11", "C10", "D8", "F8"], "B11": ["F7", "E11", "C10", "D8", "H8"], "C11": ["F7", "E11", "C10", "C9", "F8"], "D11": ["F7", "E11", "D10", "C9", "H8"], "E11": ["F7", "F11", "D8", "F9", "E10"], "F11": ["F7", "F11", "D8", "B10", "E10"], "G11": ["F7", "F11", "C9", "F9", "E10"], "H11": ["F7", "F11", "C9", "B10", "F10"]}
tiprack_num=5


def run(protocol:protocol_api.ProtocolContext):
    def final_assembly(final_assembly_dict, tiprack_num, tiprack_type="opentrons_96_filtertiprack_20ul"):
                # Constants, we update all the labware name in version 2
                #Tiprack
#                 CANDIDATE_TIPRACK_SLOTS = ['6', '9', '3', '2', '10', '8', '11']
                CANDIDATE_TIPRACK_SLOTS = ['6', '9', '11'] # add more if needed
                PIPETTE_MOUNT = 'right'
                #Plate of sample after  purification
                MAG_PLATE_TYPE = 'nest_96_wellplate_100ul_pcr_full_skirt'
                MAG_PLATE_POSITION = '5'
                #Tuberack
                TUBE_RACK_TYPE = 'nest_96_wellplate_2ml_deep'
                TUBE_RACK_POSITION = '10'
                #Destination plate
                DESTINATION_PLATE_TYPE = 'opentrons_96_aluminumblock_generic_pcr_strip_200ul'
                #Temperature control plate
                TEMPDECK_SLOT = '4'
                TEMP = 20
                TOTAL_VOL = 15
                PART_VOL = 1.5
                MIX_SETTINGS = (1, 3)
                tiprack_num=tiprack_num+1

                slots = CANDIDATE_TIPRACK_SLOTS[:tiprack_num]
                tipracks = [protocol.load_labware(tiprack_type, slot)
                    for slot in slots]

                # for transfers
                reverse_tips = [tipracks[i].wells()[::-1] for i in range(len(tipracks))]
                tip_at = 0

                # Errors
                sample_number = len(final_assembly_dict.keys())
                if sample_number > 96:
                    raise ValueError('Final assembly nummber cannot exceed 96.')


                pipette = protocol.load_instrument('p20_multi_gen2', PIPETTE_MOUNT, tip_racks=tipracks)#old code: pipette = instruments.P10_Single(mount=PIPETTE_MOUNT, tip_racks=tipracks)
                # Define Labware and set temperature
                magbead_plate = protocol.load_labware(MAG_PLATE_TYPE, MAG_PLATE_POSITION)
               #old code: magbead_plate = labware.load(MAG_PLATE_TYPE, MAG_PLATE_POSITION)
                tube_rack = protocol.load_labware(TUBE_RACK_TYPE, TUBE_RACK_POSITION)
               #old code: tube_rack = labware.load(TUBE_RACK_TYPE, TUBE_RACK_POSITION)
                tempdeck = protocol.load_module('temperature module gen2', TEMPDECK_SLOT)
               #old code: tempdeck = modules.load('tempdeck', TEMPDECK_SLOT)
                destination_plate = tempdeck.load_labware(
                DESTINATION_PLATE_TYPE, TEMPDECK_SLOT)
                tempdeck.set_temperature(TEMP)
               #old code: destination_plate = labware.load(DESTINATION_PLATE_TYPE, TEMPDECK_SLOT, share=True)tempdeck.set_temperature(TEMP)tempdeck.wait_for_temp()

                # Master mix transfers
                final_assembly_lens = []
                for values in final_assembly_dict.values():
                    final_assembly_lens.append(len(values))
                unique_assemblies_lens = list(set(final_assembly_lens))
                # master_mix_well_letters = ['A', 'B', 'C', 'D']
                for x in unique_assemblies_lens:
                    # to use as 8 channel, start well must be A
                    master_mix_well = 'A1'  # master_mix_well_letters[(x - 1) // 6] + str(x - 1)
                    # assume that every 8th index starts at A so we can use 8 channel
                    destination_inds = [i for i, lens in enumerate(final_assembly_lens) if lens == x][::8]
                    destination_wells = np.array([key for key, value in list(final_assembly_dict.items())])
                    destination_wells = list(destination_wells[destination_inds])
                    destination_wells = [destination_plate.wells_by_name()[i] for i in destination_wells]
                    custom_transfer_mastermix_water(pipette, TOTAL_VOL - x * PART_VOL,
                                                                 tube_rack.wells_by_name()[master_mix_well],
                                                                 destination_wells, new_tip='once')
                    tip_at += 8

                    '''
                     1 channel code
                    pipette.pick_up_tip(reverse_tips[tip_at // 96][tip_at % 96])
                    for destination_well in destination_wells:# make tube_rack_wells and destination_plate.wells in the same type
                        pipette.aspirate(TOTAL_VOL - x * PART_VOL, tube_rack.wells_by_name()[master_mix_well])
                        pipette.dispense(TOTAL_VOL - x * PART_VOL,destination_plate.wells_by_name()[destination_well])
                    pipette.drop_tip()
                    tip_at +=1
                    '''


                # We now need to switch the reverse pick algorithm so set an offset for the current rack
                offset_by_rack = switch_from_8_to_1(reverse_tips, tip_at)

                # Part transfers
                for key, values in list(final_assembly_dict.items()):
                    for value in values:# magbead_plate.wells and destination_plate.wells in the same type
                        # pipette.transfer(PART_VOL, magbead_plate.wells(value),
                        #                  destination_plate.wells(key), mix_after=MIX_SETTINGS,
                        #                  new_tip='always')#transfer parts in one tube

                        pipette.pick_up_tip(get_tip(tip_at, offset_by_rack, reverse_tips))
                        pipette.aspirate(PART_VOL, magbead_plate.wells_by_name()[value])
                        pipette.dispense(PART_VOL,destination_plate.wells_by_name()[key])
                        pipette.mix(3)

                        tip_at += 1
                        pipette.drop_tip()

                tempdeck.deactivate() #stop increasing the temperature

    final_assembly(final_assembly_dict=final_assembly_dict, tiprack_num=tiprack_num)

# run(protocol)
#
# for line in protocol.commands():
#     print(line)
