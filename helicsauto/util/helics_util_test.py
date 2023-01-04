# Python program to read
# json file


if __name__ == "__main__":

    input_f_name = 'sim.py'
    output_f_name = 'federate.py'
    json_f_name = 'fed_config.json'

    input_f = open(input_f_name)
    output_f = open(output_f_name, 'w')
    cur_ind = 0 
    new_ind = 0 
    ind_inc = 4
    first_sub = False

    if not input_f:
        print(f'Fail to open {input_f_name}!')

    if not output_f:
        print(f'Fail to open {output_f_name}')
        

    for line in input_f:
        line2 = line.lstrip()
        cur_ind = len(line) - len(line2)

        if len(line2) == 0:
            new_line = ' \n'
            output_f.write(new_line)
            continue

        if new_ind < cur_ind:
            new_ind = cur_ind
        
        # [TODO] Maybe we only need to mark publish/subscription 

        if '## HELICSAUTO: Register' in line2:
            print(f'## HELICSAUTO: Register')
            new_line = new_ind * ' ' + line2
            output_f.write(new_line)
            output_f.write(new_ind * ' ' + 'import helics as h\n')
            output_f.write(new_ind * ' ' + f'fed = h.helicsCreateValueFederateFromConfig(\'{json_f_name}\')\n')

        elif '## HELICSAUTO: Execute' in line2:
            print(f'## HELICSAUTO: Execute')
            new_line = new_ind * ' ' + line2
            output_f.write(new_line)
            output_f.write(new_ind * ' ' + 'h.helicsFederateEnterExecutingMode(fed)' + '\n')

            output_f.write(new_ind * ' ' + 'hours = 1' + '\n')
            output_f.write(new_ind * ' ' + 'total_interval = int(60 * 60 * hours)' + '\n')
            output_f.write(new_ind * ' ' + 'update_interval = int(h.helicsFederateGetTimeProperty(fed, h.HELICS_PROPERTY_TIME_PERIOD))' + '\n')
            output_f.write(new_ind * ' ' + 'grantedtime = 0' + '\n')

            # [TODO] what is the original python scripts already has a while loop
            output_f.write(new_ind * ' ' + 'while grantedtime < total_interval:' + '\n')
            new_ind = new_ind + ind_inc

        elif '## HELICSAUTO: Publish' in line2:
            print(f'## HELICSAUTO: Publish')
            new_line = new_ind * ' ' + line2
            output_f.write(new_line)
            # parse the comments to obtain the variable name
            pub_info = line2.split(', ')
            var_name = pub_info[1]
            var_type = pub_info[2]
            pub_name = pub_info[3].replace("\n", "")
            #print(new_ind * ' ' + 'hello'  + ')' +'\n')
            output_f.write(new_ind * ' ' + f'pubid = h.helicsFederateGetPublication(fed, \'{pub_name}\')\n')
            #output_f.write(new_ind * ' ' + 'pubid = h.helicsFederateGetPublication(fed, ' + 'IEEE_123_feeder_0/totalLoad' + 'hello hello hello' + '\n')
            if var_type == 'complex':
                output_f.write(new_ind * ' ' + f'status = h.helicsPublicationPublishComplex(pubid, {var_name}.real, {var_name}.imag)' + '\n')

        elif '## HELICSAUTO: Subscribe' in line2:
            
            if first_sub == False: # this is the first subscription
                first_sub = True
                output_f.write(new_ind * ' ' + 'requested_time = grantedtime + update_interval' + '\n')
                output_f.write(new_ind * ' ' + 'grantedtime = h.helicsFederateRequestTime(fed, requested_time)' + '\n')

            print(f'## HELICSAUTO: Subscribe')
            new_line = new_ind * ' ' + line2
            output_f.write(new_line)
            sub_info = line2.split(', ')
            var_name = sub_info[1]
            var_type = sub_info[2]
            sub_name = sub_info[3].replace("\n", "")
            output_f.write(new_ind * ' ' + f'subid = h.helicsFederateGetSubscription(fed, \'{sub_name}\')' + '\n')
            if var_type == 'complex':
                output_f.write(new_ind * ' ' + f'{var_name} = h.helicsInputGetComplex((subid))' + '\n')

        elif '## HELICSAUTO: Destroy' in line2:
            print(f'## HELICSAUTO: Destroy')
            new_ind = new_ind - ind_inc
            new_line = new_ind * ' ' + line2
            output_f.write(new_line)
            output_f.write(new_ind * ' ' + 'grantedtime = h.helicsFederateRequestTime(fed, h.HELICS_TIME_MAXTIME)' + '\n')
            output_f.write(new_ind * ' ' + 'status = h.helicsFederateDisconnect(fed)' + '\n')
            output_f.write(new_ind * ' ' + 'h.helicsFederateFree(fed)' + '\n')
            output_f.write(new_ind * ' ' + 'h.helicsCloseLibrary()' + '\n')
            
        else:
            print(f'Other codes {len(line)} {len(line2)}')
            new_line = new_ind * ' ' + line2
            output_f.write(new_line)
    
    input_f.close()
    output_f.close()
