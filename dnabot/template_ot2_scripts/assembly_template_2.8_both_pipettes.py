from opentrons import simulate, protocol_api
import numpy as np
# metadata
metadata = {
'protocolName': 'My Protocol',
'author': 'Name <email@address.com>',
'description': 'Simple protocol to get started using OT2',
'apiLevel': '2.8'
}
#protocol = simulate.get_protocol_api('2.7')
# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
# where to look for autocomplete suggestions

def run(protocol:protocol_api.ProtocolContext):
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    def final_assembly(final_assembly_dict, tiprack_num, tiprack_type="opentrons_96_filtertiprack_20ul"):
                # Constants, we update all the labware name in version 2
                #Tiprack
                CANDIDATE_TIPRACK_SLOTS = ['3', '6', '9', '2', '8', '10', '11']
                PIPETTE_MOUNT_multi = 'right'
                PIPETTE_MOUNT_single = 'left'
                #Plate of sample after  purification
                MAG_PLATE_TYPE = 'nest_96_wellplate_100ul_pcr_full_skirt'
                MAG_PLATE_POSITION = '5'
                #Tuberack
                TUBE_RACK_TYPE = 'nest_96_wellplate_2ml_deep'
                TUBE_RACK_POSITION = '7'
                #Destination plate
                DESTINATION_PLATE_TYPE = 'opentrons_96_aluminumblock_nest_wellplate_100ul'
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

                # Errors
                sample_number = len(final_assembly_dict.keys())
                if sample_number > 96:
                    raise ValueError('Final assembly nummber cannot exceed 96.')

                pipette_single = protocol.load_instrument('p20_single_gen2', PIPETTE_MOUNT_single, tip_racks=tipracks)
                pipette_multi = protocol.load_instrument('p20_multi_gen2', PIPETTE_MOUNT_multi, tip_racks=tipracks)#old code: pipette = instruments.P10_Single(mount=PIPETTE_MOUNT, tip_racks=tipracks)
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
                    # After ~3 transfers with the same tips, dripping is expected so drop the tip after 4 columns
                    for d in list(chunks(destination_wells, 3)):
                        pipette_multi.transfer(TOTAL_VOL - x * PART_VOL,
                                                                     tube_rack.wells_by_name()[master_mix_well],
                                                                     d, touch_tip=True,
                                               new_tip='once', trash=False, blow_out=True,
                                           blowout_location="destination well")

                    '''
                     1 channel code
                    pipette.pick_up_tip(reverse_tips[tip_at // 96][tip_at % 96])
                    for destination_well in destination_wells:# make tube_rack_wells and destination_plate.wells in the same type
                        pipette.aspirate(TOTAL_VOL - x * PART_VOL, tube_rack.wells_by_name()[master_mix_well])
                        pipette.dispense(TOTAL_VOL - x * PART_VOL,destination_plate.wells_by_name()[destination_well])
                    pipette.drop_tip()
                    tip_at +=1
                    '''

                # Part transfers
                for key, values in list(final_assembly_dict.items()):
                    for value in values:# magbead_plate.wells and destination_plate.wells in the same type
                        pipette_single.transfer(PART_VOL, magbead_plate.wells_by_name()[value],
                                         destination_plate.wells_by_name()[key], mix_after=MIX_SETTINGS,
                                         new_tip='always', trash=False, blow_out=True, blowout_location="destination well")#transfer parts in one tube

                tempdeck.deactivate() #stop increasing the temperature

    final_assembly(final_assembly_dict=final_assembly_dict, tiprack_num=tiprack_num)

