# Python Collection Type Comparison

# 1. List
my_list = [1, 2, 3, 2]

# 2. Tuple
my_tuple = (1, 2, 3, 2)

# 3. Set
my_set = {1, 2, 3, 2}

# 4. Dictionary
my_dict = {
    "name": "Jay",
    "age": 30,
    "job": "DBA"
}

print("===== LIST =====")
print(my_list)
print("Type :", type(my_list))
print("Index access :", my_list[0])
print("Append :", end=" ")
my_list.append(4)
print(my_list)

print("\n===== TUPLE =====")
print(my_tuple)
print("Type :", type(my_tuple))
print("Index access :", my_tuple[0])

# tuple 은 수정 불가능
# my_tuple.append(4)  # ERROR

print("\n===== SET =====")
print(my_set)
print("Type :", type(my_set))

# set 은 중복 제거됨
print("Add element :", end=" ")
my_set.add(4)
print(my_set)

# set 은 index 접근 불가능
# print(my_set[0])  # ERROR

print("\n===== DICT =====")
print(my_dict)
print("Type :", type(my_dict))

# key 로 접근
print("Name :", my_dict["name"])

# 데이터 추가
my_dict["city"] = "Seoul"
print("After add :", my_dict)