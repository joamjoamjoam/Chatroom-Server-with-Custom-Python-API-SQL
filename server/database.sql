DROP TABLE usr CASCADE;
DROP TABLE usrlist CASCADE;
DROP TABLE usrlist_contains CASCADE;
DROP TABLE message CASCADE;
DROP TABLE chat CASCADE;
DROP TABLE chatlist CASCADE;

CREATE TABLE usrlist(
        list_id serial,
        owner text,
        PRIMARY KEY(list_id));

CREATE TABLE usr(
	login text,
	password text,
	bio text,
	friendslist integer,
	PRIMARY KEY (login),
	FOREIGN KEY(friendslist) REFERENCES usrlist(list_id));


CREATE TABLE usrlist_contains(
	list_id integer,
	member text,
	PRIMARY KEY(list_id, member),
	FOREIGN KEY(list_id) REFERENCES usrlist(list_id) ON DELETE CASCADE,
	FOREIGN KEY(member) REFERENCES usr(login) ON DELETE CASCADE);


CREATE TABLE chat(
	chatroom_name text,
	initialsender text,
	PRIMARY KEY(chatroom_name),
	FOREIGN KEY(initialsender) REFERENCES usr(login));

CREATE TABLE message(
	msg_id serial,
	msg_text text NOT NULL,
	msg_ts timestamp NOT NULL,
	sender text,
	chatroom_name text,
	PRIMARY KEY(msg_id),
	FOREIGN KEY(sender) REFERENCES usr(login),
	FOREIGN KEY(chatroom_name) REFERENCES chat(chatroom_name));

CREATE TABLE chatlist(
        chatroom_name text,
        member text,
        PRIMARY KEY(chatroom_name,member),
        FOREIGN KEY(chatroom_name) REFERENCES chat(chatroom_name),
        FOREIGN KEY(member) REFERENCES usr(login));

ALTER SEQUENCE message_msg_id_seq RESTART 1;
ALTER SEQUENCE usrlist_list_id_seq RESTART 1;
