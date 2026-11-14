
CREATE DATABASE GestionClientes;
GO
USE GestionClientes;
GO
CREATE TABLE clientes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(50) NOT NULL,
    apellido NVARCHAR(50) NOT NULL,
    edad INT NOT NULL,
    telefono NVARCHAR(20) NOT NULL,
    direccion NVARCHAR(150) NOT NULL
);
GO
