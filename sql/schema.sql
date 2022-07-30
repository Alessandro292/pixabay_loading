drop table if exists examples;

CREATE TABLE examples (
  id  MEDIUMINT NOT NULL AUTO_INCREMENT,
  name varchar(80) default null,
  animal varchar(80) default null,
  language varchar(80) default null,
  format varchar(80) default null,
  mode varchar(80) default null,
  frame int default null,
  height int default null,
  width int default null,
  animated varchar(80) default null,
  primary key (id)
);
