import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
    Box,
    TextField,
    Button,
    Typography,
    Paper,
    List,
    ListItem,
    ListItemText,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import axios from 'axios';

function Chat() {
    const { documentId } = useParams();
    const [question, setQuestion] = useState('');
    const [answers, setAnswers] = useState([]);
    const [document, setDocument] = useState(null);

    useEffect(() => {
        fetchDocument();
    }, [documentId]);

    const fetchDocument = async () => {
        try {
            const response = await axios.get(`http://localhost:8000/documents/${documentId}`);
            setDocument(response.data);
            setAnswers(response.data.answers);
        } catch (error) {
            console.error('Error fetching document:', error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!question.trim()) return;

        try {
            const response = await axios.post('http://localhost:8000/ask-question/', {
                question,
                document_id: parseInt(documentId),
            });
            setAnswers([...answers, response.data]);
            setQuestion('');
        } catch (error) {
            console.error('Error asking question:', error);
        }
    };

    return (
        <Box>
            <Typography variant="h4" gutterBottom>
                Chat with PDF: {document?.filename}
            </Typography>

            <Paper elevation={3} sx={{ p: 2, mb: 2, maxHeight: '60vh', overflow: 'auto' }}>
                <List>
                    {answers.map((answer, index) => (
                        <ListItem key={index}>
                            <ListItemText
                                primary={answer.question}
                                secondary={answer.answer}
                            />
                        </ListItem>
                    ))}
                </List>
            </Paper>

            <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', gap: 1 }}>
                <TextField
                    fullWidth
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask a question about the document..."
                    variant="outlined"
                />
                <Button
                    type="submit"
                    variant="contained"
                    endIcon={<SendIcon />}
                >
                    Ask
                </Button>
            </Box>
        </Box>
    );
}

export default Chat;
