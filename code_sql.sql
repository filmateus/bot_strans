-- create a database
CREATE DATABASE BD_STRANS;
GO

USE [BD_STRANS];
GO

--- create a new table to armen new FINNS
CREATE TABLE [dbo].[autos_strans]
(
	[NUM_AUTO][varchar](50) NOT NULL PRIMARY KEY ,
	[NAM_PLACA][varchar](MAX) NOT NULL ,
	[NAM_ENDERECO][varchar](MAX) NOT NULL,
	[DT_DATA_HORA][datetime] NOT NULL,
	[COD_INFRACAO][int] NOT NULL,
	[COD_MATRICULA][int] NOT NULL,
	[CH_SNE][varchar](MAX) NOT NULL,
	[CH_ORIGIN][varchar](50)NOT NULL
)
GO

ALTER TABLE autos_strans
ADD TIP_CARRO[varchar](MAX) 
GO

--- The table with description of the finns  and agent's register was loaded from csv files 
--- we transform them

--- TRANSFORMs COLUMN TO NO NULL
ALTER TABLE INFRACOES
ALTER COLUMN COD_INFRACAO FLOAT NOT NULL;
GO

ALTER TABLE MATRICULAS
ALTER COLUMN COD_MATRICULA FLOAT NOT NULL;
GO

--- CREATE PRIMARY KEY
ALTER TABLE INFRACOES
ADD PRIMARY KEY (COD_INFRACAO)

ALTER TABLE MATRICULAS
ADD PRIMARY KEY (COD_MATRICULA)
GO

--- we have problems in table matriculas with duplicated rows, it's importante delete this rows
--- find duplicates elements
SELECT COD_MATRICULA, NOM_NOME, COUNT(*) AS "Repeti��es"
FROM MATRICULAS
GROUP BY COD_MATRICULA, NOM_NOME
HAVING COUNT(*) > 1  
ORDER BY COD_MATRICULA
GO

--- delete duplicates rows
WITH CTE ([NOM_NOME],
						 duplicatecount)
AS (SELECT [NOM_NOME],
						ROW_NUMBER() OVER (PARTITION BY [NOM_NOME]
						ORDER BY COD_MATRICULA) AS duplicatecount
			FROM MATRICULAS)
DELETE FROM CTE
WHERE DuplicateCount > 1;
GO

--- CORRECT INFORMATION
  UPDATE autos_strans
  SET CH_ORIGIN = 'RADAR'
  WHERE NUM_AUTO LIKE  '%ER%'

   UPDATE autos_strans
  SET CH_ORIGIN = 'DOFT'
  WHERE NUM_AUTO NOT LIKE  '%ER%'
  GO


--- SCRIPTS SOURCE
-- fines recorded
SELECT  COUNT(*) AS 'Autos Registrados'
FROM autos_strans


--  SNE
SELECT CH_SNE, COUNT(*) AS 'Contagem'
FROM autos_strans
GROUP BY CH_SNE
ORDER	BY	COUNT(*) DESC;


-- fine's origin: radar or traffic agent
SELECT CH_ORIGIN, COUNT(*) AS 'Contagem'
FROM autos_strans
GROUP BY CH_ORIGIN
ORDER	BY	COUNT(*) DESC;

-- car's type
SELECT TIP_CARRO, COUNT(*) AS 'Contagem'
FROM autos_strans
GROUP BY TIP_CARRO
ORDER	BY	COUNT(*) DESC;

-- fine's code
SELECT m.COD_INFRACAO , e.ST_DESCRICAO_INFRA ,  COUNT(*) AS 'Contagem'
FROM autos_strans AS m, INFRACOES AS e
WHERE m.COD_INFRACAO =  e.COD_INFRACAO
GROUP BY  m.COD_INFRACAO , e.ST_DESCRICAO_INFRA
ORDER	BY	COUNT(*) DESC;
GO

--fine's month
SELECT MONTH(m.DT_DATA_HORA) AS 'Mês' , COUNT(*) AS 'Autos por mês'
FROM autos_strans AS m
WHERE YEAR(m.DT_DATA_HORA) = 2022
GROUP BY  MONTH(m.DT_DATA_HORA) 
ORDER	BY MONTH(m.DT_DATA_HORA)
GO

-- search fine by type 
SELECT  m.NAM_ENDERECO as 'Endere�o', COUNT(*) AS 'Contagem'
FROM autos_strans AS m
WHERE m.COD_INFRACAO = 75870
GROUP BY m.NAM_ENDERECO
ORDER BY 'Contagem' DESC
GO

-- search fine in specific adrress
SELECT  m.NAM_ENDERECO as 'Endere�o', COUNT(*) AS 'Contagem'
FROM autos_strans AS m
WHERE m.NAM_ENDERECO LIKE '%FREI %'

-- search fine's adrress
SELECT  m.NAM_ENDERECO as 'Endere�o', COUNT(*) AS 'Contagem'
FROM autos_strans AS m
GROUP BY m.NAM_ENDERECO 
ORDER BY 'Contagem' DESC
GO

-- search in the old db
-- search  not paid and paid fine
SELECT  m.status, COUNT(*)
FROM MULTAS02 AS m
WHERE m.ST_PLACAVEICULO != ''
AND m.status !='NULL' AND m."status" = 'PAGA' OR m."status" = 'PENALIZADA'
AND YEAR(m.DT_DATAINFRACAO) >= 2015 AND YEAR(m.DT_DATAINFRACAO) <= 2022
AND m.LG_IMPRNOTIFICACAO = 'TRUE'
GROUP BY m.status
GO

SELECT  *
FROM INFRACOES as n
WHERE n.ST_DESCRICAO_INFRA LIKE '%ESTA %'