# Final version of the clips template to be used in actual DNA assembly experiment
# with all the correct labware
metadata = {
     'apiLevel': '2.8',
     'protocolName': 'CLIP_With_Thermocycler',
     'author': 'Group 4',
     'description': 'Implements linker ligation reactions using an opentrons OT-2, including the thermocycler module.'}

# example dictionary produced by DNA-BOT for a single construct containing 5 parts, un-comment and run to test the template
    # clips_dict={"prefixes_wells": ["A8", "A7", "C5", "C7", "C10"], "prefixes_plates": ["2", "2", "2", "2", "2"], "suffixes_wells": ["B7", "C1", "C2", "C3", "B8"], "suffixes_plates": ["2", "2", "2", "2", "2"], "parts_wells": ["E2", "F2", "C2", "B2", "D2"], "parts_plates": ["5", "5", "5", "5", "5"], "parts_vols": [1, 1, 1, 1, 1], "water_vols": [7.0, 7.0, 7.0, 7.0, 7.0]}

clips_dict = {"prefixes_wells": ["A8", "A7", "C5", "C7", "C10"], "prefixes_plates": ["2", "2", "2", "2", "2"],
              "suffixes_wells": ["B7", "C1", "C2", "C3", "B8"], "suffixes_plates": ["2", "2", "2", "2", "2"],
              "parts_wells": ["E2", "F2", "C2", "B2", "D2"], "parts_plates": ["5", "5", "5", "5", "5"],
              "parts_vols": [1, 1, 1, 1, 1], "water_vols": [7.0, 7.0, 7.0, 7.0, 7.0]}


clips_dict={"prefixes_wells": ["A1", "A3", "A3", "A5", "A3", "A3", "A7", "A3", "A3"], "prefixes_plates": ["5", "5", "5", "5", "5", "5", "5", "5", "5"], "suffixes_wells": ["A4", "A2", "A2", "A4", "A2", "A2", "A4", "A2", "A2"], "suffixes_plates": ["5", "5", "5", "5", "5", "5", "5", "5", "5"], "parts_wells": ["B1", "B2", "B3", "B1", "B2", "B3", "B1", "B2", "B3"], "parts_plates": ["5", "5", "5", "5", "5", "5", "5", "5", "5"], "parts_vols": [1, 1, 1, 1, 1, 1, 1, 1, 1], "water_vols": [7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0]}


