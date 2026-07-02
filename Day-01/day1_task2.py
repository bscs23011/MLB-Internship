print("\nLargest number in a list\n")

def largest_num(numbers):
    max=numbers[0]
    for num in numbers:
        if num > max:
            max = num
    return max

def second_largest(numbers):
    largest=largest_num(numbers)
    second_max = float('-inf')
    for num in numbers:
        if num < largest and num > second_max:
            second_max = num
    return second_max

numbers=[10000,90,4320,342,9023]
max_num = largest_num(numbers)
print(f"List : {numbers}")
print(f"largest number in the list: {max_num}\n")

print("\nSecond largest number in a list\n")

second_max_num = second_largest(numbers)
print(f"2nd largest number in the list: {second_max_num}\n")

print("\nremove duplicates\n")
def remove_duplicates(numbers):
    second_list=[]
    for num in numbers:
        if num not in second_list:
            second_list.append(num)
    return second_list

mylist=[10,10,20,20,30,30]
no_duplicates=remove_duplicates(mylist)
print(f'original list: {mylist}')
print(f'removed duplicates: {no_duplicates}')

print("\nReverse a list\n")
def reverse_list(numbers):
    reversed_list=[]
    for i in range(len(numbers)-1,-1,-1):
        reversed_list.append(numbers[i])
    return reversed_list

reversed_numbers = reverse_list(numbers)
print(f'original list: {numbers}')
print(f'reversed list: {reversed_numbers}')

print("\nCommon elements\n")
def common_elements(list1,list2):
    common_list=[]
    for num in list1:
        if num in list2:
            common_list.append(num)
    return common_list

list1=[1,2,3,4,5]
list2=[1,2,3,4,5,6,7]
common_list = common_elements(list1,list2)
print(f'list 1 : {list1}')
print(f'(list 2 : {list2})')
print(f'common list : {common_list}')

print("\nCount occurrences of an element.\n")

def count_occurrences(numbers,element):
    count = 0
    for num in numbers:
        if num == element:
            count += 1
    return count
print(f'list : {mylist}')
count = count_occurrences(mylist,10)
print(f'Occurences : {mylist} ')

print("\n Convert a tuple into a list and vice versa.\n")
def tuple_to_list(numbers):
    mylist=[]
    for num in numbers:
        mylist.append(num)
    return mylist
def list_to_tuple(numbers):
    mytuple=()
    for num in numbers:
        mytuple += (num,)
    return mytuple

numbers_tuple=(1,2,3,4,5)
converted_list=tuple_to_list(numbers_tuple)
print(f'original tuple : {numbers_tuple}')
print(f'converted list : {converted_list}')
convert_tuple=list_to_tuple(converted_list)
print(f'converted tuple : {convert_tuple}')

print("\nFind unique values from a list.\n")
def unique_values(numbers):
    unique_number=set()
    for num in numbers:
        if num not in unique_number:
            unique_number.add(num)
    return unique_number

unique_numbers=unique_values(mylist)
print(f'original list : {mylist}')
print(f'unique numbers : {unique_numbers}')


print("\nPerform union and intersection operations.\n")
set_A={1,3,4,5,6,7}
set_B={4,5,6,7,8,9}
print(f'set A : {set_A}')
print(f'set B : {set_B}')
print(f'union: {set_A | set_B}')
print(f'intersection: {set_A & set_B}')


# Dictionaries

# Create a student record dictionary.
print("\nCreate a student record dictionary.\n")
student_record = {
    "name" : "hassan",
    "class" : "12th",
    "subjects" : {"Maths" : 90, "Physics" : 80, "Chemistry" : 70}
}

print(f"Student Record: {student_record}")

# Calculate average marks of students.
total_marks = sum(student_record["subjects"].values())
average_marks = total_marks / len(student_record["subjects"])
print(f"Average Marks: {average_marks}")

# Count frequency of words in a sentence.

sentence = "messi messi messi ronaldo ronaldo neymar"
words_list= sentence.split()
word_frequency={}
duplicate_list=[]
print(f"Words List: {words_list}")
for words in words_list:
    frequency = 0
    if words not in duplicate_list:
        for i in range(len(words_list)):
            if words == words_list[i]:
                frequency+=1
        word_frequency[words] = frequency

print(f"Frequency: {word_frequency}")

        

