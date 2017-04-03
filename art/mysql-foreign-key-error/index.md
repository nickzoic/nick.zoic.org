---
category: SQL
date: '2015-08-27'
layout: article
redirect_from: '/SQL/mysql-foreign-key-error/'
slug: 'mysql-foreign-key-error'
summary: |
    Accidentally putting a foreign key between an InnoDB table and a MyISAM
    table results in an error "Cannot add or update a child row: a foreign
    key constraint fails"
tags: 'SQL, mysql, django'
title: 'MySQL: Foreign Keys between InnoDB and MyISAM'
---

Accidentally putting a foreign key between an InnoDB table and a MyISAM
table results in a misleading error at insert time:

    Cannot add or update a child row:
    a foreign key constraint fails

Putting foreign keys between InnoDB and MyISAM should be disallowed at
schema-change time (the `create table` should fail) because MyISAM
doesn't support foreign keys. But it is allowed if foreign keys checks
are switched off:

    mysql> set foreign_key_checks=0;
    Query OK, 0 rows affected (0.00 sec)

    mysql> create table old_table (
        id int(11) primary key
    ) engine=MyISAM;
    Query OK, 0 rows affected (0.00 sec)

    mysql> create table new_table (
        id int(11) primary key,
        old_table_id int(11),
        foreign key (old_table_id) references old_table (id)
    ) engine=InnoDB;
    Query OK, 0 rows affected (0.02 sec)

    mysql> set foreign_key_checks=1;
    Query OK, 0 rows affected (0.00 sec)

There's no errors or warnings until you actually try to add data, when
the foreign key constraint suddenly rears its ugly head:

    mysql> insert into old_table values (1);
    Query OK, 1 row affected (0.01 sec)

    mysql> insert into new_table values(1,1);
    ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails
    (`foo`.`new_table`, CONSTRAINT `new_table_ibfk_1` FOREIGN KEY (`old_table_id`) REFERENCES `old_table` (`id`))

This may seem like a perverse set of circumstances, but a database table
which has been created on (say) MySQL 5.1 will default to MyISAM, and
this setting will stay through an upgrade to MySQL 5.6. Databse tables
created on MySQL 5.6 will default to InnoDB. If you then create new
tables with foreign keys to the old tables, they'll be in this exact
situation.

But why would you turn the foreign key checks off? Lots of schema
migration tools, including [Django
South](https://south.readthedocs.org/en/latest/) do exactly that. They
really shouldn't.

If foreign key constraints are on, MySQL produces a terse but
appropriate error message:

    mysql> create table new_table (
        id int(11) primary key,
        old_table_id int(11),
        foreign key (old_table_id) references old_table (id)
    ) engine=InnoDB;
    ERROR 1215 (HY000): Cannot add foreign key constraint

The good news? All you have to do is migrate the old tables across to
InnoDB and it'll start working as if by magic:

    mysql> alter table old_table engine=InnoDB;
    Query OK, 1 row affected (0.07 sec)
    Records: 1  Duplicates: 0  Warnings: 0

    mysql> insert into new_table values(1,1);
    Query OK, 1 row affected (0.01 sec)

And you can make sure that all your tables are created on InnoDB by
[setting the default storage
engine](https://dev.mysql.com/doc/refman/5.5/en/server-system-variables.html#sysvar_default_storage_engine).

In this case, it takes three different misfeatures to make this happen:

-   Django's MySQL engine should explicitly use InnoDB
-   South shouldn't turn foreign key constraints off unless it really
    has to
-   MySQL shouldn't allow you to create foreign keys between InnoDB and
    MyISAM tables even if foreign keys are turned off

UPDATE: I filed this as [MySQL bug
\#78255](https://bugs.mysql.com/bug.php?id=78255).

UPDATE2: The same problem exists in MariaDB:

    MariaDB [test]> create table old_table ( id int(11) primary key ) engine=MyISAM;

    MariaDB [test]> create table new_table (
    ->     id int(11) primary key,
    ->     old_table_id int(11),
    ->     foreign key (old_table_id) references old_table (id)
    -> ) engine=InnoDB;
    ERROR 1005 (HY000): Can't create table `test`.`new_table` (errno: 150 "Foreign key constraint is incorrectly formed")

    MariaDB [test]> set foreign_key_checks=0;
    Query OK, 0 rows affected (0.00 sec)

    MariaDB [test]> create table new_table (
    ->     id int(11) primary key,
    ->     old_table_id int(11),
    ->     foreign key (old_table_id) references old_table (id)
    -> ) engine=InnoDB;
    Query OK, 0 rows affected (0.02 sec)

    MariaDB [test]> set foreign_key_checks=1;
    Query OK, 0 rows affected (0.00 sec)

    MariaDB [test]> insert into old_table values (1);
    Query OK, 1 row affected (0.00 sec)

    MariaDB [test]> insert into new_table values (1,1);
    ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails (`test`.`new_table`, CONSTRAINT `new_table_ibfk_1` FOREIGN KEY (`old_table_id`) REFERENCES `old_table` (`id`))

... so I've filed it as
[MDEV-8697](https://mariadb.atlassian.net/browse/MDEV-8697) there too.
