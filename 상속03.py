# 이건 사람을 나타내는 틀(클래스)이야. 사람마다 고유한 번호(id)와 이름(name)이 있어.
class Person:
    # 이건 Person 클래스를 만들 때 처음에 실행되는 특별한 함수야. 사람의 번호와 이름을 저장해.
    def __init__(self, id, name):
        # self는 이 사람 자신을 가리켜. id는 사람의 고유 번호야.
        self.id = id
        # name은 사람의 이름이야.
        self.name = name

    # 이건 사람의 정보를 화면에 출력하는 함수야. 번호와 이름을 보여줘.
    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}")


# 이건 Person을 물려받은 Manager 클래스야. Person의 모든 것을 가지고 있고, 추가로 직급(title)을 가지고 있어.
class Manager(Person):
    # Manager를 만들 때 실행되는 함수야. Person의 번호와 이름, 그리고 직급을 저장해.
    def __init__(self, id, name, title):
        # 먼저 Person의 __init__을 호출해서 번호와 이름을 저장해.
        super().__init__(id, name)
        # title은 이 사람의 직급이야. 예를 들어 "부장" 같은 거야.
        self.title = title

    # Manager의 정보를 출력하는 함수야. Person의 정보에다가 직급도 추가해서 보여줘.
    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}, Title: {self.title}")


# 이건 Person을 물려받은 Employee 클래스야. Person의 모든 것을 가지고 있고, 추가로 기술(skill)을 가지고 있어.
class Employee(Person):
    # Employee를 만들 때 실행되는 함수야. Person의 번호와 이름, 그리고 기술을 저장해.
    def __init__(self, id, name, skill):
        # 먼저 Person의 __init__을 호출해서 번호와 이름을 저장해.
        super().__init__(id, name)
        # skill은 이 사람이 가진 기술이야. 예를 들어 "Python" 같은 프로그래밍 언어야.
        self.skill = skill

    # Employee의 정보를 출력하는 함수야. Person의 정보에다가 기술도 추가해서 보여줘.
    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}, Skill: {self.skill}")


# 이제부터는 테스트 코드야. 우리가 만든 클래스들이 잘 작동하는지 확인해보는 거야.

# 이건 구분선이야. 테스트를 시작할 때마다 이렇게 선을 그어서 구분해.
print("=" * 50)
# 이건 첫 번째 테스트야. Person 객체를 만들고 정보를 출력해봐.
print("테스트 1: Person 객체 생성 및 정보 출력")
print("=" * 50)
# person1이라는 이름의 Person 객체를 만들었어. 번호는 1, 이름은 "김철수"야.
person1 = Person(1, "김철수")
# person1의 정보를 출력해. "ID: 1, Name: 김철수"라고 나올 거야.
person1.printInfo()

# 빈 줄을 하나 넣고, 다시 구분선을 그어.
print("\n" + "=" * 50)
# 두 번째 테스트야. Person 객체의 속성들을 직접 확인해봐.
print("테스트 2: Person 객체의 id, name 속성 확인")
print("=" * 50)
# person1의 id와 name을 직접 출력해봐.
print(f"Person ID: {person1.id}, Name: {person1.name}")

# 세 번째 테스트야. Manager 객체를 만들고 정보를 출력해봐.
print("\n" + "=" * 50)
print("테스트 3: Manager 객체 생성 및 정보 출력")
print("=" * 50)
# manager1이라는 Manager 객체를 만들었어. 번호 2, 이름 "이영희", 직급 "부장"이야.
manager1 = Manager(2, "이영희", "부장")
# manager1의 정보를 출력해. Person의 정보에 직급도 추가될 거야.
manager1.printInfo()

# 네 번째 테스트야. Manager 객체의 모든 속성을 확인해봐.
print("\n" + "=" * 50)
print("테스트 4: Manager 객체의 모든 속성 확인")
print("=" * 50)
# manager1의 id, name, title을 직접 출력해봐.
print(f"Manager ID: {manager1.id}, Name: {manager1.name}, Title: {manager1.title}")

# 다섯 번째 테스트야. Employee 객체를 만들고 정보를 출력해봐.
print("\n" + "=" * 50)
print("테스트 5: Employee 객체 생성 및 정보 출력")
print("=" * 50)
# employee1이라는 Employee 객체를 만들었어. 번호 3, 이름 "박민준", 기술 "Python"이야.
employee1 = Employee(3, "박민준", "Python")
# employee1의 정보를 출력해. Person의 정보에 기술도 추가될 거야.
employee1.printInfo()

# 여섯 번째 테스트야. Employee 객체의 모든 속성을 확인해봐.
print("\n" + "=" * 50)
print("테스트 6: Employee 객체의 모든 속성 확인")
print("=" * 50)
# employee1의 id, name, skill을 직접 출력해봐.
print(f"Employee ID: {employee1.id}, Name: {employee1.name}, Skill: {employee1.skill}")

# 일곱 번째 테스트야. 여러 Manager 객체를 만들고 출력해봐.
print("\n" + "=" * 50)
print("테스트 7: 여러 Manager 객체 생성 및 출력")
print("=" * 50)
# manager2와 manager3를 만들었어. 각각 다른 번호, 이름, 직급이야.
manager2 = Manager(4, "최민수", "이사")
manager3 = Manager(5, "정수진", "처장")
# manager2의 정보를 출력해.
manager2.printInfo()
# manager3의 정보를 출력해.
manager3.printInfo()

# 여덟 번째 테스트야. 여러 Employee 객체를 만들고 출력해봐.
print("\n" + "=" * 50)
print("테스트 8: 여러 Employee 객체 생성 및 출력")
print("=" * 50)
# employee2와 employee3를 만들었어. 각각 다른 번호, 이름, 기술이야.
employee2 = Employee(6, "한유진", "Java")
employee3 = Employee(7, "오준호", "JavaScript")
# employee2의 정보를 출력해.
employee2.printInfo()
# employee3의 정보를 출력해.
employee3.printInfo()

# 아홉 번째 테스트야. Manager와 Employee가 Person을 물려받았는지 확인해봐.
print("\n" + "=" * 50)
print("테스트 9: Manager와 Employee 객체의 상속 확인")
print("=" * 50)
# isinstance 함수는 어떤 객체가 특정 클래스의 종류인지 확인해줘.
# manager1은 Person의 종류인가? True가 나올 거야.
print(f"Manager는 Person의 인스턴스인가? {isinstance(manager1, Person)}")
# employee1은 Person의 종류인가? True가 나올 거야.
print(f"Employee는 Person의 인스턴스인가? {isinstance(employee1, Person)}")
# manager1은 Employee의 종류인가? False가 나올 거야.
print(f"Manager는 Employee의 인스턴스인가? {isinstance(manager1, Employee)}")

# 마지막 테스트야. 각 객체의 타입(종류)을 확인해봐.
print("\n" + "=" * 50)
print("테스트 10: 클래스 타입 확인")
print("=" * 50)
# type 함수는 객체의 타입을 알려줘. __name__은 타입의 이름을 가져와.
# manager1의 타입은 "Manager"야.
print(f"manager1의 타입: {type(manager1).__name__}")
# employee1의 타입은 "Employee"야.
print(f"employee1의 타입: {type(employee1).__name__}")
# person1의 타입은 "Person"야.
print(f"person1의 타입: {type(person1).__name__}")
