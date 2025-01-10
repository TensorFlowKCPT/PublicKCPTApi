import sqlite3
import datetime
class Database:
    def StartDataBase():
            with sqlite3.connect('database.db') as conn:
                conn.execute('''CREATE TABLE IF NOT EXISTS Prepods (
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                FirstName TEXT NOT NULL,
                                SecondName TEXT NOT NULL,
                                Surname TEXT NOT NULL
                             )
                             ''')
                conn.execute('''CREATE TABLE IF NOT EXISTS Groups (
                                NAME TEXT PRIMARY KEY NOT NULL 
                             )
                             ''')
                conn.execute('''CREATE TABLE IF NOT EXISTS Subjects (
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                NAME TEXT NOT NULL
                             )
                             ''')
                conn.execute('''CREATE TABLE IF NOT EXISTS Changes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                Date Date NOT NULL,
                                GroupId TEXT NOT NULL,
                                Number INTEGER,
                                Classroom TEXT,
                                PrepodId INTEGER,
                                SubjectId INTEGER,
                                Comment TEXT,
                                DeleteUrok INTEGER,
                                FOREIGN KEY (id) REFERENCES Subjects (SubjectId),
                                FOREIGN KEY (id) REFERENCES Prepods (PrepodId),
                                FOREIGN KEY (id) REFERENCES Groups (GroupId)
                             )
                             ''')
                conn.execute('''CREATE TABLE IF NOT EXISTS Uroki (
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                SubjectId INTEGER NOT NULL,
                                PrepodId INTEGER NOT NULL,
                                GroupId TEXT NOT NULL,
                                Date Date NOT NULL,
                                Number INTEGER NOT NULL,
                                Classroom TEXT,
                                FOREIGN KEY (id) REFERENCES Subjects (SubjectId),
                                FOREIGN KEY (id) REFERENCES Prepods (PrepodId),
                                FOREIGN KEY (id) REFERENCES Groups (GroupId)
                            )
                            ''')
    
    def GetPrepodsCount():
        with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT Count(*) FROM Prepods''')
                    row = cursor.fetchone()
                    if row:
                        return int(row[0])
                    else: return False

    def GetGroupsCount():
        with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT Count(*) FROM Groups''')
                    row = cursor.fetchone()
                    if row:
                        return int(row[0])
                    else: return False

    def GetUrokiCount():
        with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT Count(*) FROM Uroki''')
                    row = cursor.fetchone()
                    if row:
                        return int(row[0])
                    else: return False

    def GetSubjectsCount():
        with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT Count(*) FROM Subjects''')
                    row = cursor.fetchone()
                    if row:
                        return int(row[0])
                    else: return False
    
    def GetPrepodsList():
            with sqlite3.connect('database.db') as conn:
                cursor = conn.execute('''SELECT * FROM Prepods ORDER BY id''' )
                row = cursor.fetchall()
                output = {}
                for i in row:
                    Prepod = {
                        'id' : i[0],
                        'FirstName' : i[1],
                        'SecondName' : i[2],
                        'Surname' : i[3]
                    }
                    output[i[0]] = Prepod 
                return output

    def GetChangeById(id:int):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.execute('''SELECT * FROM Changes WHERE id = ?''', (id,))
            row = cursor.fetchone()
            res = conn.execute('''SELECT Surname, Firstname, SecondName FROM Prepods WHERE id = ?''' , (row[5],)).fetchone()
            output = {
                'id' : row[0],
                'IsChange' : True,
                'Date' : row[1],
                'Group' : row[2],
                'Urok' : row[3],
                'Classroom' : row[4],
                'Prepod' : res[0]+' '+res[1]+' '+res[2],
                'Subject' : conn.execute('''SELECT NAME FROM Subjects WHERE id = ?''' , (row[6],)).fetchone()[0],
                'Comment' : row[7]
            }
            return output
    def GetUrokById(id:int):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.execute('''SELECT * FROM Urok WHERE id = ?''' , (id),)
            row = cursor.fetchone()
            res = conn.execute('''SELECT Surname, Firstname, SecondName FROM Prepods WHERE id = ?''' , (row[5],)).fetchone()
            output = {
                'id' : row[0],
                'IsChange' : False,
                'Date' : row[1],
                'Group' : row[2],
                'Urok' : row[3],
                'Classroom' : row[4],
                'Prepod' : res[0]+' '+res[1]+' '+res[2],
                'Subject' : conn.execute('''SELECT NAME FROM Subjects WHERE id = ?''' , (row[6],)).fetchone()[0]
            }
            return output
         
    def GetChangesDay(Date:datetime.date):
        with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT * FROM Changes WHERE Date = ? ORDER BY GroupId''' , (Date.strftime('%Y-%m-%d'),))
                    row = cursor.fetchall()
                    if row:
                        output = {}
                        for i in row:
                            change = {}
                            change['id'] = i[0]
                            change['IsChange'] = True
                            change['Date'] = i[1]
                            change['Group'] = i[2]
                            change['Urok'] = i[3]
                            change['Classroom'] = i[4]
                            res = conn.execute('''SELECT Surname, Firstname, SecondName FROM Prepods WHERE id = ?''' , (i[5],)).fetchone()
                            try:
                                change['Prepod'] = res[0]+' '+res[1]+' '+res[2]
                            except TypeError:
                                change['Prepod'] = 'Вакансия'
                            change['Subject'] = conn.execute('''SELECT NAME FROM Subjects WHERE id = ?''' , (i[6],)).fetchone()[0]
                            change['Comment'] = i[7]
                            change['Delete'] = i[8]
                            output[i[0]] = change
                        return output
                    else: return False
    
    def GetAllSubjects():
         with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT NAME FROM Subjects ''' )
                    row = cursor.fetchall()
                    if row:
                        output=[]
                        for i in row:
                             output.append(i[0])
                        return sorted(output)
    def GetAllPrepods():
        with sqlite3.connect('database.db') as conn:
            cursor = conn.execute('''SELECT Surname, Firstname, SecondName FROM Prepods ORDER BY id''' )
            row = cursor.fetchall()
            if row:
                output=[]
                for i in row:
                     output.append(i[0]+' '+i[1]+' '+i[2])
                return output
    def GetAllGroups():
        with sqlite3.connect('database.db') as conn:
           cursor = conn.execute('''SELECT NAME FROM Groups ORDER BY NAME''' )
           row = cursor.fetchall()
           if row:
               output=[]
               for i in row:
                    output.append(i[0])
               return sorted(output)
    def GetSubjectById(id):
        with sqlite3.connect('database.db') as conn:
          cursor = conn.execute('''SELECT NAME FROM Subjects Where id = ?''',(int(id),))
          row = cursor.fetchone()
          if row:
            return row[0]
    def GetPrepodsDay(Date:datetime.date,Prepod):
                #Определяем, дали ли нам id препода или ФИО, если фио - переводим в id
                try:
                    Prepod = int(Prepod)
                except ValueError:
                    with sqlite3.connect('database.db') as conn:
                        fio = Prepod.split(' ')
                        cursor = conn.execute('''SELECT id FROM Prepods WHERE (Surname = ? and FirstName = ?) OR (Surname = ? and SecondName = ?)''' , (fio[0], fio[1], fio[0], fio[1],))
                        row = cursor.fetchone()
                        Prepod = int(row[0])
                #Получаем изменения для этого препода на эту дату
                with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT * FROM Changes WHERE Date = ? AND PrepodId = ?''' , (Date.strftime('%Y-%m-%d'), Prepod,))
                    row = cursor.fetchall()
                    
                    Changes = []
                    if row:
                        for i in row:
                            change = {}
                            change['IsChange'] = True
                            change['Date'] = i[1]
                            change['Group'] = i[2]
                            change['Number'] = i[3]
                            change['Classroom'] = i[4]
                            res = conn.execute('''SELECT Surname, Firstname, SecondName FROM Prepods WHERE id = ?''' , (i[5],)).fetchone()
                            change['Prepod'] = res[0]+' '+res[1]+' '+res[2]
                            change['Subject'] = conn.execute('''SELECT NAME FROM Subjects WHERE id = ?''' , (i[6],)).fetchone()[0]
                            change['Comment'] = i[7]
                            change['Delete'] = i[8]
                            Changes.append(change)
                    cursor = conn.execute('''SELECT * FROM Uroki WHERE Date = ? AND PrepodId = ? ORDER BY Number''' , (Date.strftime('%Y-%m-%d'), Prepod,))
                    row = cursor.fetchall()
                    Uroki = []
                    if row:
                        for i in row:
                            Urok = {}
                            Urok['IsChange'] = False
                            Urok['Subject'] = conn.execute('''SELECT NAME FROM Subjects WHERE id = ?''' , (i[1],)).fetchone()[0]
                            res = conn.execute('''SELECT Surname, Firstname, SecondName FROM Prepods WHERE id = ?''' , (i[2],)).fetchone()
                            Urok['Prepod'] = res[0]+' '+res[1]+' '+res[2]
                            Urok['Group'] = i[3]
                            Urok['Date'] = i[4]
                            Urok['Number'] = int(i[5])
                            Urok['Classroom'] = i[6]
                            Uroki.append(Urok)
                Output = []
                for i in Changes:
                    Output.append(i)
                    if i['Delete'] != None:
                         for j in Uroki:
                              if j['Number'] == i['Delete'] and j['Subject'] == i['Subject'] or j['Number'] == i['Delete'] and i['Comment'].lower() == 'замена':
                                   Uroki.remove(j)
                    for j in Uroki:
                            if i['Number']==j['Number'] and j['Subject'] == i['Subject'] or j['Number'] == i['Delete'] and i['Comment'].lower() == 'замена':
                                Uroki.remove(j)
                                break
                
                for i in Uroki:
                     Output.append(i)
                
                Output = list(filter(lambda i: i.get('Comment', '').lower() != 'отмена', Output))

                OutputDict = {}
                for i in sorted(Output, key=lambda x: x['Number']):
                    try: OutputDict[i['Number']] == None
                    except KeyError: OutputDict[i['Number']] = []
                    OutputDict[i['Number']] = i

                for Urok in OutputDict.copy().values():
                    with sqlite3.connect('database.db') as conn:
                        row = conn.execute('''SELECT * FROM Changes WHERE Date = ? AND GroupId = ? And DeleteUrok = ?''' , (Urok['Date'], Urok['Group'],Urok['Number'],)).fetchall()
                        if row:
                            if not Database.GetSubjectById(row[0][6]) == Urok['Subject']:
                                OutputDict.pop(Urok['Number'])

                return OutputDict

    def GetUrokByDateNumberAndGroup(Date:datetime.date, Group:str, Number:int):
         with sqlite3.connect('database.db') as conn:
            cursor = conn.execute('''SELECT * FROM Uroki WHERE Date = ? and GroupId = ? and Number = ?''' , (Date.strftime('%Y-%m-%d'), Group, Number,))
            row = cursor.fetchone()
            if row:
                if str(row[2]).lower()!='вакансия':
                    res = conn.execute('''SELECT Surname, Firstname, SecondName FROM Prepods WHERE id = ?''' , (row[2],)).fetchone()
                    try:
                        res = res[0]+' '+res[1]+' '+res[2]
                    except: res = '?'
                else:
                    res = row[2]
                output = {
                    'id' : row[0],
                    'SubjectId' : conn.execute('''SELECT NAME FROM Subjects WHERE id = ?''' , (row[1],)).fetchone()[0],
                    'Prepod' : res,
                    'Group' : row[3],
                    'Date' : row[4],
                    'Urok' : row[5],
                    'Classroom' : row[6],
                    'IsChange' : False
                }
                return output
                
            else:
                return ''
    def GetChangesDayForGroup(Date:datetime.date, Group:str):
        with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT * FROM Changes WHERE Date = ? AND GroupId = ? ORDER BY GroupId''' , (Date.strftime('%Y-%m-%d'),Group,))
                    row = cursor.fetchall()
                    if row:
                        output = []
                        for i in row:
                            change = {}
                            change['Date'] = i[1]
                            change['Group'] = i[2]
                            change['Urok'] = i[3]
                            change['Classroom'] = i[4]
                            res = conn.execute('''SELECT Surname, Firstname, SecondName FROM Prepods WHERE id = ?''' , (i[5],)).fetchone()
                            change['Prepod'] = res[0]+' '+res[1]+' '+res[2]
                            change['Subject'] = conn.execute('''SELECT NAME FROM Subjects WHERE id = ?''' , (i[6],)).fetchone()[0]
                            change['Comment'] = i[7]
                            output.append(change)
                        return output
                    else: return False
         
         
    def GetScheduleWithChangesDay(Date:datetime.date, Group:str):
         with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT * FROM Changes WHERE Date = ? AND GroupId = ?''' , (Date.strftime('%Y-%m-%d'), Group,))
                    row = cursor.fetchall()
                    Changes = []
                    if row:
                        for i in row:
                            change = {}
                            change['Date'] = i[1]
                            change['Group'] = i[2]
                            change['Number'] = i[3]
                            change['Classroom'] = i[4]
                            try:
                                res = conn.execute('''SELECT Surname, Firstname, SecondName FROM Prepods WHERE id = ?''' , (i[5],)).fetchone()
                                prepod = res[0]+' '+res[1]+' '+res[2]
                            except:
                                prepod = 'Вакансия'
                            change['Prepod'] = prepod
                            change['Subject'] = conn.execute('''SELECT NAME FROM Subjects WHERE id = ?''' , (i[6],)).fetchone()[0]
                            change['Comment'] = i[7]
                            change['Delete'] = i[8]
                            change['IsChange'] = True
                            Changes.append(change)
                    cursor = conn.execute('''SELECT * FROM Uroki WHERE Date = ? AND GroupId = ? ORDER BY GroupId''' , (Date.strftime('%Y-%m-%d'), Group,))
                    row = cursor.fetchall()
                    Uroki = []
                    if row:
                        for i in row:
                            Urok = {}
                            try:
                                Urok['Subject'] = conn.execute('''SELECT NAME FROM Subjects WHERE id = ?''' , (i[1],)).fetchone()[0]
                            except:
                                Urok['Subject'] = '?'
                            res = conn.execute('''SELECT Surname, Firstname, SecondName FROM Prepods WHERE id = ?''' , (i[2],)).fetchone()
                            try:
                                Urok['Prepod'] = res[0]+' '+res[1]+' '+res[2]
                            except TypeError:
                                Urok['Prepod'] = 'Вакансия'
                            except:
                                Urok['Prepod'] = '?'
                            Urok['Group'] = i[3]
                            Urok['Date'] = i[4]
                            Urok['Number'] = int(i[5])
                            Urok['Classroom'] = i[6]
                            Urok['IsChange'] = False
                            Uroki.append(Urok)

                    Output = []
                    for i in Changes:
                        Output.append(i)
                        if i['Delete'] != None:
                             for j in Uroki:
                                  try:
                                    if j['Number'] == i['Delete'] and j['Subject'] == i['Subject'] or j['Number'] == i['Delete'] and i['Comment'].lower() == 'замена':
                                         Uroki.remove(j)
                                  except:
                                       pass  
                        for j in Uroki:
                                try:
                                    if i['Number']==j['Number'] and j['Subject'] == i['Subject'] or j['Number'] == i['Delete'] and i['Comment'].lower() == 'замена':
                                        Uroki.remove(j)
                                        break
                                except:
                                    pass
                    
                    for i in Uroki:
                         Output.append(i)
                    
                    Output = list(filter(lambda i: i.get('Comment', '').lower() != 'отмена' if i.get('Comment') is not None else True, Output))

                        
                    OutputDict = {}
                    for i in sorted(Output, key=lambda x: x['Number']):
                        try: OutputDict[i['Number']] == None
                        except KeyError: OutputDict[i['Number']] = []
                        OutputDict[i['Number']].append(i)
                    return OutputDict
         
    def RemoveOldSchedule():
         SevenDaysAgo = (datetime.datetime.now() + datetime.timedelta(days=-7)).date().strftime('%Y-%m-%d')
         with sqlite3.connect('database.db') as conn:
                conn.execute('''DELETE FROM Uroki
                                WHERE Date < ?''',(SevenDaysAgo,))
                conn.execute('''DELETE FROM Changes
                                WHERE Date < ?''',(SevenDaysAgo,))
                
    def AddChange(Subject, Prepod, Group:str, Date:datetime.date, Number:int, Classroom:str, Comment, Delete):
        if type(Subject) is str:
            Flag = True
            while Flag:
                with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT * FROM [Subjects] WHERE NAME = ?''', (Subject,))
                    row = cursor.fetchone()
                    if row:
                        Subject = int(row[0])
                        Flag = False
                    else:
                        if not Database.AddSubject(Subject):
                            return False
                        
        if type(Prepod) is str and Prepod.lower() != 'вакансия':
            Flag = True
            fio = Prepod.split(' ')
            if '.' in fio[1]:
                fio.append(fio[1].split('.')[1]+'.')
                fio[1] = fio[1].split('.')[0]+'.'
            while Flag:
                with sqlite3.connect('database.db') as conn:
                    try:
                        cursor = conn.execute('''SELECT * FROM [Prepods] WHERE Surname = ? and FirstName = ? and SecondName = ?''', (fio[0],fio[1],fio[2],))
                        row = cursor.fetchone()
                        if row:
                            Prepod = int(row[0])
                            Flag = False
                        else:
                            if not Database.AddPrepod(fio[0],fio[1],fio[2]):
                                return False
                    except:
                            try:
                                if not Database.AddPrepod(fio[0],fio[1],''):
                                    return False
                            except IndexError:
                                if not Database.AddPrepod(fio[0], '',''):
                                    return False
                                 
        with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT * FROM [Groups] WHERE NAME = ?''', (Group,))
                    row = cursor.fetchone()
                    if not row:
                        return False

        with sqlite3.connect('database.db') as conn:
                if Delete!=None:
                    conn.execute("INSERT INTO [Changes] (SubjectId, PrepodId, GroupId, Date, Number, Classroom, Comment, DeleteUrok) Values(?, ?, ?, ?, ?, ?, ?, ?)", (Subject, Prepod, Group, Date.strftime('%Y-%m-%d'), Number, Classroom, Comment,Delete,))
                else:
                    conn.execute("INSERT INTO [Changes] (SubjectId, PrepodId, GroupId, Date, Number, Classroom, Comment) Values(?, ?, ?, ?, ?, ?, ?)", (Subject, Prepod, Group, Date.strftime('%Y-%m-%d'), Number, Classroom, Comment,))
                

    def AddUrok(Subject, Prepod, Group:str, Date:datetime.date, Number:int, Classroom:str):
        if type(Subject) is str:
            Flag = True
            while Flag:
                with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT * FROM [Subjects] WHERE NAME = ?''', (Subject,))
                    row = cursor.fetchone()
                    if row:
                        Subject = int(row[0])
                        Flag = False
                    else:
                        if not Database.AddSubject(Subject):
                            return False
                        
        if type(Prepod) is str:
            Flag = True
            try:
                fio = Prepod.split(' ')
                if '.' in fio[1]:
                    fio.append(fio[1].split('.')[1]+'.')
                    fio[1] = fio[1].split('.')[0]+'.'
            
                while Flag:
                    with sqlite3.connect('database.db') as conn:
                        cursor = conn.execute('''SELECT * FROM [Prepods] WHERE Surname = ? and FirstName = ? and SecondName = ?''', (fio[0],fio[1],fio[2],))
                        row = cursor.fetchone()
                        if row:
                            Prepod = int(row[0])
                            Flag = False
                        else:
                            if not Database.AddPrepod(fio[0],fio[1],fio[2]):
                                return False
            except:
                 Database.AddPrepod(Prepod,'','')
        with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT * FROM [Groups] WHERE NAME = ?''', (Group,))
                    row = cursor.fetchone()
                    if not row:
                        if not Database.AddGroup(Group):
                            return False
        with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT * FROM [Uroki] WHERE SubjectId = ? AND PrepodId = ? AND GroupId= ? AND Date = ? AND Number = ? AND Classroom = ?''', (Subject, Prepod, Group, Date.strftime('%Y-%m-%d'), Number, Classroom,))
                    row = cursor.fetchone()
                    if row:
                         return False

        with sqlite3.connect('database.db') as conn:
                conn.execute("INSERT INTO [Uroki] (SubjectId, PrepodId, GroupId, Date, Number, Classroom) Values(?, ?, ?, ?, ?, ?)", (Subject, Prepod, Group, Date.strftime('%Y-%m-%d'), Number, Classroom,))
        return True
    def GetAllClassrooms():
         with sqlite3.connect('database.db') as conn:
                    cursor = conn.execute('''SELECT DISTINCT Classroom FROM [Uroki]''')
                    row = cursor.fetchall()
                    output = []
                    if row:
                        for i in row:
                             output.append(i[0])
                    return sorted(output)
         
    def DeleteChange(id:int):
        with sqlite3.connect('database.db') as conn:
            conn.execute('''DELETE FROM Changes WHERE id = ?''', (id,))

    def AddSubject(Name):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.execute('''SELECT * FROM [Subjects] WHERE NAME = ?''', (Name,))
            row = cursor.fetchone()
            if row:
                return False
        try:
            with sqlite3.connect('database.db') as conn:
                conn.execute("INSERT INTO [Subjects] (Name) Values(?)", (Name,))
            return True
        except sqlite3.IntegrityError:
            return False

    def AddPrepod(Surname:str, FirstName:str, SecondName:str):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.execute('''SELECT * FROM [Prepods] WHERE FirstName = ? AND SecondName = ? AND Surname = ?''', (FirstName, SecondName, Surname,))
            row = cursor.fetchone()
            if row:
                return False
        try:
            with sqlite3.connect('database.db') as conn:
                conn.execute("INSERT INTO Prepods (FirstName, SecondName, Surname) Values(?, ?, ?)", (FirstName, SecondName, Surname,))
            return True
        except sqlite3.IntegrityError:
            return False
        
    def AddGroup(Group:str):
        try:
            with sqlite3.connect('database.db') as conn:
                conn.execute("INSERT INTO Groups Values(?)", (Group,))
            return True
        except sqlite3.IntegrityError:
            return False

Database.StartDataBase()
#Database.AddUrok('Программирование', 'Ткачук В.А.', "ИСиП 21-11-2", datetime.datetime.now().date(), 1, '303')
#Database.AddUrok('Программирование', 'Ткачук В.А.', "ИСиП 21-11-3", datetime.datetime.now().date(), 1, '101')
#Database.AddUrok('Программирование', 'Ткачук В.А.', "ИСиП 21-11-3", datetime.datetime.now().date(), 2, '101')
#Database.AddChange('Программирование', 'Ткачук В.А.', "ИСиП 21-11-2", datetime.datetime.now().date(), 1, '202', 'Замена кабинета', 1)
#Database.AddChange('Программирование', 'Ткачук В.А.', "ИСиП 21-11-3", datetime.datetime.now().date(), 2, '202', 'Замена кабинета', 2)
#Database.AddSubject('Иностранный язык')
#Database.AddChange('Иностранный язык', 'Ткачук В.А.', "ИСиП 21-11-3", datetime.datetime.now().date(), 3, '203', 'Будет', None)
