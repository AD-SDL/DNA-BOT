# Final version of the assembly template to be used in actual DNA assembly experiment
# with all the correct labware
import numpy as np
# metadata
metadata = {
'protocolName': 'My Protocol',
'author': 'Name <email@address.com>',
'description': 'Simple protocol to get started using OT2',
'apiLevel': '2.8'
}

final_assembly_dict={"A1": ["A7", "B7"], "B1": ["A7", "C7"], "C1": ["D7", "E7"], "D1": ["D7", "F7"], "E1": ["G7", "H7"], "F1": ["G7", "A8"]}
tiprack_num=1


def run(protocol):

    def final_assembly(final_assembly_dict, tiprack_num, tiprack_type="opentrons_96_tiprack_20ul"):
                # Constants, we update all the labware name in version 2
                #Tiprack
                CANDIDATE_TIPRACK_SLOTS = ['3']
                PIPETTE_MOUNT_multi = 'left'
                PIPETTE_MOUNT_single = 'right'
                #Plate of sample after  purification
                MAG_PLATE_TYPE = 'nest_96_wellplate_100ul_pcr_full_skirt'
                MAG_PLATE_POSITION = '5'
                #Tuberack
                TUBE_RACK_TYPE = 'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap'
                TUBE_RACK_POSITION = '1' #moved bc thermocycler is in 7
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
                master_mix_well_letters = ['A', 'B', 'C', 'D']
                for x in unique_assemblies_lens:
                    master_mix_well = master_mix_well_letters[(x - 1) // 6] + str(x - 1) # A4
                    destination_inds = [i for i, lens in enumerate(final_assembly_lens) if lens == x]
                    destination_wells = np.array([key for key, value in list(final_assembly_dict.items())])
                    destination_wells = list(destination_wells[destination_inds])
                    destination_wells = [destination_plate.wells_by_name()[i] for i in destination_wells]
                    pipette_single.transfer(TOTAL_VOL - x * PART_VOL,
                                                                 tube_rack.wells_by_name()[master_mix_well],
                                                                 destination_wells, new_tip='once', blow_out=True,
                                           blowout_location="destination well")

                # Part transfers
                for key, values in list(final_assembly_dict.items()):
                    for value in values:# magbead_plate.wells and destination_plate.wells in the same type
                        pipette_single.transfer(PART_VOL, magbead_plate.wells_by_name()[value],
                                         destination_plate.wells_by_name()[key], mix_after=MIX_SETTINGS,
                                         new_tip='always', blow_out=True, blowout_location="destination well")#transfer parts in one tube

                tempdeck.deactivate() #stop increasing the temperature

                protocol.pause('Transfer the plate to the thermocycler. Type yes to resume.')

                # Thermocycler Module
                tc_mod = protocol.load_module('thermocycler module')
                tc_mod.close_lid()
                tc_mod.set_lid_temperature(105)
                tc_mod.set_block_temperature(50, hold_time_minutes=45, block_max_volume=15)
                tc_mod.set_block_temperature(4, hold_time_minutes=2, block_max_volume=30)
                # Increase the hold time at 4 C if necessary
                tc_mod.set_lid_temperature(37)
                tc_mod.open_lid()

    final_assembly(final_assembly_dict=final_assembly_dict, tiprack_num=tiprack_num)

