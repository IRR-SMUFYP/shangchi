DROP Database IF EXISTS `imatch`;
Create DATABASE `imatch`;
USE `imatch`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `username` int NOT NULL,
  `password` varchar(100) NOT NULL,
  `usertype` varchar(20)  NOT NULL,
  PRIMARY KEY (`username`)
) ;

DROP TABLE IF EXISTS `faq`;
CREATE TABLE IF NOT EXISTS `faq` (
  `faqID` int NOT NULL AUTO_INCREMENT,
  `question` varchar(300) NOT NULL,
  `answer` text NOT NULL,
  `section` varchar(10) NOT NULL,
  PRIMARY KEY (`faqID`)
) ;

DROP TABLE IF EXISTS `categoryitem`;
CREATE TABLE IF NOT EXISTS `categoryitem` (
  `itemID` int NOT NULL AUTO_INCREMENT,
  `itemName` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `subCat` varchar(50) NOT NULL,
  PRIMARY KEY (`itemID`)
) ;

DROP TABLE IF EXISTS `donation`;
CREATE TABLE IF NOT EXISTS `donation` (
  `donationID` varchar(30) NOT NULL,
  `donorID` int NOT NULL,
  `itemID` int NOT NULL,
  `timeSubmitted` DATETIME NOT NULL,
  `itemStatus` varchar(50) NOT NULL,
  PRIMARY KEY (`donationID`),
  FOREIGN KEY (`itemID`) references categoryitem (`itemID`)
) ;

DROP TABLE IF EXISTS `wishlist`;
CREATE TABLE IF NOT EXISTS `wishlist` (
  `wishlistID` varchar(30) NOT NULL,
  `migrantID` int NOT NULL,
  `itemID` int NOT NULL,
  `timeSubmitted` datetime NOT NULL,
  `itemStatus` varchar(50) NOT NULL,
  PRIMARY KEY (`wishlistID`),
  FOREIGN KEY (`migrantID`) references user (`username`)
) ;

DROP TABLE IF EXISTS `request`;
CREATE TABLE IF NOT EXISTS `request` (
  `reqID` int NOT NULL AUTO_INCREMENT,
  `donationID` varchar(30) NOT NULL,
  `migrantID` int NOT NULL,
  `postalCode` varchar(6) NOT NULL,
  `timeSubmitted` datetime NOT NULL,
  PRIMARY KEY (`reqID`),
  FOREIGN KEY (`migrantID`) REFERENCES user (`username`),
  FOREIGN KEY (`donationID`) REFERENCES donation (`donationID`)
);

DROP TABLE IF EXISTS `formbuilder`;
CREATE TABLE IF NOT EXISTS `formbuilder` (
  `fieldID` int NOT NULL AUTO_INCREMENT,
  `formName` varchar(15) NOT NULL,
  `fieldName` varchar(50) NOT NULL,
  `fieldType` varchar(15) NOT NULL,
  `placeholder` varchar(50),
  `options` varchar(200),
  PRIMARY KEY (`fieldID`)
) ;

DROP TABLE IF EXISTS `formanswers`;
CREATE TABLE IF NOT EXISTS `formanswers` (
  `answerID` int NOT NULL AUTO_INCREMENT,
  `submissionID` varchar(30) NOT NULL,
  `formName` varchar(15) NOT NULL,
  `fieldID` int NOT NULL,
  `answer` varchar(50) NOT NULL,
  PRIMARY KEY (`answerID`),
  FOREIGN KEY (`fieldID`) references formbuilder (`fieldID`)
) ;

DROP TABLE IF EXISTS `matches`;
CREATE TABLE IF NOT EXISTS `matches` (
  `matchID` int NOT NULL AUTO_INCREMENT,
  `reqID` int NOT NULL,
  `migrantID` int NOT NULL,
  `donorID` int NOT NULL,
  `matchDate` datetime NOT NULL,
  PRIMARY KEY (`matchID`),
  FOREIGN KEY fk_1 (`reqID`) references request (`reqID`),
  FOREIGN KEY fk_2 (`migrantID`) references user (`username`) 
) ;

