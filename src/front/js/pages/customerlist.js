import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import "../../styles/customerlist.css";

const Customers = () => {
    const [customers, setCustomers] = useState([]);
    const navigate = useNavigate();
    useEffect(() => {
        const fetchCustomers = async () => {
            try {
                const response = await axios.get(`${process.env.BACKEND_URL}/api/customers`);
                setCustomers(response.data);
            } catch (error) {
                console.error("Error fetching customers", error);
            }
        };
        fetchCustomers();
    }, []);
    const handleRowClick = (customerId) => {
        navigate(`/customer/${customerId}`);
    };
    return (
        <div>
            <div className='border rounded-3 m-5 justify-content-center'>
                <table className='table caption-top'>
                    <caption className='p-3'>Clientes</caption>
                    <thead className='bg-light'>
                        <tr>
                            <th>#</th>
                            <th>Empresa</th>
                            <th>Nombre</th>
                            <th>Apellidos</th>
                            <th>Ciudad</th>
                            <th>Provincia</th>
                            <th>Email</th>
                        </tr>
                    </thead>
                    <tbody>
                        {customers.map(customer => (
                            <tr
                                key={customer.id}
                                className='fw-light'
                                onClick={() => handleRowClick(customer.id)}
                                style={{ cursor: 'pointer' }}
                            >
                                <td className='fw-light'>{customer.id}</td>
                                <td>{customer.billing.company}</td>
                                <td>{customer.first_name}</td>
                                <td>{customer.last_name}</td>
                                <td>{customer.billing.city}</td>
                                <td>{customer.billing.state}</td>
                                <td>{customer.email}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
export default Customers;