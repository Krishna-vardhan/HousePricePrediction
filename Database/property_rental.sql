create database property_rental;
use property_rental;
drop database property_rental;

create table admin(
admin_id int auto_increment primary key,
username varchar(223) not null ,
password varchar(223) not null
);

create table owners(
owner_id int auto_increment primary key,
name varchar(223)  not null,
email varchar(233) not null unique,
phone varchar(223) not null unique,
password varchar(223) not null,
address varchar(223) not null,
status varchar(223) not null default('unauthorized')
); 

create table users(
user_id int auto_increment primary key,
name varchar(223)  not null,
email varchar(233) not null unique,
phone varchar(223) not null unique,
password varchar(223) not null,
address varchar(223) not null
);


create table sale_properties(
sale_property_id int auto_increment primary key,
property_title varchar(223) not null,
property_value varchar(223) not null,
number_of_bedrooms int not null,
number_of_bathrooms int not null,
area_in_sqft varchar(223) not null,
address varchar(223) not null,
price_per_sqrt varchar(223) not null,
build_year varchar(223) not null,
parking_space varchar(223) not null,
residency_type varchar(223) not null,
status varchar(223) not null default('posted for sale'),
owner_id int,
summary text,
foreign key (owner_id) references owners(owner_id)
);
alter table sale_properties add city varchar(223) not null;



create table sale_property_pictures(
sale_property_picture_id int auto_increment primary key,
sale_property_id int ,
pictures varchar(223) not null
);


create table rental_properties(
rental_property_id int auto_increment primary key,
property_title varchar(223) not null,
property_value varchar(223) not null,
property_type varchar(223) not null,
number_of_bedrooms int not null,
number_of_bathrooms int not null,
area_in_sqft varchar(223) not null,
address varchar(223) not null,
security_deposit varchar(223) not null,
status varchar(223) not null default('posted for rental'),
owner_id int,
summary text,
foreign key (owner_id) references owners(owner_id)
);
alter table rental_properties add city varchar(223) not null;


create table rental_property_pictures(
rental_property_picture_id int auto_increment primary key,
rental_property_id int ,
pictures varchar(223) not null
);

create table rental_property_request(
rental_property_request_id int auto_increment primary key,
summary text,
date varchar(225),
status varchar(225) not null default('Applied for Rental'),
user_id int,
rental_property_id int ,
foreign key (rental_property_id) references rental_properties(rental_property_id),
foreign key (user_id) references users(user_id)
);
ALTER TABLE rental_property_request
MODIFY status VARCHAR(225) NOT NULL DEFAULT 'Applied for Rental';

create table sale_property_request(
sale_property_request_id int auto_increment primary key,
summary text,
date varchar(225),
status varchar(225) not null default('Applied for sale'),
user_id int,
sale_property_id int ,
foreign key (sale_property_id) references sale_properties(sale_property_id),
foreign key (user_id) references users(user_id)
);


create table rental_values(
rental_value_id int auto_increment primary key,
region_name varchar(225) not null,
date varchar(223),
predicted_value varchar(223)
);

create table home_values(
home_value_id int auto_increment primary key,
region_name varchar(225) not null,
date varchar(223),
predicted_value varchar(223)
);







