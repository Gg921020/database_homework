CREATE TABLE Student (
    Student_ID VARCHAR(255) PRIMARY KEY,
    Department VARCHAR(255),
    Grade INT,
    Class INT,
    Credit_Selected INT
);

insert into Student(Student_ID,Department,Grade,Class,Credit_Selected) values("D1149887","IECS",2,2,20);
insert into Student(Student_ID,Department,Grade,Class,Credit_Selected) values("D1149828","IECS",3,1,17);
insert into Student(Student_ID,Department,Grade,Class,Credit_Selected) values("D1149852","IECS",2,1,8);
insert into Student(Student_ID,Department,Grade,Class,Credit_Selected) values("D1149788","IECS",1,2,13);
insert into Student(Student_ID,Department,Grade,Class,Credit_Selected) values("D1148784","EE",1,2,13);
insert into Student(Student_ID,Department,Grade,Class,Credit_Selected) values("D1148783","EE",1,2,28);




CREATE TABLE Course (
    Course_ID INT PRIMARY KEY,
    Course_Name VARCHAR(255),
    Department VARCHAR(255),
    Credit INT,
    Timebegin VARCHAR(255),
    Timeend VARCHAR(255),
    Max_Capacity INT,
    Enrolled_Students INT,
    Mandatory BOOL,
    Grade INT -- 新增的欄位，表示課程開設的年級
);

insert into Course(Course_ID,Course_Name,Department,Credit,Timebegin,Timeend,Max_Capacity,Enrolled_Students,Mandatory,Grade) values(1223,"System Programing","IECS",3,"3-4","3-6",10,0,TRUE,3);
insert into Course(Course_ID,Course_Name,Department,Credit,Timebegin,Timeend,Max_Capacity,Enrolled_Students,Mandatory,Grade) values(1222,"OOP","IECS",3,"1-1","1-3",10,4,FALSE,2);
insert into Course(Course_ID,Course_Name,Department,Credit,Timebegin,Timeend,Max_Capacity,Enrolled_Students,Mandatory,Grade) values(1250,"Program Design","IECS",3,"4-5","4-7",15,13,TRUE,2);
insert into Course(Course_ID,Course_Name,Department,Credit,Timebegin,Timeend,Max_Capacity,Enrolled_Students,Mandatory,Grade) values(1249,"Program Design","IECS",3,"3-2","3-4",15,8,TRUE,1);
insert into Course(Course_ID,Course_Name,Department,Credit,Timebegin,Timeend,Max_Capacity,Enrolled_Students,Mandatory,Grade) values(1344,"Digital Design","EE",3,"4-1","4-3",15,10,TRUE,1);
insert into Course(Course_ID,Course_Name,Department,Credit,Timebegin,Timeend,Max_Capacity,Enrolled_Students,Mandatory,Grade) values(1355,"Digital design lab","EE",3,"1-1","1-3",20,10,TRUE,1);




CREATE TABLE Enrollment (
    
    Student_ID VARCHAR(255),
    Course_ID INT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID),
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID)
);

