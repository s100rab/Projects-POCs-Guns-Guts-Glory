-- 1st
create database alumni;

-- 2nd
-- right click on table and select table data import wizard

-- 3rd
-- 
use alumni;
desc college_a_hs;
--
use alumni;
desc college_a_se;
--
use alumni;
desc college_a_sj;
--
use alumni;
desc college_b_hs;
--
use alumni;
desc college_b_se;
--
use alumni;
desc college_b_sj;

-- 4th
-- answer in jupyter notebook file

-- 5th
-- file attached

-- 6th

create view College_A_HS_V as 
select RollNo,LastUpdate,Name,FatherName,MotherName,Batch,Degree,PresentStatus,HSDegree,EntranceExam,Institute,Location 
from  college_a_hs 
where 
RollNo is not null and 
LastUpdate is not null and
Name is not null and 
FatherName is not null and
MotherName is not null and
Batch is not null and
Degree is not null and
PresentStatus is not null and
HSDegree is not null and
EntranceExam is not null and
Institute is not null and
Location is not null;

select * from College_A_HS_V;

-- 7th

create view College_A_SE_V as
select RollNo
,LastUpdate
,Name
,FatherName
,MotherName
,Batch
,Degree
,PresentStatus
,Organization
,Location
from
college_a_se
where
RollNo is not null and
LastUpdate is not null and
Name is not null and
FatherName is not null and
MotherName is not null and
Batch is not null and
Degree is not null and
PresentStatus is not null and
Organization is not null and
Location is not null ;

select * from college_a_se_v;

-- 8th
create view College_A_SJ_V as select
RollNo,LastUpdate,Name,FatherName,MotherName,Batch,PresentStatus,Organization,Designation,Location
from 
college_a_sJ
where
RollNo is not null and
LastUpdate is not null and
Name is not null and
FatherName is not null and
MotherName is not null and
Batch is not null and
Degree is not null and
PresentStatus is not null and
Organization is not null and
Designation is not null and
Location is not null ;

select * from college_a_sj_v;


-- 9th
create view College_B_HS_V as
select RollNo,LastUpdate,
Name,
FatherName,
MotherName,
Branch,
Batch,
Degree,
PresentStatus,
HSDegree,
EntranceExam,
Institute,
Location
from college_b_hs
where 
RollNo is not null and
LastUpdate is not null and
Name is not null and
FatherName is not null and
MotherName is not null and
Branch is not null and
Batch is not null and
Degree is not null and
PresentStatus is not null and
HSDegree is not null and
EntranceExam is not null and
Institute is not null and
Location is not null ;

select * from College_B_HS_V;
-- 10th
create view College_B_SE_V as
select 
RollNo,
LastUpdate,
Name,
FatherName,
MotherName,
Branch,
Batch,
Degree,
PresentStatus,
Organization,
Location
from college_b_se
where
RollNo is not null and
LastUpdate is not null and
Name is not null and
FatherName is not null and
MotherName is not null and
Branch is not null and
Batch is not null and
Degree is not null and
PresentStatus is not null and
Organization is not null and
Location is not null;

select * from College_B_SE_V ;

-- 11th
create view College_B_SJ_V as
select
RollNo,
LastUpdate,
Name,
FatherName,
MotherName,
Branch,
Batch,
Degree,
PresentStatus,
Organization,
Designation,
Location
from college_b_sj
where
RollNo is not null and
LastUpdate is not null and
Name is not null and
FatherName is not null and
MotherName is not null and
Branch is not null and
Batch is not null and
Degree is not null and
PresentStatus is not null and
Organization is not null and
Designation is not null and
Location is not null;

select * from College_B_SJ_V;

-- 12th 
SELECT LOWER(Name),LOWER(FatherName),LOWER(MotherName) FROM College_a_hs_v;
SELECT LOWER(Name),LOWER(FatherName),LOWER(MotherName) FROM College_a_se_v;
SELECT LOWER(Name),LOWER(FatherName),LOWER(MotherName) FROM College_a_sj_v;
SELECT LOWER(Name),LOWER(FatherName),LOWER(MotherName) FROM College_b_hs_v;
SELECT LOWER(Name),LOWER(FatherName),LOWER(MotherName) FROM College_b_se_v;
SELECT LOWER(Name),LOWER(FatherName),LOWER(MotherName) FROM College_b_sj_v;

-- 13th
-- screenshots attached 13.1 to 13.6

-- 14th

DROP PROCEDURE get_name_collegeA
DELIMITER $$
CREATE PROCEDURE get_name_collegeA 
(
         INOUT name1 TEXT(40000)
)
BEGIN 
    DECLARE na INT DEFAULT 0;
    DECLARE namelist VARCHAR(16000) DEFAULT "";
    
    DECLARE namedetail 
           CURSOR FOR
				SELECT Name FROM college_a_hs UNION SELECT Name FROM college_a_se UNION SELECT Name FROM college_a_sj;
                
	DECLARE CONTINUE HANDLER 
            FOR NOT FOUND SET na =1;
            
	OPEN namedetail;
    
    getame :
         LOOP
         FETCH FROM namedetail INTO namelist;
         IF na = 1 THEN
              LEAVE getame;
		END IF;
        SET name1 = CONCAT(namelist,";",name1);
        
        END LOOP getame;
        CLOSE namedetail;
END $$
DELIMITER ;

SET @Name = "";
CALL get_name_collegeA(@Name);
SELECT @Name Name;

-- 15th
DROP PROCEDURE get_name_collegeB
DELIMITER $$
CREATE PROCEDURE get_name_collegeB 
(
         INOUT name1 TEXT(40000)
)
BEGIN 
    DECLARE na INT DEFAULT 0;
    DECLARE namelist VARCHAR(16000) DEFAULT "";
    
    DECLARE namedetail 
           CURSOR FOR
				SELECT Name FROM college_b_hs UNION SELECT Name FROM college_b_se UNION SELECT Name FROM college_b_sj;
                
	DECLARE CONTINUE HANDLER 
            FOR NOT FOUND SET na =1;
            
	OPEN namedetail;
    
    getame :
         LOOP
         FETCH FROM namedetail INTO namelist;
         IF na = 1 THEN
              LEAVE getame;
		END IF;
        SET name1 = CONCAT(namelist,";",name1);
        
        END LOOP getame;
        CLOSE namedetail;
END $$
DELIMITER ;

SET @Name = "";
CALL get_name_collegeB(@Name);
SELECT @Name Name;

-- 16th
-- please provide answer in remarks 