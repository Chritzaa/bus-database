import sqlite3 as sql
from sqlite3 import Error

database = "leoforia"
conn = sql.connect(database)
curr = conn.cursor()

def write_sql_command(conn):
    sql_command = input("Enter your SQL command ")
    curr.execute(sql_command)
    print(curr.fetchall())

def show_data(conn):
    t_table = input("Which table do you want to see? ")
    curr.execute("SELECT * FROM {}".format(t_table))
    print(curr.fetchall())

def show_tables(conn):
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    curr.execute(query)
    print(curr.fetchall())

def create_table(conn):
    table_name = input("Name the table ")
    att = input("Enter the attributes in brackets ")
    curr.execute("CREATE TABLE "+table_name+" "+att)
    print("Table created")

def init_database(conn):
    with open('create.sql',encoding = 'utf8') as sql_file:
        curr.executescript(sql_file.read())

def delete_table(conn):
    table_to_del = input("Which table do you want to delete? ")
    try:
        curr.execute("DROP TABLE " + table_to_del)
        print("Table deleted")
    except:
        print("This table doesn't exist")

def update_data(conn):
    up_table = input("In which table do you wish to update data? ")
    up_data = input("What would you like to chane? ")
    condition = input("Set the condition ")
    if condition =="":
        conn.execute("UPDATE "+up_table+" set "+up_data)
        conn.commit()
    else:
        conn.execute("UPDATE "+up_table+" set "+up_data+" where "+condition)
        conn.commit()

def insert_data(conn):
    att = []
    values = []
    table = input("Select the table to add values ")
    data = curr.execute("SELECT * FROM "+table)
    for column in data.description:
        att.append(column[0])
    for i in att:
        values.append(input("Enter value for: "+i+" "))
    print(tuple(values))
    values = tuple(values)
    conn.execute("INSERT INTO "+table+" VALUES "+str(values))
    conn.commit()

def timetable(conn):
    print("------Scenario 1: Which buses are active at x time------\n")
    t_start = input("Enter the time to see the active buses during that timeframe: ")
    # t_end = input("End in ")
    query = """SELECT kod_prag_dromologiou,x_coords,y_coords
               FROM pragmatiko_dromologio
               WHERE strftime('%H %M %S',pragm_xronos_liksis) > strftime('%H %M %S','{}') and strftime('%H %M %S',pragm_xronos_enarksis) < strftime('%H %M %S','{}')""".format(t_start,t_start)
    curr.execute(query)
    print (curr.fetchall())

def busnstop(conn):
    print("\n------Scenario 2: Which bus passes from x stop------\n")
    t_stop = input("Select stop: ")
    query = """SELECT DISTINCT kod_leof, programmatismenh_wra, epistrofi
               FROM anamenetai
               WHERE kod_leof in (SELECT DISTINCT leoforio_ektelesis
               FROM (apoteleitai AS a join stasi AS s ON a.onoma_stasis = s.onoma_stasis) join dromologio as d on d.kodikos_dromologiou = a.kod_dromologiou
               WHERE a.onoma_stasis = '{}') AND onoma_stasis = '{}'""".format(t_stop,t_stop)
    curr.execute(query)
    print(curr.fetchall())

def busnroute(conn):
    print("\n------Scenario 3: Which routes are completed by the specific bus------\n")
    leof_ekt = input("Select Bus: ")
    query = """SELECT dromologio.kodikos_dromologiou, programmatismeno_dromologio.xronos_enarksis,programmatismeno_dromologio.xronos_liksis
               from leoforio, dromologio ,programmatismeno_dromologio
               where dromologio.leoforio_ektelesis='{}' and leoforio.kod_leof=dromologio.leoforio_ektelesis 
               and dromologio.kodikos_dromologiou = programmatismeno_dromologio.kod_prog_dromologiou""".format(leof_ekt)
    curr.execute(query)
    print(curr.fetchall())

def prevstops(conn):
    print("\n------Scenario 4: Which stops are before depending on the line------\n")
    t_stop = input("Select your stop: ")
    t_line = input("In which line? ")
    query = """SELECT DISTINCT stasi.onoma_stasis
               FROM (apoteleitai join stasi on apoteleitai.onoma_stasis = stasi.onoma_stasis) join dromologio on dromologio.kodikos_dromologiou = apoteleitai.kod_dromologiou
               WHERE stasi.xcord_stashs < (SELECT xcord_stashs FROM stasi WHERE onoma_stasis ='{}') AND apoteleitai.kod_dromologiou LIKE ('{}%') AND dromologio.grammi in (SELECT DISTINCT dromologio.grammi
               FROM (apoteleitai join stasi on apoteleitai.onoma_stasis = stasi.onoma_stasis) join dromologio on dromologio.kodikos_dromologiou = apoteleitai.kod_dromologiou
               WHERE stasi.onoma_stasis = '{}')""".format(t_stop,t_line,t_stop)
    curr.execute(query)
    print(curr.fetchall())

def finddriver(conn):
    print("\n------Scenario 5: Which driver drives a specific route------\n")
    t_route = input("Select the route ")
    query = """SELECT onoma 
            FROM (odigos join leoforio ON odigos.kod_leof_odig = leoforio.kod_leof) JOIN dromologio on leoforio.kod_leof = dromologio.leoforio_ektelesis
            WHERE dromologio.kodikos_dromologiou = '{}' AND strftime('%H %M %S',vra_enarxis_bardias) < strftime('%H %M %S',(SELECT programmatismeno_dromologio.xronos_enarksis
            FROM dromologio join programmatismeno_dromologio on dromologio.kodikos_dromologiou = programmatismeno_dromologio.kod_prog_dromologiou
            WHERE dromologio.kodikos_dromologiou = '{}')) AND strftime('%H %M %S',vra_lixis_bardias) > strftime('%H %M %S',(SELECT programmatismeno_dromologio.xronos_enarksis
            FROM dromologio join programmatismeno_dromologio on dromologio.kodikos_dromologiou = programmatismeno_dromologio.kod_prog_dromologiou
            WHERE dromologio.kodikos_dromologiou = '{}'))""".format(t_route,t_route,t_route)
    curr.execute(query)
    print(curr.fetchall())


def main():
    init_database(conn)
    print("Available commands: Show Tables, Create Table, Delete Table, Insert Data,Show Data, Update Data, Write SQL, Scenario 1 to 5\n")
    commands = {
        'Show Tables':show_tables,
        'Create Table':create_table,
        'Delete Table':delete_table,
        'Insert Data':insert_data,
        'Show Data':show_data,
        'Update Data':update_data,
        'Write SQL':write_sql_command,
        'Scenario 1':timetable,
        'Scenario 2':busnstop,
        'Scenario 3':busnroute,
        'Scenario 4':prevstops,
        'Scenario 5':finddriver
    }
    while True:
        c = input("What do you want to do? \n")
        if c=='EXIT':break
        else:
            try: commands[c](conn)
            except: print("Not a valid command")
    conn.close()


if __name__ == '__main__':
        main()
