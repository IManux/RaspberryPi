USE test_db;

CREATE TABLE IF NOT EXISTS test_log_param(
    id BIGINT NOT NULL AUTO_INCREMENT,
	var1 INT NOT NULL,
	var2 INT NOT NULL,
	var3 FLOAT NOT NULL,
	var4 FLOAT NOT NULL,
	uploaded INT NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
)  ENGINE=INNODB;
