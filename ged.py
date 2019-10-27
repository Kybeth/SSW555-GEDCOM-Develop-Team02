from datetime import datetime
# from dateutil.relativedelta import relativedelta
# from collections import defaultdict

def gedcom_parser(path):
    """Read the contains of file"""
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError("File not found : ", path)
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
    """Single Individual including tags of id, name, gender, birthday, age, alive, death, child, partner"""

    def __init__(self, id):
        self.id = id
        self.line_num = 0
        self.name = ''
        self.gender = ''
        self.birthday = ''
        self.age = ''
        self.alive = 'TRUE'
        self.death = 'NA'
        self.child = set()
        self.partner = set()

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

    def add_partner(self, id):
        self.partner.add(id)

    def pt_row(self):
        if len(self.child) == 0:
            self.child = "NA"
        if len(self.partner) == 0:
            self.partner = "NA"
        return [self.id, self.name, self.gender, self.birthday, self.age, self.alive, self.death, self.child,
                self.partner]


class Family:
    """Family class involving id, marriage, divorce, husband:{id, name} wife:{id, name}, children"""

    def __init__(self, id):
        self.id = id
        self.marriage = 'NA'
        self.divorced = 'NA'
        self.husband_id = set()
        self.husband_name = 'NA'
        self.wife_id = set()
        self.wife_name = 'NA'
        self.children = set()

    def add_marriage(self, marriage):
        self.marriage = marriage

    def add_divorce(self, divorced):
        self.divorced = divorced

    def add_husband_id(self, id):
        self.husband_id.add(id)

    def add_husband_name(self, name):
        self.husband_name = name

    def add_wife_id(self, id):
        self.wife_id.add(id)

    def add_wife_name(self, name):
        self.wife_name = name

    def add_children(self, id):
        self.children.add(id)

    def pt_row(self):
        if len(self.children) == 0:
            self.children = 'NA'
        return [self.id, self.marriage, self.divorced, self.husband_id, self.husband_name, self.wife_id,
                self.wife_name, self.children]