DROP TABLE IF EXISTS `delivery`;
CREATE TABLE IF NOT EXISTS `delivery` (
  `matchID` int NOT NULL,
  `status` varchar(50) NOT NULL,
  `driverID` int NOT NULL,
  PRIMARY KEY (`matchID`),
  FOREIGN KEY (`matchID`) references matches (`matchID`),
  FOREIGN KEY (`driverID`) references user (`username`)
) ;


-- INSERT values
INSERT INTO user (`username`, `password`, `usertype`) VALUES 
(93261073, '$2b$12$hPh2gudOwUvmBs18PBa.deDRGOLiiDXuSkCV5qkA056I/n97blTJG', 'master');


-- for faq
INSERT INTO faq (`question`, `answer`, `section`) VALUES ('How do I donate?', 'First, head over to the "Donate" page on the top of the screen. Then you would have to fill in several key information into the form regarding yourself, as well as the item you are intending to donate before submitting the donation to be displayed on the front page of the web application.', 'donor');
INSERT INTO faq (`question`, `answer`, `section`) VALUES ('What do I donate?', 'You can refer to the wishlist seen on the homepage to see what Migrant Workers are requesting for.', 'donor');
INSERT INTO faq (`question`, `answer`, `section`) VALUES ('Who do I contact if I need help changing certain values?', 'You can contact IRR at the following email itsrainingraincoats@gmail.com, and in the subject field, let us know your phone number so we can amend the details accordingly.', 'donor');
INSERT INTO faq (`question`, `answer`, `section`) VALUES ('How do I go about selecting items I wish to donate in the dropdown list?', 'As confusing as it may seem, we have got you covered. Head over to the item catalogue seen on the donation page and click on it. What you see there is how the categories and items are mapped. So for example, if you wish to donate a shirt, you would have to select "Clothes" (Category), "Tops" (Sub-Category) and finally "Shirt" (Item name) to indicate your interest to donate that particular item.', 'donor');
INSERT INTO faq (`question`, `answer`, `section`) VALUES ('How do I request for an item?', 'Log in using your phone number after registering for an account. Then on the homepage, click on the item you wish to request and fill in the details accordingly. After an item has been matched to you, you will be notified by our admins at IRR.', 'worker');
INSERT INTO faq (`question`, `answer`, `section`) VALUES ('How do I sign up as a Driver?', 'You can drop us an email at itsrainingraincoats@gmail.com and we will help you to create an account accordingly.', 'driver');


-- for formbuilder table
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('donation', 'Postal Code', 'number');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `options`) VALUES
('donation', 'Area', 'radio', 'North;South;East;West;Central');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('donation', 'Item Photo', 'file');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `placeholder`) VALUES
('donation', 'Item Description', 'text', 'Brief description of the item you are donating');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('donation', 'Quantity', 'number');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `options`) VALUES
('donation', 'Delivery Method', 'dropdown', 'Delivery required;Arranged by donor;Self Pickup');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('wishlist', 'Quantity', 'number');


-- for formanswers table
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'donation', '1', 510323);
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'donation', '2', 'East');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'donation', '3', 'toothbrush.png');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'donation', '4', 'can make teeth sparkle sparkle');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'donation', '5', '3');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'donation', '6', 'Arranged by donor');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('test', 'wishlist', '7', '1');

