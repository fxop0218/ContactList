import { Wrapper } from "./Wrapper"
import { useState, useEffect } from "react"
import { Link } from "react-router-dom"

export const Contacts = () => {
    const [contacts, setContacts] = useState([])

    useEffect(() => {
        ;(async () => {
            const response = await fetch("http://localhost:8001/all_contacts")
            const cont = await response.json()
            setContacts(cont)
        })()
    }, [])

    const delt = async (contact_id) => {
        if (window.confirm("Click accept to delete the conctact")) {
            await fetch(`http://localhost:8000/delete_contact`, { method: "DELETE" })
            setContacts(contacts.filter((contct) => contct.id !== contact_id))
        }
    }
    return (
        <Wrapper>
            <div>
                <Link to={"/create"} className="pt-3 pb.2 mb-3 border-bottom">
                    Create
                </Link>
            </div>
            <div className="table-responsive">
                <table class="table table-striped table-sm">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Name</th>
                            <th scope="col">Telephone</th>
                            <th scope="col">Email</th>
                            <th scope="col">Owner</th>
                        </tr>
                    </thead>
                    <tbody>
                        {contacts.map((contact) => {
                            return (
                                <tr key={contact.id}>
                                    <td>{contact.id}</td>
                                    <td>{contact.name}</td>
                                    <td>{contact.telephone}</td>
                                    <td>{contact.email}</td>
                                    <td>{contact.owner}</td>
                                    <td>
                                        <a
                                            href="#"
                                            className="btn btn-sm btn-outlline-secondary"
                                            onClick={(e) => delt(contact.id)}
                                        >
                                            Delete
                                        </a>
                                    </td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            </div>
        </Wrapper>
    )
}
