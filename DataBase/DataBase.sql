CREATE TABLE IF NOT EXISTS Seed_Data_ (
    area FLOAT NOT NULL CHECK (area >= 0),
    perimeter FLOAT NOT NULL CHECK (perimeter >= 0),
    compactness FLOAT NOT NULL CHECK (compactness >= 0),
    lengthOfKernel FLOAT NOT NULL CHECK (lengthOfKernel >= 0),
    widthOfKernel FLOAT NOT NULL CHECK (widthOfKernel >= 0),
    asymmetryCoefficient FLOAT NOT NULL CHECK (asymmetryCoefficient >= 0),
    lengthOfKernelGroove FLOAT NOT NULL CHECK (lengthOfKernelGroove >= 0),
    seedType INTEGER  NOT NULL
);
DELETE FROM Seed_Data_;