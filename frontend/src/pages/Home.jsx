import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Box,
    Button,
    Typography,
    List,
    ListItem,
    ListItemText,
    Paper,
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import axios from 'axios';

function Home() {
    const [documents, setDocuments] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetchDocuments();
    }, []);

    const fetchDocuments = async () => {
        try {
            const response = await axios.get('http://localhost:8000/documents/');
            setDocuments(response.data);
        } catch (error) {
            console.error('Error fetching documents:', error);
        }
    };

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:8000/upload-pdf/', formData);
            fetchDocuments();
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    return (
        <Box>
            <Typography variant="h4" gutterBottom>
                Upload PDF Documents
            </Typography>
            <Button
                variant="contained"
                component="label"
                startIcon={<UploadFileIcon />}
                sx={{ mb: 4 }}
            >
                Upload PDF
                <input
                    type="file"
                    hidden
                    accept=".pdf"
                    onChange={handleFileUpload}
                />
            </Button>

            <Paper elevation={3} sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                    Your Documents
                </Typography>
                <List>
                    {documents.map((doc) => (
                        <ListItem
                            key={doc.id}
                            button
                            onClick={() => navigate(`/chat/${doc.id}`)}
                        >
                            <ListItemText primary={doc.filename} />
                        </ListItem>
                    ))}
                </List>
            </Paper>
        </Box>
    );
}

export default Home;
