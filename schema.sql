-- ============================================================
--  MAHADEV AI — MySQL Schema
--  Run this file once to set up your database:
--    mysql -u root -p < schema.sql
-- ============================================================

-- Create & select the database
CREATE DATABASE IF NOT EXISTS `mahadev_ai`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `mahadev_ai`;

-- ------------------------------------------------------------
-- Table: users
-- Stores registered user accounts
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `users` (
  `id`            INT           NOT NULL AUTO_INCREMENT,
  `first_name`    VARCHAR(80)   NOT NULL,
  `last_name`     VARCHAR(80)   NOT NULL,
  `username`      VARCHAR(80)   NOT NULL,
  `email`         VARCHAR(180)  NOT NULL,
  `password_hash` VARCHAR(128)  NOT NULL COMMENT 'Format: salt:sha256hash',
  `created_at`    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_username` (`username`),
  UNIQUE KEY `uq_email`    (`email`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Registered users of MAHADEV AI';

-- ------------------------------------------------------------
-- Table: chat_sessions
-- Tracks each conversation session per user
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `chat_sessions` (
  `id`         INT          NOT NULL AUTO_INCREMENT,
  `user_id`    INT          NOT NULL,
  `title`      VARCHAR(255) NOT NULL DEFAULT 'New conversation',
  `created_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (`id`),
  KEY `idx_chat_sessions_user` (`user_id`),
  CONSTRAINT `fk_chat_sessions_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Chat sessions / conversations';

-- ------------------------------------------------------------
-- Table: chat_messages
-- Stores every message (user + AI) in a session
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `chat_messages` (
  `id`         INT           NOT NULL AUTO_INCREMENT,
  `session_id` INT           NOT NULL,
  `user_id`    INT           NOT NULL,
  `role`       ENUM('user','assistant') NOT NULL,
  `content`    TEXT          NOT NULL,
  `created_at` DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (`id`),
  KEY `idx_chat_messages_session` (`session_id`),
  KEY `idx_chat_messages_user`    (`user_id`),
  CONSTRAINT `fk_chat_messages_session`
    FOREIGN KEY (`session_id`) REFERENCES `chat_sessions` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chat_messages_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Individual messages within a chat session';

-- ============================================================
-- Quick verification — shows all created tables
-- ============================================================
SHOW TABLES;