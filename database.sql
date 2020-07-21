create database TODO;

create table agents(agentid varchar(100) PRIMARY KEY, agentpw varchar(150));

create table list(title varchar(100), description varchar(100), category varchar(100), due date, agentis varchar(100), CONSTRAINT fk FOREIGN KEY(agentid) REFERENCES agents(agentid));
