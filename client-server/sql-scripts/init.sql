CREATE TABLE Room(
    id INT AUTO_INCREMENT PRIMARY KEY,
    roomName VARCHAR(255)
);

CREATE TABLE NickName(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nickName VARCHAR(255)
);

CREATE TABLE Interaction(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nickNameId INT,
    roomId INT,
    idemKey VARCHAR(255),
    messageInteraction VARCHAR(255),
    timestamp_client VARCHAR(255),
    FOREIGN KEY (nickNameId) REFERENCES NickName(id),
    FOREIGN KEY (roomId) REFERENCES Room(id)
);