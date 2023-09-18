/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE IF NOT EXISTS `wantu` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `wantu`;


CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) COLLATE utf8mb4_general_ci NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `phone_number` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `image_url` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `introduction` text COLLATE utf8mb4_general_ci,
  `personal_site` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `linked` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `balance` int DEFAULT 0,
  `bank` varchar(45) COLLATE utf8mb4_general_ci NULL,
  `bank_account` varchar(255) COLLATE utf8mb4_general_ci NULL,
  `post_no` varchar(45) COLLATE utf8mb4_general_ci NULL,
  `address_base` varchar(255) COLLATE utf8mb4_general_ci NULL,
  `address_detail` varchar(255) COLLATE utf8mb4_general_ci NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `hashtag` (
  `hashtag_id` int NOT NULL AUTO_INCREMENT,
  `text` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`hashtag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `user_hashtag` (
  `user_hashtag_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `hashtag_id` int NOT NULL,
  PRIMARY KEY (`user_hashtag_id`),
  KEY `fk_user_hashtag_user1_idx` (`user_id`),
  KEY `fk_user_hashtag_hashtag1_idx` (`hashtag_id`),
  CONSTRAINT `fk_user_hashtag_hashtag1` FOREIGN KEY (`hashtag_id`) REFERENCES `hashtag` (`hashtag_id`),
  CONSTRAINT `fk_user_hashtag_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `feed` (
  `feed_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `content` text COLLATE utf8mb4_general_ci DEFAULT NULL,
  `thumbnail_image_url` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,  
  `teaser_url` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `video_url` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `image_urls` text COLLATE utf8mb4_general_ci DEFAULT NULL,
  `title` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `introduction` text COLLATE utf8mb4_general_ci DEFAULT NULL,
  `financial_plan` text COLLATE utf8mb4_general_ci DEFAULT NULL,
  `start_at` datetime NOT NULL,
  `end_at` datetime NOT NULL,
  `release_at` datetime NOT NULL,
  `schedule` text COLLATE utf8mb4_general_ci DEFAULT NULL,
  `goal_amount`  int NOT NULL,
  `status` varchar(45) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'PENDING',
  `minimum_amount` int NULL DEFAULT 1000,
  `maximum_amount` int NULL DEFAULT NULL,
  `total_nft`  int NOT NULL,
  `nft_benefit` text COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nft_urls` text COLLATE utf8mb4_general_ci DEFAULT NULL,
  `investment_amount` int DEFAULT 0,
  `yield_amount` float DEFAULT 0,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `contract_address` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`feed_id`),
  KEY `fk_feed_user1_idx` (`user_id`),
  CONSTRAINT `fk_feed_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `feed_hashtag` (
  `feed_hashtag_id` int NOT NULL AUTO_INCREMENT,
  `feed_id` int NOT NULL,
  `hashtag_id` int NOT NULL,
  PRIMARY KEY (`feed_hashtag_id`),
  KEY `fk_feed_hashtag_feed1_idx` (`feed_id`),
  KEY `fk_feed_hashtag_hashtag1_idx` (`hashtag_id`),
  CONSTRAINT `fk_feed_hashtag_feed1` FOREIGN KEY (`feed_id`) REFERENCES `feed` (`feed_id`),
  CONSTRAINT `fk_feed_hashtag_hashtag1` FOREIGN KEY (`hashtag_id`) REFERENCES `hashtag` (`hashtag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `reply` (
  `reply_id` int NOT NULL AUTO_INCREMENT,
  `feed_id` int DEFAULT NULL,
  `community_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  `text` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`reply_id`),
  KEY `fk_reply_feed1_idx` (`feed_id`),
  KEY `fk_reply_community1_idx` (`community_id`),
  KEY `fk_reply_user1_idx` (`user_id`),
  CONSTRAINT `fk_reply_feed1` FOREIGN KEY (`feed_id`) REFERENCES `feed` (`feed_id`),
  CONSTRAINT `fk_reply_community1` FOREIGN KEY (`community_id`) REFERENCES `community` (`community_id`),
  CONSTRAINT `fk_reply_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `nested_reply` (
  `nested_reply_id` int NOT NULL AUTO_INCREMENT,
  `reply_id` int NOT NULL,
  `user_id` int NOT NULL,
  `text` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`nested_reply_id`),
  KEY `fk_nested_reply_reply1_idx` (`reply_id`),
  KEY `fk_nested_reply_user1_idx` (`user_id`),
  CONSTRAINT `fk_nested_reply_reply1` FOREIGN KEY (`reply_id`) REFERENCES `reply` (`reply_id`),
  CONSTRAINT `fk_nested_reply_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `like` (
  `like_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `feed_id` int DEFAULT NULL,
  `community_id` int DEFAULT NULL,
  `reply_id` int DEFAULT NULL,
  `nested_reply_id` int DEFAULT NULL,
  PRIMARY KEY (`like_id`),
  KEY `fk_like_feed1_idx` (`feed_id`),
  KEY `fk_like_community1_idx` (`community_id`),
  KEY `fk_like_reply1_idx` (`reply_id`),
  KEY `fk_like_nested_reply1_idx` (`nested_reply_id`),
  KEY `fk_like_user1_idx` (`user_id`),
  CONSTRAINT `fk_like_feed1` FOREIGN KEY (`feed_id`) REFERENCES `feed` (`feed_id`),
  CONSTRAINT `fk_like_community1` FOREIGN KEY (`community_id`) REFERENCES `community` (`community_id`),
  CONSTRAINT `fk_like_nested_reply1` FOREIGN KEY (`nested_reply_id`) REFERENCES `nested_reply` (`nested_reply_id`),
  CONSTRAINT `fk_like_reply1` FOREIGN KEY (`reply_id`) REFERENCES `reply` (`reply_id`),
  CONSTRAINT `fk_like_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `following` (
  `following_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `follow_user_id` int DEFAULT NULL,
  `hashtag_id` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`following_id`),
  KEY `fk_following_follow_user1_idx` (`follow_user_id`),
  KEY `fk_following_hashtag1_idx` (`hashtag_id`),
  KEY `fk_following_user1_idx` (`user_id`),
  CONSTRAINT `fk_following_follow_user1` FOREIGN KEY (`follow_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_following_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `fk_following_hashtag1` FOREIGN KEY (`hashtag_id`) REFERENCES `hashtag` (`hashtag_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `play` (
  `play_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `feed_id` int DEFAULT NULL,
  `played` int DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`play_id`),
  KEY `fk_play_feed1_idx` (`feed_id`),
  KEY `fk_play_user1_idx` (`user_id`),
  CONSTRAINT `fk_play_feed1` FOREIGN KEY (`feed_id`) REFERENCES `feed` (`feed_id`),
  CONSTRAINT `fk_play_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `investment` (
  `investment_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `feed_id` int NOT NULL,
  `amount` int NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`investment_id`),
  KEY `fk_investment_feed1_idx` (`feed_id`),
  KEY `fk_investment_user1_idx` (`user_id`),
  CONSTRAINT `fk_investment_feed1` FOREIGN KEY (`feed_id`) REFERENCES `feed` (`feed_id`),
  CONSTRAINT `fk_investment_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `deposit` (
  `deposit_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `type` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `amount` int NOT NULL,
  `status` varchar(45) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'PENDING',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`deposit_id`),
  KEY `fk_deposit_user1_idx` (`user_id`),
  CONSTRAINT `fk_deposit_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `wallet` (
  `wallet_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `xpub` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `mnemonic` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `address` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `private` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`wallet_id`),
  KEY `fk_wallet_user1_idx` (`user_id`),
  CONSTRAINT `fk_wallet_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `community` (
  `community_id` int NOT NULL AUTO_INCREMENT,
  `feed_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  `text` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`reply_id`),
  KEY `fk_reply_feed1_idx` (`feed_id`),
  KEY `fk_reply_user1_idx` (`user_id`),
  CONSTRAINT `fk_reply_feed1` FOREIGN KEY (`feed_id`) REFERENCES `feed` (`feed_id`),
  CONSTRAINT `fk_reply_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `report` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `feed_id` int DEFAULT NULL,
  `episode_id` int DEFAULT NULL,
  `community_id` int DEFAULT NULL,
  `reply_id` int DEFAULT NULL,
  `nested_reply_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  `reason` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`reply_id`),
  KEY `fk_reply_feed1_idx` (`feed_id`),
  KEY `fk_reply_episode1_idx` (`episode_id`),
  KEY `fk_reply_community1_idx` (`community_id`),
  KEY `fk_reply_reply1_idx` (`reply_id`),
  KEY `fk_reply_nested_reply1_idx` (`nested_reply_id`),
  KEY `fk_reply_user1_idx` (`user_id`),
  CONSTRAINT `fk_reply_feed1` FOREIGN KEY (`feed_id`) REFERENCES `feed` (`feed_id`),
  CONSTRAINT `fk_reply_episode1` FOREIGN KEY (`episode_id`) REFERENCES `episode` (`episode_id`),
  CONSTRAINT `fk_reply_community1` FOREIGN KEY (`community_id`) REFERENCES `community` (`community_id`),
  CONSTRAINT `fk_reply_reply1` FOREIGN KEY (`reply_id`) REFERENCES `reply` (`reply_id`),
  CONSTRAINT `fk_reply_nested_reply1` FOREIGN KEY (`nested_reply_id`) REFERENCES `nested_reply` (`nested_reply_id`),
  CONSTRAINT `fk_reply_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
