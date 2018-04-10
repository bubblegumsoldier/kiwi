
Create database collab_recommender;
Use collab_recommender;

Create Table users(
    uname VARCHAR(100) NOT NULL PRIMARY KEY
);

Create Table products(
     post_id VARCHAR(50) NOT NULL PRIMARY KEY
); 

Create Table votes(
    user VARCHAR(100) NOT NULL, 
    product VARCHAR(50) NOT NULL,
    vote TINYINT,
    vote_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user, product),
    FOREIGN KEY (user) REFERENCES users(uname),
    FOREIGN KEY (product) REFERENCES products(post_id)
);

Create USER 'collab'@'%' identified by '12345';
Grant Select, Insert ON collab_recommender.* to 'collab'@'%';