def run(protocol):
    # added run function for API 2.8

    ### Constants - these have been moved out of the def clip() for clarity

    # Tiprack
    tiprack_type = "opentrons_96_tiprack_20ul"
    INITIAL_TIP = 'A1'
    CANDIDATE_TIPRACK_SLOTS = ['1']

    # Pipettes - pipette instructions in a single location so redefining pipette type is simpler
    PIPETTE_TYPE_multi = 'p20_multi_gen2'
    # API 2 supports gen_1 pipettes like the p10_single
    PIPETTE_MOUNT_multi = 'right'
    ### Load Pipette
    # checks if it's a P20 Multi pipette
    if PIPETTE_TYPE_multi != 'p20_multi_gen2':
        print('Define labware must be changed to use', PIPETTE_TYPE_multi)
        exit()


    PIPETTE_TYPE_single = 'p20_single_gen2'
    PIPETTE_MOUNT_single = 'left'
    ### Load Pipette
    # checks if it's a P20 Single pipette
    if PIPETTE_TYPE_single != 'p20_single_gen2':
        print('Define labware must be changed to use', PIPETTE_TYPE_single)
        exit()

    # Thermocycler Module
    DESTINATION_PLATE_TYPE = 'nest_96_wellplate_100ul_pcr_full_skirt'
    tc_mod = protocol.load_module('Thermocycler Module')
    # Loads destination plate onto Thermocycler Module
    destination_plate = tc_mod.load_labware(DESTINATION_PLATE_TYPE)

    # Source Plates
    SOURCE_PLATE_TYPE = 'nest_96_wellplate_100ul_pcr_full_skirt'
    # modified from custom labware as API 2 doesn't support labware.create anymore, so the old add_labware script can't be used

    # Tube Rack
    # use a wellplate instead of a tube rack so we can use the 8 channel pipette
    TUBE_RACK_TYPE = 'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap'
    TUBE_RACK_POSITION = '3'
    MASTER_MIX_WELL = 'A1'
    WATER_WELL = 'A2'
    MASTER_MIX_VOLUME = 20

    # Mix settings
    LINKER_MIX_SETTINGS = (1, 3)
    PART_MIX_SETTINGS = (4, 5)

    def clip(
            prefixes_wells,
            prefixes_plates,
            suffixes_wells,
            suffixes_plates,
            parts_wells,
            parts_plates,
            parts_vols,
            water_vols):

        ### Loading Tiprack
        # Calculates whether one, two, or three tipracks are needed, which are in slots 3, 6, and 9 respectively
        total_tips = 4 * len(parts_wells)
        letter_dict = {'A': 0, 'B': 1, 'C': 2,
                       'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        tiprack_1_tips = (
                                 13 - int(INITIAL_TIP[1:])) * 8 - letter_dict[INITIAL_TIP[0]]
        if total_tips > tiprack_1_tips:
            tiprack_num = 1 + (total_tips - tiprack_1_tips) // 96 + \
                          (1 if (total_tips - tiprack_1_tips) % 96 > 0 else 0)
        else:
            tiprack_num = 1
        slots = CANDIDATE_TIPRACK_SLOTS[:tiprack_num]

        # loads the correct number of tipracks
        tipracks = [protocol.load_labware(tiprack_type, slot) for slot in slots]
        # changed to protocol.load_labware for API 2.8

        # Loads pipette according to constants assigned above
        pipette_single = protocol.load_instrument(PIPETTE_TYPE_single, mount=PIPETTE_MOUNT_single, tip_racks=tipracks)

        # changed to protocol.load_labware for API 2.8
        # removed 'pipette.start_at_tip(tipracks[0].well(INITIAL_TIP))'
        # start_at_tip supported by API v1 up to API v2.7, but returns error for 2.8:
        # 'InstrumentContext' object has no attribute 'start_at_tip'
        # Because of this, ability to specify INITIAL_TIP was removed. Possible future improvement.

        # Defines where the destination wells are within the destination plate
        destination_wells = destination_plate.wells()[0:len(parts_wells)]

        # old code:
        # destination_wells = destination_plate.wells(INITIAL_DESTINATION_WELL, length=int(len(parts_wells)))
        # For API 2.8 and above, '.wells' will no longer take length arguments
        # Therefore the length arguement replaced by '[0:len(parts_wells)]'
        # Because of this, ability to specify INITIAL_DESTINATION_WELL was removed. Possible future improvement.

        ### Load Tube Rack
        # Loads tube rack according to constants assigned above
        tube_rack = protocol.load_labware(TUBE_RACK_TYPE, TUBE_RACK_POSITION)
        # changed to protocol.load_labware for API 2.8

        # Defines positions of master mix and water within the tube rack
        # master_mix = tube_rack.wells(MASTER_MIX_WELL)
        master_mix = tube_rack.wells_by_name()[MASTER_MIX_WELL]
        water = tube_rack.wells_by_name()[WATER_WELL]
        # water = [tube_rack.wells_by_name()[i] for i in WATER_WELLS]

        ### Loading Source Plates
        # Makes a source plate key for where prefixes, suffixes, and parts are located, according to the dictionary generated by the DNA-BOT
        source_plates = {}
        source_plates_keys = list(set((prefixes_plates + suffixes_plates + parts_plates)))

        # Loads plates according to the source plate key
        for key in source_plates_keys:
            source_plates[key] = protocol.load_labware(SOURCE_PLATE_TYPE, key)
            # changed to protocol.load_labware for API 2.8

        ### Transfers

        # transfer master mix into destination wells

        # added blowout into destination wells ('blowout_location' only works for API 2.8 and above)
        pipette_single.pick_up_tip()
        pipette_single.transfer(MASTER_MIX_VOLUME, master_mix, destination_wells, blow_out=True, blowout_location='destination well', new_tip='never')
        pipette_single.drop_tip()


        # transfer water into destination wells
        # added blowout into destination wells ('blowout_location' only works for API 2.8 and above)
        pipette_single.transfer(water_vols,
                           water,
                           destination_wells, blow_out=True, blowout_location='destination well',
                           new_tip='always')


        for clip_num in range(len(parts_wells)):
            pipette_single.transfer(1, source_plates[prefixes_plates[clip_num]].wells_by_name()[prefixes_wells[clip_num]],
                                    destination_wells[clip_num], blow_out=True, blowout_location='destination well', new_tip='always',
                                    mix_after=LINKER_MIX_SETTINGS)

            pipette_single.transfer(1, source_plates[suffixes_plates[clip_num]].wells_by_name()[suffixes_wells[clip_num]],
                                    destination_wells[clip_num], blow_out=True, blowout_location='destination well', new_tip='always',
                                    mix_after=LINKER_MIX_SETTINGS)

            pipette_single.transfer(parts_vols[clip_num], source_plates[parts_plates[clip_num]].wells_by_name()[parts_wells[clip_num]],
                                    destination_wells[clip_num], blow_out=True, blowout_location='destination well', new_tip='always',
                                    mix_after=PART_MIX_SETTINGS)


    # the run function will first define the CLIP function, and then run the CLIP function with the dictionary produced by DNA-BOT
    clip(**clips_dict)

    ### PCR Reaction in Thermocycler

    # close lid and set lid temperature, PCR will not start until lid reaches 37C
    tc_mod.close_lid()
    tc_mod.set_lid_temperature(105)

    # Runs 20 cycles of 37C for 2 minutes and 20C for 1 minute, then holds for 60C for 10 minutes
    profile = [
        {'temperature': 37, 'hold_time_minutes': 2},
        {'temperature': 20, 'hold_time_minutes': 1}]
    tc_mod.execute_profile(steps=profile, repetitions=20, block_max_volume=30)
    tc_mod.set_block_temperature(60, hold_time_minutes=10, block_max_volume=30)
    tc_mod.set_block_temperature(4, hold_time_minutes=2, block_max_volume=30)
    # Q Does block_max_volume define total volume in block or individual wells?
    tc_mod.set_lid_temperature(37)
    tc_mod.open_lid()
