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

from prettytable import PrettyTable
from datetime import datetime
from dateutil.relativedelta import relativedelta


def file_reader(path):
    """Read the contains of file"""
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError("File not found : ", path)
    except IOError:
        raise IOError("Error opening file : ", path)
    else:
        with fp:
            for line_num, line in enumerate(fp):
                fields = line.strip().split()
                if len(fields) >= 3:
                    fields = line.strip().split(" ", 2)
                elif len(fields) < 1:
                    raise ValueError("Excepted number of fields is not present in row.")
                else:
                    fields = line.strip().split()
                    fields.append("")
                yield fields


class Individual:
    """Single Individual"""
    def __init__(self, id):
        self.id = id
        self.name = ''
        self.gender = ''
        self.birthday = ''
        self.age = ''
        self.alive = 'TRUE'
        self.death = 'NA'
        self.child = set()
        self.spouse = set()

    def add_name(self, name):
        self.name = name

    def add_gender(self, gender):
        self.gender = gender

    def add_birthday(self, birthday):
        self.birthday = birthday

    def add_age(self, flag, current_tagdate):
        if flag == 'Death':
            birthday = datetime.strptime(self.birthday, '%Y-%m-%d')
            end_date = datetime.strptime(current_tagdate, '%Y-%m-%d')
        else:
            birthday = datetime.strptime(self.birthday, '%Y-%m-%d')
            end_date = datetime.today()
        age = end_date.year - birthday.year - ((end_date.month, end_date.day) < (birthday.month, birthday.day))
        self.age = age

    def add_death(self, death):
        self.death = death

    def add_alive(self, alive):
        self.alive = alive

    def add_child(self, id):
        self.child.add(id)

    def add_spouse(self, id):
        self.spouse.add(id)

    def pt_row(self):
        if len(self.child) == 0:
            self.child = "NA"
        if len(self.spouse) == 0:
            self.spouse = "NA"
        return [self.id, self.name, self.gender, self.birthday, self.age, self.alive, self.death, self.child, self.spouse]


class Family:
    """Single Family"""
    def __init__(self, id):
        self.id = id
        self.marriage = 'NA'
        self.divorced = 'NA'
        self.hubby_id = set()
        self.hubby_name = 'NA'
        self.wife_id = set()
        self.wife_name = 'NA'
        self.children = set()

    def add_marriage(self, marriage):
        self.marriage = marriage

    def add_divorce(self, divorced):
        self.divorced = divorced

    def add_hubby_id(self, id):
        self.hubby_id.add(id)

    def add_hubby_name(self, name):
        self.hubby_name = name

    def add_wife_id(self, id):
        self.wife_id.add(id)

    def add_wife_name(self, name):
        self.wife_name = name

    def add_children(self, id):
        self.children.add(id)

    def pt_row(self):
        if len(self.children) == 0:
            self.children = 'NA'
        return [self.id, self.marriage, self.divorced, self.hubby_id, self.hubby_name, self.wife_id,
                self.wife_name, self.children]

class Repo:

    def __init__(self):
        """All information about Individual and Family"""
        self.individual = dict()
        self.family = dict()

    def add_individual(self, level, args, tag):
        self.individual[args] = Individual(args)

    def add_family(self, level, args, tag):
        self.family[args] = Family(args)

    def indi_table(self):
        pt = PrettyTable(
            Columns=['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse'])
        for key in sorted(self.individual.keys()):
            pt.add_row(self.individual[key].pt_row())
        print(pt)

    def family_table(self):
        pt = PrettyTable(
            Columns=['ID', 'Married', 'Divorced', 'hubby ID', 'hubby Name', 'Wife ID', 'Wife Name', 'Children'])
        for key in sorted(self.family.keys()):
            pt.add_row(self.family[key].pt_row())
        print(pt)

    def read_file(self, path):
        for level, tag, args in file_reader(path):
            result = list()
            valid_tags = {'NAME': '1', 'SEX': '1', 'MARR': '1',
                          'BIRT': '1', 'DEAT': '1', 'FAMC': '1', 'FAMS': '1',
                          'HUSB': '1', 'WIFE': '1', 'CHIL': '1',
                          'DIV': '1', 'DATE': '2', 'HEAD': '0', 'TRLR': '0', 'NOTE': '0'}
            special_valid_tags = {'INDI': '0', 'FAM': '0'}

            valid_tag_level = False
            if args in ['INDI', 'FAM']:
                special_tags = True
                for current_tag, current_level in special_valid_tags.items():
                    if level == current_level and args == current_tag:
                        valid_tag_level = True
                        break
            else:
                special_tags = False
                for current_tag, current_level in valid_tags.items():
                    if level == current_level and tag == current_tag:
                        valid_tag_level = True
                        break

            if valid_tag_level and special_tags:
                result.append(level)
                result.append(args)
                result.append("Y")
                result.append(tag)
                if args in ["INDI"]:
                    self.add_individual(level, tag, args)
                    current_id = tag
                else:
                    self.add_family(level, tag, args)
                    current_id = tag
            elif not valid_tag_level and not special_tags:
                result.append(level)
                result.append(tag)
                result.append("N")
                result.append(args)
            elif valid_tag_level and not special_tags:
                result.append(level)
                result.append(tag)
                result.append("Y")
                result.append(args)
                if tag == "NAME":
                    self.individual[current_id].add_name(args)
                elif tag == "SEX":
                    self.individual[current_id].add_gender(args)
                elif tag == "FAMC":
                    self.individual[current_id].add_child(args)
                elif tag == "FAMS":
                    self.individual[current_id].add_spouse(args)
                elif tag in "HUSB":
                    self.family[current_id].add_hubby_id(args)
                    self.family[current_id].add_hubby_name(self.individual[args].name)
                elif tag in "WIFE":
                    self.family[current_id].add_wife_id(args)
                    self.family[current_id].add_wife_name(self.individual[args].name)
                elif tag in "CHIL":
                    self.family[current_id].add_children(args)
                elif tag in ["BIRT", "DEAT", "DIV", "MARR"]:
                    check_date_tag = True
                    previous_tag = tag
                elif tag == "DATE" and check_date_tag is True:
                    args = datetime.strptime(args, '%d %b %Y').strftime('%Y-%m-%d')
                    if previous_tag == "BIRT":
                        self.individual[current_id].add_birthday(args)
                        self.individual[current_id].add_age('Birth', args)
                    elif previous_tag == "DEAT":
                        self.individual[current_id].add_death(args)
                        self.individual[current_id].add_alive("False")
                        self.individual[current_id].add_age('Death', args)
                    elif previous_tag == "MARR":
                        self.family[current_id].add_marriage(args)
                    elif previous_tag == "DIV":
                        self.family[current_id].add_divorce(args)

            else:
                result.append(level)
                result.append(args)
                result.append("N")
                result.append(tag)
    
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
    path = 'My-Family-7-Oct-2019-205.ged'
    repo = Repo()
    repo.read_file(path)

    print("\n Individual PrettyTable")
    repo.indi_table()

    print("\n Family PrettyTable")
    repo.family_table()
    
    # Test calling
    my_family.us15()
    my_family.us16()


if __name__ == '__main__':
    main()

