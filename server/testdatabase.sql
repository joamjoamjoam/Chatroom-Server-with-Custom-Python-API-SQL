


CREATE TABLE "friendlist" (
  "listid" SERIAL PRIMARY KEY
);

CREATE TABLE "usr" (
  "login" TEXT PRIMARY KEY,
  "passwd" TEXT NOT NULL,
  "bio" TEXT NOT NULL,
  "age" INTEGER,
  "listid" INTEGER NOT NULL
);

CREATE INDEX "idx_usr__listid" ON "Usr" ("listid");

ALTER TABLE "usr" ADD CONSTRAINT "fk_usr__listid" FOREIGN KEY ("listid") REFERENCES "friendlist" ("listid");

CREATE TABLE "chat" (
  "chatid" SERIAL PRIMARY KEY,
  "senderlogin" TEXT NOT NULL
);

CREATE INDEX "idx_chat__senderlogin" ON "chat" ("senderlogin");

ALTER TABLE "chat" ADD CONSTRAINT "fk_chat__senderlogin" FOREIGN KEY ("senderlogin") REFERENCES "Usr" ("login");

CREATE TABLE "message" (
  "msgid" SERIAL PRIMARY KEY,
  "senderlogin" TEXT NOT NULL,
  "chatid" INTEGER NOT NULL
);

CREATE INDEX "idx_message__chatid" ON "message" ("chatid");

CREATE INDEX "idx_message__senderlogin" ON "message" ("senderlogin");

ALTER TABLE "message" ADD CONSTRAINT "fk_message__chatid" FOREIGN KEY ("chatid") REFERENCES "chat" ("chatid");

ALTER TABLE "message" ADD CONSTRAINT "fk_message__senderlogin" FOREIGN KEY ("senderlogin") REFERENCES "Usr" ("login")
