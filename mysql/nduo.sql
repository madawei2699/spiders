-- FB Likes Data.

CREATE TABLE IF NOT EXISTS NDUO (
  UID            TINYBLOB          NOT NULL,
  Timestamp      BIGINT UNSIGNED   NOT NULL,
  Downloads      INT,

  PRIMARY KEY (UID(255), Timestamp)
);
