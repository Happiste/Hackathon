#First Hhackaton 22/11/2024
import setup_bdd as bdd
import do_things as dt


def display_menu(me):
    print("""\033[1;31m
            Welcome young athlete ! 
        Are you ready to this journey ?
          FROM BUDDHA TO APPOLON\033[0m
          """)
    print('(c): Calculate my basal metabolism')
    print('(a): Add a new lunch')
    print('(w): Add a new Workout')
    print('(d): Display the summary of the day')
    print('(e): Export data in json format')
    print('(x): Exit')
    response =  input('>>> ').lower()

    if response == 'c':
        me.cal_basal_metabolism()
    elif response == 'a':
        me.add_dish()
    elif response == 'w':
        me.add_workout()
    elif response == 'd':
        me.display()
    elif response == 'e':
        me.export_data()
    elif response == 'x':
        print('\033[1;36mBye young Appolon\033[0m')
        exit()

def main():
    bdd.create_tables()
    me =  dt.myFitPlanner()
    while True:
        display_menu(me)

if __name__=='__main__':
    main()