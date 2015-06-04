-- RETAILMENOT Data.

CREATE TABLE IF NOT EXISTS RETAILMENOT (
  UID            TINYBLOB          NOT NULL,
  Timestamp      BIGINT UNSIGNED   NOT NULL,
  Site           TINYBLOB          NOT NULL,
  OfferType      TINYBLOB,
  OfferDesc      TINYBLOB,
  UsedToday      INT,

  PRIMARY KEY (UID(255), Site(255), Timestamp)
);
