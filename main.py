#Project           : GEDCOM SSW 555 
#Program name      : main.py
#Author            : Tanvi Hanamshet, Anirudh Bezzam, Yuan Zhang, Vignesh Mohan, Lifu Xiao
#Purpose           : User story Implementation of US11, US12, US13, US14, US15, US16, US17, US18, US19, US20

# US11:  No Bigamy
# US12:  Parents not too old
# US13:  Siblings spacing
# US14:  Multiple Births <= 5
# US15:  Fewer than 15 siblings
# US16:  Male last name
# US17:  No marriages to children
# US18:  Siblings should not marry
# US19:  First cousins should not marry
# US20:  Aunts and Uncles

from datetime import date, datetime, timedelta
from prettytable import PrettyTable as pt

def calculate_age(birthday):
    """ Calculate the induviduals date and DOB """

    current = datetime.today()
    return current.year - birthday.year - ((current.month, current.day) < (birthday.month, birthday.day))

class Gedcom(object):
    """Define all the valid tags"""
    valid = {
    '0':(['INDI','FAM'],'HEAD','TRLR','NOTE'),
    '1':('NAME','SEX','BIRT','DEAT','FAMC','FAMS','MARR','HUSB','WIFE','CHIL','DIV'),
    '2':('DATE'),
    }

    def __init__(self, path):
        self.path = path
        file = self.parse_file()
        self.fam = file['fam']
        self.indi = file['indi']


    def parse_file(self):
        """Reads the file from the path and stores all the information in a dictionary. Uses Pretty table to print out further information about the family.
        """
        try:
            gp = open(self.path, 'r', encoding='utf-8')
        except FileNotFoundError:
            raise FileNotFoundError('%s not exist' % (self.path))
        else:
            with gp:
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
                    elif len(family) > 1 and level in Gedcom.valid and tag in Gedcom.valid[level]:
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

        return {'fam':fam, 'indi':indi}

    def print_table(self):
        """Pretty Table info for induvidual"""

        indiTable = pt(["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"])
        
        for key in self.indi.keys():
            # print birth date
            birth_str = self.indi[key]['BIRT'].strftime('%Y-%m-%d')
            
            """Condition for alive"""
            if 'DEAT' in self.indi[key]:
                death = self.indi[key]['DEAT']
                death_str = 'False'
            else:
                death_str ='True'

            """Condition for Death column"""  #Note that I am using same "deat" keyword for alive and dead
            if 'DEAT' in self.indi[key]:
                alive = self.indi[key]['DEAT']
                alive_str = death.strftime('%Y-%m-%d')
            else:
                alive_str ='NA'

            """Condition for Children"""
            if 'FAMC' in self.indi[key]:
                child = self.indi[key]['FAMC']
            else:
                child = None
            
            """Spouse Situation LOL"""
            if 'FAMS' in self.indi[key]:
                spouse = self.indi[key]['FAMS']
            else:
                spouse = 'NA'

            age = calculate_age(self.indi[key]['BIRT'])
            indiTable.add_row([self.indi[key]['id'],self.indi[key]['name'],self.indi[key]['sex'], birth_str, age, death_str, alive_str, child, spouse])
        
        """Pretty table info for family relations"""

        famTable =pt(['ID','Married','Divorced','Husband ID','Husband Name','Wife ID','Wife name','Children'])
        for key in self.fam.keys():
            if 'DIV' in self.fam[key]:
                div_str = self.fam[key]['DIV'].strftime('%Y-%m-%d')

            else: 
                div_str = "NA"

            if "HUSB" in self.fam[key]:
                hubID = self.fam[key]['HUSB']
                hubName = self.indi[hubID]['name']
            else:
                hubID = "NA"
                hubName = "NA"

            if "WIFE" in self.fam[key]:
                wifeID = self.fam[key]['WIFE']
                wifeName = self.indi[wifeID]['name']
            else:
                wifeID = "NA"
                wifeName = "NA"

            if 'CHIL' in self.fam[key] :
                chil = self.fam[key]['CHIL']
            else:
                chil = "NA"

            if 'MARR' in self.fam[key]:
                marr_str = self.fam[key]['MARR'].strftime('%Y-%m-%d')
            else:
                marr_str = "NA"

            famTable.add_row([key, marr_str, div_str, hubID, hubName, wifeID, wifeName, chil])
        
        print(indiTable)
        print(famTable)
    
    
    
    def us15(self): #Fewer than 15 siblings - by Tanvi
        false = False
        for key in self.fam.keys():
            if 'CHIL' in self.fam[key] :
                chil = self.fam[key]['CHIL']
                if len(chil) < 15:
                    print(f"US15: Error: No more than fourteen children should be born in each family.'{len(chil)}' children born in family '{key}'")
                    false = True
        return false

            


    def us16(self): #Male last names - Tanvi
        for i in self.indi:
            if 'FAMC' in self.indi[i].keys():
                fam_id = ''.join(self.indi[i]['FAMC'])
                if self.indi[i]['sex'] == 'M':
                    first_name = self.indi[i]['name'].split('/')[0]
                    print(first_name)
                # if "HUSB" in self.fam[fam_id]:
                #     hubID = self.fam[fam_id]['HUSB']
                #     hubName = self.indi[hubID]['name']
                #     print(hubName)




def main():
    my_family = Gedcom('My-Family-7-Oct-2019-205.ged')
    my_family.print_table()

    
    my_family.us15()
    my_family.us16()

if __name__ == '__main__':
    main()
