/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 100432 (10.4.32-MariaDB)
 Source Host           : localhost:3306
 Source Schema         : apotek

 Target Server Type    : MySQL
 Target Server Version : 100432 (10.4.32-MariaDB)
 File Encoding         : 65001

 Date: 01/06/2024 10:27:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for detail_transaksi_penjualan
-- ----------------------------
DROP TABLE IF EXISTS detail_transaksi_penjualan;
CREATE TABLE detail_transaksi_penjualan  (
  id_detail_transaksi int NOT NULL AUTO_INCREMENT,
  id_transaksi_penjualan int NULL DEFAULT NULL,
  id_obat int NULL DEFAULT NULL,
  jumlah_beli int NULL DEFAULT NULL,
  harga_satuan double NULL DEFAULT NULL,
  PRIMARY KEY (id_detail_transaksi) USING BTREE,
  INDEX id_transaksi_penjualan(id_transaksi_penjualan ASC) USING BTREE,
  INDEX id_obat(id_obat ASC) USING BTREE,
  CONSTRAINT detail_transaksi_penjualan_ibfk_1 FOREIGN KEY (id_transaksi_penjualan) REFERENCES transaksi_penjualan (id_transaksi_penjualan) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT detail_transaksi_penjualan_ibfk_2 FOREIGN KEY (id_obat) REFERENCES obat (id_obat) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of detail_transaksi_penjualan
-- ----------------------------

-- ----------------------------
-- Table structure for obat
-- ----------------------------
DROP TABLE IF EXISTS obat;
CREATE TABLE obat  (
  id_obat int NOT NULL AUTO_INCREMENT,
  nama_obat varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  jenis_obat varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  harga double NULL DEFAULT NULL,
  jumlah_stok int NULL DEFAULT NULL,
  tanggal_kadaluwarsa date NULL DEFAULT NULL,
  PRIMARY KEY (id_obat) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of obat
-- ----------------------------
INSERT INTO obat VALUES (1, 'obat1', 'string', 0, 0, '2024-05-28');
INSERT INTO obat VALUES (2, 'obat1', 'string', 0, 0, '2024-05-28');
INSERT INTO obat VALUES (3, 'string', 'string', 0, 0, '2024-05-29');

-- ----------------------------
-- Table structure for pelanggan
-- ----------------------------
DROP TABLE IF EXISTS pelanggan;
CREATE TABLE pelanggan  (
  id_pelanggan int NOT NULL AUTO_INCREMENT,
  nama_pelanggan varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  alamat varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  nomor_telepon varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (id_pelanggan) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pelanggan
-- ----------------------------

-- ----------------------------
-- Table structure for pemasok
-- ----------------------------
DROP TABLE IF EXISTS pemasok;
CREATE TABLE pemasok  (
  id_pemasok int NOT NULL AUTO_INCREMENT,
  nama_perusahaan varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  nomor_telepon varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (id_pemasok) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pemasok
-- ----------------------------

-- ----------------------------
-- Table structure for resep_dokter
-- ----------------------------
DROP TABLE IF EXISTS resep_dokter;
CREATE TABLE resep_dokter  (
  id_resep int NOT NULL AUTO_INCREMENT,
  id_pelanggan int NULL DEFAULT NULL,
  tanggal_resep varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  catatan_dokter text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  PRIMARY KEY (id_resep) USING BTREE,
  INDEX id_pelanggan(id_pelanggan ASC) USING BTREE,
  CONSTRAINT resep_dokter_ibfk_1 FOREIGN KEY (id_pelanggan) REFERENCES pelanggan (id_pelanggan) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of resep_dokter
-- ----------------------------

-- ----------------------------
-- Table structure for transaksi_penjualan
-- ----------------------------
DROP TABLE IF EXISTS transaksi_penjualan;
CREATE TABLE transaksi_penjualan  (
  id_transaksi_penjualan int NOT NULL AUTO_INCREMENT,
  tanggal_transaksi date NULL DEFAULT NULL,
  total_pembayaran double NULL DEFAULT NULL,
  PRIMARY KEY (id_transaksi_penjualan) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of transaksi_penjualan
-- ----------------------------

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS user;
CREATE TABLE user  (
  id_user int NOT NULL AUTO_INCREMENT,
  nama_user varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  role int NULL DEFAULT NULL,
  email varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  password varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  alamat varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (id_user) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO user VALUES (1, 'admin', 0, 'admin@admin.com', '$2b$12$KBfvwkEXbIuH9y6lF.5CceXGfShxaTZa5/vP2EvL68E.bleVU6qJu', NULL);

SET FOREIGN_KEY_CHECKS = 1;