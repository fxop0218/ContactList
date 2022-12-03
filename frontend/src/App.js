import "./App.css"
import { Contacts } from "./components/Contacts"
import { CreateC } from "./components/Create_cont"
import { BrowserRouter, Routes, Route } from "react-router-dom"

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Contacts />} />
                <Route path="/create_contact" element={<CreateC />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
