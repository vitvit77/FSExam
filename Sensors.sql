/*
 Navicat Premium Data Transfer

 Source Server         : Modem
 Source Server Type    : MySQL
 Source Server Version : 50726
 Source Host           : 10.0.19.122:3306
 Source Schema         : FullStack

 Target Server Type    : MySQL
 Target Server Version : 50726
 File Encoding         : 65001

 Date: 08/12/2022 22:25:10
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for Sensors
-- ----------------------------
DROP TABLE IF EXISTS `Sensors`;
CREATE TABLE `Sensors`  (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `qty` int(3) NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
