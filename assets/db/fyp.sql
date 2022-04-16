DROP Database IF EXISTS `fyp`;
Create DATABASE `fyp`;
USE `fyp`;

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
  `answer` varchar(300) NOT NULL,
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

DROP TABLE IF EXISTS `carousel`;
CREATE TABLE IF NOT EXISTS `carousel` (
  `carouselID` varchar(30) NOT NULL,
  `donorID` int NOT NULL,
  `itemID` int NOT NULL,
  `timeSubmitted` DATETIME NOT NULL,
  `itemStatus` varchar(50) NOT NULL,
  PRIMARY KEY (`carouselID`),
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
  `carouselID` varchar(30) NOT NULL,
  `migrantID` int NOT NULL,
  `deliveryLocation` varchar(300) NOT NULL,
  `requestQty` int NOT NULL,
  `timeSubmitted` datetime NOT NULL,
  PRIMARY KEY (`reqID`),
  FOREIGN KEY (`migrantID`) REFERENCES user (`username`),
  FOREIGN KEY (`carouselID`) REFERENCES carousel (`carouselID`)
);

DROP TABLE IF EXISTS `delivery`;
CREATE TABLE IF NOT EXISTS `delivery` (
  `deliveryReqID` int NOT NULL AUTO_INCREMENT,
  `driverID` int NOT NULL,
  `deliveryStatus` varchar(50) NOT NULL,
  `reqID` int NOT NULL,
  PRIMARY KEY (`deliveryReqID`),
  FOREIGN KEY (`reqID`) references request (`reqID`),
  FOREIGN KEY (`driverID`) references user (`username`)
) ;

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
  FOREIGN KEY (`submissionID`) references carousel (`carouselID`),
  FOREIGN KEY (`submissionID`) references wishlist (`wishlistID`),
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

-- INSERT values

-- for carousel table
-- INSERT INTO carousel (`itemName`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
-- ('toothbrush', 'basic toiletries', 'yew wei', 'pasir ris grove', '92251521', 'toiletries', 1, 'yes', 'east', now(), 'available', 'toothbrush.png');
-- INSERT INTO carousel (`itemName`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
-- ('hair dryer', 'for hair', 'yuanyuan', '510121', '12345678', 'home appliances', 1, 'yes', 'west', now(), 'available', 'hairdryer.jpg');
-- INSERT INTO carousel (`itemName`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
-- ('t-shirts', 'free size t-shirts', 'amanda', '510425', '87654321', 'clothing', 1, 'yes', 'north', now(), 'available', 't-shirt.jpg');
-- INSERT INTO carousel (`itemName`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
-- ('rice cooker', 'to cook rice', 'nicole', '510180', '92251521', 'home appliances', 1, 'yes', 'south', now(), 'available', 'ricecooker.jpg');
-- INSERT INTO carousel (`itemName`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
-- ('fan', 'for sg hot weather', 'vanessa', 'pasir ris', '92251521', 'home appliances', 1, 'yes', 'east', now(), 'available', 'fan.jpg');
-- INSERT INTO carousel (`itemName`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
-- ('jeans', 'jeans in size 40', 'mei fang', 'pasir ris', '92251521', 'clothing', 1, 'yes', 'east', now(), 'available', 'jeans.jpg');


-- for wishlist table
-- INSERT INTO wishlist (`itemName`, `quantity`, `category`, `subCat`, `timeSubmitted`, `itemStatus`) VALUES
-- ('Large Blender', 1,'Kitchen', 'Small Appliances', now(), 'available'),
-- ('TV', 2, 'Electronics', 'TVs', now(), 'available');



-- for user table
-- INSERT INTO user(`username`, `password`, `userType`) VALUES 
-- (93261073, ENCRYPT('cheah1124'), 'admin');
INSERT INTO `user` (`username`, `password`, `usertype`) VALUES (12345678, 'test', 'worker');
INSERT INTO `user` (`username`, `password`, `usertype`) VALUES (87654321, 'test2', 'worker');


-- for faq
INSERT INTO faq (`question`, `answer`, `section`) VALUES ('How do I donate?', 'Just do it!', 'donor');
INSERT INTO faq (`question`, `answer`, `section`) VALUES ('What do I donate?', 'Check out our wishlist', 'donor');
INSERT INTO faq (`question`, `answer`, `section`) VALUES ('How do I request for an item?', 'Just do it!', 'worker');
INSERT INTO faq (`question`, `answer`, `section`) VALUES ('How do I drive?', 'Just do it!', 'driver');


-- for formbuilder table
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `placeholder`) VALUES
('carousel', 'Name', 'text', 'Your name or the Organization you are representing');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('carousel', 'Address', 'text');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `options`) VALUES
('carousel', 'Area', 'radio', 'North;South;East;West;Central');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('carousel', 'Item Photo', 'file');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `placeholder`) VALUES
('carousel', 'Item Description', 'text', 'Brief description of the item you are donating');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('carousel', 'Quantity', 'number');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `options`) VALUES
('carousel', 'Delivery Method', 'dropdown', 'Delivery required;Arranged by donor');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `placeholder`) VALUES
('wishlist', 'Address', 'text', 'Enter Address');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('wishlist', 'Quantity', 'number');


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

-- for newcarousel table
INSERT INTO carousel (`donorID`, `carouselID`, `itemID`, `timeSubmitted`, `itemStatus`) VALUES
(92251521, '2022-02-15 21:35:42 92251521', 152, '2022-02-24 21:35:42', 'available');

-- for newwishlist table
INSERT INTO wishlist (`wishlistID`, `migrantID`, `itemID`, `timeSubmitted`, `itemStatus`) VALUES 
('test', 12345678, 1, now(), 'available');

-- for newrequest table
INSERT INTO request (`reqID`, `migrantID`, `deliveryLocation`, `carouselID`, `requestQty`, `timeSubmitted`) VALUES
(1, 12345678, 'pasir ris', '2022-02-15 21:35:42 92251521', 1, now());

-- for matches table
INSERT INTO matches (`matchID`, `reqID`, `migrantID`, `donorID`, `matchDate`) VALUES
(1, 1, 12345678, 11888811, now());

-- for formanswers table
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'carousel', '1', 'yew wei');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'carousel', '2', 'pasir ris grove');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'carousel', '3', 'East');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'carousel', '4', 'toothbrush.png');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'carousel', '5', 'can make teeth sparkle sparkle');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'carousel', '6', '3');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'carousel', '7', 'Arranged by donor');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('test', 'wishlist', '8', 'pasir ris');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('test', 'wishlist', '9', '1');

-- select * from request;
