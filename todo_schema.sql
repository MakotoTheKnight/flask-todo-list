PRAGMA foreign_keys = ON;
CREATE TABLE entry
(
  id        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  text      TEXT                              NOT NULL,
  completed BOOLEAN DEFAULT 0 NOT NULL,
  list_id   INTEGER,
  FOREIGN KEY (list_id) REFERENCES list (id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE list
(
  id   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name TEXT                              NOT NULL UNIQUE
);
CREATE TABLE list_entry
(
  list_id  INTEGER NOT NULL,
  entry_id INTEGER NOT NULL,
  PRIMARY KEY (list_id, entry_id),
  FOREIGN KEY (list_id) REFERENCES list (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (entry_id) REFERENCES entry (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_list_name ON list (name);

CREATE TRIGGER join_table_integrity
AFTER INSERT ON entry
FOR EACH ROW
BEGIN
  INSERT INTO list_entry (list_id, entry_id) VALUES (new.list_id, new.id);
END;