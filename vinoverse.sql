-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 20-12-2024 a las 17:29:07
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `vinoverse`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bodegas`
--

CREATE TABLE `bodegas` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `ubicacion` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `bodegas`
--

INSERT INTO `bodegas` (`id`, `nombre`, `ubicacion`, `descripcion`) VALUES
(2, 'casa', 'en un lugar alejado de tu casa', 'ta feo el lugar no vayas'),
(3, 'olaquetal', 'en ul lugar raro', 'papa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito`
--

CREATE TABLE `carrito` (
  `id` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_factura`
--

CREATE TABLE `detalle_factura` (
  `id` int(11) NOT NULL,
  `id_factura` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) GENERATED ALWAYS AS (`cantidad` * `precio_unitario`) STORED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_factura`
--

INSERT INTO `detalle_factura` (`id`, `id_factura`, `id_producto`, `cantidad`, `precio_unitario`) VALUES
(1, 1, 1, 5, 0.00),
(2, 5, 1, 1, 0.00),
(3, 5, 2, 10, 0.00),
(4, 7, 1, 1, 0.00),
(5, 7, 2, 1, 0.00),
(6, 8, 1, 1, 0.00),
(7, 8, 2, 1, 0.00),
(8, 9, 1, 1, 0.00),
(9, 9, 2, 1, 0.00),
(10, 10, 1, 1, 0.00),
(11, 10, 2, 1, 0.00),
(12, 11, 1, 3, 0.00),
(13, 11, 2, 1, 0.00),
(14, 15, 1, 1, 0.00),
(15, 15, 2, 1, 0.00),
(16, 16, 1, 1, 0.00),
(17, 16, 2, 1, 0.00),
(18, 17, 1, 1, 0.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empresas_transporte`
--

CREATE TABLE `empresas_transporte` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `contacto` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empresas_transporte`
--

INSERT INTO `empresas_transporte` (`id`, `nombre`, `contacto`) VALUES
(1, 'alejo', 'alejo@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `eventos`
--

CREATE TABLE `eventos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `fecha` date NOT NULL,
  `ubicacion_corta` varchar(255) NOT NULL,
  `ubicacion_completa` text NOT NULL,
  `leve_descripcion` varchar(255) DEFAULT NULL,
  `descripcion_detallada` text NOT NULL,
  `duracion` decimal(5,2) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `organizador_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `eventos`
--

INSERT INTO `eventos` (`id`, `nombre`, `fecha`, `ubicacion_corta`, `ubicacion_completa`, `leve_descripcion`, `descripcion_detallada`, `duracion`, `precio`, `imagen`, `organizador_id`) VALUES
(4, 'Vinoverse 2', '2025-02-14', 'Cerro los gemelos y 22 de diciembre', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d413.10145243775605!2d-68.82649202508301!3d-32.964051834207744!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x967e0b9d9a7a3df3%3A0x561c56c99b238acc!2sCerro%20los%20Gemelos%20%26%2022%20de%20Diciembre%2C%20Maip%C3%BA%2C%20Mendoza!5e0!3m2!1ses-419!2sar!4v1731568784173!5m2!1ses-419!2sar\" width=\"600\" height=\"450\" style=\"border:0;\" allowfullscreen=\"\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade', 'lorem ', 'lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem \r\nlorem lorem lorem lorem lorem lorem lorem lorem lorem lorem , lorem lorem lorem lorem lorem lorem ', 3.00, 35000.00, 'WhatsApp_Image_2024-11-10_at_3.33.44_PM.jpeg', 1),
(5, 'evento', '2024-12-26', 'Cerro los gemelos y 22 de diciembre', 'https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d418.44047454593476!2d-68.8267891!3d-32.9635799!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x967e0b9d9a7a3df3%3A0x561c56c99b238acc!2sCerro%20los%20Gemelos%20%26%2022%20de%20Diciembre%2C%20Maip%C3%BA%2C%20Mendoza!5e0!3m2!1ses-419!2sar!4v1731628188850!5m2!1ses-419!2sar\" width=\"600\" height=\"450\" style=\"border:0;\" allowfullscreen=\"\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade', 'EVENTO NO SE QUE', 'EVENTO NO SE QUE EVENTO NO SE QUE EVENTO NO SE QUE EVENTO NO SE QUE EVENTO NO SE QUE EVENTO NO SE QUE EVENTO NO SE QUE EVENTO NO SE QUE EVENTO NO SE QUE EVENTO NO SE QUE EVENTO NO SE QUE EVENTO NO SE QUE EVENTO NO SE QUE EVENTO NO SE QUE EVENTO NO SE QUE EVENTO NO SE QUE ', 5.00, 0.00, 'WhatsApp_Image_2024-11-10_at_3.33.44_PM.jpeg', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `experiencias`
--

CREATE TABLE `experiencias` (
  `id` int(11) NOT NULL,
  `publicacion_id` int(11) DEFAULT NULL,
  `tipo_experiencia` varchar(50) DEFAULT NULL,
  `ubicacion` varchar(100) DEFAULT NULL,
  `fecha_inicio` datetime DEFAULT NULL,
  `fecha_fin` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura`
--

CREATE TABLE `factura` (
  `id` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `total` decimal(10,2) NOT NULL,
  `metodo_pago` enum('Tarjeta de crédito','Tarjeta de débito','Mercado Pago','Transferencia') DEFAULT 'Tarjeta de crédito',
  `direccion_envio` varchar(255) NOT NULL,
  `dni` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `factura`
--

INSERT INTO `factura` (`id`, `id_usuario`, `fecha`, `total`, `metodo_pago`, `direccion_envio`, `dni`) VALUES
(1, 1, '2024-11-15 07:18:30', 117500.00, '', 'Cerro los gemelos 223', '45724003'),
(2, 1, '2024-11-15 07:18:32', 0.00, '', 'Cerro los gemelos 223', '45724003'),
(5, 1, '2024-11-15 07:34:44', 344500.00, '', 'Cerro los gemelos 223', '45724003'),
(6, 1, '2024-11-15 07:37:41', 0.00, '', 'Cerro los gemelos 223', '45724003'),
(7, 1, '2024-11-15 07:40:55', 55600.00, '', 'Cerro los gemelos 223', '45724003'),
(8, 1, '2024-11-15 07:43:51', 55600.00, '', 'Cerro los gemelos 223', '45724003'),
(9, 1, '2024-11-15 07:45:30', 55600.00, 'Transferencia', 'Cerro los gemelos 223', '45724003'),
(10, 1, '2024-11-15 07:45:45', 55600.00, '', 'Cerro los gemelos 223', '45724003'),
(11, 1, '2024-11-15 07:49:23', 102600.00, '', 'Cerro los gemelos 223', '45724003'),
(12, 1, '2024-11-15 07:49:29', 0.00, '', 'Cerro los gemelos 223', '45724003'),
(13, 1, '2024-11-15 07:53:38', 0.00, '', 'Cerro los gemelos 223', '45724003'),
(14, 1, '2024-11-15 07:56:30', 0.00, '', 'Cerro los gemelos 223', '45724003'),
(15, 1, '2024-11-15 07:56:40', 55600.00, '', 'Cerro los gemelos 223', '45724003'),
(16, 1, '2024-11-15 07:58:21', 55600.00, '', 'Cerro los gemelos 223', '45724003'),
(17, 1, '2024-11-15 13:21:55', 23500.00, '', 'aa', '1234567789');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fotos_grupo`
--

CREATE TABLE `fotos_grupo` (
  `id` int(11) NOT NULL,
  `grupo_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `nombre_archivo` varchar(255) DEFAULT NULL,
  `fecha_subida` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fotos_videos`
--

CREATE TABLE `fotos_videos` (
  `id` int(11) NOT NULL,
  `publicacion_id` int(11) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grupos`
--

CREATE TABLE `grupos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `foto_perfil` varchar(255) DEFAULT NULL,
  `creador_id` int(11) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `grupos`
--

INSERT INTO `grupos` (`id`, `nombre`, `descripcion`, `foto_perfil`, `creador_id`, `fecha_creacion`) VALUES
(3, 'grupo 3', 'grupo 3', 'WhatsApp_Image_2024-11-10_at_3.33.44_PM.jpeg', 3, '2024-11-10 23:03:19'),
(4, 'Grupo 4', 'algo', 'loslocos.png', 3, '2024-11-10 23:03:56'),
(6, 'aasdas', 'sadsdasd', 'WhatsApp_Image_2024-11-10_at_3.33.44_PM.jpeg', 1, '2024-11-12 00:55:48'),
(7, 'grupo 2', 'dasdad', 'Habilidades_blandas.png', 4, '2024-11-12 05:32:17'),
(8, 'Grupo los locos', 'Estoy muy loco', 'loslocos.png', 21, '2024-11-14 01:03:20');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `guardados`
--

CREATE TABLE `guardados` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `publicacion_id` int(11) NOT NULL,
  `fecha_guardado` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `guardados`
--

INSERT INTO `guardados` (`id`, `usuario_id`, `publicacion_id`, `fecha_guardado`) VALUES
(9, 3, 32, '2024-11-10 19:31:08'),
(10, 3, 24, '2024-11-10 19:34:16'),
(11, 3, 33, '2024-11-10 19:34:29'),
(13, 3, 23, '2024-11-10 19:44:34'),
(14, 3, 18, '2024-11-10 19:46:13'),
(15, 3, 36, '2024-11-10 19:47:03'),
(21, 4, 39, '2024-11-12 05:31:41'),
(22, 21, 42, '2024-11-14 01:00:52'),
(25, 22, 43, '2024-11-14 01:47:29'),
(28, 3, 39, '2024-11-15 00:31:52'),
(31, 1, 43, '2024-11-15 16:37:56');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `hoteles`
--

CREATE TABLE `hoteles` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `ubicacion` varchar(100) DEFAULT NULL,
  `contacto` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `hoteles`
--

INSERT INTO `hoteles` (`id`, `nombre`, `ubicacion`, `contacto`) VALUES
(1, 'casa triste', 'lejos de tu casa', 'no hay contacto gil');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imagenes_publicacion`
--

CREATE TABLE `imagenes_publicacion` (
  `id` int(11) NOT NULL,
  `id_publicacion` int(11) NOT NULL,
  `nombre_archivo` varchar(255) NOT NULL,
  `fecha_subida` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `imagenes_publicacion`
--

INSERT INTO `imagenes_publicacion` (`id`, `id_publicacion`, `nombre_archivo`, `fecha_subida`) VALUES
(6, 32, 'fotoperfil.jpg', '2024-11-09 23:10:03'),
(7, 33, 'dengue.jpg', '2024-11-09 23:11:30'),
(9, 36, 'Habilidades_blandas.png', '2024-11-09 23:39:15'),
(11, 38, 'WhatsApp_Image_2024-11-10_at_3.33.44_PM.jpeg', '2024-11-11 03:13:17'),
(12, 39, 'WhatsApp_Image_2024-11-01_at_5.44.17_PM.jpeg', '2024-11-11 03:16:21'),
(15, 42, 'loslocos.png', '2024-11-14 01:00:49'),
(16, 43, 'Ejemplo_de_Encuesta.jpeg', '2024-11-14 01:47:23');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mensajes`
--

CREATE TABLE `mensajes` (
  `id` int(11) NOT NULL,
  `emisor_id` int(11) DEFAULT NULL,
  `receptor_id` int(11) DEFAULT NULL,
  `contenido` text DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `leido` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mensajes`
--

INSERT INTO `mensajes` (`id`, `emisor_id`, `receptor_id`, `contenido`, `fecha`, `leido`) VALUES
(1, 3, 1, 'hola hola hola', '2024-10-24 06:21:53', 0),
(2, 1, 3, 'Hola', '2024-10-24 07:22:16', 0),
(3, 4, 1, 'prueba 2', '2024-10-24 07:29:03', 0),
(4, 1, 4, 'dasda', '2024-10-24 07:42:12', 0),
(5, 1, 3, 'dsadasd', '2024-10-24 07:42:19', 0),
(6, 1, 3, 'dasdad', '2024-10-24 07:42:24', 0),
(7, 1, 3, 'sadasd', '2024-10-24 07:47:27', 0),
(8, 1, 13, 'asdsad', '2024-10-24 07:47:37', 0),
(9, 3, 1, 'dasda', '2024-11-09 22:13:15', 0),
(10, 3, 12, 'Hola\r\n', '2024-11-10 19:10:18', 0),
(11, 3, 1, 'hola\r\n', '2024-11-10 19:10:52', 0),
(12, 1, 17, 'hol\r\n', '2024-11-11 03:12:44', 0),
(13, 21, 1, 'Hola gordo\r\n', '2024-11-14 01:01:19', 0),
(14, 22, 1, 'hola\r\n', '2024-11-14 01:47:43', 0),
(15, 1, 14, 'hola\r\n', '2024-11-15 00:03:08', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mensajes_grupo`
--

CREATE TABLE `mensajes_grupo` (
  `id` int(11) NOT NULL,
  `grupo_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `mensaje` text NOT NULL,
  `fecha_envio` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mensajes_grupo`
--

INSERT INTO `mensajes_grupo` (`id`, `grupo_id`, `usuario_id`, `mensaje`, `fecha_envio`) VALUES
(1, 6, 1, 'Hola\r\n', '2024-11-12 05:10:51'),
(2, 3, 1, 'Hola lucas\r\n', '2024-11-12 05:11:10'),
(3, 3, 3, 'Hola nahuel\r\n', '2024-11-12 05:11:39'),
(4, 3, 4, 'Hola\r\n', '2024-11-12 05:12:11'),
(5, 8, 21, 'Hola\r\n', '2024-11-14 01:03:46'),
(6, 7, 21, 'hola\r\n', '2024-11-14 01:04:22');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `miembros_grupo`
--

CREATE TABLE `miembros_grupo` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `grupo_id` int(11) NOT NULL,
  `rol` enum('miembro','admin') DEFAULT 'miembro',
  `fecha_entrada` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `miembros_grupo`
--

INSERT INTO `miembros_grupo` (`id`, `usuario_id`, `grupo_id`, `rol`, `fecha_entrada`) VALUES
(8, 3, 3, 'miembro', '2024-11-12 04:53:32'),
(9, 1, 3, 'miembro', '2024-11-12 05:05:17'),
(10, 4, 3, 'miembro', '2024-11-12 05:12:04'),
(11, 21, 7, 'miembro', '2024-11-14 01:04:14'),
(12, 1, 8, 'miembro', '2024-11-14 01:05:48'),
(13, 1, 4, 'miembro', '2024-11-14 01:06:27');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paquetes_turisticos`
--

CREATE TABLE `paquetes_turisticos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `transporte_id` int(11) DEFAULT NULL,
  `hotel_id` int(11) DEFAULT NULL,
  `bodega_id` int(11) DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `paquetes_turisticos`
--

INSERT INTO `paquetes_turisticos` (`id`, `nombre`, `descripcion`, `precio`, `transporte_id`, `hotel_id`, `bodega_id`, `imagen`) VALUES
(5, 'olaola', 'un lugar raro', 100000.00, 1, 1, 2, 'paquete_1.png'),
(6, 'casa grande', 'hola', 99999999.99, 1, 1, 3, 'paquete_2.png');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perfiles`
--

CREATE TABLE `perfiles` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `foto_perfil` varchar(255) DEFAULT NULL,
  `biografia` text DEFAULT NULL,
  `ubicacion` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `id_vendedor` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `descripcion`, `precio`, `imagen`, `id_vendedor`) VALUES
(1, 'Vino cabernet', 'Vino cabernet puro de la bodega trivento', 23500.00, 'OIP.jpg', 1),
(2, 'Vino Malbec ', 'texto', 32100.00, 'red-wine-1369425-1920.jpeg', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `publicaciones`
--

CREATE TABLE `publicaciones` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `tipo_publicacion` varchar(50) DEFAULT NULL,
  `titulo` varchar(100) DEFAULT NULL,
  `contenido` text DEFAULT NULL,
  `fecha_publicacion` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `publicaciones`
--

INSERT INTO `publicaciones` (`id`, `usuario_id`, `tipo_publicacion`, `titulo`, `contenido`, `fecha_publicacion`) VALUES
(18, 1, NULL, 'SASA', 'DASDASD', '2024-10-23 23:40:41'),
(23, 3, NULL, 'sadasd', 'dasdas', '2024-10-24 05:01:41'),
(24, 12, NULL, 'asdasd', 'sdasdasd', '2024-10-24 05:02:50'),
(25, 3, NULL, 'Lucas', 'prueba', '2024-10-24 10:19:01'),
(32, 1, NULL, 'Hola', 'dasdasd', '2024-11-09 23:10:03'),
(33, 1, NULL, 'dsada', 'dasdasda', '2024-11-09 23:11:30'),
(36, 14, NULL, 'sadasd', 'asdasdasd', '2024-11-09 23:39:15'),
(38, 1, NULL, 'espeon', 'God', '2024-11-11 03:13:17'),
(39, 3, NULL, 'espeon', 'God', '2024-11-11 03:16:21'),
(42, 21, NULL, 'Hola', 'me gusta mucho la pija', '2024-11-14 01:00:49'),
(43, 22, NULL, 'Holap', 'Me encanta mucho los merinos', '2024-11-14 01:47:23'),
(44, 1, NULL, 'hola', 'como estas', '2024-11-15 00:04:02');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `relaciones`
--

CREATE TABLE `relaciones` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `amigo_id` int(11) DEFAULT NULL,
  `estado` enum('pendiente','amigo','rechazado') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `relaciones`
--

INSERT INTO `relaciones` (`id`, `usuario_id`, `amigo_id`, `estado`) VALUES
(15, 3, 4, 'amigo'),
(21, 1, 4, 'amigo'),
(40, 1, 11, 'amigo'),
(96, 3, 12, 'amigo'),
(101, 1, 6, 'pendiente'),
(106, 1, 9, 'pendiente'),
(108, 21, 1, 'amigo'),
(109, 21, 17, 'amigo'),
(110, 21, 18, 'amigo'),
(111, 21, 19, 'amigo'),
(112, 22, 1, 'amigo'),
(113, 22, 17, 'amigo'),
(115, 1, 14, 'amigo'),
(116, 3, 1, 'amigo'),
(118, 1, 17, 'amigo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

CREATE TABLE `reservas` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `fecha` date NOT NULL,
  `personas` int(11) NOT NULL,
  `paquete_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reservas`
--

INSERT INTO `reservas` (`id`, `nombre`, `email`, `fecha`, `personas`, `paquete_id`) VALUES
(6, 'hola', 'martinmamani05@gmail.com', '2222-02-02', 2, 5),
(7, 'tommycmr', 'tomascmr24@gmail.com', '2024-02-25', 30, 6),
(8, 'hola', 'prueba@gmail.com', '2222-02-02', 2, 5),
(9, 'Alejandro', 'santi.sr67@gmail.com', '2024-02-20', 19, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reseñas_vinos`
--

CREATE TABLE `reseñas_vinos` (
  `id` int(11) NOT NULL,
  `publicacion_id` int(11) DEFAULT NULL,
  `vino_id` int(11) DEFAULT NULL,
  `puntuacion` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `contraseña` varchar(255) DEFAULT NULL,
  `fecha_registro` date DEFAULT NULL,
  `tipo_cuenta` enum('individual','empresa') DEFAULT 'individual',
  `tipo_empresa` enum('Bodega','Hotel','Transporte') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `contraseña`, `fecha_registro`, `tipo_cuenta`, `tipo_empresa`) VALUES
(1, 'Martin', 'Mamani', 'martinmamani05@gmail.com', 'gabiteamo', '2024-08-28', 'individual', NULL),
(3, 'Lucas', 'Mamani', 'lucasmamani@gmail.com', 'lucas', '2024-08-30', 'individual', NULL),
(4, 'nahuel', 'mamani', 'nahuelmamani@gmail.com', 'nahuel', '2024-08-30', 'individual', NULL),
(5, 'hola', 'hola', 'holahola@hotmail.com', 'ololahola', '2024-08-30', 'individual', NULL),
(6, 'prueba1', 'prueba2', 'prueba@gmail.com', 'hola', '2024-08-30', 'individual', NULL),
(7, 'prueba2', 'prueba2', 'prueba2@gmail.com', 'hola', '2024-08-30', 'individual', NULL),
(8, 'prueba3', 'prueba3', 'prueba3@gmail.com', 'prueba3', '2024-08-30', 'individual', NULL),
(9, 'prueba4', 'pasda', 'prueba4@gmail.com', 'hola', '2024-08-30', 'individual', NULL),
(10, 'prueba5', 'pasda', 'prueba5@gmail.com', 'hola', '2024-08-30', 'individual', NULL),
(11, 'pruebaM', 'pruebaM', 'pruebaM@gmail.com', 'holahola', '2024-10-07', 'individual', NULL),
(12, 'ESTOY', 'CANSADO', 'yabasta@gmail.com', 'hola', '2024-10-23', 'empresa', NULL),
(13, 'estoy', 'CANSADO', 'estoycansado2@gmail.com', 'hola', '2024-10-23', 'individual', NULL),
(14, 'empresa', 'empresa', 'empresa@gmail.com', 'hola', '2024-11-09', 'empresa', NULL),
(17, 'Bodega', 'Trivento', 'bodega@gmail.com', 'hola', '2024-11-09', 'empresa', 'Bodega'),
(18, 'Hotel', 'Algo', 'hotel@gmail.com', 'hola', '2024-11-09', 'empresa', 'Hotel'),
(19, 'Transporte', 'Miguel', 'transporte@gmail.com', 'hola', '2024-11-09', 'empresa', 'Transporte'),
(20, 'empresa2', 'hola', 'holaempresa@hola.com', 'hola', '2024-11-11', 'empresa', 'Hotel'),
(21, 'Renzo', 'Merino', 'renzomerino@gmail.com', 'renzo', '2024-11-13', 'individual', NULL),
(22, 'Ludmila', 'Roldan', 'ludmilaroldan@gmail.com', 'lud', '2024-11-13', 'individual', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vinos`
--

CREATE TABLE `vinos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `bodega_id` int(11) DEFAULT NULL,
  `tipo_vino` varchar(50) DEFAULT NULL,
  `año` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `bodegas`
--
ALTER TABLE `bodegas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `detalle_factura`
--
ALTER TABLE `detalle_factura`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_factura` (`id_factura`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `empresas_transporte`
--
ALTER TABLE `empresas_transporte`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `eventos`
--
ALTER TABLE `eventos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `organizador_id` (`organizador_id`);

--
-- Indices de la tabla `experiencias`
--
ALTER TABLE `experiencias`
  ADD PRIMARY KEY (`id`),
  ADD KEY `publicacion_id` (`publicacion_id`);

--
-- Indices de la tabla `factura`
--
ALTER TABLE `factura`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `fotos_grupo`
--
ALTER TABLE `fotos_grupo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `grupo_id` (`grupo_id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `fotos_videos`
--
ALTER TABLE `fotos_videos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `publicacion_id` (`publicacion_id`);

--
-- Indices de la tabla `grupos`
--
ALTER TABLE `grupos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `creador_id` (`creador_id`);

--
-- Indices de la tabla `guardados`
--
ALTER TABLE `guardados`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `publicacion_id` (`publicacion_id`);

--
-- Indices de la tabla `hoteles`
--
ALTER TABLE `hoteles`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `imagenes_publicacion`
--
ALTER TABLE `imagenes_publicacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_id_publicacion` (`id_publicacion`);

--
-- Indices de la tabla `mensajes`
--
ALTER TABLE `mensajes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `emisor_id` (`emisor_id`),
  ADD KEY `receptor_id` (`receptor_id`);

--
-- Indices de la tabla `mensajes_grupo`
--
ALTER TABLE `mensajes_grupo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `grupo_id` (`grupo_id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `miembros_grupo`
--
ALTER TABLE `miembros_grupo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `grupo_id` (`grupo_id`);

--
-- Indices de la tabla `paquetes_turisticos`
--
ALTER TABLE `paquetes_turisticos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `transporte_id` (`transporte_id`),
  ADD KEY `hotel_id` (`hotel_id`),
  ADD KEY `bodega_id` (`bodega_id`);

--
-- Indices de la tabla `perfiles`
--
ALTER TABLE `perfiles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_vendedor` (`id_vendedor`);

--
-- Indices de la tabla `publicaciones`
--
ALTER TABLE `publicaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `relaciones`
--
ALTER TABLE `relaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `amigo_id` (`amigo_id`);

--
-- Indices de la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `paquete_id` (`paquete_id`);

--
-- Indices de la tabla `reseñas_vinos`
--
ALTER TABLE `reseñas_vinos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `publicacion_id` (`publicacion_id`),
  ADD KEY `vino_id` (`vino_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `vinos`
--
ALTER TABLE `vinos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bodega_id` (`bodega_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `bodegas`
--
ALTER TABLE `bodegas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `carrito`
--
ALTER TABLE `carrito`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT de la tabla `detalle_factura`
--
ALTER TABLE `detalle_factura`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `empresas_transporte`
--
ALTER TABLE `empresas_transporte`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `eventos`
--
ALTER TABLE `eventos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `experiencias`
--
ALTER TABLE `experiencias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `factura`
--
ALTER TABLE `factura`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `fotos_grupo`
--
ALTER TABLE `fotos_grupo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `fotos_videos`
--
ALTER TABLE `fotos_videos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `grupos`
--
ALTER TABLE `grupos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `guardados`
--
ALTER TABLE `guardados`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de la tabla `hoteles`
--
ALTER TABLE `hoteles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `imagenes_publicacion`
--
ALTER TABLE `imagenes_publicacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `mensajes`
--
ALTER TABLE `mensajes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `mensajes_grupo`
--
ALTER TABLE `mensajes_grupo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `miembros_grupo`
--
ALTER TABLE `miembros_grupo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `paquetes_turisticos`
--
ALTER TABLE `paquetes_turisticos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `perfiles`
--
ALTER TABLE `perfiles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `publicaciones`
--
ALTER TABLE `publicaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT de la tabla `relaciones`
--
ALTER TABLE `relaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=119;

--
-- AUTO_INCREMENT de la tabla `reservas`
--
ALTER TABLE `reservas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `reseñas_vinos`
--
ALTER TABLE `reseñas_vinos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `vinos`
--
ALTER TABLE `vinos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `carrito_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `detalle_factura`
--
ALTER TABLE `detalle_factura`
  ADD CONSTRAINT `detalle_factura_ibfk_1` FOREIGN KEY (`id_factura`) REFERENCES `factura` (`id`),
  ADD CONSTRAINT `detalle_factura_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `eventos`
--
ALTER TABLE `eventos`
  ADD CONSTRAINT `eventos_ibfk_1` FOREIGN KEY (`organizador_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `experiencias`
--
ALTER TABLE `experiencias`
  ADD CONSTRAINT `experiencias_ibfk_1` FOREIGN KEY (`publicacion_id`) REFERENCES `publicaciones` (`id`);

--
-- Filtros para la tabla `factura`
--
ALTER TABLE `factura`
  ADD CONSTRAINT `factura_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `fotos_grupo`
--
ALTER TABLE `fotos_grupo`
  ADD CONSTRAINT `fotos_grupo_ibfk_1` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`),
  ADD CONSTRAINT `fotos_grupo_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `fotos_videos`
--
ALTER TABLE `fotos_videos`
  ADD CONSTRAINT `fotos_videos_ibfk_1` FOREIGN KEY (`publicacion_id`) REFERENCES `publicaciones` (`id`);

--
-- Filtros para la tabla `grupos`
--
ALTER TABLE `grupos`
  ADD CONSTRAINT `grupos_ibfk_1` FOREIGN KEY (`creador_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `guardados`
--
ALTER TABLE `guardados`
  ADD CONSTRAINT `guardados_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `guardados_ibfk_2` FOREIGN KEY (`publicacion_id`) REFERENCES `publicaciones` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `imagenes_publicacion`
--
ALTER TABLE `imagenes_publicacion`
  ADD CONSTRAINT `imagenes_publicacion_ibfk_1` FOREIGN KEY (`id_publicacion`) REFERENCES `publicaciones` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `mensajes`
--
ALTER TABLE `mensajes`
  ADD CONSTRAINT `mensajes_ibfk_1` FOREIGN KEY (`emisor_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `mensajes_ibfk_2` FOREIGN KEY (`receptor_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `mensajes_grupo`
--
ALTER TABLE `mensajes_grupo`
  ADD CONSTRAINT `mensajes_grupo_ibfk_1` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`),
  ADD CONSTRAINT `mensajes_grupo_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `miembros_grupo`
--
ALTER TABLE `miembros_grupo`
  ADD CONSTRAINT `miembros_grupo_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `miembros_grupo_ibfk_2` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`);

--
-- Filtros para la tabla `paquetes_turisticos`
--
ALTER TABLE `paquetes_turisticos`
  ADD CONSTRAINT `paquetes_turisticos_ibfk_1` FOREIGN KEY (`transporte_id`) REFERENCES `empresas_transporte` (`id`),
  ADD CONSTRAINT `paquetes_turisticos_ibfk_2` FOREIGN KEY (`hotel_id`) REFERENCES `hoteles` (`id`),
  ADD CONSTRAINT `paquetes_turisticos_ibfk_3` FOREIGN KEY (`bodega_id`) REFERENCES `bodegas` (`id`);

--
-- Filtros para la tabla `perfiles`
--
ALTER TABLE `perfiles`
  ADD CONSTRAINT `perfiles_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_vendedor`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `publicaciones`
--
ALTER TABLE `publicaciones`
  ADD CONSTRAINT `publicaciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `relaciones`
--
ALTER TABLE `relaciones`
  ADD CONSTRAINT `relaciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `relaciones_ibfk_2` FOREIGN KEY (`amigo_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD CONSTRAINT `reservas_ibfk_1` FOREIGN KEY (`paquete_id`) REFERENCES `paquetes_turisticos` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `reseñas_vinos`
--
ALTER TABLE `reseñas_vinos`
  ADD CONSTRAINT `reseñas_vinos_ibfk_1` FOREIGN KEY (`publicacion_id`) REFERENCES `publicaciones` (`id`),
  ADD CONSTRAINT `reseñas_vinos_ibfk_2` FOREIGN KEY (`vino_id`) REFERENCES `vinos` (`id`);

--
-- Filtros para la tabla `vinos`
--
ALTER TABLE `vinos`
  ADD CONSTRAINT `vinos_ibfk_1` FOREIGN KEY (`bodega_id`) REFERENCES `bodegas` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
