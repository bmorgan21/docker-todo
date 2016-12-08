CREATE TABLE role (
    user_id INT(11) NOT NULL,
    name VARCHAR(16) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
    id INT(11) AUTO_INCREMENT NOT NULL,
    INDEX user_id (user_id),
    PRIMARY KEY (id)
) ENGINE=InnoDB COLLATE=latin1_swedish_ci;
CREATE TABLE todo (
    name TEXT CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
    is_complete TINYINT(1) NOT NULL DEFAULT 0,
    user_id INT(11) NOT NULL,
    id INT(11) AUTO_INCREMENT NOT NULL,
    INDEX user_id (user_id),
    PRIMARY KEY (id)
) ENGINE=InnoDB COLLATE=latin1_swedish_ci;
CREATE TABLE `user` (
    first_name VARCHAR(16) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
    last_name VARCHAR(16) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
    email VARCHAR(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
    password TEXT CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
    temp_password TEXT CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
    password_expires DATETIME NULL DEFAULT NULL,
    tick INT(11) NOT NULL DEFAULT 1,
    verified TINYINT(1) NOT NULL DEFAULT 0,
    verified_at DATETIME NULL DEFAULT NULL,
    id INT(11) AUTO_INCREMENT NOT NULL,
    CONSTRAINT email UNIQUE KEY(email),
    PRIMARY KEY (id)
) ENGINE=InnoDB COLLATE=latin1_swedish_ci;
ALTER TABLE role ADD CONSTRAINT role_ibfk_1 FOREIGN KEY (user_id) REFERENCES user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE todo ADD CONSTRAINT todo_ibfk_1 FOREIGN KEY (user_id) REFERENCES user (id) ON UPDATE NO ACTION ON DELETE NO ACTION;

CREATE TABLE `property` (
  `name` varchar(16) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO property (name, value) VALUES ('schema_version', '738ceb5ed5326373be16c7ff828cd638')
  ON DUPLICATE KEY UPDATE value='738ceb5ed5326373be16c7ff828cd638';
