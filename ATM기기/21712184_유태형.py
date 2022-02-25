import pickle #계좌를 저장하기 위한 모듈
import os #계좌를 읽고 쓰기 위한 모듈

#Account 객체(계좌)들은 작업디렉토리/21712184_유태형_계좌폴더/계좌번호.p로 저장되며
#프로그램 시작시 폴더내에 파일들을 읽어 Account의 user딕셔너리를 초기화 하고
#변동사항이 있을시 해당 계좌 파일들을 갱신하였습니다.


class Account:
    user ={} #프로그램 실행중 빠른 계산을 위한 딕셔너리(모든 계좌 저장)
    
    def __init__(self,name,account,password,balance): #생성자
        self.__name=name
        self.__account=account
        self.__password=password
        self.__balance=balance
        Account.user[account]=self #딕셔너리에 추가하여 계좌를 키로 접근가능



    def withdraw(self,amount,password): #출금
        if self.__password != password: #비밀번호 확인
            return "비밀번호 틀림"
        try:
            temp=str(amount)
            amount=int(temp) #int로 바꿈으로써 정수인지 확인합니다.
            if amount < 0: #출금액이 음수일때
                return "잘못된 금액(출금액이 음수)"
            elif self.__balance < amount: #잔액부족
                return "잔액부족"
        except ValueError: #출금액이 정수가 아닐때
            return "잘못된 금액(출금액이 정수가 아님)"

        self.__balance -= amount
        return str(amount)+"이 출금되었습니다.(잔액 "+str(self.__balance)+"원)" #정상실행 결과


    def deposit(self,amount): #입금
        try:
            temp=str(amount)
            amount=int(temp) #int로 형변환 함으로써 정수인지 확인
            if amount < 0: #입금액이 음수
                return "잘못된 금액(입금액이 음수)"
        except ValueError: #정수가 아님
            return "잘못된 금액(입금액이 정수가 아님)"
            
        self.__balance += amount
        return str(amount)+"이 입금되었습니다.(잔액 "+str(self.__balance)+"원)" #정상실행 결과


    def trans(self,amount,account,password): #송금
        if self.__password != password: #비밀번호 확인
            return "비밀번호 틀림"
        try:
            temp=str(amount)
            amount=int(temp)
            if amount < 0:
                return "잘못된 금액(송금액이 음수)"
            elif self.__balance < amount:
                return "잔액부족"
        except ValueError:
            return "잘못된 금액(송금액이 정수가 아님)"
        
        if account not in Account.user: #딕셔너리에 송금계좌가 존재하는지 확인
            return "잘못된 계좌"
        
        self.__balance -= amount
        Account.user[account].deposit(amount)#송금액만큼 송금계좌에 입금
        return str(amount)+"이 "+account+"님에게 송금되었습니다. (잔액 "+str(self.__balance)+"원)"
        #정상실행 결과
    
    def check(self,password): #계좌조회
        if self.__password != password:
            return "비밀번호 틀림"

        return "예금주: "+str(self.__name) + ", 잔액: "+str(self.__balance)

    def getName(self):
        return self.__name

    def getAccount(self):
        return self.__account


def admin_menu():#관리자 메뉴
    sub_menu=0
    while True:
        sub_menu=int(input("1. 계좌생성 2. 계좌삭제 3.계좌현황 4.돌아가기 : "))

        if sub_menu == 1: #계좌생성
            name = input("예금주 : ")
            account = input("계좌번호 : ")
            balance = int(input("잔고 : "))
            password = input("비밀번호 : ") #정보들을 기입합니다.
            
            if account in Account.user: #이미 존재하는 계좌
                print("계좌가 이미 존재합니다.")
            else: #새로 만든계좌
                temp = Account(name,account,password,balance)
                with open(dir_name+"/"+account+".p","wb") as f: #계좌번호로 계좌 데이터 저장
                    pickle.dump(temp, f) #폴더에 파일로 저장합니다.
                print("계좌가 생성되었습니다.")

        elif sub_menu == 2: #계좌 삭제
            account = input("삭제할 계좌번호 : ")

            if account not in Account.user: #삭제하려는 계좌가 존재하지 않음
                print("해당 계좌가 존재하지 않습니다.")
            else: #삭제하려는 계좌가 존재
                os.remove(dir_name+"/"+account+".p") #폴더에서 해당 계좌파일 삭제
                Account.user.pop(account) #딕셔너리에서 해당 계좌 삭제
                print("계좌가 삭제되었습니다.")

        elif sub_menu == 3:#계좌 현황
            print("예금주     계좌번호")
            print("===================")
            for obj in Account.user: #딕셔너리에서 차례로
                print(Account.user[obj].getName()+"     "+obj) #계좌 출력


        elif sub_menu == 4: #시작메뉴
            print("시작 메뉴 이동")
            return
            
                
            

