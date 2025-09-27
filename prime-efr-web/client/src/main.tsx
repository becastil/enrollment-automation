import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ConfigProvider } from 'antd'
import './index.css'
import App from './App.tsx'
import { ThemeProvider } from './theme/ThemeProvider'
import { antdTheme } from './theme/antd-theme'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ConfigProvider theme={antdTheme}>
      <ThemeProvider>
        <App />
      </ThemeProvider>
    </ConfigProvider>
  </StrictMode>,
)
