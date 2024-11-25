import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider, createTheme } from '@mui/material'
import Layout from './components/Layout'
import Home from './pages/Home'
import Chat from './pages/Chat'
import './App.css'

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
})

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chat/:documentId" element={<Chat />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  )
}

export default App