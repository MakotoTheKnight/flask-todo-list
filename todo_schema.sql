PRAGMA foreign_keys = ON;
CREATE TABLE entry
(
  id        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  text      TEXT                NOT NULL,
  completed INTEGER DEFAULT 0 NOT NULL
);
CREATE TABLE list
(
  id      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name    TEXT                NOT NULL,
  entries INTEGER,
  FOREIGN KEY (entries) REFERENCES entry(id)
);
CREATE TABLE list_entry
(
  list_id  INTEGER NOT NULL,
  entry_id INTEGER NOT NULL,
  PRIMARY KEY (list_id, entry_id),
  FOREIGN KEY (list_id) REFERENCES list(id),
  FOREIGN KEY (entry_id) REFERENCES entry(id)
);
