BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "order" (
	"id"	INTEGER NOT NULL,
	"reference"	VARCHAR(5),
	"first_name"	VARCHAR(20),
	"last_name"	VARCHAR(20),
	"phone_number"	INTEGER,
	"email"	VARCHAR(50),
	"address"	VARCHAR(100),
	"city"	VARCHAR(100),
	"status"	VARCHAR(10),
	"payment_type"	VARCHAR(10),
	"payment_method"	VARCHAR(10),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "product" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(50),
	"price"	INTEGER,
	"stock"	INTEGER,
	"description"	VARCHAR(500),
	"image"	VARCHAR(100),
	"manu_name"	TEXT,
	"type"	TEXT,
	PRIMARY KEY("id"),
	UNIQUE("name")
);
CREATE TABLE IF NOT EXISTS "sales" (
	"id"	INTEGER,
	"pName"	TEXT,
	"unit_sales"	INTEGER,
	"unit_price"	INTEGER,
	"total_price"	INTEGER,
	"store_region"	TEXT,
	"date"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "customers" (
	"id"	INTEGER,
	"cust_name"	TEXT,
	"username"	TEXT,
	"email"	TEXT,
	"password"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "contract_customers" (
	"id"	INTEGER,
	"username"	TEXT,
	"account_number"	TEXT,
	"billing_date"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "infrequent_customers" (
	"id"	INTEGER,
	"username"	TEXT,
	"card_info"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "warehouses" (
	"id"	INTEGER,
	"pName"	TEXT,
	"stock"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "stores" (
	"id"	INTEGER,
	"store_region"	TEXT,
	"pName"	TEXT,
	"stock"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "reorders" (
	"id"	INTEGER,
	"pName"	TEXT,
	"quantity"	INTEGER,
	"manu_name"	TEXT,
	"date"	TEXT,
	"status"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "manufacturers" (
	"id"	INTEGER,
	"manu_name"	TEXT,
	"pName"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "order" VALUES (1,'EBACA','Anne','Nasimiyu',254745993511,'makhanuanne@gmail.com','26560','Nairobi','PENDING','Card',NULL);
INSERT INTO "product" VALUES (5,'Hp Pavillion',97000,20,'14T-15 1035G7 10th GEN 10GB','http://127.0.0.1:5000/_uploads/photos/Hp-pavilion.jpg','HP','Laptops');
INSERT INTO "product" VALUES (6,'Nokia 7.2',25500,0,'IPS LCD, HDR10 1080 x 2280 pixels 64GB 4GB RAM','http://127.0.0.1:5000/_uploads/photos/Nokia-7.2_2.png','Nokia','Phones');
INSERT INTO "product" VALUES (7,'iPhone-12-Pro-Max',135999,30,' 6.7 inches, 1284 x 2778 pixels RAM: 6GB Storage: 256GB','http://127.0.0.1:5000/_uploads/photos/iPhone-12-Pro-Max-256GB_1.jpg','Apple','Phones');
INSERT INTO "product" VALUES (8,'Canon-ixus',13000,2,'185 20MP Digital Camera 1803C001AA Black','http://127.0.0.1:5000/_uploads/photos/canon-ixus.jpg','Canon','Cameras');
COMMIT;
