from datetime import datetime
from prettytable import PrettyTable as pt

"""Define all the valid tags"""
valid = {
    '0':(['INDI','FAM'],'HEAD','TRLR','NOTE'),
    '1':('NAME','SEX','BIRT','DEAT','FAMC','FAMS','MARR','HUSB','WIFE','CHIL','DIV'),
    '2':('DATE'),
}


def calculate_age(birthday):
    """ Calculate the induviduals date and DOB """

    birthdate = datetime.strptime(birthday, '%d%b%Y')  #Year/ Month/ Date
    current = datetime.today()
    return current.year - birthdate.year - ((current.month, current.day) < (birthdate.month, birthdate.day))

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
                        indi[currentInd][currentDate] = arguments   

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
                        fam[currentFam][currentDate] =arguments
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
            birth = datetime.strptime(indi[key]['BIRT'],'%d%b%Y')  # print birth date
            birth_str = birth.strftime('%Y-%m-%d')
            
            """Condition for alive"""
            if 'DEAT' in indi[key]:
                death = datetime.strptime(indi[key]['DEAT'],'%d%b%Y')
                death_str = 'False'
            else:
                death_str ='True'

            """Condition for Death column"""  #Note that I am using same "deat" keyword for alive and dead
            if 'DEAT' in indi[key]:
                alive = datetime.strptime(indi[key]['DEAT'],'%d%b%Y')
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
                div = datetime.strptime(fam[key]['DIV'],'%d%b%Y')
                div_str = div.strftime('%Y-%m-%d')

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
                marr = datetime.strptime(fam[key]['MARR'],'%d%b%Y')
                marr_str = marr.strftime('%Y-%m-%d')
            else:
                marr_str = "NA"

            famTable.add_row([key, marr_str, div_str, hubID, hubName, wifeID, wifeName, chil])
        
        print(indiTable)
        print(famTable)

    return {'fam':fam, 'indi':indi}


define_your_file_here = parse_file('My-Family-9-Sep-2019-696.ged')
            
