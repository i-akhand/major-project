import { Container, AppBar, Toolbar, Typography, Box } from '@mui/material';

function Layout({ children }) {
    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        PDF Chatbot
                    </Typography>
                </Toolbar>
            </AppBar>
            <Container sx={{ mt: 4 }}>
                {children}
            </Container>
        </Box>
    );
}

export default Layout;
