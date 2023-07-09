USE [JobLangInsight]
GO

/****** Object: Table [dbo].[Job] Script Date: 7/9/2023 9:19:02 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Job] (
    [Id]          CHAR (10)      NOT NULL,
    [Title]       NVARCHAR (150) NOT NULL,
    [Url]         VARCHAR (200)  NULL,
    [Source]      VARCHAR (50)   NULL,
    [Area]        NVARCHAR (50)  NULL,
    [Type]        INT            NULL,
    [Processed]   BIT            NOT NULL,
    [Detail]      NVARCHAR (MAX) NULL,
    [CreatedTime] DATETIME       NOT NULL,
    [Experience]  NVARCHAR (10)  NULL,
    [Closed]      BIT            NULL
);


