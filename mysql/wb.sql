-- FB Likes Data.

CREATE TABLE IF NOT EXISTS WB (
  UID            TINYBLOB          NOT NULL,
  Timestamp      BIGINT UNSIGNED   NOT NULL,
  Following      INT,
  Followers      INT,

  PRIMARY KEY (UID(255), Timestamp)
);
