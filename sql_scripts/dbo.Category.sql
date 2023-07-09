USE [JobLangInsight]
GO

/****** Object: Table [dbo].[Category] Script Date: 7/9/2023 9:18:15 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Category] (
    [Id]   INT           IDENTITY (1, 1) NOT NULL,
    [Name] NVARCHAR (50) NULL
);


