from ged import Individual, Family, gedcom_parser
from prettytable import PrettyTable
from datetime import datetime

class Repo:
    def __init__(self):
        """All information about Individual and Family"""
        self.individual = dict()
        self.family = dict()

    def add_individual(self, level, argument, tag):
        self.individual[argument] = Individual(argument)

    def add_family(self, level, argument, tag):
        self.family[argument] = Family(argument)

    def individual_table(self):
        pt = PrettyTable(
            field_names=['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'partner'])
        for key in sorted(self.individual.keys()):
            pt.add_row(self.individual[key].pt_row())
        print(pt)

    def family_table(self):
        pt = PrettyTable(
            field_names=['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])
        for key in sorted(self.family.keys()):
            pt.add_row(self.family[key].pt_row())
        print(pt)

    def read_file(self, path):
        for level, tag, argument in gedcom_parser(path):
            # print(level, tag, argument)
            result = list()
            valid_tags = {'NAME': '1', 'SEX': '1', 'MARR': '1',
                          'BIRT': '1', 'DEAT': '1', 'FAMC': '1', 'FAMS': '1',
                          'HUSB': '1', 'WIFE': '1', 'CHIL': '1',
                          'DIV': '1', 'DATE': '2', 'HEAD': '0', 'TRLR': '0', 'NOTE': '0'}
            special_valid_tags = {'INDI': '0', 'FAM': '0'}

            valid_tag_level = False
            if argument in ['INDI', 'FAM']:
                special_tags = True
                for current_tag, current_level in special_valid_tags.items():
                    if level == current_level and argument == current_tag:
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
                result.append(argument)
                result.append("Y")
                result.append(tag)
                if argument in ["INDI"]:
                    self.add_individual(level, tag, argument)
                    current_id = tag
                else:
                    self.add_family(level, tag, argument)
                    current_id = tag
            elif not valid_tag_level and not special_tags:
                result.append(level)
                result.append(tag)
                result.append("N")
                result.append(argument)
            elif valid_tag_level and not special_tags:
                result.append(level)
                result.append(tag)
                result.append("Y")
                result.append(argument)
                if tag == "NAME":
                    self.individual[current_id].add_name(argument)
                elif tag == "SEX":
                    self.individual[current_id].add_gender(argument)
                elif tag == "FAMC":
                    self.individual[current_id].add_child(argument)
                elif tag == "FAMS":
                    self.individual[current_id].add_partner(argument)
                elif tag in "HUSB":
                    self.family[current_id].add_husband_id(argument)
                    self.family[current_id].add_husband_name(self.individual[argument].name)
                elif tag in "WIFE":
                    self.family[current_id].add_wife_id(argument)
                    self.family[current_id].add_wife_name(self.individual[argument].name)
                elif tag in "CHIL":
                    self.family[current_id].add_children(argument)
                elif tag in ["BIRT", "DEAT", "DIV", "MARR"]:
                    check_date_tag = True
                    previous_tag = tag
                elif tag == "DATE" and check_date_tag is True:
                    argument = datetime.strptime(argument, '%d %b %Y').strftime('%Y-%m-%d')
                    if previous_tag == "BIRT":
                        self.individual[current_id].add_birthday(argument)
                        self.individual[current_id].add_age('Birth', argument)
                    elif previous_tag == "DEAT":
                        self.individual[current_id].add_death(argument)
                        self.individual[current_id].add_alive("False")
                        self.individual[current_id].add_age('Death', argument)
                    elif previous_tag == "MARR":
                        self.family[current_id].add_marriage(argument)
                    elif previous_tag == "DIV":
                        self.family[current_id].add_divorce(argument)

            else:
                result.append(level)
                result.append(argument)
                result.append("N")
                result.append(tag)

    """Vignesh Mohan"""

    """US01 Dates before current date"""
    def US01(self):
        #getting todays date 
        today = datetime.today().strftime('%Y-%m-%d')

        result = False
        for key, individual in self.individual.items():
            for key, family in self.family.items():
                if individual.birthday > today:
                    print("Error US01:-Birthdate ", individual.birthday ,"is after current date")
                    result = True
                if individual.death > today:
                    print("Error US01:- Deathdate ", individual.death ,"is after current date")
                    result = True
                if family.marriage > today:
                    print("Error US01:- MarriageDate ", family.marriage ,"is after current date")
                    result = True
                if family.divorced > today:
                    print("Error US01:- DivorceDate ", family.divorced,"is after current date")
                    result = True
        return result

    """US02 Birth before Marriage"""
    def US02(self):
        result = False
        for key, individual in self.individual.items():  #Implementing as a dictionary.
            for key, family in self.family.items():
                if individual.birthday != 'NA' or family.marriage != 'NA':
                    if family.marriage > individual.birthday :
                        print(
                            "ANOMALY: FAMILY: US02: " + key + " Birth " + individual.birthday + " should not occur before marriage  " + family.marriage)
                        result = True
        return result

    """Anirudh Bezzam"""

    """US03 Birth before Death of Individual"""
    def US03(self):
        result = False
        for key, individual in self.individual.items():  #dict implementation
            if individual.birthday != 'NA' or individual.death != 'NA':
                if individual.birthday > individual.death:
                    print(
                        "Error: Individual: US03: " + key + " Birth " + individual.birthday + "should occur before death " + individual.death)
                    result = True
        return result

    """US04	Marriage before divorce"""
    def US04(self):
        result = False
        for key, family in self.family.items():
            if family.marriage < family.divorced:
                print(
                    "Error: FAMILY : US04 : " + key + " Marriage " + family.marriage + " should occur before divorce " + family.divorced)
                result = True
        return result

    """US13 - Birth Dates of Sibilings should be more than 8 months apart or less than 2 days apart"""
    def US13(self):
        result = False
        sibday = []
        sibmonth = []
        for key, family in self.family.items():
            children_list = list(family.children)
            if self.individual[list(family.children)[0]].id in family.children:
                for each_sibiling in children_list:
                    sib_birthday_month = datetime.today().strptime(self.individual[each_sibiling].birthday,
                                                                   '%Y-%m-%d').month
                    sib_birthday_day = datetime.today().strptime(self.individual[each_sibiling].birthday,
                                                                 '%Y-%m-%d').day
                    sibday.append(sib_birthday_day)
                    sibmonth.append(sib_birthday_month)
                    for each_month_element in range(len(sibmonth) - 1):
                        month_diff = sibmonth[each_month_element + 1] - sibmonth[each_month_element]
                        if month_diff > 8:
                            result = True
                        else:
                            print(
                                "Error: FAMILY : US13: Family sibiling spacing should be more than 8 months apart or less than 2 days apart",
                                key)

                    for each_day_element in range(len(sibday) - 1):
                        day_diff = sibday[each_day_element + 1] - sibday[each_day_element]
                        if day_diff < 2:
                            result = True
                        else:
                            print(
                                "Error: FAMILY : US13: Family sibiling spacing should be more than 8 months apart or less than 2 days apart",
                                key)
        return result

    """US14 - Multiple births <= 5"""
    def US14(self):
        result = False
        for key, family in self.family.items():
            birthday_list = list()
            list_of_children = family.children
            for child in list_of_children:
                birthday_list.append(self.individual[child].birthday)
            count_dict = dict((i, birthday_list.count(i)) for i in birthday_list)
            list_birthdays = count_dict.values()
            if max(list_birthdays) <= 5:
                result = True
            else:
                print(
                    "Error: FAMILY : US14: " + key + "Number of children born in a single birth should not be greater than 5")
        return result

    """Tanvi Hanamshet"""
    """unique first name in families"""
    def US25(self):
        
        
        # for key, family in self.family.items():
        #     print(family.husband_name[key])
        # for key, family in self.family.items():
        for key, individual in self.individual.items():
            unique_names = []
            names = []
            list_of_names = individual.name.split("/")[0]
            names.append(list_of_names)
            for i in names:
                if i not in unique_names:
                    unique_names.append(i)
            for name in unique_names:
                print("ANOMALY: FAMILY : US25: " + key + " Unique name in family: "+ name)
            # unique_names = []
            # names = []
            # list_of_names = family.husband_name.split("/")[0]
            # list_of_names2 = family.wife_name.split("/")[0]
            # # list_of_names = family.children.split("/")[0]
            # names.append(list_of_names)
            # names.append(list_of_names2)
            # for i in names:
            #     if i not in unique_names:
            #         unique_names.append(i)
            #         print(key, i)
            # del names[:]
            # del unique_names
                     
        

            # print(key,family.husband_name)

    # def US26(self): #corresponding enteries

    """Lifu Xiao"""
    def US07(self): #  US07 Less then 150 years old
        result = list()
        for key, individual in self.individual.items():
            if(individual.age > 150):
                print("ERROR: INDIVIDUAL: US07: " + key + "  More than 150 years old: Birth date "+ individual.birthday)
                result.append(key)
        return result

    def US08(self): #  US08 Birth before marriage of parents
        result = list()
        for key, individual in self.individual.items():
            if(individual.child != 'NA'):
                for c in individual.child:
                    fam = self.family[c]
                    if(fam.divorced != 'NA'):
                        div_date = datetime.strptime(fam.divorced, '%Y-%m-%d')
                        child_birth_date = datetime.strptime(individual.birthday, '%Y-%m-%d')
                        if(child_birth_date > div_date):
                            print('ANOMALY: FAMILY: US08: ' + c + ' Child ' + key + ' born ' + individual.birthday + ' after divorce on ' + fam.divorced)
                            result.append(key)
                    if(fam.marriage != 'NA'):
                        marr_date = datetime.strptime(fam.marriage, '%Y-%m-%d')
                        child_birth_date = datetime.strptime(individual.birthday, '%Y-%m-%d')
                        if(marr_date > child_birth_date):
                            print('ANOMALY: FAMILY: US08: ' + c + ' Child ' + key + ' born ' + individual.birthday + ' before marriage on ' + fam.marriage)
                            result.append(key)
        return result
    
    def US17(self): #  US17: No marriages to children
        result = list()
        for key, individual in self.individual.items():
            if(individual.partner != 'NA'):
                for p in individual.partner:
                    fam = self.family[p]
                    if(fam.children != 'NA'):
                        if (fam.children & set(fam.wife_id) != set() or fam.children & set(fam.husband_id) != set()):
                            print('ERROR: FAMILY: US17: Parent ' + key + ' marries with children or parents.')
                            result.append(key)
        return result

    """Yuan Zhang"""

def main():
    repo1 = Repo()
    repo1.read_file('ged/myfamily.ged')
    print("\n Individual Summary")
    repo1.individual_table()

    print("\n Family Summary")
    repo1.family_table()
    repo1.US07()
    repo1.US08()
    repo1.US17()

    repo2 = Repo()
    repo2.read_file('ged/das.ged')
    repo2.US03()
    repo2.US04()
    repo2.US13()
    repo2.US14()

    repo3 = Repo()
    repo3.read_file('ged/us17.ged')
    repo3.US17()


    
if __name__ == '__main__':
    main()