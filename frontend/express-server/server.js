const express = require('express');
const multer = require('multer');
const path = require('path');
const app = express();
const port = 3001;

// Set up the storage destination for uploaded files
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, '../../backend/logs'); // Save files to the 'uploads' folder
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname); // Use the original file name
    },
});

const upload = multer({ storage });

app.post('/upload', upload.single('file'), (req, res) => {
    // File has been uploaded and saved to the 'uploads' folder
    res.status(200).json({ message: 'File uploaded successfully' });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
