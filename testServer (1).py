from twisted.internet import protocol, reactor
import sqlite3
from datetime import datetime

conn= sqlite3.connect("vending_machine")
curs = conn.cursor()
transports = set()
class Chat(protocol.Protocol):
    def connectionMade(self):
        transports.add(self.transport)
        
    def dataReceived(self, data):
        global conn
        global curs
        d=data.decode()
        if 'c' in d:
             print(str(self.transport.getPeer())+"에서 coke 팔림")
             curs.execute("SELECT Remains,Sales FROM VM WHERE Name='coke';")
             row = curs.fetchone() 
             curs.execute("UPDATE VM SET Remains="+str(int(row[0])-1)+",Sales="+str(int(row[1])+1)+" WHERE Name='coke';")
             now = datetime.now()
             dt=str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)+str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)
             curs.execute("insert into log values(000001,"+dt+")")
             conn.commit()
             
        elif 'p' in d:
             print(str(self.transport.getPeer())+"에서 pepsi 팔림")
             curs.execute("SELECT Remains,Sales FROM VM WHERE Name='pepsi';")
             row = curs.fetchone() 
             curs.execute("UPDATE VM SET Remains="+str(int(row[0])-1)+",Sales="+str(int(row[1])+1)+" WHERE Name='pepsi';")
             now = datetime.now()
             dt=str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)+str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)
             curs.execute("insert into log values(000002,"+dt+")")
             conn.commit()
 
        elif 's' in d:
             print(str(self.transport.getPeer())+"에서 sprite 팔림")
             curs.execute("SELECT Remains,Sales FROM VM WHERE Name='sprite';")
             row = curs.fetchone() 
             curs.execute("UPDATE VM SET Remains="+str(int(row[0])-1)+",Sales="+str(int(row[1])+1)+" WHERE Name='sprite';")
             now = datetime.now()
             dt=str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)+str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)
             curs.execute("insert into log values(000003,"+dt+")")
             conn.commit()
        elif 'a' in d:
             print(str(self.transport.getPeer())+"에 누적 판매량 전송")
             curs.execute("SELECT COUNT(CASE WHEN ID=1 THEN '' END) ,COUNT(CASE WHEN ID=2 THEN '' END) ,COUNT(CASE WHEN ID=3 THEN '' END) FROM log;")
             rows = curs.fetchall()
             temp=""
             for i in range(len(rows)):
                 for j in range(len(rows[i])):
                     temp+=str(rows[i][j])
                     if j!=len(rows[i])-1: temp+=" "
                 if i!=len(rows)-1: temp+="/"
             temp+="^"
             self.transport.write(temp.encode('utf-8'))
        elif 'm' in d:
             print(str(self.transport.getPeer())+"에 "+d[-2:]+"월 판매량 전송")
             now = datetime.now()
             curs.execute("SELECT COUNT(CASE WHEN ID=1 THEN ' ' END) ,COUNT(CASE WHEN ID=2 THEN ' ' END) , COUNT(CASE WHEN ID=3 THEN ' ' END) FROM log WHERE DATE LIKE '"+str(now.year)+d[-2:]+"%';")
             rows = curs.fetchall()
             temp=""
             for i in range(len(rows)):
                 for j in range(len(rows[i])):
                     temp+=str(rows[i][j])
                     if j!=len(rows[i])-1: temp+=" "
                 if i!=len(rows)-1: temp+="/"
             temp+="^"
             self.transport.write(temp.encode('utf-8'))
        elif 't' in d:
             print(str(self.transport.getPeer())+"에 오늘 판매량 전송")
             now = datetime.now()
             dt=str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)
             curs.execute("SELECT COUNT(CASE WHEN ID=1 THEN ' ' END) ,COUNT(CASE WHEN ID=2 THEN ' ' END) , COUNT(CASE WHEN ID=3 THEN ' ' END) FROM log WHERE DATE LIKE '"+dt+"%';")
             rows = curs.fetchall()
             temp=""
             for i in range(len(rows)):
                 for j in range(len(rows[i])):
                     temp+=str(rows[i][j])
                     if j!=len(rows[i])-1: temp+=" "
                 if i!=len(rows)-1: temp+="/"
             temp+="^"
             self.transport.write(temp.encode('utf-8'))
        elif 'd' in d:
             print(str(self.transport.getPeer())+"에 재고, 판매량 전송")
             curs.execute("SELECT Name,Remains,Sales FROM VM;")
             rows = curs.fetchall()
             temp=""
             for i in range(len(rows)):
                 for j in range(len(rows[i])):
                     temp+=rows[i][j]
                     if j!=len(rows[i])-1: temp+=" "
                 if i!=len(rows)-1: temp+="/"
             temp+="^"
             self.transport.write(temp.encode('utf-8'))
class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()

print('Server started!')
reactor.listenTCP(8100, ChatFactory())
reactor.run()
print('Server End')
curs.close()
conn.close()
