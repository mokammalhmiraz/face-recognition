# numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
#
# odd_sum = 0
# even_sum = 0
#
# for num in numbers:
#     if num % 2 == 0:
#         even_sum += num
#     else:
#         odd_sum += num
#
# print("Sum of odd:", odd_sum)
# print("Sum of even:", even_sum)
#
# ########################################### 1
#
#
# side1 = float(input("Side 1: "))
# side2 = float(input("Side 2: "))
# side3 = float(input("Side 3: "))
#
#
# if (side1 + side2 > side3) and (side2 + side3 > side1) and (side1 + side3 > side2):
#     print("Triangle is valid.")
# else:
#     print("Triangle is not valid.")
#
# ################################################## 2
#
# class Student:
#     pass
#
# class Marks:
#     pass
#
# student_instance = Student()
# marks_instance = Marks()
#
# print("checking student is the class of student_instance:",isinstance(student_instance, Student))
# print("checking marks is the class of marks_instance:", isinstance(marks_instance, Marks))
#
# print("Student class is the subclass of build object:",issubclass(Student, object))
# print("Mark class is the subclass of build object:",issubclass(Marks, object))

###################################################### 3

# class Student:
#     def __init__(std, studentName, marks):
#         std.studentName = studentName
#         std.marks = marks
#
#
# # Creating an instance of the Student class
# student = Student("Miraz", 50)
#
#
# print("Original values:")
# print(f"Student Name:", student.studentName)
# print(f"Marks:",student.marks)
#
# # Modifying the attribute values
# student.studentName = "Clone Miraz"
# student.marks = 100
#
#
# print("\nModified values:")
# print(f"Student Name:", student.studentName)
# print(f"Marks:", student.marks)
#
#
# ######################################################## 4
#
# class Student:
#     def __init__(std, studentId, studentName):
#         std.studentId = studentId
#         std.studentName = studentName
#
#     def add_student_class(std, studentClass):
#         std.studentClass = studentClass
#
#
# # Creating an instance of the Student class
# student = Student(201002054, "Miraz")
#
# # Adding the studentClass attribute
# student.add_student_class("Data Minning")
#
# # Displaying all the attributes and their values
# print("All attributes and their values:")
# print(f"Student ID:", student.studentId)
# print(f"Student Name:", student.studentName)
# print(f"Student Class:", student.studentClass)
#
# # Removing the studentName attribute
# del student.studentName
#
# # Displaying all the attributes and their values after removing studentName
# print("\nAll attributes and their values after removing studentName:")
# print(f"Student ID:", student.studentId)
# # print(f"Student Name:", student.studentName)
# print(f"Student Class:", student.studentClass)
#
# #
# # ########################################################## 5
# #
class Student:
    def __init__(std, studentId, studentName):
        std.studentId = studentId
        std.studentName = studentName

    def add_student_class(std, studentClass):
        std.studentClass = studentClass

    def display_attributes(std):
        for attr, value in std.__dict__.items():
            print(f"{attr}: {value}")



student = Student(201002054, "Miraz")


student.add_student_class("Data Minning")


student.display_attributes()
