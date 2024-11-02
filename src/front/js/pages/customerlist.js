import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import "../../styles/customerlist.css";

const Customers = () => {
    const [customers, setCustomers] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchCustomers = async (page) => {
            try {
                const response = await axios.get(`${process.env.BACKEND_URL}/api/customers?page=${page}&limit=25`);
                setCustomers(response.data.customers);
                setTotalPages(response.data.totalPages);
            } catch (error) {
                console.error("Error fetching customers", error);
            }
        };

        fetchCustomers(currentPage);
    }, [currentPage]);

    const handleRowClick = (customerId) => {
        navigate(`/customer/${customerId}`);
    };

    const handlePageChange = (page) => {
        setCurrentPage(page);
    };

    return (
        <div>
            <div className='border rounded-3 m-5 justify-content-center'>
                <table className='table caption-top'>
                    <caption className='p-3'>Clientes</caption>
                    <thead className='bg-light'>
                        <tr>
                            <th>#</th>
                            <th>Company</th>
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
                                <td>{customer.billing?.company}</td>
                                <td>{customer.first_name}</td>
                                <td>{customer.last_name}</td>
                                <td>{customer.billing?.city}</td>
                                <td>{customer.billing?.state}</td>
                                <td>{customer.email}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <div className='pagination'>
                    {Array.from({ length: totalPages }, (_, index) => (
                        <button 
                            key={index + 1} 
                            onClick={() => handlePageChange(index + 1)}
                            className={`page-item ${currentPage === index + 1 ? 'active' : ''}`}
                        >
                            {index + 1}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Customers;