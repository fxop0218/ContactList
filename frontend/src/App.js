import "./App.css"
import { Contacts } from "./components/Contacts"
import { BrowserRouter, Routes, Route } from "react-router-dom"

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Contacts />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