-- categoryitem table
INSERT INTO `categoryitem` (`itemname`, `category`, `subcat`) VALUES
('Mattress', 'Beddings', 'Beddings'),
('Pillow Cover', 'Beddings', 'Beddings'),
('Bedsheets', 'Beddings', 'Beddings'),
('Blanket', 'Beddings', 'Beddings'),
('Pillow', 'Beddings', 'Beddings'),
('Others', 'Beddings', 'Beddings'),
('Socks', 'Clothes', 'Accessories'),
('Belt', 'Clothes', 'Accessories'),
('Others', 'Clothes', 'Accessories'),
('Shorts', 'Clothes', 'Bottoms'),
('Pants', 'Clothes', 'Bottoms'),
('Lungi', 'Clothes', 'Bottoms'),
('Others', 'Clothes', 'Bottoms'),
('T-Shirt', 'Clothes', 'Tops'),
('Long Sleeve Shirt', 'Clothes', 'Tops'),
('Jersey', 'Clothes', 'Tops'),
('Others', 'Clothes', 'Tops'),
('Walking Shoes/Sport Shoes', 'Clothes', 'Shoes'),
('Safety Boots', 'Clothes', 'Shoes'),
('Slippers', 'Clothes', 'Shoes'),
('Others', 'Clothes', 'Shoes'),
('Headphones', 'Electronics', 'Audio'),
('Bluetooth Speaker', 'Electronics', 'Audio'),
('Others', 'Electronics', 'Audio'),
('Phone', 'Electronics', 'Devices'),
('Laptop', 'Electronics', 'Devices'),
('Camera', 'Electronics', 'Devices'),
('Tablet', 'Electronics', 'Devices'),
('Smartwatch', 'Electronics', 'Devices'),
('Others', 'Electronics', 'Devices'),
('TV', 'Electronics', 'TVs'),
('Others', 'Electronics', 'TVs'),
('Extension Cord', 'Electronics', 'Add-ons'),
('Charging Cord', 'Electronics', 'Add-ons'),
('Power Bank', 'Electronics', 'Add-ons'),
('Others', 'Electronics', 'Add-ons'),
('Coffee', 'Food', 'Drinks'),
('Tea', 'Food', 'Drinks'),
('Milo', 'Food', 'Drinks'),
('Milk', 'Food', 'Drinks'),
('Others', 'Food', 'Drinks'),
('Biscuits/Cookies', 'Food', 'Snacks'),
('Nuts', 'Food', 'Snacks'),
('Candy', 'Food', 'Snacks'),
('Chocolate', 'Food', 'Snacks'),
('Others', 'Food', 'Snacks'),
('Cakes', 'Food', 'Breads'),
('Bread', 'Food', 'Breads'),
('Others', 'Food', 'Breads'),
('Meat', 'Food', 'Cooking Ingredients'),
('Vegetables', 'Food', 'Cooking Ingredients'),
('Cooking Oil', 'Food', 'Cooking Ingredients'),
('Rice', 'Food', 'Cooking Ingredients'),
('Flour', 'Food', 'Cooking Ingredients'),
('Chicken', 'Food', 'Cooking Ingredients'),
('Fish', 'Food', 'Cooking Ingredients'),
('Dates', 'Food', 'Cooking Ingredients'),
('Others', 'Food', 'Cooking Ingredients'),
('Instant Noodles (Cup)', 'Food', 'Instant Food'),
('Instant Noodles (Packet)', 'Food', 'Instant Food'),
('Others', 'Food', 'Instant Food'),
('Fruit', 'Food', 'Fruits'),
('Others', 'Food', 'Fruits'),
('Cricket Equipment', 'Entertainment', 'Sports'),
('Food Equipment', 'Entertainment', 'Sports'),
('Football Equipment', 'Entertainment', 'Sports'),
('Gym Equipment', 'Entertainment', 'Sports'),
('Jersey', 'Entertainment', 'Sports'),
('Others', 'Entertainment', 'Sports'),
('Poker Cards', 'Entertainment', 'Card Games'),
('Others', 'Entertainment', 'Card Games'),
('Carrum', 'Entertainment', 'Board Games'),
('Others', 'Entertainment', 'Board Games'),
('Instruments', 'Entertainment', 'Music'),
('Others', 'Entertainment', 'Music'),
('Art Supplies (Paint/Brush)', 'Entertainment', 'Art'),
('Art pieces', 'Entertainment', 'Art'),
('Others', 'Entertainment', 'Art'),
('Panadol', 'Healthcare', 'Medication'),
('Others', 'Healthcare', 'Medication'),
('Hair Growth Medicine/Tea', 'Healthcare', 'Supplements'),
('Vitamins', 'Healthcare', 'Supplements'),
('Others', 'Healthcare', 'Supplements'),
('Blood Pressure Monitor', 'Healthcare', 'Health Monitors'),
('Finger Oximeter', 'Healthcare', 'Health Monitors'),
('Others', 'Healthcare', 'Health Monitors'),
('Muscle Cream', 'Healthcare', 'Ointments'),
('Others', 'Healthcare', 'Ointments'),
('Iron', 'Homecare', 'Small Appliances'),
('Table Fan', 'Homecare', 'Small Appliances'),
('Vacuum', 'Homecare', 'Small Appliances'),
('Reading Lamp', 'Homecare', 'Small Appliances'),
('Hair Dryer', 'Homecare', 'Small Appliances'),
('Others', 'Homecare', 'Small Appliances'),
('Washing Machine', 'Homecare', 'Large Appliances'),
('Aircon', 'Homecare', 'Large Appliances'),
('Ceiling Fan', 'Homecare', 'Large Appliances'),
('Others', 'Homecare', 'Large Appliances'),
('General Toolbox', 'Homecare', 'Tools and Maintenance'),
('Others', 'Homecare', 'Tools and Maintenance'),
('Water Heater/Kettle', 'Kitchen', 'Small Appliances'),
('Curry Cooker', 'Kitchen', 'Small Appliances'),
('Juicer', 'Kitchen', 'Small Appliances'),
('Small Blender', 'Kitchen', 'Small Appliances'),
('Large Blender', 'Kitchen', 'Small Appliances'),
('Rice Cooker', 'Kitchen', 'Small Appliances'),
('Electric Cooker', 'Kitchen', 'Small Appliances'),
('Air Fryer', 'Kitchen', 'Small Appliances'),
('Microwave', 'Kitchen', 'Small Appliances'),
('Electric Oven', 'Kitchen', 'Small Appliances'),
('Bread Toaster', 'Kitchen', 'Small Appliances'),
('Pressure Cooker', 'Kitchen', 'Small Appliances'),
('Pestle and Mortar', 'Kitchen', 'Small Appliances'),
('Induction Stove', 'Kitchen', 'Small Appliances'),
('Others', 'Kitchen', 'Small Appliances'),
('Refrigerator', 'Kitchen', 'Large Appliances'),
('Gas Stove', 'Kitchen', 'Large Appliances'),
('BBQ Pit', 'Kitchen', 'Large Appliances'),
('Others', 'Kitchen', 'Large Appliances'),
('Frying Pan', 'Kitchen', 'Cooking Needs and Crockery'),
('Pot', 'Kitchen', 'Cooking Needs and Crockery'),
('Plates', 'Kitchen', 'Cooking Needs and Crockery'),
('Utensils', 'Kitchen', 'Cooking Needs and Crockery'),
('Bowls', 'Kitchen', 'Cooking Needs and Crockery'),
('Spatula/Ladle', 'Kitchen', 'Cooking Needs and Crockery'),
('Others', 'Kitchen', 'Cooking Needs and Crockery'),
('Detergent', 'Laundry', 'Laundry'),
('Others', 'Laundry', 'Laundry'),
('Luggage', 'Personal Use', 'Bags'),
('Bag', 'Personal Use', 'Bags'),
('Deodorant', 'Personal Use', 'Fragrance'),
('Perfume', 'Personal Use', 'Fragrance'),
('Others', 'Personal Use', 'Fragrance'),
('Raincoat', 'Personal Use', 'Travel Use'),
('Umbrella', 'Personal Use', 'Travel Use'),
('Bicycle', 'Personal Use', 'Travel Use'),
('Others', 'Personal Use', 'Travel Use'),
('Water Bottle', 'Personal Use', 'Bottles'),
('Thermos Flask', 'Personal Use', 'Bottles'),
('Others', 'Personal Use', 'Bottles'),
('Janamaz', 'Personal Use', 'Prayer Mat'),
('Others', 'Personal Use', 'Prayer Mat'),
('Sunglasses', 'Personal Use', 'Small Items'),
('Hair Clipper', 'Personal Use', 'Small Items'),
('Napkins', 'Personal Use', 'Small Items'),
('Watch', 'Personal Use', 'Small Items'),
('Face Masks', 'Personal Use', 'Small Items'),
('Torchlight', 'Personal Use', 'Small Items'),
('Wallet', 'Personal Use', 'Small Items'),
('Others', 'Personal Use', 'Small Items'),
('Toothpaste', 'Toiletries', 'Dental Care'),
('Toothbrush', 'Toiletries', 'Dental Care'),
('Others', 'Toiletries', 'Dental Care'),
('Hair Trimmer/Shaver', 'Toiletries', 'Grooming Products'),
('Others', 'Toiletries', 'Grooming Products'),
('Body Lotion', 'Toiletries', 'Body Care'),
('Soap', 'Toiletries', 'Body Care'),
('Sunblock', 'Toiletries', 'Body Care'),
('Body Spray', 'Toiletries', 'Body Care'),
('Others', 'Toiletries', 'Body Care'),
('Face Cream', 'Toiletries', 'Facial Care'),
('Others', 'Toiletries', 'Facial Care'),
('Shampoo', 'Toiletries', 'Hair Care'),
('Hair Gel', 'Toiletries', 'Body Care'),
('Conditioner', 'Toiletries', 'Hair Care'),
('Others', 'Toiletries', 'Hair Care'),
('Towel', 'Toiletries', 'Towel'),
('Others', 'Toiletries', 'Towel'),
('Bedside Table', 'Furniture', 'Tables'),
('Dining Table', 'Furniture', 'Tables'),
('Study Table', 'Furniture', 'Tables'),
('Others', 'Furniture', 'Tables'),
('Dining Chair', 'Furniture', 'Chair'),
('Study Chair', 'Furniture', 'Chair'),
('Outdoor Chair', 'Furniture', 'Chair'),
('Others', 'Furniture', 'Chair'),
('Bedside Lamp', 'Furniture', 'Lighting'),
('Lightbulbs', 'Furniture', 'Lighting'),
('Standing Lamp', 'Furniture', 'Lighting'),
('Ceiling Lamp', 'Furniture', 'Lighting'),
('Others', 'Furniture', 'Lighting'),
('Drawer', 'Furniture', 'Bedroom Essentials'),
('Cupboard', 'Furniture', 'Bedroom Essentials'),
('Clothes Hanger', 'Furniture', 'Bedroom Essentials'),
('Bedframe', 'Furniture', 'Bedroom Essentials'),
('Others', 'Furniture', 'Bedroom Essentials'),
('Sim Card', 'Others', 'Others'),
('Care Pack', 'Others', 'Others');

-- for donation table
INSERT INTO donation (`donorID`, `donationID`, `itemID`, `timeSubmitted`, `itemStatus`) VALUES
(92251521, '2022-02-15 21:35:42 92251521', 152, '2022-02-24 21:35:42', 'available');

-- for wishlist table
INSERT INTO wishlist (`wishlistID`, `migrantID`, `itemID`, `timeSubmitted`, `itemStatus`) VALUES 
('test', 12345678, 1, now(), 'available');

-- for request table
INSERT INTO request (`reqID`, `migrantID`, `postalCode`, `donationID`, `timeSubmitted`) VALUES
(1, 12345678, '518136', '2022-02-15 21:35:42 92251521', now());

-- for matches table
INSERT INTO matches (`matchID`, `reqID`, `migrantID`, `donorID`, `matchDate`) VALUES
(1, 1, 12345678, 11888811, now());

-- for delivery table
INSERT INTO delivery (`matchID`, `status`, `driverID`) VALUES
(1, 'available', 12312312);

-- UPDATE user set usertype = 'master' where username = 93261073;
-- select * from donation;
