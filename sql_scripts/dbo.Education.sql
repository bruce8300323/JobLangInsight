USE [JobLangInsight]
GO

/****** Object: Table [dbo].[Education] Script Date: 7/9/2023 9:18:56 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Education] (
    [Id]     INT           IDENTITY (1, 1) NOT NULL,
    [Degree] NVARCHAR (10) NOT NULL,
    [Class]  INT           NULL
);


