# Person 클래스 정의
class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}")


# Manager 클래스 - Person 상속
class Manager(Person):
    def __init__(self, id, name, title):
        super().__init__(id, name)
        self.title = title
    
    def printInfo(self):
        super().printInfo()
        print(f"Title: {self.title}")


# Employee 클래스 - Person 상속
class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill
    
    def printInfo(self):
        super().printInfo()
        print(f"Skill: {self.skill}")


# 10개의 인스턴스 생성 및 사용
if __name__ == "__main__":
    # Person 인스턴스 2개
    person1 = Person(1, "김철수")
    person2 = Person(2, "이영희")
    
    # Manager 인스턴스 4개
    manager1 = Manager(101, "박준호", "프로젝트 매니저")
    manager2 = Manager(102, "최민정", "개발팀장")
    manager3 = Manager(103, "정하진", "마케팅 매니저")
    manager4 = Manager(104, "이준영", "영업 매니저")
    
    # Employee 인스턴스 4개
    employee1 = Employee(201, "김민수", "Python")
    employee2 = Employee(202, "최지은", "JavaScript")
    employee3 = Employee(203, "박현우", "Java")
    employee4 = Employee(204, "손미연", "SQL")
    
    # 모든 인스턴스 출력
    print("=== Person 인스턴스 ===")
    person1.printInfo()
    print()
    person2.printInfo()
    
    print("\n=== Manager 인스턴스 ===")
    manager1.printInfo()
    print()
    manager2.printInfo()
    print()
    manager3.printInfo()
    print()
    manager4.printInfo()
    
    print("\n=== Employee 인스턴스 ===")
    employee1.printInfo()
    print()
    employee2.printInfo()
    print()
    employee3.printInfo()
    print()
    employee4.printInfo()
