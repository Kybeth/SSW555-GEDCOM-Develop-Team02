from datetime import datetime, timedelta
from prettytable import PrettyTable as pt

"""Define all the valid tags"""
valid = {
    '0':(['INDI','FAM'],'HEAD','TRLR','NOTE'),
    '1':('NAME','SEX','BIRT','DEAT','FAMC','FAMS','MARR','HUSB','WIFE','CHIL','DIV'),
    '2':('DATE'),
}


def calculate_age(birthday):
    """ Calculate the induviduals date and DOB """

    current = datetime.today()
    return current.year - birthday.year - ((current.month, current.day) < (birthday.month, birthday.day))

def parse_file(path,encode = 'utf-8'):
    """Reads the file from the path and stores all the information in a dictionary. Uses Pretty table to print out further information about the family.
    """

    with open(path,'r',encoding=encode) as gp:  #remember that gp is the file
        isValid = 'N'
        IsIND = True
        indi = {}
        fam = {}
        currentDate = ''                        
        currentInd = ''
        currentFam = ''
        
        for line in gp:    
            family = line.strip().split()
            arguments = ''.join(family[2:])
            tag = 'NA'
            level = 'NA'

            if len(family) == 1:
                level = family[0]
            elif len(family) > 1:
                level = family[0]
                tag = family[1]

            if len(family) == 3 and family[0] == '0' and family[2] in ('INDI', 'FAM'):
                isValid = 'Y'
                tag = family[2]
            elif len(family) > 1 and level in valid and tag in valid[level]:
                isValid = 'Y'
            
            if isValid == 'Y':
                if level== '0' and tag == 'INDI':
                    currentInd = family[1]
                    IsIND = True

                    ''' Implement the unique key identifier'''
                    
                    indi[currentInd] = {'id':family[1]}

                if IsIND:
                    if level == '1' and tag == 'NAME':
                        indi[currentInd]['name'] = arguments
                    if level == '1' and tag == 'BIRT' or tag == 'DEAT':
                        currentDate = tag 
                    if level == '2' and currentDate != '' and tag == 'DATE':
                        indi[currentInd][currentDate] = datetime.strptime(arguments,'%d%b%Y')   

                    if level == '1' and tag == 'SEX':
                        indi[currentInd]['sex'] = arguments   
                    if level == '1' and tag in ('FAMC','FAMS'):
                        if tag in indi[currentInd]:
                            indi[currentInd][tag].add(arguments)
                        else:
                            indi[currentInd][tag] = {arguments}  
   
                if level=='0' and tag == 'FAM':
                    IsIND = False
                    currentFam = family[1]
                    fam[currentFam] = {'fam':currentFam}
                    
                if IsIND == False:
                    if level == '1' and family[1] == 'MARR' or family[1] == 'DIV':
                        currentDate = tag
                    if level == '2' and tag == 'DATE':
                        fam[currentFam][currentDate] =datetime.strptime(arguments,'%d%b%Y')
                    if level == '1' and tag in ('HUSB','WIFE'):
                        fam[currentFam][tag] = arguments
                    if level == '1' and tag == 'CHIL':
                        if tag in fam[currentFam]:
                            fam[currentFam][tag].add(arguments)
                        else:
                            fam[currentFam][tag] = {arguments}

        """Pretty Table info for induvidual"""

        indiTable = pt(["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"])
        
        for key in indi.keys():
            # print birth date
            birth_str = indi[key]['BIRT'].strftime('%Y-%m-%d')
            
            """Condition for alive"""
            if 'DEAT' in indi[key]:
                death = indi[key]['DEAT']
                death_str = 'False'
            else:
                death_str ='True'

            """Condition for Death column"""  #Note that I am using same "deat" keyword for alive and dead
            if 'DEAT' in indi[key]:
                alive = indi[key]['DEAT']
                alive_str = death.strftime('%Y-%m-%d')
            else:
                alive_str ='NA'

            """Condition for Children"""
            if 'FAMC' in indi[key]:
                child = indi[key]['FAMC']
            else:
                child = None
            
            """Spouse Situation LOL"""
            if 'FAMS' in indi[key]:
                spouse = indi[key]['FAMS']
            else:
                spouse = 'NA'

            age = calculate_age(indi[key]['BIRT'])
            indiTable.add_row([indi[key]['id'],indi[key]['name'],indi[key]['sex'], birth_str, age, death_str, alive_str, child, spouse])
        
        """Pretty table info for family relations"""

        famTable =pt(['ID','Married','Divorced','Husband ID','Husband Name','Wife ID','Wife name','Children'])
        for key in fam.keys():
            if 'DIV' in fam[key]:
                div_str = fam[key]['DIV'].strftime('%Y-%m-%d')

            else: 
                div_str = "NA"

            if "HUSB" in fam[key]:
                hubID = fam[key]['HUSB']
                hubName = indi[hubID]['name']
            else:
                hubID = "NA"
                hubName = "NA"

            if "WIFE" in fam[key]:
                wifeID = fam[key]['WIFE']
                wifeName = indi[wifeID]['name']
            else:
                wifeID = "NA"
                wifeName = "NA"

            if 'CHIL' in fam[key] :
                chil = fam[key]['CHIL']
            else:
                chil = "NA"

            if 'MARR' in fam[key]:
                marr_str = fam[key]['MARR'].strftime('%Y-%m-%d')
            else:
                marr_str = "NA"

            famTable.add_row([key, marr_str, div_str, hubID, hubName, wifeID, wifeName, chil])
        
        print(indiTable)
        print(famTable)

        # US02 Birth before marriage of individual - By Vignesh Mohan
        for i in indi:
            if "FAMC" in indi[i].keys():
                child_birth = indi[i]['BIRT']
                fam_id = ''.join(indi[i]['FAMC'])
                if 'MARR' in fam[fam_id].keys():
                    marry_date = fam[fam_id]['MARR']
                    if child_birth < marry_date:
                        print('ANOMALY: FAMILY: US02: ' + fam[fam_id]['fam'] + ' Child ' + indi[i]['id'] + ' born ' + child_birth.strftime('%Y-%m-%d') + ' before marriage on ' + marry_date.strftime('%Y-%m-%d'))
                
        
        #US05 Marriage before death - By Tanvi
        '''
        for i in indi:
            if "FAMC" in indi[i].keys():
                marry_date = indi[i]['MARR']
                fam_id = ''.join(indi[i]['FAMC'])
                if 'DEAT' in fam[fam_id].keys():
                    death_dt = fam[fam_id]['DEAT']
                    if  death_dt > marry_date:
                        print('US05: ' + fam[fam_id]['fam'] + ' Person ' + indi[i]['id'] + ' Marriage ' + marry_date.strftime('%Y-%m-%d') + ' before death on ' + death_dt.strftime('%Y-%m-%d'))
        

        #US06 Divorce before death - By Tanvi
        for i in indi:
            if "FAMC" in indi[i].keys():
                divorce_dt = indi[i]['DIV']
                fam_id = ''.join(indi[i]['FAMC'])
                if 'DEAT' in fam[fam_id].keys():
                    death_dt = fam[fam_id]['DEAT']
                    if death_dt > divorce_dt:
                        print('US06: ' + fam[fam_id]['fam'] + ' Person ' + indi[i]['id'] + ' Divorce ' + divorce_dt.strftime('%Y-%m-%d') + ' before death on ' + death_dt.strftime('%Y-%m-%d'))
        '''

        # US07 Less then 150 years old - By Lifu
        for i in indi:
            if 'DEAT' in indi[i].keys():
                if indi[i]['DEAT'] - indi[i]['BIRT'] > timedelta(days = 54750):
                    print('ERROR: INDIVIDUAL: US07: ' + indi[i]['id'] + ' More than 150 years old at death - Birth ' + indi[i]['BIRT'].strftime('%Y-%m-%d') + ' Death ' + indi[i]['DEAT'].strftime('%Y-%m-%d'))
            else:
                if datetime.today() - indi[i]['BIRT'] > timedelta(days = 54750):
                    print('ERROR: INDIVIDUAL: US07: ' + indi[i]['id'] + ' More than 150 years old - Birth '  + indi[i]['BIRT'].strftime('%Y-%m-%d'))
        
        # US08 Birth before marriage of parents - By Lifu
        for i in indi:
            if "FAMC" in indi[i].keys():
                child_birt = indi[i]['BIRT']
                fam_id = ''.join(indi[i]['FAMC'])
                if 'MARR' in fam[fam_id].keys():
                    marry_date = fam[fam_id]['MARR']
                    if marry_date > child_birt:
                        print('ANOMALY: FAMILY: US08: ' + fam[fam_id]['fam'] + ' Child ' + indi[i]['id'] + ' born ' + child_birt.strftime('%Y-%m-%d') + ' before marriage on ' + marry_date.strftime('%Y-%m-%d'))
                if 'DIV' in fam[fam_id].keys():
                    div_date = fam[fam_id]['DIV']
                    if div_date < child_birt:
                        print('ANOMALY: FAMILY: US08: ' + fam[fam_id]['fam'] + ' Child ' + indi[i]['id'] + ' born ' + child_birt.strftime('%Y-%m-%d') + ' after divorce on ' + div_date.strftime('%Y-%m-%d'))

        # US09 Birth before death of parents - by Yuan
        for i in indi:
            if 'FAMC' in indi[i].keys():
                child_birt = indi[i]['BIRT']
                fam_id = ''.join(indi[i]['FAMC'])
                mom_id = fam[fam_id]['WIFE']
                dad_id = fam[fam_id]['HUSB']
                if 'DEAT' in indi[mom_id].keys():
                    mom_deat = indi[mom_id]['DEAT']
                    if child_birt > mom_deat:
                        print('ERROR: FAMILY: US09: ' + fam_id + ' Child ' + indi[i]['id'] + ' born ' + indi[i]['BIRT'].strftime('%Y-%m-%d') + " after mother's death on " + mom_deat.strftime('%Y-%m-%d'))
                if 'DEAT' in indi[dad_id].keys():
                    dad_deat = indi[dad_id]['DEAT']
                    if dad_deat - child_birt < timedelta(days = 270):
                        print('ERROR: FAMILY: US09: ' + fam_id + ' Child ' + indi[i]['id'] + ' born ' + indi[i]['BIRT'].strftime('%Y-%m-%d') + " after nine months after father's death on " + dad_deat.strftime('%Y-%m-%d'))
        
        # US10 Marriage after 14 - by Yuan
        for i in fam:
            if 'MARR'in fam[i].keys():
                marry_date = fam[i]['MARR']
                fam_id = i
                husb_id = fam[i]['HUSB']
                wife_id = fam[i]['WIFE']
                husb_birt = indi[husb_id]['BIRT']
                wife_birt = indi[wife_id]['BIRT']
                if marry_date - husb_birt < timedelta(days = 5110): # 365days/yr * 14yr = 5110
                    print('ERROR: FAMILY: US10: ' + fam_id + ' Husband ' + indi[husb_id]['id'] + ' married on ' + marry_date.strftime('%Y-%m-%d') + ' before 14 years old (born on ' + husb_birt.strftime('%Y-%m-%d') + ')')
                if marry_date - wife_birt < timedelta(days = 5110): # 365days/yr * 14yr = 5110:
                    print('ERROR: FAMILY: US10: ' + fam_id + ' Wife ' + indi[wife_id]['id'] + ' married on ' + marry_date.strftime('%Y-%m-%d') + ' before 14 years old (born on ' + wife_birt.strftime('%Y-%m-%d') + ')')


        

    return {'fam':fam, 'indi':indi}


define_your_file_here = parse_file('My-Family-1-Oct-2019-278.ged'
            
