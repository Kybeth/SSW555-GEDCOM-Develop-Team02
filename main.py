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


