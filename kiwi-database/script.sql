Create database content_recommender;
Use content_recommender;

Create Table users(
    uname VARCHAR(100) NOT NULL PRIMARY KEY
);

Create Table products(
    post_id VARCHAR(50) NOT NULL PRIMARY KEY,
    tags VARCHAR(1000) NOT NULL    
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

Create database random_recommender;
Use random_recommender;

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

Create database knn_recommender;
Use knn_recommender;

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

Create database svd_recommender;
Use svd_recommender;

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


Create USER 'svd'@'%' identified by '12345';
Grant Select, Insert ON svd_recommender.* to 'svd'@'%';
Create USER 'content'@'%' identified by '12345';
Grant Select, Insert ON content_recommender.* to 'content'@'%';
Create USER 'random'@'%' identified by '12345';
Grant Select, Insert ON random_recommender.* to 'random'@'%';
Create USER 'knn'@'%' identified by '12345';
Grant Select, Insert ON knn_recommender.* to 'knn'@'%';




