
import os
import math

marks = 0
feedback = ""


failed_tests = ""

# t-single tests
tsingle = 0
place = 1

while place <= 5:
  print("Running test t-single/0" + str(place))
  os.system("python ./SRPN/srpn.py < t-single/0" + str(place) + " > test.txt")
  diff = os.system("diff test.txt t-single/0" + str(place) + ".result.term > temp.txt")
  if diff == 0:
    tsingle+=1
    marks+=1
    print("Test passed")
  else:
    print("Test failed")
    failed_tests += "t-single/0" + str(place) + "\n"
  f = open("test.txt", 'r')
  content = f.read()
  resultF = open("t-single/0" + str(place) + ".result.term", 'r')
  resultContent = resultF.read()
  print("Your output: \n"+content)
  print("Expected output: \n"+resultContent)

  place+=1

feedback += "t-single : " + str(tsingle) + "/5\n"

# t-multiple tests
tmultiple = 0
place = 1

while place <= 5:
  print("Running test t-multiple/0" + str(place))
  os.system("python ./SRPN/srpn.py < t-multiple/0" + str(place) + " > test.txt")
  diff = os.system("diff test.txt t-multiple/0" + str(place) + ".result.term > temp.txt")
  if diff == 0:
    tmultiple+=1;
    marks+=1
    print("Test passed")
  else:
    print("Test failed")
    failed_tests += "t-multiple/0" + str(place) + "\n"
  f = open("test.txt", 'r')
  content = f.read()
  resultF = open("t-multiple/0" + str(place) + ".result.term", 'r')
  resultContent = resultF.read()
  print("Your output: \n"+content)
  print("Expected output: \n"+resultContent)
  place+=1

feedback += "t-multiple : " + str(tmultiple) + "/5\n"

# t-saturation
tsaturation = 0
place = 1

while place <= 5:
  print("Running test t-saturation/0" + str(place))
  os.system("python ./SRPN/srpn.py < t-saturation/0" + str(place) + " > test.txt")
  diff = os.system("diff test.txt t-saturation/0" + str(place) + ".result.term > temp.txt")
  if diff == 0:
    tsaturation+=1
    marks+=1
    print("Test passed")
  else:
    failed_tests += "t-saturation/0" + str(place) + "\n"
    print("Test failed")
  
  f = open("test.txt", 'r')
  content = f.read()
  resultF = open("t-saturation/0" + str(place) + ".result.term", 'r')
  resultContent = resultF.read()
  print("Your output: \n"+content)
  print("Expected output: \n"+resultContent)
  place+=1

feedback += "t-saturation : " + str(tsaturation) + "/5\n"

# t-obscure tests
tobscure = 0
place = 1

while place <= 5:
  print("Running test t-obscure/0" + str(place))
  os.system("python ./SRPN/srpn.py < t-obscure/0" + str(place) + " > test.txt")
  diff = os.system("diff test.txt t-obscure/0" + str(place) + ".result.term > temp.txt")
  if diff == 0:
    tobscure+=1;
    marks+=1
    print("Test passed")
  else:
    failed_tests += "t-obscure/0" + str(place) + "\n"
    print("Test failed")

  f = open("test.txt", 'r')
  content = f.read()
  resultF = open("t-obscure/0" + str(place) + ".result.term", 'r')
  resultContent = resultF.read()
  print("Your output: \n"+content)
  print("Expected output: \n"+resultContent)
  place+=1

feedback += "t-obscure : " + str(tobscure) + "/5\n"

# Code quality and design
# running a python linter over the code which gives a mark out of 10
# which is then made to be out of 40
os.system("pylint --rcfile pylintrc ./SRPN/srpn.py > code-report.txt")

print(feedback)
print("Running with expected input : " + str(marks) +"/20")
print("\nExamples of Failed Tests \n" + failed_tests)