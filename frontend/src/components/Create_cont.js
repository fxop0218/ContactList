import { Wrapper } from "./Wrapper"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

export const CreateC = () => {
    const [name, setName] = useState("")
    const [email, setEmail] = useState("")
    const [telephone, setTelephone] = useState("")
    const [owner, setOwner] = useState("")
    const navigate = useNavigate()

    const submit = async (e) => {
        e.preventDefault()

        await fetch("http://localhost:8001/create", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, telephone, owner }),
        })

        await navigate(-1)
    }
    return (
        <Wrapper>
            <from className="mt-3" onSubmit={submit}>
                <div className="form-floatin pb-3">
                    <input
                        className="form-control"
                        placeholder="Contact name"
                        onChange={(e) => setName(e.target.value)}
                    />

                    <div className="form-floatin pb-3">
                        <input
                            className="form-control"
                            placeholder="E-Mail"
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>

                    <div className="form-floatin pb-3">
                        <input
                            className="form-control"
                            placeholder="Telephone"
                            onChange={(e) => setTelephone(e.target.value)}
                        />
                    </div>

                    <div className="form-floatin pb-3">
                        <input
                            className="form-control"
                            placeholder="Owner (Delete this ONLY TEST)"
                            onChange={(e) => setOwner(e.target.value)}
                        />
                    </div>
                </div>
                <button className="w-100 btn btn-lg btn-primary" type="submit">
                    Submit
                </button>
            </from>
        </Wrapper>
    )
}
