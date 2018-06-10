CREATE TABLE IF NOT EXISTS url (
    id          VARCHAR(50) NOT NULL PRIMARY KEY,
    hits        INTEGER,
    destination TEXT
);

CREATE TABLE IF NOT EXISTS url_tags (
    id  VARCHAR(50) NOT NULL,
    tag TEXT,
    FOREIGN KEY (id) REFERENCES url(id)
        ON DELETE CASCADE
);
