USE [JobLangInsight]
GO

/****** Object: Table [dbo].[Company] Script Date: 7/9/2023 9:18:41 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Company] (
    [Id]       INT            IDENTITY (1, 1) NOT NULL,
    [Name]     NVARCHAR (100) NOT NULL,
    [Category] NVARCHAR (50)  NULL
);


