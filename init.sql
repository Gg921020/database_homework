CREATE TABLE Student (
    Student_ID VARCHAR(255) PRIMARY KEY,
    Department VARCHAR(255),
    Grade INT,
    Class INT,
    Credit_Selected INT
);

insert into Student(Student_ID,Department,Grade,Class,Credit_Selected) values("D1149887","IECS",2,2,20);
insert into Student(Student_ID,Department,Grade,Class,Credit_Selected) values("D1149828","IECS",2,1,17);
insert into Student(Student_ID,Department,Grade,Class,Credit_Selected) values("D1149852","IECS",2,1,11);



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

insert into Course(Course_ID,Course_Name,Department,Credit,Timebegin,Timeend,Max_Capacity,Enrolled_Students,Mandatory,Grade) values(1223,"System Programing","IECS",3,"3-4","3-6",10,0,TRUE,2);
insert into Course(Course_ID,Course_Name,Department,Credit,Timebegin,Timeend,Max_Capacity,Enrolled_Students,Mandatory,Grade) values(1222,"OOP","IECS",3,"1-1","1-3",10,10,FALSE,2);
insert into Course(Course_ID,Course_Name,Department,Credit,Timebegin,Timeend,Max_Capacity,Enrolled_Students,Mandatory,Grade) values(1250,"Program Design","IECS",3,"4-5","4-7",15,14,TRUE,2);


CREATE TABLE Schedule (
    Student_ID INT,
    Course_ID INT,
    Day VARCHAR(10),
    Start_Time TIME,
    End_Time TIME,
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID)
);


CREATE TABLE Enrollment (
    Enrollment_ID INT AUTO_INCREMENT PRIMARY KEY,
    Student_ID VARCHAR(255),
    Course_ID INT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID),
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID)
);