def customer_login(login_account): #고객 메뉴
    sub_menu = 0
    temp = Account.user[login_account] #로그인한 계좌의 객체 불러옵니다.
    while True:
        sub_menu = int(input("1.입금 2.출금 3.송금 4.잔액조회 5.로그아웃 : "))
        if sub_menu == 1: #입금
            amount = input("입금액 : ")            
            print(temp.deposit(amount))

                
        elif sub_menu == 2: #출금
            amount = input("출금액 : ")
            password = input("비밀번호 : ")
            print(temp.withdraw(amount,password))

                
        elif sub_menu == 3: #송금
            account = input("송금계좌 : ")
            amount = input("송금액 : ")
            password = input("비밀번호 : ")
            print(temp.trans(amount,account,password))
            if account in Account.user: #잘못된 송금계좌가 아닐 경우(송금계좌가 존재)
                trans_temp=Account.user[account]
                os.remove(dir_name+"/"+account+".p") #이전 데이터 삭제
                with open(dir_name+"/"+account+".p","wb") as f:
                    pickle.dump(trans_temp, f) #새로운 데이터 갱신
                    
        elif sub_menu == 4: #잔액조회
            password = input("비밀번호 : ")
            print(temp.check(password))

        elif sub_menu == 5: #시작메뉴
            print("시작메뉴로 이동")
            return

        os.remove(dir_name+"/"+login_account+".p") #현재계좌 이전 데이터 삭제
        with open(dir_name+"/"+login_account+".p","wb") as f:
            pickle.dump(temp, f) #현재계좌 새로운 데이터 갱신

        
#시작시 가장 먼저 저장중인 데이터파일들을 읽어들여 클래스의 딕셔너리에 저장합니다.
dir_name="21712184_유태형_계좌폴더" #데이터를 저장하는 폴더(상대경로)
if not os.path.isdir(dir_name): #없을 경우 
    os.mkdir(dir_name) #새로 만듦

file_list = os.listdir(dir_name) #폴더에서 데이터 파일들을 리스트로 받습니다.
for user_list in file_list:
    with open(dir_name+"/"+user_list,"rb") as f:
        temp = pickle.load(f) #데이터 파일들을 차례로 읽어 옵니다.
    Account.user[temp.getAccount()] = temp #Account클래스의 user딕셔너리 초기화


    
#모든 계좌 데이터는 작업디렉토리/21712184_유태형_계좌폴더/계좌번호.p로 저장됩니다.


main_menu = 0 #시작메뉴
while True:
    main_menu=int(input("1.관리자메뉴 2.고객로그인 3.종료 : "))
                  
    if main_menu == 1: #관리자메뉴
        admin_menu()
    elif main_menu == 2: #고객메뉴
        login_account = input("계좌번호 : ")
        if login_account in Account.user: #계좌가 존재할시 고객메뉴로 이동
            print(Account.user[login_account].getName() + "님 반갑습니다.")
            customer_login(login_account) #로그인한 계좌를 고객메뉴함수의 인자로 전달합니다.
        else: #없을시
            print("잘못된 계좌") #시작메뉴
    elif main_menu == 3: #종료
        print("프로그램 종료")
        break

