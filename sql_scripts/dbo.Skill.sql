USE [JobLangInsight]
GO

/****** Object: Table [dbo].[Skill] Script Date: 7/9/2023 9:19:20 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Skill] (
    [Id]    INT           IDENTITY (1, 1) NOT NULL,
    [Name]  NVARCHAR (25) NOT NULL,
    [Alias] NVARCHAR (50) NULL,
    [Type]  INT           NULL
);


