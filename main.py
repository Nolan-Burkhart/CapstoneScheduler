from settings import *

def sort_students(array):
  if len(array) > 1:
    midpoint = len(array)//2
    left = array[:midpoint]
    right = array[midpoint:]

    sort_students(left)
    sort_students(right)

    left_index = 0
    right_index = 0
    array_index = 0

    while left_index < len(left) and right_index < len(right):
      if (left[left_index].grade > right[right_index].grade):
        array[array_index] = left[left_index]
        left_index += 1
      else:
        array[array_index] = right[right_index]
        right_index += 1
      array_index += 1
    
    while left_index < len(left):
      array[array_index] = left[left_index]
      left_index += 1
      array_index += 1
    
    while right_index < len(right):
      array[array_index] = right[right_index]
      right_index += 1
      array_index += 1


class student:
  assigned = False
  assignment = 0
  prefrences = []
  name = ""
  advisory = ""
  email = ""
  grade = 9
  def __init__(self, name, email, prefrences_raw, advisory):
    self.assigned = False
    self.advisory = advisory
    self.assignment = 0
    self.name = name
    self.email = email
    try:
      self.grade = 32-(int)(self.email[email.find("@")-2:email.find("@")])
    except ValueError:
      self.grade=12
    self.prefrences = []
    for p in prefrences_raw:
      for i in range(0,20):
        if i == 14:
          print(p)
        o = l.get_setting("Option"+str(i))
        if(o == p):
          self.prefrences.append(i)
          break

class room:
  size_limit = 0
  size = 0
  name = ""
  capstones = []
  def __init__(self, name, size_limit):
    self.name = name
    self.size = 0
    self.size_limit = int(size_limit)
    self.capstones = []

class capstone:
  name = ""
  id = 0
  size_limit = 0
  students = []
  room = 0
  def __init__(self, name, id, size_limit, room):
    self.id = id
    self.name = name
    self.size_limit = size_limit
    self.room = room
    room.capstones.append(self)
    self.size = 0
    self.students = []
  def add_student(self, student):
    if self.size < self.size_limit:
      student.assigned = True
      student.assignment = self
      self.students.append(student)
      self.size += 1
      return True
    else:
      return False
  


students = []
capstones = []
rooms = []

l = settings_loader("settings.ncfg").result

print("Creating Rooms")

for i in range(1,8):
  o = l.get_setting("Room"+str(i))
  t = l.get_setting("Room"+str(i)+"Size")
  rooms.append(room(o,t))

print("Creating Capstones")

for i in range(1,14):
  o = l.get_setting("Option"+str(i))
  c = int(l.get_setting("Option"+str(i)+"Room"))
  size = int(int(rooms[c-1].size_limit)/2)
  capstones.append(capstone(o,i,size,rooms[c-1]))

print("Hotfix")

for i in range(0,7):
  if len(rooms[i].capstones) == 1:
    rooms[i].capstones.append(rooms[i].capstones[0])

print("Creating Students")

import csv
with open('responses.csv', newline='') as csvfile: 
  reader = csv.DictReader(csvfile)
  for row in reader:
    raw = [row["First Choice"],row["Second Choice"],row["Third Choice"]]
    students.append(student(row["First Name"] + " "+row["Last Name"],row["Email Address"],raw,row["Advisory"]))

print("Sorting Students")

sort_students(students)

print("Populating Capstones")

for student in students:
  if student.prefrences != [0,0,0]:
    for choice in student.prefrences:
      if capstones[choice-1].add_student(student):
        break
      
print("Filling in people who couldn't spend 5 minutes to do the form")

for student in students:
  if student.name == "Jennifer Zhang":
    print(student.prefrences)
    print(student.assigned)
  assigned = False
  if student.prefrences == [0,0,0] or student.assigned == False:
    lowest = -1
    for i in range(0,13):
      if capstones[i].size < capstones[i].size_limit and lowest == -1:
        lowest = i
        continue
      if capstones[i].size < capstones[i].size_limit and capstones[i].size < capstones[lowest].size:
        print(str(capstones[i].size)+"/"+str(capstones[i].size_limit))
        lowest = i
        
    assigned = capstones[lowest].add_student(student)
    assert assigned, "All Full"


print("Displaying Results")

for capstone in capstones:
  print("---"+capstone.name+"---")
  print("Students: ("+str(len(capstone.students))+")")
  for student in capstone.students:
    print("- "+student.email +" | "+str(student.grade))

print("Saving")
with open('output.csv', mode='w') as csv_file:
  fieldnames = ['Name','Advisory','Capstone 1','Capstone 2','Room']
  writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

  writer.writeheader()
  writer.writerow({'Name': 'Made by Nolan Burkhart :)'})
  for student in students:
    writer.writerow({'Name': student.name, 'Advisory': student.advisory, 'Capstone 1': student.assignment.room.capstones[0].name, 'Capstone 2': student.assignment.room.capstones[1].name, 'Room': student.assignment.room.name})