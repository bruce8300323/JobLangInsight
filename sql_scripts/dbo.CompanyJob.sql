USE [JobLangInsight]
GO

/****** Object: Table [dbo].[CompanyJob] Script Date: 7/9/2023 9:18:47 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[CompanyJob] (
    [CompanyId] INT       NOT NULL,
    [JobId]     CHAR (10) NOT NULL
);


