CREATE TABLE  IF NOT EXISTS  category(
    category_id int GENERATED ALWAYS AS IDENTITY,
    category_name varchar(100) NOT NULL,
    CONSTRAINT cat_key PRIMARY KEY (category_id),
    CONSTRAINT catna_uniq UNIQUE (category_name)
);

CREATE TABLE  IF NOT EXISTS apps(

    app_id bigint GENERATED ALWAYS AS IDENTITY,
    app_name varchar(1000) NOT NULL,
    rating float,
    price float NOT NULL,
    category_id int NOT NULL,
    size bigint NOT NULL,
    num_lang bigint NOT NULL,
    licensed int NOT NULL,
    app_desc varchar(10000),
    cont_rating varchar(10) NOT NULL,
    CONSTRAINT cooat_key PRIMARY KEY (app_id),
    CONSTRAINT catin_key FOREIGN KEY (category_id) REFERENCES category (category_id)
);

CREATE TABLE  IF NOT EXISTS users(
    user_id bigint GENERATED ALWAYS AS IDENTITY,
    user_name varchar(100) NOT NULL,
    email varchar(100) NOT NULL,
    password varchar(100) NOT NULL,
    CONSTRAINT catww_key PRIMARY KEY (user_id),
    CONSTRAINT email_uniq UNIQUE (email),
    CONSTRAINT user_uniq UNIQUE (user_name),
    CONSTRAINT check_min CHECK((length((password)::text) >= 10))
);

CREATE TABLE  IF NOT EXISTS developers(
    developer_id bigint GENERATED ALWAYS AS IDENTITY,
    developer_name varchar(100) NOT NULL,
    email varchar(100) NOT NULL,
    password varchar(100) NOT NULL,
    CONSTRAINT casst_key PRIMARY KEY (developer_id),
    CONSTRAINT emal_uniq UNIQUE (email),
    CONSTRAINT dev_uniq UNIQUE (developer_name),
    CONSTRAINT chek_min CHECK((length((password)::text) >= 10))
);

CREATE TABLE IF NOT EXISTS installs (
    user_id bigint NOT NULL,
    app_id bigint NOT NULL,
    CONSTRAINT userin_key FOREIGN KEY (user_id) REFERENCES users (user_id)
    ON DELETE CASCADE,
    CONSTRAINT appin_key FOREIGN KEY (app_id) REFERENCES apps (app_id)
    ON DELETE CASCADE
);

CREATE TABLE  IF NOT EXISTS developed(
    developer_id bigint NOT NULL,
    app_id bigint NOT NULL,
    CONSTRAINT devin_key FOREIGN KEY (developer_id) REFERENCES developers (developer_id)
    ON DELETE CASCADE,
    CONSTRAINT appappin_key FOREIGN KEY (app_id) REFERENCES apps (app_id)
    ON DELETE CASCADE
);

CREATE TABLE  IF NOT EXISTS reviews(
    app_id bigint NOT NULL,
    user_id bigint NOT NULL,
    review varchar(100) NOT NULL,
    CONSTRAINT uswerin_key FOREIGN KEY (user_id) REFERENCES users (user_id)
    ON DELETE CASCADE,
    CONSTRAINT appwin_key FOREIGN KEY (app_id) REFERENCES apps (app_id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS  search_history (
    search_id bigint GENERATED ALWAYS AS IDENTITY,
    user_id bigint NOT NULL,
    search varchar(1000) NOT NULL,
    CONSTRAINT cer_key PRIMARY KEY (search_id),
    CONSTRAINT uswersin_key FOREIGN KEY (user_id) REFERENCES users (user_id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS  apps_store(
    app_id bigint NOT NULL,
    app_name varchar(1000) NOT NULL,
    price float NOT NULL,
    rating float,
    ver_rating float,
    ver varchar(100),
    cont_rating varchar(10) NOT NULL,
    category_name varchar(100) NOT NULL,
    num_lang bigint NOT NULL,
    licensed int NOT NULL,
    size1 float NOT NULL,
    size bigint NOT NULL
    
);

CREATE TABLE  IF NOT EXISTS app_description(
    app_name varchar(1000) NOT NULL,
    app_desc varchar(10000) NOT NULL
)




