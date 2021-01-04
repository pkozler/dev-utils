
def write_temp_file(temp_file, fk_field, fk_pk_field, fk_broken_list):

    try:
        with open(temp_file, 'w+') as fw:
            fw.write(f'{fk_field.table}.{fk_pk_field}:{fk_field.table}.{fk_field}\n')

            for fk in fk_broken_list:
                fw.write(f'{fk[0]}:{fk[1]}\n')

        print(f'Temporary file writing completed.')
    except Exception as e:
        print(f'Temporary file writing failed!\n{str(e)}')
        exit(1)
